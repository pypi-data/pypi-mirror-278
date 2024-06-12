import sys
import json
import boto3
import openai
import subprocess


def get_secret():
    if len(sys.argv) != 3:
        print("Command to use: getHelp <interpreter> <path_to_program>")
    else:
        secret_name = "openAIsk"
        region_name = "eu-west-2"
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        secret = get_secret_value_response['SecretString']
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
