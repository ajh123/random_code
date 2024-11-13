from typing import List, Dict, Optional

class MessageBoard:
    def __init__(self, location: str, x: int, z: int, num_lanes: int = 3):
        self.location: str = location
        self.x: int = x  # X-coordinate in the world
        self.z: int = z  # Z-coordinate in the world
        self.speed_limit: int = -1
        # Initialize each lane as open by default, with string keys for lane numbers
        self.lane_statuses: Dict[str, bool] = {str(lane): True for lane in range(1, num_lanes + 1)}
        self.general_message: str = ""

    def set_speed_limit(self, speed: int) -> None:
        self.speed_limit = speed
        print(f"MessageBoard at {self.location} (X:{self.x}, Z:{self.z}): Set speed limit to {speed} mph")

    def set_lane_status(self, lane: str, status: bool) -> None:
        if lane in self.lane_statuses:
            self.lane_statuses[lane] = status
            status_msg = "open" if status else "closed"
            print(f"MessageBoard at {self.location} (X:{self.x}, Z:{self.z}): Lane {lane} is now {status_msg}")
        else:
            print(f"MessageBoard at {self.location} (X:{self.x}, Z:{self.z}): Invalid lane {lane}")

    def display_message(self, message: str) -> None:
        self.general_message = message
        print(f"MessageBoard at {self.location} (X:{self.x}, Z:{self.z}): Display message - '{message}'")

    def display_end(self) -> None:
        self.general_message = "End"
        self.speed_limit = -1
        # Re-open all lanes when "End" is displayed
        for lane in self.lane_statuses:
            self.lane_statuses[lane] = True
        print(f"MessageBoard at {self.location} (X:{self.x}, Z:{self.z}): Display message - 'End', all lanes open")

    def show_board(self) -> None:
        print(f"\nMessageBoard at {self.location} (X:{self.x}, Z:{self.z}):")
        print(f"  Speed Limit: {self.speed_limit} mph" if self.speed_limit else "  No speed limit set")
        print("  Lanes:")
        for lane, status in self.lane_statuses.items():
            print(f"    Lane {lane}: {'Open' if status else 'Closed'}")
        if self.general_message:
            print(f"  Message: {self.general_message}")


    def to_dict(self) -> dict:
        return {
            "location": self.location,
            "x": self.x,
            "z": self.z,
            "speed_limit": self.speed_limit,
            "lane_statuses": self.lane_statuses,
            "general_message": self.general_message
        }


class SmartMotorway:
    def __init__(self):
        self.message_boards: Dict[str, MessageBoard] = {}

    def add_message_board(self, location: str, x: int, z: int, num_lanes: int = 3) -> MessageBoard:
        if location in self.message_boards:
            raise ValueError(f"MessageBoard at location {location} already exists.")
        board = MessageBoard(location, x, z, num_lanes)
        self.message_boards[location] = board
        return board

    def get_board(self, location: str) -> Optional[MessageBoard]:
        return self.message_boards.get(location)

    def delete_board(self, location: str) -> bool:
        if location in self.message_boards:
            del self.message_boards[location]
            return True
        return False

    def update_board(self, location: str, speed: Optional[int] = None, lane_statuses: Optional[Dict[str, bool]] = None, message: Optional[str] = None):
        board = self.get_board(location)
        if not board:
            raise ValueError(f"MessageBoard at location {location} does not exist.")
        
        if speed is not None:
            board.set_speed_limit(speed)

        if lane_statuses:
            for lane, status in lane_statuses.items():
                board.set_lane_status(lane, status)

        if message:
            board.display_message(message)

    def reset_board(self, location: str):
        board = self.get_board(location)
        if not board:
            raise ValueError(f"MessageBoard at location {location} does not exist.")
        
        board.set_speed_limit(-1)

        for lane, _ in board.lane_statuses:
            board.set_lane_status(lane, True)
        
        board.display_message("")

    def get_all_boards(self) -> List[dict]:
        return [board.to_dict() for board in self.message_boards.values()]

    def show_all_boards(self) -> None:
        for board in self.message_boards.values():
            board.show_board()
