import xmlrpc.client
import os
import ssl
from dotenv import load_dotenv, find_dotenv

def create_sales_order(customer_identifier, product_ids, quantities):
    """
    Creates a sales order in Odoo with multiple products for a specified customer identified by ID or name.

    Parameters:
    - customer_identifier (int or str): The customer ID or name.
    - product_ids (list of int): List of product IDs.
    - quantities (list of int): Corresponding quantities for each product.

    Returns:
    - str: A message indicating the success or failure of the operation.
    """
    if len(product_ids) != len(quantities):
        return "Error: Product IDs and quantities must have the same length."

    load_dotenv(find_dotenv())

    url = os.getenv('URL')
    db = os.getenv('DB_NAME')
    username = os.getenv('USERNAME_odoo')
    password = os.getenv('PASSWORD')

    try:
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context

        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True, verbose=False, use_datetime=True, context=ssl._create_unverified_context())
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), allow_none=True, verbose=False, use_datetime=True, context=ssl._create_unverified_context())
        uid = common.authenticate(db, username, password, {})

        if isinstance(customer_identifier, int):
            customer_id = customer_identifier
        elif isinstance(customer_identifier, str):
            customer_ids = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['name', '=', customer_identifier]]])
            if not customer_ids:
                raise ValueError(f"No customer found with name {customer_identifier}")
            customer_id = customer_ids[0]
        else:
            raise ValueError("Customer identifier must be an integer (ID) or string (name)")

        order_lines = []
        for product_id, quantity in zip(product_ids, quantities):
            order_lines.append((0, 0, {'product_id': product_id, 'product_uom_qty': quantity}))

        order_id = models.execute_kw(db, uid, password, 'sale.order', 'create', [{
            'partner_id': customer_id,
            'order_line': order_lines
        }])

        models.execute_kw(db, uid, password, 'sale.order', 'action_confirm', [order_id])

        return f'Successfully created and confirmed order with ID: {order_id}'
    except Exception as e:
        return f'Failed to create order: {e}'
