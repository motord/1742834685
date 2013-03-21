# -*- coding: utf-8 -*-
__author__ = 'peter'

import qrcode

def alpha():
    return qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
        )

def beta():
    return qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=15,
        border=6,
        )

def gamma():
    return qrcode.QRCode(
        version=6,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=20,
        border=8,
        )

defaults={'alpha':alpha, 'beta':beta, 'gamma':gamma}

def default_image(spec, data):
    encoder=defaults[spec]()
    encoder.clear()
    encoder.add_data(data)
    encoder.make(fit=True)
    return encoder.make_image()
