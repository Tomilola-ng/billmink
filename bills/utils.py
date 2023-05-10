import secrets

def custom_id():
    return secrets.token_urlsafe(8)

def deposited_amount(bill_amount):

    dep_amount = bill_amount - ( bill_amount * 0.05 + 100 )

    return dep_amount