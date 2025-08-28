import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Fetch API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "❌ OPENAI_API_KEY is missing. Please set it in your .env file "
        "or export it as an environment variable."
    )

# Initialize OpenAI client
client = OpenAI(api_key=api_key)


def ask_agent(question: str) -> str:
    """
    Ask the AI agent a question about fuel estimation, routes, or aircraft performance.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Small, cost-effective model
            messages=[
                {"role": "system", "content": "You are an assistant that helps with aircraft fuel optimization."},
                {"role": "user", "content": question}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Agent error: {e}"
