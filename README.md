# zebrapl2

Python 3 ZPL2 library that generates ZPL2 code which can be sent to Zebra or similar label printers. The library uses only millimeters (mm) as a unit and converts them internally according to printer settings.

## Example use

```python
from zebrapl2 import Label

label=Label(89,36)

# Main Box
label.origin(6,2)
label.draw_box(80,33)
label.endorigin()

# QR Code Box
label.origin(6,2)
label.draw_box(20,22.5)
label.endorigin()

## Date String
label.origin(6,20.5)
label.textblock(20)
label.write_text("14/06/2019", char_height=2, char_width=2)
label.endorigin()

## QR Code
label.origin(9.5,5.5)
label.write_qrcode('ptkr.uk/dm/bc/uss/1090',error_correction="L",magnification=6)
label.endorigin()

# Text Box
label.origin(26,2)
label.draw_box(60,22.5)
label.endorigin()

label.origin(28,4)
label.textblock(60, lines=4, justification="L", line_spacing=0.7)
label.write_text("S-3AX-UA\&sjzgreig\&HPSI0114i-b\&bezi_1 D3", char_height=4, char_width=4)
label.endorigin()

# 1D Barcode
label.origin(11,25.5)
label.write_barcode(5,'C',print_interpretation_line='N')
label.write_text('ptkr.uk/dm/bc/uss/1090')
label.endorigin()

label.origin(6,31.5)
label.textblock(80)
label.write_text("ptkr.uk/dm/bc/uss/1090", char_height=2.5, char_width=2.5)
label.endorigin()

print(label.dumpZPL())
l.preview()
```

The generated ZPL2 code is:

```
^XA^FO72,24^GB960,396,1,B,0^FS^FO72,24^GB240,270,1,B,0^FS^FO72,246^FB240,1,0,C,0^A0N,24,24^FD14/06/2019^FS^FO114,66^BQN,2,6,L,7^FDLA,ptkr.uk/dm/bc/uss/1090^FS^FO312,24^GB720,270,1,B,0^FS^FO336,48^FB720,4,8,L,0^A0N,48,48^FDS-3AX-UA\&sjzgreig\&HPSI0114i-b\&bezi_1 D3^FS^FO132,306^BY3^BCN,60,N,N,N^FDptkr.uk/dm/bc/uss/1090^FS^FO72,378^FB960,1,0,C,0^A0N,30,30^FDptkr.uk/dm/bc/uss/1090^FS^XZ
```
   
## Installation

```sh    
$ pip install --user zebrapl2
```

## Requirements

* PIL or Pillow
