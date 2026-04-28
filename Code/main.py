import read
import write
import operation
import datetime

def display_products(products):
    """
    Displays the available products with their selling prices in a table format.
    """
    print("\nAvailable Products:")
    print("-" * 116)
    print(f"| {'S.N.':<5} | {'Product Name':30} | {'Brand':20} | {'Country':20} | {'Quantity':10} | {'Price (NPR)':12} |")
    print("-" * 116)

    index = 1
    for product in products:
        selling_price = operation.calculate_selling_price(product['cost_price'])
        print(f"| {index:<5} | {product['name']:30} | {product['brand']:20} | {product['country']:20} | {product['quantity']:<10} | {selling_price:12.2f} |")
        index += 1

    print("-" * 116)

