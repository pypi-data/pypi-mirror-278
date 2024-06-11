import os
import pickle
import pytest
from picklecachefunc import picklecachefunc

@picklecachefunc(arg_name='file_name')
def compute_expensive_function(file_name, x, y):
    return x + y

def test_picklecachefunc_decorator(tmpdir):
    file_name = tmpdir.join("test_cache.pkl")

    result1 = compute_expensive_function(file_name=str(file_name), x=3, y=4)
    assert result1 == 7

    result2 = compute_expensive_function(file_name=str(file_name), x=5, y=6)
    assert result2 == 7  # Should load the cached result

    with open(str(file_name), 'rb') as f:
        cached_result = pickle.load(f)
    assert cached_result == 7

if __name__ == "__main__":
    pytest.main()
