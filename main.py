import sys
from database import init_db
from agent import run_agent

def main():
    print("Initializing Database...")
    init_db()
    print("Database Initialized (todos.db).")
    print("\n" + "="*60)
    print("Welcome to your Natural Language Todo Assistant!")
    print("Powered by Groq LLM (llama3) and LangChain.")
    print("Type 'exit' or 'quit' to quit.")
    print("="*60 + "\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
                
            print("\nAssistant: Processing request...")
            response = run_agent(user_input)
            print(f"Assistant: {response}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAssistant: An error occurred: {str(e)}\n")

if __name__ == "__main__":
    main()
