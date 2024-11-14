from api import *

client = SmartMotorwayClient("https://jdps73nn-5000.uks1.devtunnels.ms/message_boards")


# Update a message board

# response = client.update_message_board("M1_J2_A", speed_limit=60, lane_statuses={"3": False}, message="Exit closed")
# print(response)

# response = client.reset_message_board("M1_J2_A")
# print(response)

# response = client.update_message_board("M1_J2_A", speed_limit=-1, lane_statuses={"3": True}, message="")
# print(response)