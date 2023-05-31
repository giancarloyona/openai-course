import openai
import argparse
from colorama import init, Fore, Style
from openai import ChatCompletion
from dotenv import dotenv_values

config = dotenv_values('../../.env')
openai.api_key = config['OPENAI_API_KEY']


def ask_gpt(messages):
    chat = ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    return chat


def print_answer(response):
    print(Style.NORMAL + Fore.RED + "Assistant: " +
          response["choices"][0]["message"]["content"])


def main():

    init(autoreset=True)

    args = parser.parse_args()
    personality = args.personality

    messages = [{"role": "system", "content": ""}]
    initial_prompt = f"You are a conversational chatbot. Your personality is {personality}"
    messages.append({"role": "user", "content": initial_prompt})

    while True:
        try:
            user_input = input(Style.NORMAL + Fore.BLUE + "You: ")
            messages.append({"role": "user", "content": user_input})

            res = ask_gpt(messages)
            gpt_msg = res["choices"][0]["message"]
            messages.append(gpt_msg)

            print_answer(res)

        except KeyboardInterrupt:
            print("Exiting...")
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simple command line chatbot with ChatGPT")
    parser.add_argument("--personality", type=str,
                        help="Sets a personality for the chatbot", default='friendly and helpful')

    main()
