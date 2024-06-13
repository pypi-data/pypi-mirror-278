[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/tharungoka/labneura/CI)](https://github.com/tharungoka/labneura/actions)

# LabNeura

LabNeura is a comprehensive library designed for implementing basic to advanced algorithms in C++, with a focus on efficiency. The library is exposed as a module using Pybind11, allowing users to call its functionality from both Python and C++. LabNeura covers a wide range of algorithms, from basic sorting and graph algorithms to machine learning, reinforcement learning, and deep learning algorithms.

## Table of Contents

- [LabNeura](#labneura)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Using LabNeura in Python](#using-labneura-in-python)
    - [Using LabNeura in C++](#using-labneura-in-c)
  - [Features](#features)
  - [Contributing](#contributing)
  - [License](#license)

## Installation

### Prerequisites

- C++11 or later
- Python 3.8 or later
- CMake 3.14 or later
- pybind11

### Install from PyPI

You can install LabNeura from PyPI using pip:

```sh
pip install labneura
```

### Build from Source

1. Clone the repository:

```sh
git clone https://github.com/yourusername/labneura.git
cd labneura
```

2. Build & Install the project using Make:

```sh
make install
```

## Usage

### Using LabNeura in Python

Here's an example of how to use LabNeura's sorting algorithms in Python:

```python
import labneura

# Create an instance of the Sorting class
sorting = labneura.Sorting([3, 6, 8, 10, 1, 2, 1])

# Perform bubble sort
sorting.bubble()
print("Bubble sorted array:", sorting.data)

# Perform quick sort
sorting.quick()
print("Quick sorted array:", sorting.data)
```

### Using LabNeura in C++

Include the LabNeura headers in your C++ project:

```cpp
#include <labneura/sorting.hpp>

int main() {
    std::vector<int> data = {3, 6, 8, 10, 1, 2, 1};
    Sorting sorting(data);

    // Perform bubble sort
    sorting.bubble();
    std::cout << "Bubble sorted array: ";
    for (const auto& num : sorting.getData()) {
        std::cout << num << " ";
    }
    std::cout << std::endl;

    // Perform quick sort
    sorting.quick();
    std::cout << "Quick sorted array: ";
    for (const auto& num : sorting.getData()) {
        std::cout << num << " ";
    }
    std::cout << std::endl;

    return 0;
}
```

## Features

- **Sorting Algorithms**: Bubble Sort, Quick Sort, and more.
- **Graph Algorithms**: Basic graph traversal and search algorithms.
- **Machine Learning**: Basic algorithms such as Linear Regression.
- **Reinforcement Learning**: (Coming soon)
- **Deep Learning**: (Coming soon)

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING](CONTRIBUTING.md) guidelines for more information.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
