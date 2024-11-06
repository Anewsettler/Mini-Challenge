from flask import Blueprint, jsonify
from app.controllers.classification_controller import get_initial_question, classify_user_response

main = Blueprint('main', __name__)

@main.route('/health', methods=['GET'])
def health_check():
    """
    Health check route to verify that the server is running.
    """
    return jsonify({"status": "Server is running"}), 200

@main.route('/initial-question', methods=['POST'])
def initial_question_route():
    """
    Route to scrape content from URL and generate the initial question.
    """
    return get_initial_question()

@main.route('/classify-user-response', methods=['POST'])
def classify_user_response_route():
    """
    Route to classify a user's interest or generate a follow-up question based on user input.
    """
    return classify_user_response()
