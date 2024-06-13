# Streaming statistics calculator

This tool allows users to calculate statistical features such as mean, median, variance, standard deviation, and skewness, along with the minimum and maximum of a series of numbers in real time without storing them. It can calculate all these features in O(1) space complexity. 

This is very useful when dealing with large series of numbers on a resource contrained system. It uses different mathematical logic to keep track of certain variables for its functioning. 

# Installation 

    pip install streaming-stats

# Execution

```Python
from streaming_stats import StreamingStats

example_series = [4.45, -2, 7.1, -8.7, 3, -2, 45, ,6, -12.3, 53.6, 2.7, 0, 3.6]

object = StreamingStats()

for number in example_series:
  object.update(number)

print(object.get_mean())
print(object.get_median())
print(object.get_std())
print(object.get_variance())
print(object.get_min())
print(object.get_max())
print(object.get_skewness())
```
Other features of the tool includes merging of two different `StreamingStats` objects. There can be situation when users would need to find variance (suppose) of the combined series. The `merge()` method helps in achieving the same.

```Python
object1 = StreamingStats()
object2 = StreamingStats()

for number in series1:
  object1.update(number)

for number in series2:
  object.update(number)

merged_object = object1.merge(object2)

print(merged_object.get_mean())
print(merged_object.get_median())
print(merged_object.get_std())
print(merged_object.get_variance())
print(merged_object.get_min())
print(merged_object.get_max())
print(merged_object.get_skewness())
```

> Note that the `example_series` list was created just for demonstration. Users don't need to have the numbers of the series stored anywhere. The numbers can be added to the `StreamingStats` object as soon as it is recieved.
