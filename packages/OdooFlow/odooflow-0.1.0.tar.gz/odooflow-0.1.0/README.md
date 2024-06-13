# OdooFlow

OdooFlow is a Python package to create sales orders in Odoo with multiple products for a specified customer identified by ID or name.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install OdooFlow.

```bash
pip install OdooFlow

```
```bash
from OdooFlow import create_sales_order

customer_identifier = 'John Doe'  # Could also be an integer ID
product_ids = [30, 42]  # Product IDs
quantities = [5, 2]  # Corresponding quantities

result = create_sales_order(customer_identifier, product_ids, quantities)
print(result)
```