from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
from research_engine_simple import ResearchEngine, KNOWLEDGE_BASE, QUICK_FACTS
import json
from datetime import datetime

app = Flask(__name__)

print("Loading AI model...")
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")
print("✓ Model loaded!")

research = ResearchEngine()
chat_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400
    
    ai_response = ""
    sources = []
    
    # Check knowledge base first
    for key, value in KNOWLEDGE_BASE.items():
        if key in user_message.lower():
            ai_response = format_knowledge_response(key, value)
            sources = [{"title": f"Knowledge Base - {key.title()}", "source": "Internal DB"}]
            break
    
    # Check quick facts
    if not ai_response:
        for fact_key, fact_value in QUICK_FACTS.items():
            if fact_key in user_message.lower():
                ai_response = f"💡 {fact_key.title()}: {fact_value}"
                sources = [{"title": "Quick Facts", "source": "Verified"}]
                break
    
    # Try web search
    if not ai_response:
        try:
            search_result = research.search_web(user_message)
            if search_result.get("results"):
                ai_response = "Based on my research:\n\n"
                for i, result in enumerate(search_result["results"][:2], 1):
                    ai_response += f"{i}. {result['body']}\n"
                    if result.get('link'):
                        sources.append({
                            "title": result.get('title', 'Result'),
                            "link": result['link'],
                            "source": "Web"
                        })
        except:
            pass
    
    # Fallback to AI generation
    if not ai_response:
        try:
            input_ids = tokenizer.encode(user_message[:100], return_tensors='pt')
            output = model.generate(
                input_ids,
                max_length=80,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=tokenizer.eos_token_id
            )
            ai_response = tokenizer.decode(output[0], skip_special_tokens=True)
            sources = [{"title": "AI Generated", "source": "GPT-2"}]
        except:
            ai_response = "I'm not sure about that. Could you rephrase your question?"
    
    # Save to history
    chat_history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user_message,
        "ai": ai_response,
        "sources": sources
    })
    
    return jsonify({
        'response': ai_response,
        'sources': sources,
        'timestamp': datetime.now().strftime("%H:%M:%S"),
        'has_research': len(sources) > 0
    })

def format_knowledge_response(topic, data):
    """Format knowledge base response"""
    response = f"📚 **{topic.upper()}**\n\n"
    
    for key, value in data.items():
        if isinstance(value, list):
            response += f"**{key.replace('_', ' ').title()}:**\n"
            for item in value:
                response += f"  • {item}\n"
            response += "\n"
        else:
            response += f"**{key.replace('_', ' ').title()}:** {value}\n"
    
    return response

@app.route('/api/history', methods=['GET'])
def get_history():
    return jsonify(chat_history)

@app.route('/api/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query', '').strip()
    
    result = research.search_web(query)
    return jsonify(result)

@app.route('/api/clear', methods=['POST'])
def clear_history():
    global chat_history
    chat_history = []
    return jsonify({'status': 'cleared'})

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)