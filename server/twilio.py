from twilio.rest import Client

account_sid ="***REMOVED***"
auth_token ="***REMOVED***"
client = Client(account_sid, auth_token)

call = client.calls.create(
    to="number",
    from_="‭+447588706341‬",
    url="http://demo.twilio.com/docs/voice.xml"
)
