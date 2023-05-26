import random
from django.shortcuts import render
from requests import request

from transbank.error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction

from webpay_plus import bp

return_url = "https://webpay3gint.transbank.cl"
commerce_code = "597055555532"
api_key = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"

def webpay_plus_create():
    print("Webpay Plus Transaction.create")
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = str(random.randrange(1000000, 99999999))
    amount = random.randrange(10000, 1000000)
    return_url = request.url_root + 'webpay-plus/commit'

    create_request = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": return_url
    }

    response = (Transaction()).create(buy_order, session_id, amount, return_url)

    print(response)

    return render('webpay/plus/create.html', request=create_request, response=response)



def webpay_plus_commit():
    token = request.args.get("token_ws")
    print("commit for token_ws: {}".format(token))

    response = (Transaction()).commit(token=token)
    print("response: {}".format(response))

    return render('webpay/plus/commit.html', token=token, response=response)

def webpay_plus_commit_error():
    token = request.form.get("token_ws")
    print("commit error for token_ws: {}".format(token))

    #response = Transaction.commit(token=token)
    #print("response: {}".format(response))
    response = {
        "error": "Transacción con errores"
    }

    return render('webpay/plus/commit.html', token=token, response=response)    



def webpay_plus_refund():
    token = request.form.get("token_ws")
    amount = request.form.get("amount")
    print("refund for token_ws: {} by amount: {}".format(token, amount))

    try:
        response = (Transaction()).refund(token, amount)
        print("response: {}".format(response))

        return render("webpay/plus/refund.html", token=token, amount=amount, response=response)
    except TransbankError as e:
        print(e.message)



def webpay_plus_refund_form():
    return ("webpay/plus/refund-form.html")