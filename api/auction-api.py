from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
socketio = SocketIO(app, cors_allowed_origins="*")

captains = [
    {"id": 1, "name": "Deep Goyani", "points": 1200, "team": []},
    {"id": 2, "name": "Krutgya Kaneria", "points": 1200, "team": []},
    {"id": 3, "name": "Jagjeet Dangar", "points": 1200, "team": []},
    {"id": 4, "name": "Yashvi Dholkiya", "points": 1200, "team": []},
]

@app.route('/place-bid', methods=['POST'])
def place_bid():
    data = request.json
    bid = data['bid']
    captain_id = data['captainId']

    captain = next((c for c in captains if c['id'] == captain_id), None)
    if not captain:
        return jsonify({"message": "Invalid captain ID."}), 400

    if len(captain['team']) >= 13:
        return jsonify({"message": "You can only buy 13 players."}), 400

    if bid > captain['points']:
        return jsonify({"message": "Not enough points to place this bid."}), 400

    # Emit socket event for real-time updates
    socketio.emit('bidUpdate', {'captains': captains})
    return jsonify({"captains": captains})

@app.route('/pass-player', methods=['POST'])
def pass_player():
    # Emit socket event for real-time updates
    socketio.emit('passUpdate', {'message': 'Player passed'})
    return jsonify({"message": "Player passed successfully"})

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
