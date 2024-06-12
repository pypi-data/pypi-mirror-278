import sys
import json
import boto3
import openai
import subprocess
import requests

endpoint_url = "https://rgwge4ffdqvnmylps4jm3ybbkq0togzi.lambda-url.eu-west-2.on.aws/"


def retreiveSecretKey():
    if len(sys.argv) != 3:
        print("Command to use: getHelp <interpreter> <path_to_program>")
    else:
        response = requests.get(endpoint_url)
        response_payload = response.json()
        print(response_payload)
        secret = response_payload.get("open AI API secret key")
        run_program(sys.argv[1], sys.argv[2],secret)


def run_program(interpreter, file_path,secret):
    def genAIErrorMessage(error_message,secret):
        openai.api_key = secret

        chat_complete = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=[{"role":"user","content":str(error_message)}])

        print(chat_complete.choices[0].message.content)
    try:
        result = subprocess.run(
            [interpreter, file_path],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            genAIErrorMessage(result.stderr,secret)
        else:
            print("Program output:")
            print(result.stdout)
    
    except Exception as e:
        print(f"An exception occurred: {e}")
