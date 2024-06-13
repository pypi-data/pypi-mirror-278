from collections import defaultdict, namedtuple
import csv
import json
import logging
import math
import os
from pathlib import Path
import re
from typing import Any, Dict, List, Literal, Optional, Union

from genson import SchemaBuilder
from mcap.writer import Writer
from roboto.domain import topics
from roboto_ingestion_utils.ingestion_utils import compute_checksum

from .metrics import RunningStats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



TYPE_MAPPING = {
        "string": str,
        "boolean": bool,
        "integer": int,
        "number": float,
        }

TYPE_MAPPING_CANONICAL = {
        "string": topics.CanonicalDataType.String,
        "boolean": topics.CanonicalDataType.Boolean,
        "number":  topics.CanonicalDataType.Number,
        "integer": topics.CanonicalDataType.Number
        }

MAX_UINT64 = 2**64 - 1

def create_json_schema(
        field_type_dict: Dict[str, str]
) -> Dict[str, Any]:
    """
    Creates a JSON schema based on a message definition.

    This function iterates over each field in the message definition and constructs
    a JSON schema. Fields starting with '_padding' are ignored. The function supports
    handling both array and non-array types.

    Args:
    - message_definition: A list of tuples, each representing a field in the message.
      Each tuple contains the field type, array size, and field name.

    Returns:
    - A dictionary representing the constructed JSON schema.
    """
    schema = {"type": "object", "properties": {}, "required": []}
    for field_name, field_type in field_type_dict.items():
        schema_property = {"type": field_type}

        schema["properties"][field_name] = schema_property
        schema["required"].append(field_name)

    return schema

def convert_value(field_type: str, value: Any) -> Any:
    """
    Converts a field value to its corresponding JSON type.

    Args:
    - field_type: The type of the field as a string.
    - value: The value to be converted.

    Returns:
    - The converted value in its appropriate JSON type.
    """
    if field_type == "integer":
        value = int(value)
    elif field_type == "number":
        value = float(value)
    elif field_type == "boolean":
        value = bool(int(value))
    elif field_type == "json":
        value = json.loads(value)
    elif field_type == "string":
        value = str(value)
    
    if field_type in ["integer", "number"]:
        if math.isnan(value):
            return None
        elif math.isinf(value):
            return None

    return value

def infer_types(csv_line): 
    """
    infer type string from the first value in each csv
    """
    types = []
    for value in csv_line:
        if value.isnumeric(): # only 0-9, no ., etc
            types.append("integer")
        elif re.match(r'^\d+\.\d+$', value):  # matches simple decimal numbers
            types.append("number")
        elif re.match(r'^[+-]?\d*\.?\d+([eE][+-]?\d+)?$', value):  # matches scientific notation
            types.append("number")
        elif value.lower() in ["true", "false"]:
            types.append("boolean")
        # try to parse as json
        elif value[0] == "{" and value[-1] == "}":
            try:
                json.loads(value)
                types.append("json")
            except:
                types.append("string")
        else:
            types.append("string")
    return types

def format_field_name(orig_name: str):
    """
    replace whitespace, periods, and slashes
    """
    disallowed_chars = "./\\ "
    for char in disallowed_chars:
        orig_name = orig_name.replace(char, "_")
    return orig_name

def infer_timestamp_column(fields: List):
    column_idx = None
    # TODO @YVES: pick better priorities/list of smart guesses
    candidate_stubs = ['time', 'offset', 'ts', 'seconds']
    for candidate in candidate_stubs:
        if not column_idx:
            for idx, field_name in enumerate(fields):
                if not column_idx:
                    if candidate in field_name.lower():
                        column_idx = idx
                        logger.info(f"Found probable timestamp key `{field_name}`")
                else:
                    break
        else:
            break
    if column_idx:
        return column_idx
    else:
        return 0 # default to returning the first column if you can't find anything

def csv_to_mcap(
        input_dir: Union[str, Path],
        rel_file_path: Union[str, Path],
        output_dir: Union[str, Path],
        calculate_metrics: bool=True,
        timestamp_key: Optional[str]=None,
        timestamp_format: Literal["seconds", "milliseconds", "nanoseconds"]="nanoseconds"
                ):
    """
    Ingest one csv and save the output as a single-topic MCAP file
    to the output directory output_dir. Optionally calculate metrics
    """
    if isinstance(input_dir, str):
        input_dir = Path(input_dir)
    if isinstance(output_dir, str):
        output_dir = Path(output_dir)
    csv_file = input_dir / rel_file_path
    if isinstance(csv_file, str):
        csv_file = Path(csv_file).resolve()
    assert output_dir.is_dir()

    field_names = list()
    raw_msg_list = list()
    field_type_mappings = {}
    json_field_schemes = {} # keep track of additional scheme info for json fields
    timestamp_column = None

    with open(csv_file, 'r') as f:
        for i, line in enumerate(csv.reader(f)):
            if i == 0:
                field_names = [format_field_name(str(x)) for x in line]
                if timestamp_key:
                    assert timestamp_key in field_names,\
                            "Error: TIMESTAMP_KEY must be a valid key in file {csv_file.name}"
                    timestamp_column = field_names.index(timestamp_key)
                else:
                    if 'timestamp' in field_names:
                        timestamp_column = field_names.index('timestamp')
                    # otherwise, infer timestamp from available keys
                    else:
                        logger.info("Inferring timestamp from available keys...")
                        timestamp_column = infer_timestamp_column(field_names)
                field_names.pop(timestamp_column)
                raw_msg_list = []
            else:
                timestamp_raw = line.pop(timestamp_column)
                if i == 1:
                    field_types = infer_types(line)
                    field_type_mappings = {name: type_str for name, type_str in zip (field_names, field_types)} 
                    json_field_schemes = {name: SchemaBuilder() for name in field_names if field_type_mappings[name] == "json"}
                
                # Convert form in CSV file to nanoseconds for compatibility
                timestamp = float(timestamp_raw)
                if timestamp_format == "seconds":
                    timestamp *= 1e9
                elif timestamp_format == "milliseconds":
                    timestamp *= 1e6
                elif timestamp_format == "nanoseconds":
                    pass
                timestamp = int(timestamp)
                
                # add all fields to one raw message dictionary
                raw_msg = {}
                for i, val in enumerate(line):
                    field = field_names[i]
                    field_type = field_type_mappings[field]
                    if field_type == "json":
                        json_field_schemes[field].add_object(val) # add data to build schema per field
                    raw_msg[field] = (field_type, val)
                raw_msg_list.append((timestamp, raw_msg))
    #  raw_msg_list now contains a list of tuples (timestamp, {field: (type_str, val) for field in fields})

    # collect extra information about entire topic
    msg_count = len(raw_msg_list)
    start_time_ns = raw_msg_list[0][0]
    end_time_ns = raw_msg_list[-1][0]

    # set up topic file output
    topic_name = csv_file.stem
    topic_rel_fname = os.path.splitext(rel_file_path)[0]
    logger.info(f"{topic_rel_fname=}")
    topic_fname = f"{topic_rel_fname}.mcap"
    topic_mcap_file = output_dir / topic_fname
    # make parent directories if necessary
    topic_mcap_file.parent.mkdir(parents=True, exist_ok=True)


    # create json schema for topic
    topic_json_schema = create_json_schema(field_type_dict=field_type_mappings)

    # parse more advanced schema if any types are json
    if json_field_schemes:
        for key, builder in json_field_schemes.items():
            schema = builder.to_schema()
            # update default schema with json info
            topic_json_schema["properties"][key] = schema
    msgdef = json.dumps(topic_json_schema)
    schema_checksum = compute_checksum(topic_json_schema)
    # keep track of running statistics 
    topic_stats = defaultdict(RunningStats)
    print(topic_stats)
    
    # stream messages into topic mcap file one at a time
    with open(topic_mcap_file, "wb") as stream:
        writer = Writer(stream)
        writer.start()
        schema_id = writer.register_schema(
            name=topic_fname,
            encoding="jsonschema",
            data=msgdef.encode(),
        )

        channel_id = writer.register_channel(
            schema_id=schema_id,
            topic=topic_fname,
            message_encoding="json",
        )

        for i, (timestamp, raw_msg) in enumerate(raw_msg_list):
            # skip messages that will overflow
            if timestamp > MAX_UINT64:
                continue

            # convert values to correct types
            json_msg_instance = {f: convert_value(t,v) for f, (t,v) in raw_msg.items()}
            # add numeric values to running stats
            if calculate_metrics:
                for path, value in json_msg_instance.items():
                    if isinstance(value, (int, float)):
                        print(f"updating {path} with {value}")
                        topic_stats[path].update(value)
                        
                    
            writer.add_message(
            channel_id=channel_id,
            log_time=timestamp,
            sequence=i,
            data=json.dumps(json_msg_instance).encode("utf-8"),
            publish_time=timestamp,
            )
        writer.finish()
    logger.info(f"Saved output to {topic_mcap_file}")
    
    # return a dict of information for use in actions
    topic_info_dict = {}

    # store the statistics for each message path
    topic_metrics_dict = {} 
    if calculate_metrics:
        # Retrieve stats for each topic and path
        for path, stats in topic_stats.items():
            topic_metrics_dict[path] = stats.get_stats()

    topic_info_entry = dict()
    topic_info_entry["topic_name"] = topic_name
    topic_info_entry["mcap_path"] = topic_mcap_file
    topic_info_entry["nr_msgs"] = msg_count
    topic_info_entry["first_timestamp"] = start_time_ns
    topic_info_entry["last_timestamp"] = end_time_ns
    # note: this is only informative when each topic only has one msg path
    topic_info_entry["msg_type"] = topic_json_schema
    topic_info_entry["checksum"] = schema_checksum

    # return info inside dict keyed to the topic name for compatibility
    topic_info_dict[topic_name] = topic_info_entry     
    image_topics_info_dict = {} # keep empty, return for compatibility w/other ingestion actions
    return topic_info_dict, topic_metrics_dict, image_topics_info_dict, field_type_mappings 

def create_message_path_records(field_type_dict: dict, metrics_dict: dict) -> List:
    """
    Creates message path records for a given topic.

    Args:
    - topic: The topic object to which the message paths will be added.
    - field_data: A list of field data objects containing the message definition.
    """
    message_path_list = list()

    for field_name, field_type in field_type_dict.items():
        if field_type not in TYPE_MAPPING_CANONICAL.keys():
            canonical_data_type = topics.CanonicalDataType.Unknown
        else:
            canonical_data_type = TYPE_MAPPING_CANONICAL[field_type]
        
        metadata_dict = dict()
        if field_name in metrics_dict.keys():
            metadata_dict = metrics_dict[field_name]

        message_path_list.append(topics.AddMessagePathRequest(
                message_path=field_name,
                data_type=field_type,
                canonical_data_type=canonical_data_type,
                metadata=metadata_dict,
            )
        )

        logger.info(
            f"Adding field: {field_name}, type: {field_type}, canonical: {canonical_data_type}"
        )
    return message_path_list
