from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import json
from datetime import datetime
from komar_personality import PERSONALITY, get_personality_response

# Initialize Komar Uni AI
print("=" * 70)
print(f"  Welcome to {PERSONALITY['name']}")
print(f"  Role: {PERSONALITY['role']}")
print("=" * 70)
print(f"  {PERSONALITY['greeting']}")
print("  Type 'help' for commands | 'quit' to exit\n")

# Load model and tokenizer
print("📚 Loading AI model... (this may take a moment)")
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
print("✓ Model loaded successfully!\n")

# Chat history
chat_file = "komar_chat_history.json"
chat_history = []

def save_chat(user_msg, ai_msg):
    """Save chat to file"""
    chat_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user_msg,
        "ai": ai_msg
    }
    chat_history.append(chat_entry)
    with open(chat_file, 'w') as f:
        json.dump(chat_history, f, indent=2)

def show_help():
    """Show available commands"""
    print("\n" + "="*70)
    print("📖 AVAILABLE COMMANDS:")
    print("  'help'    - Show this help menu")
    print("  'history' - Show chat history")
    print("  'clear'   - Clear chat history")
    print("  'about'   - About Komar Uni AI")
    print("  'quit'    - Exit the chatbot")
    print("="*70 + "\n")

def show_history():
    """Display chat history"""
    if not chat_history:
        print("\n📭 No chat history yet!\n")
        return
    
    print("\n" + "="*70)
    print("📋 CHAT HISTORY:")
    print("="*70)
    for i, entry in enumerate(chat_history, 1):
        print(f"\n[{i}] {entry['timestamp']}")
        print(f"   You: {entry['user'][:50]}...")
        print(f"   AI:  {entry['ai'][:50]}...")
    print("="*70 + "\n")

def show_about():
    """Show about information"""
    print("\n" + "="*70)
    print(f"🤖 ABOUT {PERSONALITY['name']}")
    print("="*70)
    print(f"Name: {PERSONALITY['name']}")
    print(f"Role: {PERSONALITY['role']}")
    print(f"Model: GPT-2 (OpenAI)")
    print(f"Subjects: {', '.join(PERSONALITY['subjects'])}")
    print("="*70 + "\n")

# Main chat loop
while True:
    try:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
        
        # Handle commands
        if user_input.lower() == "quit":
            print(f"\n🎓 Komar Uni AI: Thank you for learning with me! Goodbye! 👋")
            print(f"💾 Chat saved to: {chat_file}\n")
            break
        
        elif user_input.lower() == "help":
            show_help()
            continue
        
        elif user_input.lower() == "history":
            show_history()
            continue
        
        elif user_input.lower() == "clear":
            chat_history = []
            with open(chat_file, 'w') as f:
                json.dump([], f)
            print("\n✓ Chat history cleared!\n")
            continue
        
        elif user_input.lower() == "about":
            show_about()
            continue
        
        # Check for personality-based response
        personality_response = get_personality_response(user_input)
        if personality_response:
            print(f"🤖 Komar Uni AI: {personality_response}\n")
            save_chat(user_input, personality_response)
            continue
        
        # Generate AI response
        print("🔄 Generating response...")
        input_ids = tokenizer.encode(user_input, return_tensors='pt')
        output = model.generate(
            input_ids, 
            max_length=100, 
            num_beams=5, 
            no_repeat_ngram_size=2, 
            temperature=0.7, 
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id
        )
        response = tokenizer.decode(output[0], skip_special_tokens=True)
        
        print(f"🤖 Komar Uni AI: {response}\n")
        
        # Save to history
        save_chat(user_input, response)
    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Your chat has been saved.\n")
        break
    except Exception as e:
        print(f"❌ Error: {e}\n")