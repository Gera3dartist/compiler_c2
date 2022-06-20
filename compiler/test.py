from contextlib import contextmanager

@contextmanager
def test():
    print("before")
    yield
    print("after")

with test():
    print("in the middle")