import uuid
from flask import Flask, request, jsonify, render_template, session
from experta import *
from pymongo import MongoClient
from .decision_engine import DecisionEngine
from .nlp_utils import tokenize
from .utils import generate_follow_up_question

app = Flask(__name__)
app.secret_key = 'hahaha'
client = MongoClient('mongodb+srv://biancanicolemaxino:bn123@thesisproject.flhik1e.mongodb.net/Feedback')
db = client['Feedback']

CHATBOT_STATE = []
user_sessions = {}

class Inquiry(Fact):
    pass

class Greeting(Fact):
    pass

greetings = [
    "Hi there! How can I assist you today?",
    "Hello! How may I help you?",
    "Hi! How can I assist you?",
    "Hello. What can I do for you?",
    "How may I assist you?",
    "I'm Lilbot. How can I help you today?"
]

def check_or_create_session_state():
    user_id = session.get('user_id')
    if not user_id:
        user_id = generate_user_id()
        session['user_id'] = user_id

    def get_current_user_id(chatbot_state, user_id):
        for index, instance in enumerate(chatbot_state):
            if instance['user_id'] == user_id:
                return index
        return None

    instance = get_current_user_id(CHATBOT_STATE, user_id)
    if instance is None:
        engine = DecisionEngine()
        CHATBOT_STATE.append({'user_id': user_id, 'chatbot_state': engine})
    else:
        engine = CHATBOT_STATE[instance]['chatbot_state']
    return user_id, engine

def generate_user_id():
    return str(uuid.uuid4())

@app.route('/')
def index():
    user_id, _ = check_or_create_session_state()
    return render_template('library.html')

def process_inquiry(user_message, user_id):
    engine = DecisionEngine()
    tokenized_input = tokenize(user_message)
    engine.declare(Inquiry(sentence=tokenized_input))
    engine.run()
    response = engine.response
    predefined_text = engine.predefined_text
    follow_up_question = ""

    if engine.ask_follow_up:
        follow_up_question = generate_follow_up_question()

    if user_message.lower() in ["hi", "hello", "good morning", "good evening", "good day", "good eve"]:
        response = choice(greetings)
        follow_up_question = False

    if not response and not predefined_text:
        response = "I'm sorry, I don't understand that."
        follow_up_question = generate_follow_up_question()

    return {'user_id': user_id, 'response': response, 'predefined_text': predefined_text, 'follow_up_question': follow_up_question}

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    user_id = session.get('user_id')
    result = process_inquiry(user_message, user_id)
    return jsonify(result)

@app.route('/reset_chatbot', methods=['GET'])
def reset_chatbot():
    CHATBOT_STATE.clear()
    return jsonify({'status': 'success', 'message': 'Chatbot reset successfully.'})

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    try:
        data = request.json
        rating = data.get('emoji')
        emoji = data.get('rating')
        feedback_collection = db['feedback']
        feedback_collection.insert_one({'rating': rating, 'criteria': emoji})
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)})