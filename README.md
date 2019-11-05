# zebrapl2

Python 3 ZPL2 library that generates ZPL2 code which can be sent to Zebra or similar label printers. The library uses only millimeters (mm) as a unit and converts them internally according to printer settings.

## Example use

```python
from zebrapl2 import Label

label=Label(89,36)

# Main Box
label.origin(2,6)
label.draw_box(33,80)
label.endorigin()

# QR Code Box
label.origin(12.5,6)
label.draw_box(22.5,20)
label.endorigin()

## Date String
label.origin(14.5,6)
label.textblock(20)
label.write_text("14/06/2019", char_height=2, char_width=2, orientation="R")
label.endorigin()

## QR Code
label.origin(19,9)
label.write_qrcode('ptkr.uk/dm/bc/uss/1090',error_correction="L",magnification=6,orientation='R')
label.endorigin()

# Text Box
label.origin(12.5,26)
label.draw_box(22.5,60)
label.endorigin()

label.origin(14,28)
label.textblock(60, lines=4, justification="L", line_spacing=0.7)
label.write_text("S-3AX-UA\&sjzgreig\&HPSI0114i-b\&bezi_1 D3", char_height=4, char_width=4, orientation='R')
label.endorigin()

# 1D Barcode
label.origin(6.5,11)
label.write_barcode(5,'C',print_interpretation_line='N',orientation='R')
label.write_text('ptkr.uk/dm/bc/uss/1090')
label.endorigin()

label.origin(3,6)
label.textblock(80)
label.write_text("ptkr.uk/dm/bc/uss/1090", char_height=2.5, char_width=2.5, orientation='R')
label.endorigin()

print(label.dumpZPL())
label.preview()
```

The generated ZPL2 code is:

```
^XA^FO72,24^GB960,396,1,B,0^FS^FO72,24^GB240,270,1,B,0^FS^FO72,246^FB240,1,0,C,0^A0N,24,24^FD14/06/2019^FS^FO114,66^BQN,2,6,L,7^FDLA,ptkr.uk/dm/bc/uss/1090^FS^FO312,24^GB720,270,1,B,0^FS^FO336,48^FB720,4,8,L,0^A0N,48,48^FDS-3AX-UA\&sjzgreig\&HPSI0114i-b\&bezi_1 D3^FS^FO132,306^BY3^BCN,60,N,N,N^FDptkr.uk/dm/bc/uss/1090^FS^FO72,378^FB960,1,0,C,0^A0N,30,30^FDptkr.uk/dm/bc/uss/1090^FS^XZ
```

The preview image (generate by the Labelary API) can be found [here](http://api.labelary.com/v1/printers/12dpmm/labels/1.417323x3.503937/0/%5EXA%5EFO24%2C72%5EGB396%2C960%2C1%2CB%2C0%5EFS%5EFO150%2C72%5EGB270%2C240%2C1%2CB%2C0%5EFS%5EFO174%2C72%5EFB240%2C1%2C0%2CC%2C0%5EA0R%2C24%2C24%5EFD14%2F06%2F2019%5EFS%5EFO228%2C108%5EBQR%2C2%2C6%2CL%2C7%5EFDLA%2Cptkr.uk%2Fdm%2Fbc%2Fuss%2F1090%5EFS%5EFO150%2C312%5EGB270%2C720%2C1%2CB%2C0%5EFS%5EFO168%2C336%5EFB720%2C4%2C8%2CL%2C0%5EA0R%2C48%2C48%5EFDS-3AX-UA%5C%26sjzgreig%5C%26HPSI0114i-b%5C%26bezi_1%20D3%5EFS%5EFO78%2C132%5EBY3%5EBCR%2C60%2CN%2CN%2CN%5EFDptkr.uk%2Fdm%2Fbc%2Fuss%2F1090%5EFS%5EFO36%2C72%5EFB960%2C1%2C0%2CC%2C0%5EA0R%2C30%2C30%5EFDptkr.uk%2Fdm%2Fbc%2Fuss%2F1090%5EFS%5EXZ).

## Installation

```sh    
$ pip install --user zebrapl2
```

## Requirements

* PIL or Pillow
