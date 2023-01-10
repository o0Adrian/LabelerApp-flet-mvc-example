from flet_mvc import FletController, alert
from api import luxmo_api
import flet as ft

# Controller
class Controller(FletController):
    
    def item_selected(self, e=None, invoice_number=None, file=None):
        if e.data == "true":
            self.model.checked_items.set_value(self.model.checked_items() + 1) 
            self.model.files().append(file)
        else:
            self.model.checked_items.set_value(self.model.checked_items() - 1) 
            self.model.files().remove(file)            
            
    def reload_app(self, e=None, show_alert=True):
        last_one = self.model.n_invoices()
        self.model.n_invoices.reset()
        self.model.files.reset()
        self.model.info.current.value = self.model.found_invoices()
        self.model.create_checkboxes()
        self.model.checked_items.reset() 
        
        if show_alert:
        # Update Msg
            diff = self.model.n_invoices() - last_one
            if diff == 0:
                update_msg = "No Invoice Found."
            elif diff > 0:
                update_msg = f"{diff} new invoices were found." if diff != 1 else "A new invoice was found."
            else:
                update_msg = f"{diff * -1} invoices have been removed." if diff != -1 else "One invoice has been removed"
            
            self.alert(f"The view has been reloaded. {update_msg}", alert.INFO)

        self.update()
        
    def create_labels(self, e):
        # Error handling
        if self.model.checked_items() == 0:
            self.alert("! [ERROR] No invoice was selected. Please select an invoice and try again.", alert.ADVICE)
        elif self.model.utility() <= 0 and type(self.model.utility()) != str:
            self.alert("! [ERROR] - Utility percentage should be greater than 0.0%", alert.ADVICE)

        # Creating labels
        else:
            try:
                # Main
                luxmo_api(self.model.utility(), self.model.files())
                
                # Reload view
                self.reload_app(show_alert=False)
                
                # Succeed msg
                self.alert("The labels have been created. The selected invoices\nhave been moved to the 'labeled_invoices' folder", alert.SUCCESS)

            except Exception as e:
                self.alert(f"[ERROR] Contact support -- Error found: {e}")

            
    def check_digits_only(self, e):
        try:
            self.model.utility.set_value(float(e.data))
            e.control.error_text = None
        except ValueError:
            self.model.utility.reset()
            e.control.error_text = "[ERROR] Only digits are allowed"
        
        self.update()
        
    def on_keyboard(self, e: ft.KeyboardEvent):
        if e.key == "D" and e.alt and e.shift:
            self.page.show_semantics_debugger = not self.page.show_semantics_debugger
            self.page.update()
