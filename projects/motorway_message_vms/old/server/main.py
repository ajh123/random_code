from boards import *

# Set up motorway and add independent message boards
motorway = SmartMotorway()
motorway.add_message_board("M1 J10", x=100, z=200)
motorway.add_message_board("M1 J15", x=150, z=200)
motorway.add_message_board("M1 J20", x=160, z=200)
motorway.add_message_board("M1 J25", x=170, z=200)
motorway.add_message_board("M1 J30", x=180, z=200)

# Apply individual settings to a single board
motorway.get_board("M1 J10").set_speed_limit(50)
motorway.get_board("M1 J10").display_message("Slow down")

# # Create a temporary group to apply a speed limit and lane closure across multiple boards
# motorway.apply_to_group(
#     ["M1 J15", "M1 J20", "M1 J25"],
#     speed=40,
#     lane_statuses={1: True, 2: False},  # Lane 1 open, lane 2 closed
#     message="Roadworks ahead"
# )

# Show all boards to see the final state
motorway.show_all_boards()
