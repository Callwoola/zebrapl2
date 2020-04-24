import re, math, io
from PIL import Image
import PIL.ImageOps

try: from urllib.request import urlopen
except ImportError: from urllib2 import urlopen

class Label(object):
    def __init__(self, height, width=110.0, dpmm=12.0):
        self.height=height
        self.width=width
        self.dpmm=dpmm

        self.code="^XA"

    def origin(self, x,y):
        self.code+="^FO{},{}".format(int(x*self.dpmm), int(y*self.dpmm))

    def endorigin(self):
        self.code+='^FS'

    def textblock(self, width, justification='C', lines=1, line_spacing=0):
        assert justification in ['L','R','C','J']
        self.code+="^FB{},{},{},{},{}".format(int(width*self.dpmm), lines, int(line_spacing*self.dpmm), justification, 0)

    def write_text(self, text, char_height=None, char_width=None, font='0', orientation='N',
                   line_width=None, max_line=1, line_spaces=0, justification='L', hanging_indent=0):
        if char_height and char_width and font and orientation:
            assert orientation in 'NRIB', "Invalid orientation"
            if re.match(r'^[A-Z0-9]$', font):
                self.code+="^A{}{},{},{}".format(font[0], orientation[0], int(char_height*self.dpmm),
                                               int(char_width*self.dpmm))
            elif re.match(r'[REBA]?:[A-Z0-9\_]+\.(FNT|TTF|TTE)', font):
                self.code+="^A@{},{},{},{}".format(orientation[0], int(char_height*self.dpmm),
                                               int(char_width*self.dpmm), font)
            else: raise ValueError("Invalid font.")
        if line_width:
            assert justification in "LCRJ", "Invalid justification"
            self.code+="^FB{},{},{},{},{}".format(int(line_width*self.dpmm), max_line, line_spaces,
                                                justification[0], hanging_indent)
        self.code+="^FD{}".format(text)

    def set_default_font(self, height, width, font='0'):
        assert re.match(r'[A-Z0-9]', font), "Invalid font"
        self.code+="^CF{},{},{}".format(font[0], height*self.dpmm, width*self.dpmm)

    def _convert_image(self, image, width, height, compression_type='A'):
        image=image.resize((int(width*self.dpmm), int(height*self.dpmm)))
        # invert, otherwise we get reversed B/W
        # https://stackoverflow.com/a/38378828
        image=PIL.ImageOps.invert(image.convert('L')).convert('1')

        if compression_type == "A": return image.tobytes().hex().upper()
        # TODO this is not working
        #elif compression_type == "B": return image.tostring()
        else: raise Exception("Unsupported compression type")


    def upload_graphic(self, name, image, width, height=0):
        if not height: height=int(float(image.size[1])/image.size[0]*width)
        assert 1 <= len(name) <= 8, "Filename must have length [1:8]"

        totalbytes=math.ceil(width*self.dpmm/8.0)*height*self.dpmm
        bytesperrow=math.ceil(width*self.dpmm/8.0)

        data=self._convert_image(image, width, height)

        self.code+="~DG{}.GRF,{},{},{}".format(name, totalbytes, bytesperrow, data)

        return height

    def write_graphic(self, image, width, height=0, compression_type="A"):
        if not height: height=int(float(image.size[1])/image.size[0]*width)

        totalbytes=math.ceil(width*self.dpmm/8.0)*height*self.dpmm
        bytesperrow=math.ceil(width*self.dpmm/8.0)

        data=self._convert_image(image, width, height, compression_type=compression_type)

        if compression_type == "A":
            self.code+="^GFA,{},{},{},{}".format(len(data), totalbytes, bytesperrow, data)
        # TODO this is not working:
        elif compression_type == "B":
            self.code+="^GFB,{},{},{},{}".format(len(data), totalbytes, bytesperrow, data)
        else: raise Exception("Unsupported compression type.")

        return height

    def draw_box(self, width, height, thickness=1, color='B', rounding=0):
        assert color in 'BW', "Invalid color"
        assert rounding <= 8, "Invalid rounding"
        self.code+="^GB{},{},{},{},{}".format(int(width*self.dpmm), int(height*self.dpmm), thickness, color[0], int(rounding*self.dpmm))

    def draw_ellipse(self, width, height, thickness=1, color='B'):
        assert color in 'BW', "Invalid color"
        self.code+="^GE,{},{},{},{}".format(int(width*self.dpmm), int(height*self.dpmm), thickness, color[0])

    def print_graphic(self, name, scale_x=1, scale_y=1):
        self.code+="^XG{},{},{}".format(name, scale_x, scale_y)

    def run_script(self, filename):
        self.code+="^XF{}^FS"

    def write_field_number(self, number, name=None, char_height=None, char_width=None, font='0',
                           orientation='N', line_width=None, max_line=1, line_spaces=0,
                           justification='L', hanging_indent=0):
        if char_height and char_width and font and orientation:
            assert re.match(r'[A-Z0-9]', font), "Invalid font"
            assert orientation in 'NRIB', "Invalid orientation"
            self.code+="^A{}{},{},{}".format(font[0], orientation[0], int(char_height*self.dpmm),
                                             int(char_width*self.dpmm))
        if line_width:
            assert justification in "LCRJ", "Invalid justification"
            self.code+="^FB{},{},{},{},{}".format(int(line_width*self.dpmm), max_line, line_spaces,
                                                  justification[0], hanging_indent)
        self.code+="^FN{}" % number
        if name:
            assert re.match("^[a-zA-Z0-9 ]+$", name), "Name may only contain alphanumerical characters and spaces"
            self.code+='"{}"' % name

    def write_barcode(self, height, barcode_type, orientation='N', check_digit='N',
                       print_interpretation_line='Y', print_interpretation_line_above='N', mode='N', module_width=3):

        assert barcode_type in ['2', '3', 'C', 'U'], "Unsupported barcode type"

        self.code+="^BY{}".format(module_width)

        if barcode_type == '2':
            barcode_zpl='^B{}{},{},{},{},{}'.format(barcode_type, orientation, int(height*self.dpmm),
                                                    print_interpretation_line,
                                                    print_interpretation_line_above,
                                                    check_digit)
        elif barcode_type == '3':
            barcode_zpl='^B{}{},{},{},{},{}'.format(barcode_type, orientation,
                                                    check_digit, int(height*self.dpmm),
                                                    print_interpretation_line,
                                                    print_interpretation_line_above)

        elif barcode_type == 'C':
            barcode_zpl='^B{}{},{},{},{},{}'.format(barcode_type, orientation, int(height*self.dpmm),
                                                    print_interpretation_line,
                                                    print_interpretation_line_above,
                                                    check_digit)

        elif barcode_type == 'U':
            barcode_zpl='^B{}{},{},{},{},{},{}'.format(barcode_type, orientation, int(height*self.dpmm),
                                                       print_interpretation_line,
                                                       print_interpretation_line_above,
                                                      check_digit, mode)

        self.code+=barcode_zpl

    def write_qrcode(self, data, model=2, magnification=3, error_correction="Q", mask_value=7, orientation='N'):
        assert model in (1,2)
        assert magnification in range(1,11)
        assert error_correction in ("H","Q","M","L")
        assert mask_value in range(0,8)

        self.code+='^BQ{},{},{},{},{}'.format(orientation,model,magnification,error_correction,mask_value)
        self.code+='^FD{}A,{}'.format(error_correction,data)

    def dumpZPL(self): return self.code+"^XZ"

    def saveFormat(self, name):
        self.code= self.code[:3]+"^DF{}^FS".format(name)+self.code[3:]

    def preview(self, index=0):
        try:
            url='http://api.labelary.com/v1/printers/{}dpmm/labels/{:f}x{:f}/{}/'.format(
                int(self.dpmm), self.width/25.4, self.height/25.4, index)
            print(url)
            res=urlopen(url, self.dumpZPL().encode()).read()
            Image.open(io.BytesIO(res)).show()
        except IOError: raise Exception("Invalid preview received, mostlikely bad ZPL2 code uploaded.")