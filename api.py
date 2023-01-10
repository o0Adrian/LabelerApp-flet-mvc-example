"""
Client: Test Market
Product: Labeler
Developer: C. Adrián Monroy
Description: Convert XML files to an excel
spreadsheet and printable labels
"""


from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from typing import List
import os
import xmltodict
import pandas as pd


def read_xml_files():
    # Get the directory containing the script
    script_dir = os.path.dirname(__file__)

    # Set the directory where the files are located
    files_dir = os.path.join(script_dir, 'xml')

    return [os.path.join(files_dir, file) for file in os.listdir(files_dir)]

def create_printing_labels(invoice_number, labels):
    script_dir = os.path.dirname(__file__)
    output_dir = os.path.join(script_dir, 'labels')
    
    # Create a canvas with the desired page size
    c = canvas.Canvas(os.path.join(output_dir, f"{invoice_number}.pdf"), pagesize=letter)
    c.setFontSize(6)

    # Iterate through the rows of the DataFrame
    for i, label in enumerate(labels):
        # Calculate the position of the label based on the current iteration
        x = 10 + (i % 8) * 75   # 10 is the start position - 7 the items in a row - 60 the span between items in a row
        y = 750 - (i // 8) * 48  # 750 because that will position the top row of labels at the top of the page
    
        # Draw the label contents on the canvas, using an space of 8 between items
        c.drawString(x, y+16, label["final price"])
        c.drawString(x, y+8, label["product"])
        c.drawString(x, y, label["invoice_number"])

        # If we have drawn 50 labels, start a new page
        if (i+1) % 80 == 0:
            c.showPage()
            c.setFontSize(8)

    # Save the canvas to a PDF file
    c.save()


def convert_to_dataframe(xmldict, utility):
    # Datos
    invoice_number = xmldict['Invoice']['InvoiceNumber']
    products = xmldict['Invoice']['Products']['Product']
    tax_pct = 0.16
    
    labels = []
    numbers = {}
    data = []
    
    products = [products] if type(products) != list else products 
    for product in products:
        price = float(product["price"])
        
        data.append({
            "Quantity": product["quantity"],
            "Product": product["name"],
            "Price": price,
            "Utility Percentage": str(utility*100)+"%",
            "Price before tax": (price * (utility+1)),
            "TAX": (price * (utility+1)) * tax_pct,
            "Final Price": (price * (utility+1)) * (1+tax_pct),
        })  # Every item is a row
        
        df = pd.DataFrame(data)
        
        for i in range(int(product["quantity"])):
            numbers[product["name"]] = numbers.get(product['name'], 0) + 1
            labels.append(
                {
                    "final price": f"${round((price * (utility+1)) * (1+tax_pct), 2)}",
                    "product": product["name"],
                    "invoice_number": f"{invoice_number} #{numbers[product['name']]}", 
                }
            )
        
    # Create printing labels
    create_printing_labels(invoice_number, labels)
    
    # Export to excel
    convert_to_excel(df, invoice_number)

    return df


def convert_to_excel(df, invoice_number):
    script_dir = os.path.dirname(__file__)
    output_dir = os.path.join(script_dir, 'excel')
    
    df.to_excel(os.path.join(output_dir, f'{invoice_number}.xlsx'), sheet_name=invoice_number, index=False)


def luxmo_api(utility: float, files: List[str]):
    utility = utility/100
    for file in files:
        # Open the XML file
        with open(file, 'r') as f:
            # Parse the XML document
            dic = xmltodict.parse(f.read())
            convert_to_dataframe(dic, utility)
            
        path_parts = file.split(os.sep)
        path_parts[-2] = "labeled_invoices"
        new_path = os.sep.join(path_parts)
        os.rename(file, new_path)

if __name__ == "__main__":
    files = read_xml_files()
    utility = 15
    luxmo_api()
