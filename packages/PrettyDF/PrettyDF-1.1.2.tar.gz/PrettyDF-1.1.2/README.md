# PrettyDF Package

The PrettyDF package is a Python library crafted by DawnSaju, designed to enhance the visual representation of pandas DataFrames. It provides a set of tools to make your DataFrames more readable and visually appealing.

## Installation

You can install the PrettyDF package via pip:

```bash
pip install PrettyDF
```

## Usage

Import the required functions from the package in your Python script:

```python
from PrettyDF import table
```

And the `table` function to display your DataFrame in a tabular format:

```python
import pandas as pd

data = pd.DataFrame({
    'Name': ['John', 'Anna', 'Peter'],
    'Age': [28, 24, 35],
    'City': ['New York', 'Paris', 'Berlin']
})

table(data)
```