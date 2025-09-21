
import os
import requests
import argparse
import json
from dotenv import load_dotenv

load_dotenv()

def check_grammar_and_spell(text):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Error: GROQ_API_KEY not found in .env file."

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "model": "grok-1.5-fast",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that checks grammar and spelling in LaTeX files."}, 
                {"role": "user", "content": f"Please check the grammar and spelling of the following LaTeX content and provide corrections. Only output the corrected text, without any other text or explanation. Do not modify the LaTeX commands.:\n\n{text}"}
            ]
        })
    )

    if response.status_code == 200:
        try:
            return response.json()["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            return f"Error parsing API response: {e}"
    else:
        return f"Error: API request failed with status code {response.status_code}\n{response.text}"

def main():
    parser = argparse.ArgumentParser(description="Spell and grammar check for LaTeX files.")
    parser.add_argument("file_path", type=str, help="The absolute path to the LaTeX file.")
    args = parser.parse_args()

    try:
        with open(args.file_path, "r") as f:
            latex_content = f.read()
            corrected_text = check_grammar_and_spell(latex_content)
            print(corrected_text)
    except FileNotFoundError:
        print(f"Error: File not found at {args.file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
