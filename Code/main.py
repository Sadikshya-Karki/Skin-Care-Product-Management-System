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

def sell_products(products):
    """
    Shows selling products to a customer and generates an invoice.
    """
    display_products(products)
    customer_name = input("Enter customer name: ")
    products_bought = {}
    total_amount = 0

    while True:
        product_name = input("Enter product name (or 'no' to finish): ").strip()
        if product_name.lower() == 'no':
            break

        # Validate product name
        product_to_buy = find_product(products, product_name)
        if not product_to_buy:
            print("Product not found.")
            continue

        quantity = input(f"Enter quantity of {product_name} to buy: ")
        try:
            quantity = int(quantity)
            if quantity <= 0:
                print("Quantity must be a positive integer.")
                continue
        except ValueError:
            print("Invalid quantity. Please enter a number.")
            continue

        # Update product and calculate amount
        if operation.update_product(products, product_name, quantity):
            selling_price = operation.calculate_selling_price(product_to_buy['cost_price'])
            amount = selling_price * quantity
            total_amount += amount

            products_bought[product_to_buy['name']] = {
                'name': product_to_buy['name'],
                'quantity': quantity,
                'unit_price': selling_price,
                'total': amount
            }
            print(f"Added {quantity} {product_name}(s) to the purchase.")
        else:
            print("Failed to add to purchase due to quantity issues.")

    # Generate invoice data
    now = datetime.datetime.now()
    if products_bought:
        subtotal = total_amount / 1.13
        vat_amount = total_amount - subtotal

        # Prepare formatted products for the invoice
        formatted_products = []
        for item in products_bought.values():
            formatted_products.append(item)

            invoice_data = {
            "customer_name": customer_name,
            "date": f"{now.year}-{now.month:02d}-{now.day:02d} {now.hour:02d}:{now.minute:02d}:{now.second:02d}",
            "items": formatted_products,
            "subtotal": round(subtotal, 2),
            "vat_percent": 13,
            "vat_amount": round(vat_amount, 2),
            "total_amount": round(total_amount, 2)
        }

        write.generate_invoice(invoice_data, invoice_type="sale")

        # Save updated product quantities to products.txt
        write_products_to_file("products.txt", products)
    else:
        # Generate a "no products bought" invoice
        invoice_data = {
            "customer_name": customer_name,
            "date": f"{now.year}-{now.month:02d}-{now.day:02d} {now.hour:02d}:{now.minute:02d}:{now.second:02d}",
            "items": []
        }
        write.generate_invoice(invoice_data, invoice_type="sale")

def restock_products(products):
    """
    Handles restocking of products.
    """
    display_products(products)
    vendor_name = input("Enter vendor name: ")
    product_name = input("Enter product name: ").strip()

    # Validate product name
    product_to_restock = find_product(products, product_name)
    if not product_to_restock:
        print("Product not found.")
        return

    quantity = input(f"Enter quantity to restock for {product_name}: ")
    try:
        quantity = int(quantity)
        if quantity <= 0:
            print("Quantity must be a positive integer.")
            return
    except ValueError:
        print("Invalid quantity. Please enter a number.")
        return

    cost_price = input(f"Enter new cost price for {product_name}: ")
    try:
        cost_price = float(cost_price)
        if cost_price <= 0:
            print("Cost price must be a positive number.")
            return
    except ValueError:
        print("Invalid cost price. Please enter a number.")
        return

    # Update product information
    product_to_restock['quantity'] += quantity
    product_to_restock['cost_price'] = cost_price

    # Generate invoice data
    now = datetime.datetime.now()
    total_amount = quantity * cost_price

    # Prepare invoice details
    invoice_data = {
        "vendor_name": vendor_name,
        "date": f"{now.year}-{now.month:02d}-{now.day:02d} {now.hour:02d}:{now.minute:02d}:{now.second:02d}",
        "product_name": product_name,
        "quantity_restocked": quantity,
        "cost_price": cost_price,
        "total_amount": total_amount
    }

    # Generate invoice
    write.generate_invoice(invoice_data, invoice_type="restock")

    # Save updated product list to products.txt
    write_products_to_file("products.txt", products)

def find_product(products, product_name):
    """
    Finds a product in the list of products by name.
    """
    for product in products:
        if product['name'].lower() == product_name.lower():
            return product
    return None

def write_products_to_file(filename, products):
    """
    Writes the product data back to the file.
    """
    try:
        with open(filename, 'w') as file:
            for product in products:
                line = f"{product['name']},{product['brand']},{product['quantity']},{product['cost_price']},{product['country']}\n"
                file.write(line)
        print("Product data updated in products.txt")
    except Exception as e:
        print(f"Error writing to file: {e}")

def main():
    """
    Main function to run the skin care product sale system.
    """
    products = read.read_products_from_file()
    if not products:
        print("Could not load products.")
        return

    while True:
        print("\nOptions:")
        print("1. Display Products")
        print("2. Sell Products")
        print("3. Restock Products")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            display_products(products)
        elif choice == '2':
            sell_products(products)
        elif choice == '3':
            restock_products(products)
        elif choice == '4':
            print("Goodbye")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()