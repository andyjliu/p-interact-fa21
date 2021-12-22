import os
import openai

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

List_dead = []
Main_char = input("what is your name")
first_friend = input("what is your 1st friend’s name")
second_friend = input("what is your 1st friend’s name")
third_friend = input("what is your 1st friend’s name")
List_Alive = [Main_char, first_friend, second_friend, third_friend]


prompt = '''a group of friends are camping in a forest, but then they see'''

response = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=50)

print(response)

Dead_friend = input("Pick a number 1,2, or 3")
print(  " You look to your left and see that… "+ List_Alive[int(Dead_friend)] + " IS DEAD")

List_dead.append(List_Alive[int(Dead_friend)] )