import os
from datetime import datetime

import barcode
from PIL import Image
from barcode.writer import ImageWriter
from reportlab.pdfgen.canvas import Canvas

from shining_brain.constants import work_directory


class LabelCanvas:

    def __init__(self, components=None):
        self.__components = components

    def save(self):
        def draw_rect(canvas, parameter):
            r, g, b = parameter['stroke-color']
            canvas.setStrokeColorRGB(r, g, b)
            canvas.setLineWidth(parameter['line-width'])
            canvas.rect(parameter['x'], parameter['y'], parameter['width'], parameter['height'])

        def draw_string(canvas, parameter):
            canvas.setFont(parameter['font-name'], parameter['font-size'])
            canvas.drawString(parameter['x'], parameter['y'], parameter['text'])

        def draw_image(canvas, parameter):
            canvas.drawImage(parameter['image-path'], parameter['x'], parameter['y'], parameter['width'], parameter['height'])

        def draw_line(canvas, parameter):
            r, g, b = parameter['stroke-color']
            canvas.setStrokeColorRGB(r, g, b)
            canvas.setLineWidth(parameter['line-width'])
            canvas.line(parameter['x1'], parameter['y1'], parameter['x2'], parameter['y2'])

        tmp = work_directory + os.sep + 'tmp' + os.sep

        def generate_barcode(code128, text):
            code = code128(text, writer=ImageWriter())
            barcode_filename = datetime.now().timestamp()
            code.save(tmp + f"{barcode_filename}")
            barcode_file = code.render()
            barcode_filepath = tmp + f"{barcode_filename}.png"
            barcode_file.save(barcode_filepath)
            cropped_barcode_filename = tmp + f'{datetime.now().timestamp()}.png'
            with Image.open(barcode_filepath) as img:
                crop_box = (29, 10, img.width - 29, img.height - 10)
                cropped_img = img.crop(crop_box)
                cropped_img.save(cropped_barcode_filename)
            return cropped_barcode_filename

        def draw_barcode(canvas, parameter):
            barcode.base.Barcode.default_writer_options['write_text'] = False
            code128 = barcode.get_barcode_class('code128')
            cropped_barcode_filename = generate_barcode(code128, parameter['text'])
            canvas.drawImage(cropped_barcode_filename, parameter['x'], parameter['y'], parameter['width'], parameter['height'])

        functions = {
            "rect": draw_rect,
            "text": draw_string,
            "line": draw_line,
            "barcode": draw_barcode,
            "image": draw_image
        }
        filepath = work_directory + os.sep + 'tmp' + os.sep + f'{datetime.now().timestamp()}.pdf'
        c = Canvas(filepath)
        for component in self.__components:
            c.setPageSize(component['pagesize'])
            for e in component['elements']:
                func = functions.get(e['type'])
                if not func:
                    continue
                func(c, e['parameter'])
            c.showPage()

        c.save()
        return filepath
