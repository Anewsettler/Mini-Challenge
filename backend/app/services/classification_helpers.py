from app.models.classification import Classification
from app import db
import re

def fetch_classification_hierarchy():
    """
    Fetches all classifications from the database and formats them hierarchically,
    supporting up to three levels.
    Returns a formatted string for GPT to understand.
    """
    classifications = db.session.query(Classification).all()
    classification_dict = {}

    for classification in classifications:
        if classification.parent_id is None:
            classification_dict[classification.id] = {
                'name': classification.classification,
                'subcategories': {}
            }
        else:
            parent = classification_dict.get(classification.parent_id)
            if parent:
                parent['subcategories'][classification.id] = {
                    'name': classification.classification,
                    'subcategories': []
                }
            else:
                for main_category in classification_dict.values():
                    sub_parent = main_category['subcategories'].get(classification.parent_id)
                    if sub_parent:
                        sub_parent['subcategories'].append(classification.classification)
                        break

    formatted_output = []
    for main_category in classification_dict.values():
        formatted_output.append(f"- {main_category['name']}")
        for sub_id, subcategory in main_category['subcategories'].items():
            formatted_output.append(f"  - {subcategory['name']}")
            if subcategory['subcategories']:
                sub_subcategories = ", ".join(subcategory['subcategories'])
                formatted_output.append(f"    - {sub_subcategories}")

    return "\n".join(formatted_output)


def get_classification_id_by_name(classification_name):
    """
    Finds the classification ID based on the provided classification name.
    
    Parameters:
        classification_name (str): The name of the classification to search for.
    
    Returns:
        int or None: The ID of the classification if found, or None if not found.
    """
    classification = db.session.query(Classification).filter_by(classification=classification_name).first()
    if classification:
        return classification.id
    else:
        print(f"Classification '{classification_name}' not found in the database.")
        return None


def organize_question_data(question_data_raw):
    """
    Parses and organizes question text and options from a raw question data string
    into a standardized dictionary format.
    
    Args:
        question_data_raw (str): Raw question data containing question and options.
    
    Returns:
        dict: Organized question data with 'question' and 'options' keys.
    """
    if "Options:" in question_data_raw:
        question_text = question_data_raw.split("Options:")[0].replace("Question: ", "").strip().strip('"')
        options_raw = question_data_raw.split("Options:")[1].strip()

        if '\n' in options_raw:
            options = [line.strip().strip('"') for line in options_raw.splitlines() if line.strip()]
        elif '[' in options_raw and ']' in options_raw:
            options = re.findall(r'"(.*?)"', options_raw)
        else:
            options = re.findall(r'[A-D]\.\s(.*?)(?=\s[A-D]\.|$)', options_raw)

        options = [option.strip() for option in options]
        return {"question": question_text, "options": options}

    return {"question": question_data_raw, "options": []}
