import pytest

def caclulate_temp_change(cycle):
    if cycle < 0:
        cycle = 0
    return (cycle**2.0)

def temp_change_test():
    assert caclulate_temp_change(0.03) == 0.0009