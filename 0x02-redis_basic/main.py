#!/usr/bin/env python3
""" Main file """

# Import the Cache class from the exercise module
Cache = __import__('exercise').Cache

# Create an instance of Cache
cache = Cache()

# Store some values and print their keys
s1 = cache.store("first")
print(s1)
s2 = cache.store("second")  # Corrected spelling from "secont" to "second"
print(s2)
s3 = cache.store("third")
print(s3)

# Retrieve and print the inputs and outputs from Redis
inputs = cache._redis.lrange(f"{cache.store.__qualname__}:inputs", 0, -1)
outputs = cache._redis.lrange(f"{cache.store.__qualname__}:outputs", 0, -1)

# Decode bytes to strings for better readability
inputs_decoded = [inp.decode('utf-8') for inp in inputs]
outputs_decoded = [out.decode('utf-8') for out in outputs]

print("inputs: {}".format(inputs_decoded))
print("outputs: {}".format(outputs_decoded))

