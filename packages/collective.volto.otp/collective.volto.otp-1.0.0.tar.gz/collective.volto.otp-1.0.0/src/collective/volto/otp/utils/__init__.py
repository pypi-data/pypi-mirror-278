import base64

import pyotp
from plone.keyring.interfaces import IKeyManager
from zope.component import getUtility

EMAIL_OTP_LIFETIME = 5 * 60


def generate_email_token(uid="", email=""):
    """Generates the email verification token"""
    keymanager = getUtility(IKeyManager)

    totp = pyotp.TOTP(base64.b32encode((uid + email + keymanager.secret()).encode()))

    return totp.now()


def validate_email_token(uid="", email="", token=""):
    keymanager = getUtility(IKeyManager)

    totp = pyotp.TOTP(base64.b32encode((uid + email + keymanager.secret()).encode()))

    return totp.verify(token, valid_window=EMAIL_OTP_LIFETIME)
