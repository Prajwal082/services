from services.messaging.lga import LogicApp

obj = LogicApp()

_to = 'abc@gmail.com'
_cc = 'xyz@gmail.com'
_subject = 'Test email from Logic App!'
_body = None

obj.send_email(
    to=_to,
    cc=_cc,
    subject=_subject,
    body=_body
)