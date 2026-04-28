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


