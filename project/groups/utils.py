# project/groups/utils.py
import qrcode
import io
import base64
import numpy as np
import os
from PIL import Image

from flask import current_app

def make_qr_code(text, color):

    qr = qrcode.QRCode(
        version=8,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
    )

    qr.add_data(text)
    qr.make(fit=True)

    # qrcode as background
    bg = qr.make_image(fill_color=color, back_color='white')
    bg_w, bg_h = bg.size

    # logo as foreground
    logo_path = os.path.join(current_app.root_path, 'static/images/wu-logo.png')
    logo = Image.open(logo_path, 'r')
    data = np.array(logo)

    # changing color of logo to desired color
    r1, g1, b1 = 255, 255, 255
    r2, g2, b2 = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) # convert hex to rgb
    
    # reading colors
    red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
    
    mask = (red < r1) & (green < g1) & (blue < b1) # mask for fill
    data[:,:,:3][mask] = [r2, g2, b2] # converting colors
    
    logo = Image.fromarray(data)
    logo_w, logo_h = logo.size

    # putting logo over qr code
    offset = ((bg_w - logo_w) // 2, (bg_h - logo_h) // 2)
    bg.paste(logo, offset, logo)
    bg.resize((100, 100))
    # returning qr code bytes written in ascii string so it can be parsed by browser
    bytes_io = io.BytesIO()
    bg.save(bytes_io, format='PNG')
    output = base64.b64encode(bytes_io.getvalue()).decode('ascii')

    return output

