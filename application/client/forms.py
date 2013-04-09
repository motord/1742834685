# -*- coding: utf-8 -*-
__author__ = 'peter'

from flaskext import wtf
from flaskext.wtf import validators


class CampaignForm(wtf.Form):
    name = wtf.TextField('Name', validators=[validators.Required()])
    description = wtf.TextAreaField('Description')
    redirect = wtf.TextField('Redirect')

class QRCodeForm(wtf.Form):
    redirect = wtf.TextField('Redirect')
