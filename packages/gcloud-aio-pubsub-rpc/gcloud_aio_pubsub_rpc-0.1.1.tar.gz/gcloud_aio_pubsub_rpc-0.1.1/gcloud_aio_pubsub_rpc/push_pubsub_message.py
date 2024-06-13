from pydantic import BaseModel, Field
import datetime

class PushPubsubMessage(BaseModel):
    data: str  # base64 encoded string
    attributes: dict[str, str] | None
    message_id: str = Field(alias='message_id')
    publish_time: datetime.datetime = Field(alias='publish_time')

class PushSubscriptionPayload(BaseModel):
    message: PushPubsubMessage
    subscription: str

# Example of parsing incoming data:
# Assuming 'incoming_json' is a dict that contains the payload from a Pub/Sub push subscription.
# Example:
# incoming_json = {
#     "message": {
#         "data": "SGVsbG8sIFdvcmxkIQ==",  # "Hello, World!" base64 encoded
#         "attributes": {
#             "key1": "value1",
#             "key2": "value2"
#         },
#         "message_id": "1234567890",
#         "publish_time": "2021-05-26T12:34:56.789Z"
#     },
#     "subscription": "projects/my-project/subscriptions/my-subscription"
# }

# Using the Pydantic model to parse and validate the JSON:
# payload = PushSubscriptionPayload(**incoming_json)
# print(payload)
