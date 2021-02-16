# SPDX-License-Identifier: Apache-2.0

import io


class ReadHandle:
    def read(self, size: int = -1) -> bytes:
        pass

    def close(self) -> None:
        pass


class WriteHandle:
    def write(self, b: bytes) -> int:
        pass

    def close(self) -> None:
        pass


class Cache:
    '''Cache API docs

    No need to inherit form this. This is just a documenation
    of the interface between CacheControl and a cache
    '''

    # TODO: are keys really str?
    def open_read(self, key: str) -> ReadHandle:
        pass

    def open_write(self, key: str, expires=None) -> WriteHandle:
        pass

    def delete(self, key):
        pass

    def close(self):
        '''Cleanup any temporary files, database connections etc.'''
        pass


# An example to use while prototyping
class ExampleCache:
    # Why is ExampleCache.data not a dict[str, io.BytesIO]?
    # 1. I did not want the stream position to be shared by all readers and writers
    # 2. https://docs.python.org/3/library/io.html#io.BytesIO
    #    The buffer is discarded when the close() method is called.
    class WriteHandle:
        def __init__(self, commit):
            self.commit = commit
            self.fd = io.BytesIO()

        def write(self, b):
            return self.fd.write(b)

        def close(self):
            self.commit(self.fd.getvalue())
            self.fd.close()

    def __init__(self):
        self.data = {}

    def open_read(self, key):
        return io.BytesIO(self.data[key])

    def open_write(self, key, expires=None):
        def commit(b):
            self.data[key] = b
        return WriteHandle(commit=commit)

    def delete(self, key):
        del self.data[key]

    def close(self):
        pass
