#!/usr/bin/env python3
import pyotp

key = 'WFQDADAJLJUP3C2CIUG4UGZDEBCQF7FF'
totp = pyotp.TOTP(key)
print(totp.now())
