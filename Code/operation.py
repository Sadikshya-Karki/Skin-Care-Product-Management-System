def calculate_selling_price(cost_price, apply_vat=True):
    """
    Calculates the selling price based on a 200% markup of the cost price,
    with an optional 13% VAT.

    Args:
        cost_price (float): The cost price of the item.
        apply_vat (bool): Whether to apply 13% VAT (default: True).

    Returns:
        float: The calculated selling price including VAT if applicable.
    """
    markup_price = cost_price * 2  
    if apply_vat:
        return markup_price * 1.13  
    return markup_price

def update_product(products, product_name, quantity_sold):
    """
    Updates the quantity of a product after a sale.  Applies the 'buy three get one free' policy.

    Args:
        products (list): A list of dictionaries, where each dictionary represents a product
                         and has keys like 'name' (str) and 'quantity' (int).
        product_name (str): The name of the product being sold.
        quantity_sold (int): The number of products sold.

    Returns:
        bool: True if the stock was updated successfully, False otherwise (e.g., not enough stock).
    """
    for product in products:
        if product['name'].lower() == product_name.lower():
            # Calculate the total quantity the customer receives (including free items)
            total_received = quantity_sold + (quantity_sold // 3)

            if product['quantity'] >= total_received:
                product['quantity'] -= total_received
                return True
            else:
                print(f"Not enough quantity for {product_name}. Available: {product['quantity']}")
                return False
    print(f"Product {product_name} not found.")
    return False


if __name__ == '__main__':
    # Example (for testing purposes):
    products = [
        {'name': 'Vitamin C Serum', 'brand': 'Garnier', 'quantity': 10, 'cost_price': 200, 'country': 'France'}
    ]
    selling_price = calculate_selling_price(200)
    print(f"Selling price: {selling_price}")

    if update_product(products, 'Vitamin C Serum', 3):
        print(f"Quantity updated. Remaining: {products[0]['quantity']}")
    else:
        print("Quantity update failed.")

