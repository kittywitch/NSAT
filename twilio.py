from twilio.rest import Client

account_sid ="new needed"
auth_token ="new needed"
client = Client(account_sid, auth_token)

call = client.calls.create(
    to="number",
    from_="‭number‬",
    url="http://demo.twilio.com/docs/voice.xml"
)
