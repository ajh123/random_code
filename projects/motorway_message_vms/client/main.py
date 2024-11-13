from api import *

client = SmartMotorwayClient("http://localhost:5000/message_boards")


# Update a message board

# response = client.update_message_board("M1_J2_A", speed_limit=60, lane_statuses={"3": False}, message="Exit closed")
# print(response)

response = client.reset_message_board("M1_J2_A")
print(response)

