import os
from app.services.classification_helpers import get_classification_id_by_name
from openai import OpenAI
from app import db
from app.models.user import User

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def generate_question(content):
    prompt = f"""
    The following content is extracted from a webpage. Based on this content, generate a high-level question aimed at identifying the user's general area of interest, rather than specific or detailed information. Focus on broad categories or themes rather than detailed items or job titles, ensuring that the question encourages further exploration.

    Content:
    "{content}"

    Examples:
    1. If the content is from a job listing page mentioning various job titles (e.g., "Software Engineer", "Product Manager", "Sales Associate"):
       - Question: "What type of role are you interested in exploring on this page?"
       - Options: ["A. Technology Roles", "B. Sales Roles", "C. Management Roles", "D. Creative Roles"]

    2. If the content is from a page covering career planning topics such as "interview preparation," "resume tips," and "networking advice":
       - Question: "What area of career planning are you interested in?"
       - Options: ["A. Job Search Advice", "B. Professional Development", "C. Networking", "D. Interview Preparation"]

    Generate a question and options similar to the examples above, aiming to identify the user's high-level interests in broad themes or areas without focusing on specific titles or items.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()


def classify_user_initial(initial_question, user_selection, classifications, content, user_id=None, user_name=None):
    question_text = initial_question.get("question", "")
    classification_result = identify_classification(question_text, user_selection, classifications)

    if classification_result != "need_follow_up":
        save_classification_to_user(user_id, user_name, classification_result)
        return {"classification": classification_result}

    follow_up_question = generate_follow_up_question(content, question_text, user_selection)
    return {"follow_up_question": follow_up_question}

def classify_user_follow_up(follow_up_question, user_selection, classifications, content, user_id=None, user_name=None, attempt_count=1, max_attempts=3):
    classification_result = identify_classification(follow_up_question, user_selection, classifications)

    if classification_result != "need_follow_up":
        save_classification_to_user(user_id, user_name, classification_result)
        return {"classification": classification_result}

    if attempt_count >= max_attempts:
        return {"error": "Unable to classify after multiple attempts"}

    next_follow_up_question = generate_follow_up_question(content, follow_up_question, user_selection)
    return {"follow_up_question": next_follow_up_question, "attempt_count": attempt_count + 1}

def identify_classification(question, user_selection, classifications):
    prompt = f"""
    Based on the following question and user-selected answer, classify the user's interest into the most specific subcategory available within the provided classification hierarchy. 

    Only return the most detailed subcategory level as a single string, and do not stop at broader levels. For example, if "Technology > Software Development > Frontend Development" is available, return "Frontend Development" rather than just "Technology" or "Software Development."

    If additional information is needed to make a precise classification, respond with "need_follow_up" instead of attempting to generalize.

    Question:
    "{question}"

    User selected: "{user_selection}"

    Classification hierarchy:
    {classifications}

    Respond with only the final classification as a single string. If more information is needed, respond with "need_follow_up".
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50
    )
    output = response.choices[0].message.content.strip()
    return "need_follow_up" if "need_follow_up" in output else output


def generate_follow_up_question(content, previous_question, user_selection):
    prompt = f"""
    Based on the content, previous question, and user-selected answer, generate a follow-up question with multiple-choice options to clarify the user's specific area of interest.

    Content:
    "{content}"

    Previous question:
    "{previous_question}"

    User selected: "{user_selection}"

    Examples:
    1. Content about Amazon services with previous question "Which area of Amazon's operations are you interested in?" and selection "A. Financial Services":
       - Question: "Which type of financial service are you interested in?"
       - Options: ["A. Payment Processing", "B. Lending", "C. Financial Analytics", "D. Insurance"]

    2. Content about healthcare with previous question "Which area of healthcare do you want to learn about?" and selection "B. Pharmaceuticals":
       - Question: "Which aspect of pharmaceuticals are you interested in?"
       - Options: ["A. Drug Research", "B. Drug Manufacturing", "C. Sales & Marketing", "D. Regulatory Affairs"]

    Generate a similar follow-up question and options.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

def save_classification_to_user(user_id, user_name, classification_name):
    """
    Saves the classification to the user, converting classification_name to its ID.

    Parameters:
        user_id (int): The ID of the user.
        user_name (str): The name of the user.
        classification_name (str): The name of the classification to store.
    """
    classification_id = get_classification_id_by_name(classification_name)
    if classification_id is None:
        print(f"Error: Classification '{classification_name}' not found. User classification not saved.")
        return
    
    user = User.query.filter_by(user_id=user_id).first()
    if user:
        user.classification_id = classification_id
    else:
        user = User(user_id=user_id, user_name=user_name, classification_id=classification_id)
        db.session.add(user)
    
    db.session.commit()
