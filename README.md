# SyncPool

SyncPool is a Python library providing a thread-safe solution for managing a pool of objects, inspired by Go's sync.Pool implementation. The library aims to minimize memory-related overhead by efficiently reusing already allocated objects.

## Features

* Thread-Safe: SyncPool ensures safe access to the object pool across multiple threads, preventing race conditions and ensuring data integrity.
* Efficient Object Reuse: Objects are recycled and reused, reducing the need for frequent memory allocation and deallocation operations.
* Customizable Callbacks: Optional callback functions allow you to execute custom logic when objects are retrieved from or returned to the pool.
* Flexible Configuration: You can specify the maximum capacity of the pool and the class of objects to be managed, providing flexibility to suit your specific use case.

## Installation

You can install the SyncPool library using pip:
`pip install syncpool-py`

## Usage
### Basic Usage
```
from syncpool_py import SyncObjectPool
# Create an object pool with a maximum capacity of 10 objects
pool = SyncObjectPool(max_len=10)

# Put an object into the pool
pool.put(my_object)

# Get an object from the pool
obj = pool.get()
```

### Custom Callbacks
```
def on_put(obj):
    print("Object put into the pool:", obj)

def on_get(obj):
    print("Object retrieved from the pool:", obj)

# Create an object pool with custom callbacks
pool = SyncObjectPool(max_len=10, on_put=on_put, on_get=on_get)
```

#### Asynchronous Module

SyncPool also provides an asynchronous module (`AsyncObjectPool`) for managing object pools across multiple coroutines. This module offers similar functionality to the synchronous module but is designed to be used in asynchronous contexts.

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests via GitHub.

## License

This project is licensed under the MIT License - see the LICENSE file for details.