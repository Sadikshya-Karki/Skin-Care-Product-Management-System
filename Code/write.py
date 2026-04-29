import datetime

def generate_invoice(invoice_data, invoice_type="sale"):
    """
    Generates an invoice as a string and saves it to a text file with a timestamped filename.

    Args:
        invoice_data (dict): Invoice details.
        invoice_type (str): Type of invoice (default: "sale").

    Returns:
        None
    """
    now = datetime.datetime.now()
    timestamp = f"{now.year}{now.month:02d}{now.day:02d}_{now.hour:02d}{now.minute:02d}{now.second:02d}"
    filename = f"invoice_{invoice_type}_{timestamp}.txt"

    try:
        with open(filename, 'w') as file:
            file.write("=" * 100 + "\n")
            file.write(f"{'INVOICE':^100}\n")
            file.write("=" * 100 + "\n")
            file.write(f"Date          : {invoice_data['date']}\n")

            if invoice_type == "sale":
                file.write(f"Customer Name : {invoice_data['customer_name']}\n")
                file.write("-" * 100 + "\n")

                items = invoice_data.get("items", [])
                if items:
                    file.write(f"{'S.N.':<5} {'Product Name':<25} {'Quantity':<10} {'Unit Price (NPR)':<25} {'Total (NPR)':<15}\n")
                    file.write("-" * 100 + "\n")

                    i = 1
                    for product in items:
                        name = product['name']
                        quantity = product['quantity']
                        price = product['unit_price']
                        total = product['total']
                        file.write(f"{i:<5} {name:<25} {quantity:<10} {price:<25.2f} {total:<15.2f}\n")
                        i +=1

                    file.write("-" * 100 + "\n")
                    file.write(f"{'Subtotal':>45}: NPR {invoice_data['subtotal']:.2f}\n")
                    file.write(f"{'VAT (13%)':>45}: NPR {invoice_data['vat_amount']:.2f}\n")
                    file.write(f"{'Total Amount':>45}: NPR {invoice_data['total_amount']:.2f}\n")
                    file.write("=" * 100 + "\n")
                    file.write("Thank you for shopping!\n")
                else:
                    file.write("No products were bought.\n")

            elif invoice_type == "restock":
                file.write(f"Vendor Name   : {invoice_data['vendor_name']}\n")
                file.write("-" * 100 + "\n")
                file.write(f"{'S.N.':<5} {'Product Name':<25} {'Quantity Restocked':<25} {'Cost Price':<20} {'Total':<15}\n")
                file.write("-" * 100 + "\n")

                file.write(f"{1:<5} {invoice_data['product_name']:<25} {invoice_data['quantity_restocked']:<25} "
                        f"{invoice_data['cost_price']:<20.2f} {invoice_data['total_amount']:<15.2f}\n")

                file.write("-" * 100 + "\n")
                file.write(f"{'Total Amount':>45}: NPR {invoice_data['total_amount']:.2f}\n")
                file.write("=" * 100 + "\n")
                file.write("Thank you for your purchase!\n")

        print(f"Invoice saved to {filename}")
    except Exception as e:
        print(f"Error writing invoice to file: {e}")