from typing import List, Dict, Optional
import requests


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