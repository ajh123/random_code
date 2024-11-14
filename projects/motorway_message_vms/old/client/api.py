from typing import Any, List, Dict, Optional
import requests

class MessageBoard:
    def __init__(self, client: 'SmartMotorwayClient', location: str):
        super().__setattr__('client', client)
        super().__setattr__('location', location)
        super().__setattr__('_data', self.client.get_message_board(location))
        
        # Initialize attributes with data from API
        self.x = self._data.get('x', 0)
        self.z = self._data.get('z', 0)
        self.speed_limit = self._data.get('speed_limit', -1)
        self.lane_statuses = self._data.get('lane_statuses', {str(lane): True for lane in range(1, 4)})
        self.general_message = self._data.get('general_message', "")

    def __getattribute__(self, name: str):
        # Fetch fresh data for primary attributes
        if name in {'x', 'z', 'speed_limit', 'lane_statuses', 'general_message'}:
            self.refresh()
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value):
        # Update data on the server for primary attributes
        if name in {'speed_limit', 'lane_statuses', 'general_message'}:
            # Prepare data for update
            update_data = {
                'speed_limit': self.speed_limit if name != 'speed_limit' else value,
                'lane_statuses': self.lane_statuses if name != 'lane_statuses' else value,
                'message': self.general_message if name != 'general_message' else value
            }
            self.client.update_message_board(self.location, **update_data)
        
        # Set attribute locally
        super().__setattr__(name, value)

    def set_lane_status(self, lane: str, status: bool) -> None:
        if lane in self.lane_statuses:
            self.lane_statuses[lane] = status  # This will trigger __setattr__ to update via API
            status_msg = "open" if status else "closed"
            print(f"Lane {lane} is now {status_msg} at {self.location}")
        else:
            print(f"Invalid lane {lane} at {self.location}")

    def display_message(self, message: str) -> None:
        self.general_message = message  # This will trigger __setattr__ to update via API
        print(f"Display message: '{message}' at {self.location}")

    def display_end(self) -> None:
        self.speed_limit = -1
        self.general_message = "End"
        self.lane_statuses = {str(lane): True for lane in self.lane_statuses}  # Opens all lanes
        print(f"Display message 'End', all lanes open at {self.location}")

    def refresh(self) -> None:
        """Refresh the message board's data from the API."""
        super().__setattr__('_data', self.client.get_message_board(self.location))
        for key, value in self._data.items():
            super().__setattr__(key, value)

    def to_dict(self) -> dict:
        return {
            "location": self.location,
            "x": self.x,
            "z": self.z,
            "speed_limit": self.speed_limit,
            "lane_statuses": self.lane_statuses,
            "general_message": self.general_message
        }

class SmartMotorwayClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_all_message_boards(self):
        response = requests.get(self.base_url)
        return response.json()

    def get_message_board(self, location: str):
        response = requests.get(f"{self.base_url}/{location}")
        return response.json()

    def create_message_board(self, location: str, x: int, z: int, num_lanes: int = 3):
        data = {
            "location": location,
            "x": x,
            "z": z,
            "num_lanes": num_lanes
        }
        response = requests.post(self.base_url, json=data)
        return response.json()

    def update_message_board(self, location: str, speed_limit: Optional[int] = None, lane_statuses: Optional[Dict[str, bool]] = None, message: Optional[str] = None):
        data = {
            "speed_limit": speed_limit,
            "lane_statuses": lane_statuses,
            "message": message
        }
        response = requests.put(f"{self.base_url}/{location}", json=data)
        return response.json()

    def delete_message_board(self, location: str):
        response = requests.delete(f"{self.base_url}/{location}")
        return response.json()

    def update_message_boards_group(self, locations: List[str], speed_limit: Optional[int] = None, lane_statuses: Optional[Dict[str, bool]] = None, message: Optional[str] = None):
        data = {
            "locations": locations,
            "speed_limit": speed_limit,
            "lane_statuses": lane_statuses,
            "message": message
        }
        response = requests.put(f"{self.base_url}/group", json=data)
        return response.json()

    def reset_message_board(self, location: str):
        response = requests.delete(f"{self.base_url}/reset/{location}")
        return response.json()

    def update_message_board_attribute(self, location: str, attribute: str, data):
        response = requests.post(f"{self.base_url}/attribute/{location}/{attribute}", json=data)
        return response.json()

    def get_message_board_attribute(self, location: str, attribute: str):
        response = requests.get(f"{self.base_url}/attribute/{location}/{attribute}")
        return response.json()