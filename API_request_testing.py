#json for securely retreiving openai key
#https://towardsdatascience.com/keeping-things-secret-d9060c73089b
import json
def get_keys(path):
    with open(path) as f:
        return json.load(f)

keys = get_keys(r"C:\Users\zac\OneDrive\Documents\GitHub\p-interact\secret.json")


import os
import openai

# Load your API key from an environment variable or secret management service
#openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = keys['OPENAI_API_KEY']
response = openai.Completion.create(engine="davinci", prompt="This is a test", max_tokens=5)

print('success')