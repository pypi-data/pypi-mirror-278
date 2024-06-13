class StreamingStats:
    def __init__(self, number=None):
        if number is None:
            self.count = 0
            self.mean = 0
            self.second_moment = 0
            self.cubes = 0
            self.median = 0
            self.min = 0
            self.max = 0
        else:
            self.count = 1
            self.mean = number
            self.second_moment = 0
            self.cubes = 0
            self.median = number
            self.min = number
            self.max = number

    def update(self, x):
        self.count += 1
        
        # Variance
        delta = x - self.mean
        self.mean += delta / self.count
        delta2 = x - self.mean
        self.second_moment += delta * delta2
        
        # skewness
        self.cubes += x**3

        # Median
        self.median += (x - self.median) / self.count

        # Min
        if self.count == 1:
            self.min = x
        else:
            self.min = min(self.min, x)
        # Max
        self.max = max(self.max, x)
    
    def merge(self, other):
        if other == None:
            return self
        
        combined = StreamingStats()
        combined.count = self.count + other.count

        combined.cubes = self.cubes + other.cubes

        delta = other.mean - self.mean
        combined.mean = (self.count * self.mean + other.count * other.mean) / combined.count

        combined.second_moment = self.second_moment + other.second_moment + delta**2 * self.count * other.count / combined.count

        combined.min = min(self.min, other.min) if self.min is not None and other.min is not None else self.min or other.min
        combined.max = max(self.max, other.max) if self.max is not None and other.max is not None else self.max or other.max

        combined.median = (self.median * self.count + other.median * other.count) / (self.count + other.count)

        return combined
    
    def get_mean(self):
        return self.mean
    
    # reservoir sampling technique
    def get_median(self):
        return self.median
    
    def get_variance(self):
        return self.second_moment / self.count if self.count > 1 else 0
    
    def get_std(self):
        return (self.get_variance())**0.5
    
    def get_skewness(self):
        if self.second_moment == 0 or self.count < 2:
            return 0
        return (self.cubes - (self.mean**3)*self.count - 3*((self.get_variance() + self.mean**2) * self.count)*self.mean + 3*(self.mean**3)*self.count)/((self.count-1)*self.get_std()**3)
    
    def get_min(self):
        return self.min
    
    def get_max(self):
        return self.max
    
    def get_total(self):
        return self.mean*self.count

