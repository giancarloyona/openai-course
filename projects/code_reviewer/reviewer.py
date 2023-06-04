import argparse
import openai
import os
from dotenv import load_dotenv


def code_review(file_path,  model="gpt-3.5-turbo"):
    with open(file_path, "r") as file:
        content = file.read()

    generated_code_review = make_code_review_request(content, model)
    print(generated_code_review)


def make_code_review_request(file_content, model):

    PROMPT = """
        You will receive a file's content as text.
        Generate a code review for the file and indicate what changes should be 
        made to improve its style, performance, readability, and maintanability. 
        
        If there are any reputable libraries that could be introduced to improve 
        the code, suggest them. Be kind and constructive.

        For each suggested change, include line numbers to which you are 
        referring.
    """

    messages = [
        {"role": "system", "content": PROMPT},
        {"role": "system", "content": f"Code review the following file: {file_content}"}
    ]

    res = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )

    return res["choices"][0]["message"]["content"]


def main():
    parser = argparse.ArgumentParser(
        description="Simple code reviewer for a file",
    )
    parser.add_argument("file", type=str)
    parser.add_argument("--model", default="gpt-3.5-turbo")
    args = parser.parse_args()
    
    code_review(args.file, args.model)

if __name__ == "__main__":

    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    main()
