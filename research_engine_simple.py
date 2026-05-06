import requests
import json
from datetime import datetime

class ResearchEngine:
    """Simplified research engine"""
    
    def __init__(self):
        self.sources = []
    
    def search_web(self, query):
        """Search using free API"""
        try:
            # Using DuckDuckGo API (no key needed)
            url = f"https://api.duckduckgo.com/?q={query}&format=json"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            results = []
            if data.get("RelatedTopics"):
                for item in data["RelatedTopics"][:3]:
                    results.append({
                        "title": item.get("Text", ""),
                        "body": item.get("Text", "")[:200],
                        "link": item.get("FirstURL", "")
                    })
            
            return {"results": results}
        except Exception as e:
            return {"error": str(e)}
    
    def get_definition(self, topic):
        """Get quick definition"""
        definitions = {
            "python": "Python is a high-level, interpreted programming language known for simplicity and versatility.",
            "ai": "Artificial Intelligence is the simulation of human intelligence by machines.",
            "machine learning": "Machine Learning enables computers to learn from data without explicit programming.",
            "deep learning": "Deep Learning uses neural networks with multiple layers to process complex data.",
            "neural network": "A neural network is inspired by biological neurons and processes information through interconnected nodes.",
            "kust": "KUST (Komar University of Science and Technology) - Established 2009 with motto: Ethics, Knowledge, Skills",
            "flask": "Flask is a lightweight Python web framework for building web applications.",
            "javascript": "JavaScript is a programming language used for interactive web pages.",
            "api": "API (Application Programming Interface) allows different software to communicate.",
            "database": "A database is an organized collection of data stored and accessed electronically."
        }
        
        for key, value in definitions.items():
            if key in topic.lower():
                return value
        
        return None

# Knowledge base
KNOWLEDGE_BASE = {
    "python": {
        "description": "Python is a high-level, interpreted programming language",
        "uses": ["Web development", "Data science", "AI/ML", "Automation", "Scientific computing"],
        "advantages": ["Easy to learn", "Versatile", "Large community", "Extensive libraries"],
        "libraries": ["NumPy", "Pandas", "TensorFlow", "Scikit-learn", "Flask", "Django"],
        "resources": ["python.org", "Real Python", "Codecademy", "DataCamp"]
    },
    "ai": {
        "description": "Artificial Intelligence - making machines intelligent",
        "types": ["Machine Learning", "Deep Learning", "NLP", "Computer Vision", "Robotics"],
        "applications": ["Chatbots", "Recommendations", "Autonomous vehicles", "Healthcare diagnosis"],
        "frameworks": ["TensorFlow", "PyTorch", "Keras", "Scikit-learn"],
        "resources": ["Fast.ai", "Andrew Ng Courses", "Coursera", "arXiv Papers"]
    },
    "machine learning": {
        "description": "ML enables systems to learn from data and improve",
        "types": ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning"],
        "algorithms": ["Linear Regression", "Decision Trees", "Random Forest", "SVM", "Neural Networks"],
        "applications": ["Predictions", "Classification", "Clustering", "Recommendations"],
        "resources": ["Scikit-learn docs", "Google ML Crash Course", "Kaggle"]
    },
    "javascript": {
        "description": "JavaScript - The language of the web",
        "uses": ["Web development", "Frontend interactions", "Backend (Node.js)", "Mobile apps", "Games"],
        "frameworks": ["React", "Vue.js", "Angular", "Node.js", "Express.js"],
        "advantages": ["Runs in browsers", "Versatile", "Large ecosystem", "Easy to learn"],
        "resources": ["MDN Web Docs", "JavaScript.info", "Codecademy"]
    },
    "web development": {
        "description": "Creating websites and web applications",
        "frontend": ["HTML", "CSS", "JavaScript", "React", "Vue.js"],
        "backend": ["Python/Flask", "Node.js/Express", "Java", "C#/.NET", "PHP"],
        "databases": ["MySQL", "PostgreSQL", "MongoDB", "Firebase"],
        "tools": ["Git", "Docker", "VS Code", "Chrome DevTools"]
    },
    "kust": {
        "full_name": "Komar University of Science and Technology",
        "founded": 2009,
        "location": "Sulaymaniyah, Iraq",
        "motto": "Ethics - Knowledge - Skills",
        "departments": ["Computer Science", "Engineering", "Science", "Business", "Education"],
        "website": "https://www.kust.edu.iq",
        "mission": "Providing quality education in science and technology"
    }
}

# Quick facts
QUICK_FACTS = {
    "python version": "Latest: Python 3.12",
    "flask latest": "Flask 3.0+",
    "tensorflow latest": "TensorFlow 2.13+",
    "pytorch latest": "PyTorch 2.0+",
    "ai trends 2024": "Generative AI, Large Language Models, Multimodal AI",
    "gpt-2 params": "1.5 billion parameters",
    "kust established": "2009",
    "kust students": "Thousands of students in various programs"
}