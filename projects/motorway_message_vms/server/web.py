from boards import *
from flask import Flask, request, jsonify


app = Flask(__name__)
motorway = SmartMotorway()

@app.route('/message_boards', methods=['GET'])
def get_message_boards():
    return jsonify(motorway.get_all_boards()), 200

@app.route('/message_boards/<location>', methods=['GET'])
def get_message_board(location: str):
    board = motorway.get_board(location)
    if board:
        return jsonify(board.to_dict()), 200
    return jsonify({"error": "Message board not found"}), 404

@app.route('/message_boards', methods=['POST'])
def create_message_board():
    data = request.get_json()
    location = data.get("location")
    x = data.get("x")
    z = data.get("z")
    num_lanes = data.get("num_lanes", 3)

    if not location or not x or not z:
        return jsonify({"error": "Location, x, and z coordinates are required."}), 400

    try:
        board = motorway.add_message_board(location, x, z, num_lanes)
        return jsonify(board.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/message_boards/reset/<location>', methods=['DELETE'])
def reset_message_board(location: str):
    try:
        motorway.reset_board(location)
        board = motorway.get_board(location)
        return jsonify(board.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@app.route('/message_boards/<location>', methods=['PUT'])
def update_message_board(location: str):
    print("B")
    data = request.get_json()
    speed = data.get("speed_limit")
    lane_statuses = data.get("lane_statuses")
    message = data.get("message")

    try:
        motorway.update_board(location, speed, lane_statuses, message)
        board = motorway.get_board(location)
        return jsonify(board.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@app.route('/message_boards/<location>', methods=['DELETE'])
def delete_message_board(location: str):
    if motorway.delete_board(location):
        return jsonify({"message": "Message board deleted"}), 200
    return jsonify({"error": "Message board not found"}), 404

@app.route('/message_boards/group', methods=['PUT'])
def update_message_boards_group():
    data = request.get_json()
    locations = data.get("locations", [])
    speed = data.get("speed_limit")
    lane_statuses = data.get("lane_statuses")
    message = data.get("message")

    if not locations:
        return jsonify({"error": "Locations are required."}), 400

    for location in locations:
        try:
            motorway.update_board(location, speed, lane_statuses, message)
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    # Optionally, you could return all updated boards here
    updated_boards = [motorway.get_board(location).to_dict() for location in locations if motorway.get_board(location)]
    return jsonify(updated_boards), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")