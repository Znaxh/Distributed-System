from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Task Manager!"})

if __name__ == '__main__':
    app.run(debug=True)

tasks = []
task_id = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id
    data = request.get_json()
    task = {
        'id': task_id,
        'title': data['title'],
        'description': data['description']
    }
    tasks.append(task)
    task_id += 1
    return jsonify(task), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)


@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = next((task for task in tasks if task['id'] == id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task)

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = next((task for task in tasks if task['id'] == id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    task['title'] = data.get('title', task['title'])
    task['description'] = data.get('description', task['description'])
    return jsonify(task)

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    global tasks
    task = next((task for task in tasks if task['id'] == id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    tasks = [task for task in tasks if task['id'] != id]
    return jsonify({"message": "Task deleted"}), 200
