# Sorting Algorithms Package

A collection of sorting algorithms implemented in Python.

## Introduction
This repository contains a collection of sorting algorithms implemented in Python. The goal of this project is to provide a comprehensive set of sorting algorithms that can be used for educational and practical purposes.

## Features
* Implementation of various sorting algorithms, including:
	+ Bubble sort
	+ Selection sort
	+ Insertion sort

## Installation
You can install this package using pip:
```
pip install siwp2005-james-sort
```

## Usage
You can use the sorting algorithms as follows:
```python
from siwp2005-james-sort.src.sort import bubble_sort, insertion_sort, quick_sort

arr = [3, 2, 1]
arr = bubble_sort(arr)
print(arr)  # [1, 2, 3]

arr = [3, 2, 1]
arr = insertion_sort(arr)
print(arr)  # [1, 2, 3]

arr = [3, 2, 1]
arr = quick_sort(arr)
print(arr)  # [1, 2, 3]
```

## Running Tests
To run the tests, navigate to the root directory of the project and run the following command:
```
python -m unittest tests/test_bubble_sort.py
```
```
python -m unittest tests/test_insertion_sort.py
```
```
python -m unittest tests/test_quick_sort.py
```

This will execute the test cases in `test_bubble_sort.py`,`test_insertion_sort.py`,`test_quick_sort.py` and report any failures or errors.
Alternatively, you can run all tests in the `tests` directory using:
```
python -m unittest discover -s tests -p 'test_*.py'
```
This will discover and run all test files in the `tests` directory that match the pattern `test_*.py`.
