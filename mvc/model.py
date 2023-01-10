import flet as ft
import xmltodict
import flet_mvc
from functools import partial
from api import read_xml_files

# Model
class Model():
    def __init__(self):
        # References
        self.info = ft.Ref[ft.Text]()
        self.checkboxes = ft.Ref[ft.ListView]()

            # # Initial State FIXME!! How do we make it visible on the start of the model without waiting the view to run...
            # self.create_checkboxes()
        
        # [Optional]
        self.controller = None

    @flet_mvc.data
    def n_invoices(self):
        return len(self.xml_files())

    @flet_mvc.data
    def checked_items(self):
        return 0
    
    @flet_mvc.data
    def utility(self):
        return 0.0
    
    @flet_mvc.data
    def files(self):
        return []

    def create_checkboxes(self):
        self.checkboxes.current.controls = []
        for file in self.xml_files():
            with open(file, 'r') as f:
                invoice_number = xmltodict.parse(f.read())['Invoice']['InvoiceNumber']
                
            self.checkboxes.current.controls.append(
                ft.Row(
                    controls=[
                        ft.Checkbox(on_change=partial(self.controller.item_selected, invoice_number=invoice_number, file=file)),
                        ft.Text(invoice_number, size=18),
                    ]
                ),
            )

    def found_invoices(self):
        if self.n_invoices() == 0:
            return "No invoices were found in the 'xml' folder."
        else:
            return f"{f'{self.n_invoices()}' if self.n_invoices() > 1 else 'One'} {'invoices were' if self.n_invoices() > 1 else 'invoice was'} found.\nSelect the required invoices to label:"
    
    def xml_files(self):
        return read_xml_files()
