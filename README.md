# Labeler

This Flet app example converts an xml invoice into printable labels that can be added to the products with the final price (Utility + Tax) and an excel to keep all calculation.

This example app uses the flet-mvc package (https://pypi.org/project/flet-mvc/). Thus providing an example on how to use the MVC structure in Flet


## Usage/Steps

1. Place the invoices to be labeled in the "xml" folder. (already provided)
2. Run labeler.py
3. Choose the invoices to be labeled
4. Enter the percentage of utility
5. Press "Create Labels" (The xmls will be moved to "labeled_invoices")

You can now review "labels" and "excel" folder for the result.

You can move again the xml file that was moved into "labeled_invoices" to "xml" folder again and in order to see it, press "reload" icon on the top right corner.