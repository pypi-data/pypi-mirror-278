import heapq

class RunningStats:
    def __init__(self):
        self.min = float('inf')
        self.max = float('-inf')
        self.sum = 0
        self.count = 0
        self.lower_half = []  # Max-heap (invert values to use heapq as max-heap)
        self.upper_half = []  # Min-heap

    def update(self, value):
        # Update min and max
        if value < self.min:
            self.min = value
        if value > self.max:
            self.max = value

        # Update sum and count for mean calculation
        self.sum += value
        self.count += 1

        # Update heaps for median calculation
        if len(self.lower_half) == 0 or value <= -self.lower_half[0]:
            heapq.heappush(self.lower_half, -value)
        else:
            heapq.heappush(self.upper_half, value)

        # Balance the heaps
        if len(self.lower_half) > len(self.upper_half) + 1:
            heapq.heappush(self.upper_half, -heapq.heappop(self.lower_half))
        if len(self.upper_half) > len(self.lower_half):
            heapq.heappush(self.lower_half, -heapq.heappop(self.upper_half))

    @property
    def mean(self):
        if self.count == 0:
            return None
        return self.sum / self.count

    @property
    def median(self):
        if self.count == 0:
            return None
        if len(self.lower_half) > len(self.upper_half):
            return -self.lower_half[0]
        return (-self.lower_half[0] + self.upper_half[0]) / 2

    def get_stats(self):
        return {
            "min": self.min,
            "max": self.max,
            "mean": self.mean,
            "median": self.median,
        }
