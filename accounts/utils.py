import pyotp
from datetime import timedelta, datetime

def send_otp(req):
    totp = pyotp.TOTP(pyotp.random_base32(), interval = 300)
    otp = totp.now()
    req.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=5)
    req.session['otp_valid_date'] = str(valid_date)

    def prints(e):
        i = 0
        while i < 5:
            print(f'Your one time password is : {e}')
            i = 1 + i

    prints(otp)
    