from random import choice

def generate_follow_up_question():
    questions = ["You can ask me another question. Or here are some things I can help you with ⬇️"]
    return choice(questions)

def getCriteriaForEmoji(emoji):
    criteria_dict = {
        '1': 'Poor',
        '2': 'Fair',
        '3': 'Good',
        '4': 'Very Good',
        '5': 'Excellent'
    }
    return criteria_dict.get(emoji, 'Unknown')