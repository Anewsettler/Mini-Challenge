from flask import jsonify, request
from app.services.scrapeService import scrape_content
from app.services.classificationService import (
    generate_question,
    classify_user_initial,
    classify_user_follow_up,
)
from app.services.classification_helpers import fetch_classification_hierarchy, organize_question_data

HARD_CODED_USER = {"user_id": 1, "user_name": "DemoUser"}
MAX_ATTEMPTS = 5

def get_initial_question():
    """
    Scrapes content from the provided URL and generates an initial question.
    """
    data = request.json
    url = data.get('url')
    content = scrape_content(url)

    if not content:
        return jsonify({"error": "Failed to retrieve content from the URL"}), 500

    question_data_raw = generate_question(content)
    question_data = organize_question_data(question_data_raw)

    return jsonify({
        "initial_question": question_data,
        "content_preview": content[:500],
        "user_id": HARD_CODED_USER["user_id"],
        "user_name": HARD_CODED_USER["user_name"]
    })

def classify_user_response():
    """
    Classifies user response or generates a follow-up question based on the selection.
    Stops after MAX_ATTEMPTS with a message if classification is unresolved.
    """
    data = request.json
    user_selection = data.get('user_selection')
    initial_question = data.get('initial_question')
    attempt_count = data.get('attempt_count', 1)
    classifications = fetch_classification_hierarchy()

    if attempt_count >= MAX_ATTEMPTS:
        return jsonify({"message": "Unable to identify the specific classification after multiple attempts."}), 400

    if attempt_count == 1:
        classification_result = classify_user_initial(
            initial_question=initial_question,
            user_selection=user_selection,
            classifications=classifications,
            content=None,
            user_id=HARD_CODED_USER["user_id"],
            user_name=HARD_CODED_USER["user_name"]
        )
    else:
        follow_up_question = data.get('follow_up_question')
        content = data.get('content')
        classification_result = classify_user_follow_up(
            follow_up_question=follow_up_question,
            user_selection=user_selection,
            classifications=classifications,
            content=content,
            user_id=HARD_CODED_USER["user_id"],
            user_name=HARD_CODED_USER["user_name"],
            attempt_count=attempt_count
        )

    if "classification" in classification_result:
        return jsonify({"classification": classification_result["classification"]})
    elif "follow_up_question" in classification_result:
        follow_up_data = organize_question_data(classification_result["follow_up_question"])
        return jsonify({
            "initial_question": follow_up_data,
            "attempt_count": attempt_count + 1 
        })
    else:
        return jsonify({"error": "Unable to classify after multiple attempts"}), 400
