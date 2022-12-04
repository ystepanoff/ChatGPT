import argparse
from chatgpt import ChatGPT

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--email',
        type=str,
        required=True,
        help='OpenAI e-mail',
    )
    parser.add_argument(
        '--password',
        type=str,
        required=True,
        help='OpenAI password',
    )
    args = parser.parse_args()
    chat = ChatGPT(args.email, args.password)
    while True:
        message = input('> ')
        print(chat.get_response(message))
