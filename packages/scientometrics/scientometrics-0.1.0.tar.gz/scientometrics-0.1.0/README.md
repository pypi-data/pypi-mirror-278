# Scientometrics

Scientometrics is a Python package designed to calculate various bibliometric indices used to measure the impact and productivity of researchers. These indices include the H-index, G-index, and X-index.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Indices](#indices)
  - [H-index](#h-index)
  - [G-index](#g-index)
  - [X-index](#x-index)
- [License](#license)
- [Contributing](#contributing)

## Installation

To install the package, clone the repository and install the required dependencies.

```bash
git clone https://github.com/yourusername/scientometrics.git
cd scientometrics
pip install -r requirements.txt
```

## Usage
To use the package, you can import the desired index calculation functions from the indices module.

```bash
from scientometrics.indices import h_index, g_index, x_index

# Example usage for h-index and g-index
citations = [10, 8, 5, 4, 3]

h = h_index(citations)
g = g_index(citations)

# Example usage for X-index with edge list
edge_list = [
    (1, 'entity1', 10),
    (2, 'entity2', 8),
    (3, 'entity1', 5),
    (4, 'entity3', 4),
    (5, 'entity2', 3)
]

x = x_index.calculate(edge_list)

# print the results
print(f"H-index: {h}")
print(f"G-index: {g}")
print(f"X-index: {x}")
```

## Indices
### H-index
The H-index is a measure that aims to quantify the productivity and citation impact of a researcher. It is defined as the maximum value of h such that the given researcher has published h papers that have each been cited at least h times.

### G-index
The G-index is an index for quantifying scientific productivity based on publication record. It is calculated as the largest number g such that the top g articles received (together) at least g^2 citations.

### X-index
The X-index is a hybrid metric that combines aspects of both the H-index and the G-index. It aims to provide a balanced measure of both productivity and citation impact.

## License
This project is licensed under the MIT License. See the LICENSE.txt file for details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request on GitHub.
Feel free to modify the `git clone` URL and other details according to your specific project setup.
