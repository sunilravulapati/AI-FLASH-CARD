from flask import Flask, jsonify, request
from flask_cors import CORS

# Initialize the Flask application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for all routes
CORS(app)

# Predefined flashcard data for different programming topics
flashcard_data = {
    "Python": [
        "Python is a high-level programming language.",
        "Python supports multiple programming paradigms, including procedural, object-oriented, and functional programming.",
        "Python has a large standard library that supports many common programming tasks.",
        "Python is known for its readability and simplicity.",
        "Python is widely used in web development, data analysis, artificial intelligence, and scientific computing."
    ],
    "Java": [
        "Java is a high-level, class-based, object-oriented programming language.",
        "Java is designed to have as few implementation dependencies as possible.",
        "Java is used for building platform-independent applications.",
        "Java has a rich API and a large ecosystem of libraries.",
        "Java is widely used in enterprise applications and Android app development."
    ],
    "C++": [
        "C++ is a general-purpose programming language created as an extension of the C programming language.",
        "C++ supports both procedural and object-oriented programming.",
        "C++ is widely used for system/software development and game programming.",
        "C++ provides low-level memory manipulation capabilities.",
        "C++ is known for its performance and efficiency."
    ]
}

# List to store user-created flashcards
flashcards = []
next_id = 1  # Variable to keep track of the next flashcard ID

# Route to get all user-created flashcards
@app.route('/flashcards', methods=['GET'])
def get_flashcards():
    return jsonify(flashcards)

# Route to create a new flashcard
@app.route('/flashcards', methods=['POST'])
def create_flashcard():
    global next_id
    data = request.json  # Get the JSON data from the request
    flashcard = {
        'id': next_id,
        'question': data['question'],
        'answer': data['answer']
    }
    flashcards.append(flashcard)  # Add the new flashcard to the list
    next_id += 1  # Increment the ID for the next flashcard
    return jsonify(flashcard), 201  # Return the created flashcard with a 201 status

# Route to get a specific flashcard by ID
@app.route('/flashcards/<int:flashcard_id>', methods=['GET'])
def get_flashcard(flashcard_id):
    flashcard = next((fc for fc in flashcards if fc['id'] == flashcard_id), None)
    if flashcard is None:
        return jsonify({'error': 'Flashcard not found'}), 404  # Return error if not found
    return jsonify(flashcard)  # Return the found flashcard

# Route to update a specific flashcard by ID
@app.route('/flashcards/<int:flashcard_id>', methods=['PUT'])
def update_flashcard(flashcard_id):
    data = request.json  # Get the JSON data from the request
    flashcard = next((fc for fc in flashcards if fc['id'] == flashcard_id), None)
    if flashcard is None:
        return jsonify({'error': 'Flashcard not found'}), 404  # Return error if not found
    # Update the question and answer if provided
    flashcard['question'] = data.get('question', flashcard['question'])
    flashcard['answer'] = data.get('answer', flashcard['answer'])
    return jsonify(flashcard)  # Return the updated flashcard

# Route to delete a specific flashcard by ID
@app.route('/flashcards/<int:flashcard_id>', methods=['DELETE'])
def delete_flashcard(flashcard_id):
    global flashcards
    flashcards = [fc for fc in flashcards if fc['id'] != flashcard_id]  # Remove the flashcard
    return jsonify({'result': 'Flashcard deleted'})  # Return success message

# Route to generate flashcards based on a topic
@app.route('/generate_flashcard', methods=['POST'])
def generate_flashcard():
    data = request.json  # Get the JSON data from the request
    topic = data.get('topic')  # Extract the topic from the request

    # Check if the topic is provided
    if topic in flashcard_data:
        return jsonify({'flashcards': flashcard_data[topic]})  # Return predefined flashcards for the topic
    else:
        return jsonify({'error': 'Topic not found'}), 404  # Return error if topic is not found

if __name__ == '__main__':
    app.run(debug=True)