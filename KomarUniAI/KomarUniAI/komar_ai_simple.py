from transformers import AutoModelForCausalLM, AutoTokenizer
import json
from datetime import datetime

print("=" * 70)
print("  Welcome to KOMAR UNI AI")
print("  Your Smart University Assistant")
print("=" * 70)
print("  Type 'help' for commands | 'quit' to exit\n")

print("📚 Loading AI model...")
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")
print("✓ Model loaded!\n")

chat_file = "chat_history.json"
chat_history = []

def save_chat(user_msg, ai_msg):
    chat_history.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user_msg,
        "ai": ai_msg
    })
    with open(chat_file, 'w') as f:
        json.dump(chat_history, f, indent=2)

while True:
    user_input = input("You: ").strip()
    
    if user_input.lower() == "quit":
        print("\n👋 Goodbye! Chat saved.\n")
        break
    elif user_input.lower() == "help":
        print("\nCommands: help | quit | history\n")
        continue
    elif user_input.lower() == "history":
        print(f"\n📋 Chat history ({len(chat_history)} messages):\n")
        for i, msg in enumerate(chat_history, 1):
            print(f"[{i}] You: {msg['user'][:40]}...")
        print()
        continue
    
    if not user_input:
        continue
    
    input_ids = tokenizer.encode(user_input, return_tensors='pt')
    output = model.generate(input_ids, max_length=80, temperature=0.7, top_p=0.9)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    
    print(f"🤖 Komar Uni AI: {response}\n")
    save_chat(user_input, response)