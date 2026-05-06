from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Initialize Komar Uni AI
print("=" * 60)
print("Welcome to KOMAR UNI AI - Your University Assistant")
print("=" * 60)
print("Type 'quit' to exit\n")

# Load model and tokenizer
print("Loading AI model... (this may take a moment)")
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

print("✓ Model loaded successfully!\n")

while True:
    # Get user input
    user_input = input("You: ").strip()
    
    if user_input.lower() == "quit":
        print("\nKomar Uni AI: Thank you for chatting! Goodbye! 👋")
        break
    
    if not user_input:
        continue
    
    # Generate response
    input_ids = tokenizer.encode(user_input, return_tensors='pt')
    output = model.generate(input_ids, max_length=100, num_beams=5, no_repeat_ngram_size=2, temperature=0.7, top_p=0.9)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    
    print(f"Komar Uni AI: {response}\n")