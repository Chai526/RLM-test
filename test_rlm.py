import os
from dotenv import load_dotenv
from rlm import RLM

load_dotenv()

STORAGE_FILE = "./knowledge_base.txt"

def load_context():
    if not os.path.exists(STORAGE_FILE):
        return ""
    with open(STORAGE_FILE, "r", encoding="utf-8") as f:
        return f.read()

def main():
    # 1. Setup RLM
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("AZURE_API_KEY")
    if not api_key:
        print("❌ Error: API Key missing!")
        return

    rlm = RLM(
        model="gpt-4.1-mini", # Optimized for cost/speed
        max_iterations=15,
        api_key=api_key
    )

    # 2. Load the text extracted from PDFs
    context = load_context()
    if not context or len(context.strip()) < 10:
        print("⚠️ Knowledge base is empty. Please run ingest_pdfs.py first.")
        return

    print("--- RLM PDF Chatbot (Type 'exit' to quit) ---")
    print(f"Current knowledge base size: {len(context):,} characters.")

    # 3. Chat Loop
    while True:
        query = input("\nUser: ").strip()
        
        if query.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye!")
            break
        
        if not query:
            continue

        print("\nThinking (RLM Processing)...")
        try:
            # Use RLM to process the massive text block
            result = rlm.complete(query, context)
            
            print(f"\nBot: {result}")
            print(f"\n[Stats: {rlm.stats['iterations']} iterations | {rlm.stats['llm_calls']} LLM calls]")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()