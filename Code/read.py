def read_products_from_file(filename="products.txt"):
    """
    Reads product information from the text file "products.txt".

    Args:
        filename (str): The name of the file to read from (default: "products.txt").

    Returns:
        list: A list of dictionaries, where each dictionary represents a product.
              Returns an empty list if the file is not found or an error occurs.
    """
    products = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                # Split each line into product details
                product_data = [item.strip() for item in line.strip().split(',')]  

                # Makes sure there are enough values in the line
                if len(product_data) == 5:
                    name, brand, quantity, cost_price, country = product_data

                    # Convert quantity and cost_price to the correct data types
                    try:
                        quantity = int(quantity)
                        cost_price = float(cost_price)
                    except ValueError:
                        print(f"Error: Invalid quantity or cost price in line: {line.strip()}")
                        continue 

                    # Create a dictionary for the product
                    product = {
                        'name': name,
                        'brand': brand,
                        'quantity': quantity,
                        'cost_price': cost_price,
                        'country': country
                    }
                    products.append(product)
                else:
                    print(f"Error: Invalid data format in line: {line.strip()}")

    except FileNotFoundError:
        print(f"Error: File not found: {filename}")
    except Exception as e:
        print(f"Error reading file: {e}")

    return products

if __name__ == '__main__':
    # Example
    product_list = read_products_from_file()
    if product_list:
        for product in product_list:
            print(product)