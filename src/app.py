# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from QALD_main_7112029008 import process_question  # Import your process_question function

app = Flask(__name__)
CORS(app)  # Enable CORS

@app.route('/api/question', methods=['POST'])
def handle_question():
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    answer = process_question(question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)



# python C:/Users/user/my-app/public/QALD_7112029008/app.py
#python C:/Users/user/my-app/src/app.py 
# http://localhost:3000/
# http://192.168.56.1:3000