from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory user data
users = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"}
}

# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# GET user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# POST new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "Missing name or email"}), 400
    new_id = max(users.keys()) + 1
    users[new_id] = {"name": data["name"], "email": data["email"]}
    return jsonify({"message": "User created", "id": new_id}), 201

# PUT update user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    user["name"] = data.get("name", user["name"])
    user["email"] = data.get("email", user["email"])
    return jsonify({"message": "User updated"})

# DELETE user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return jsonify({"message": "User deleted"})
    return jsonify({"error": "User not found"}), 404

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
