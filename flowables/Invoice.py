from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table

from flowables.FlowableInvoiceHeading import FlowableInvoiceHeading


class Invoice:

    def __init__(self, output_path: str, data: dict):
        '''
        Create an Invoice object.

        data format is
        data = {
            "number": "xxx",
            "p_iva_cliente": " xxx",
            "cf_cliente": "xxx",
            "path_logo": "https://...",
            "items_list": [
                    {
                        "quantity": 0,
                        "description": "Generatore fatture",
                        "unityPrice": 150
                    }
                ]
        }

        :param output_path: Path where to save the output file
        :param logo_path: Path of the logo
        :param data: Data to write in table
        '''
        self.__output_path = output_path
        self.__data = data

    def generate(self):
        doc = SimpleDocTemplate(self.__output_path, pagesize=A4, leftMargin=0, topMargin=0, bottomMargin=0,
                                rightMargin=0)
        elements = list()
        date_today = datetime.now()
        invoiceHeading = FlowableInvoiceHeading(numero_fattura=self.__data['invoice_number'], data=date_today.strftime("%d/%m/%Y"),
                                                partita_iva_cliente=self.__data['p_iva_customer'],
                                                codice_fiscale_cliente=self.__data['cf_customer'], logo_path=self.__data["path_logo"])
        elements.append(invoiceHeading)
        elements.append(self.__generate_products_table())

        # write the document to disk
        doc.build(elements)

    def __generate_products_table(self, x=0, y=0, margin=0):
        # width = 575 - margin
        height = 400
        # starting_x = x + margin
        # starting_y = y - margin - height

        # canvas.rect(x=starting_x, y=starting_y, width=width, height=height, stroke=1, fill=0)
        table_data = self.__generate_array_from_data()
        table_data.insert(0, ['quantità', 'descrizione', 'prezzo unitario', 'totale'])

        table = Table(table_data, colWidths=[100, 265, 100, 100])
        table.setStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('ROWBACKGROUNDS', (0, 0), (-1, 0), [HexColor('#0396ffa')]),
                        ('ROWBACKGROUNDS', (0, 1), (-1, len(table_data) - 1), [HexColor('#abdcff'), HexColor('#81caff')])])

        return table

    def __generate_array_from_data(self) -> list:
        table_data = []
        for element in self.__data["items_list"]:
            total_price = element['quantity'] * element['unityPrice']
            table_data.append([element['quantity'], element['description'], element['unityPrice'], total_price])

        return table_data
