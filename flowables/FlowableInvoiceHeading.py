from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Flowable


class FlowableInvoiceHeading(Flowable):
    __flowable_width = 0
    __flowable_height = 0

    def __init__(self, numero_fattura: str = None, data: str = None, partita_iva_cliente: str = None,
                 codice_fiscale_cliente: str = None, xoffset=0,
                 size=None, logo_path=None):
        super().__init__()
        self.__numero_fattura = numero_fattura
        self.__data = data
        self.__partita_iva_cliente = partita_iva_cliente
        self.__codice_fiscale_cliente = codice_fiscale_cliente
        self.__logo_path = logo_path

        if size is None: size = 4 * cm
        self.xoffset = xoffset
        self.size = size
        # normal size is 4 cm
        self.scale = size / (4.0 * cm)

    def wrap(self, availWidth, availHeight, *args):
        self.__flowable_width = availWidth
        self.__flowable_height = 200
        return self.__flowable_width, self.__flowable_height

    def draw(self):
        canvas = self.canv
        # canvas.rect(x=0, y=0, width=self.__flowable_width, height=self.__flowable_height, stroke=1)
        starting_x, starting_y = self.__generate_company_logo(canvas, x=0, y=self.__flowable_height, margin=10)
        self.__generate_company_info(canvas, x=starting_x, y=self.__flowable_height, margin=10)

    def __generate_company_logo(self, canvas, x=0, y=0, margin=0):
        width = 200
        height = 150
        starting_x = x + margin
        starting_y = y - height - margin
        # canvas.rect(x=starting_x, y=starting_y, width=width, height=height, stroke=1)
        if self.__logo_path:
            img = ImageReader(self.__logo_path)
            img_width, img_height = img.getSize()

            resize_height, resize_width = self.get_image_sizes(height, img_height, img_width, width)
            starting_x, starting_y = self.get_startinz_coordinates(height, resize_height, resize_width, starting_x,
                                                                   starting_y, width)
            canvas.drawImage(self.__logo_path, x=starting_x, y=starting_y, width=resize_width, height=resize_height,
                             mask='auto')
        return starting_x + width, starting_y

    def get_startinz_coordinates(self, height, resize_height, resize_width, starting_x, starting_y, width):
        if resize_height < height:
            starting_y = starting_y + ((height - resize_height) / 2)
        if resize_width < width:
            starting_x = starting_x + ((width - resize_width) / 2)
        return starting_x, starting_y

    def get_image_sizes(self, height, img_height, img_width, width):
        target_ratio = height / width
        im_ratio = img_height / img_width
        if target_ratio > im_ratio:
            # It must be fixed by width
            resize_width = width
            resize_height = round(resize_width * im_ratio)
        else:
            # Fixed by height
            resize_height = height
            resize_width = round(resize_height / im_ratio)
        return resize_height, resize_width

    def __generate_company_info(self, canvas, x=0, y=0, margin=0):
        # width = 370
        height = 180
        text_margin = 15
        starting_x = x + margin
        starting_y = y - margin - height
        ending_y = y - margin
        # canvas.rect(x=starting_x, y=starting_y, width=width, height=height, stroke=1, fill=0)
        canvas.drawString(starting_x + 10, ending_y - text_margin, f"Fattura n°: {self.__numero_fattura}")
        canvas.drawString(starting_x + 10, ending_y - text_margin * 2, f"Data: {self.__data}")
        canvas.drawString(starting_x + 10, ending_y - text_margin * 3,
                          f"Partita iva del cliente: {self.__partita_iva_cliente}")
        canvas.drawString(starting_x + 10, ending_y - text_margin * 4,
                          f"Codice fiscale del cliente: {self.__codice_fiscale_cliente}")
        return starting_x, starting_y
