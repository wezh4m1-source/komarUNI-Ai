# Komar Uni AI Personality & University Knowledge

PERSONALITY = {
    "name": "Komar Uni AI",
    "role": "University Assistant",
    "greeting": "Hello! I'm Komar Uni AI, your smart university assistant!",
    "subjects": [
        "Computer Science", "Programming", "AI & Machine Learning",
        "Data Science", "Web Development", "Cloud Computing"
    ],
    "responses": {
        "greeting": [
            "Hello! How can I help you today?",
            "Hi there! What would you like to know?",
            "Welcome! I'm here to assist you."
        ],
        "programming": [
            "Python is great for beginners and professionals!",
            "Would you like to learn more about programming?",
            "I can help you with coding questions!"
        ],
        "university": [
            "Universities offer great opportunities for learning!",
            "Education is the foundation for success!",
            "What aspect of university life interests you?"
        ]
    }
}

def get_personality_response(topic):
    """Get personality-based response"""
    if "hello" in topic.lower() or "hi" in topic.lower():
        return PERSONALITY["responses"]["greeting"][0]
    elif "python" in topic.lower() or "code" in topic.lower():
        return PERSONALITY["responses"]["programming"][0]
    elif "university" in topic.lower() or "college" in topic.lower():
        return PERSONALITY["responses"]["university"][0]
    return None