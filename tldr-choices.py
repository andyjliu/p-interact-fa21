
#tldr summary function:

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

""" tldrSummary = openai.Completion.create(
  engine="davinci",
    prompt = inputStory + "\n\n" + "tl;dr"
  temperature=0.3,
  max_tokens=200,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
) """

#generate summary state of most recently generated story
#take from tldr? maybe add more methods later. Maybe add the table method.
#when updating summary state to get new tldr feed it new input story and old tldr story
#use update_tldr for initial generation as well as updating
#some way of s
# newStory --> str
# firstStory --> bool
# tldrSummary --> str
def update_tldr(newStory, firstStory = True, tldrSummary = ""):

    if firstStory:
        tldrUpdated = openai.Completion.create(
        engine="davinci",
        prompt = newStory + "\n\n" + "tl;dr:",
        temperature=0.3,
        max_tokens=200,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )
        firstStory = False

    else: 

        tldrUpdated = openai.Completion.create(
        engine="davinci",
        prompt = tldrSummary + "\n\n" + newStory + "\n\n" + "tl;dr:",
        temperature =0.3,
        max_tokens=200,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )

    return tldrUpdated

#display choices
#when choice clicked send choice to generation
# newStory --> str
# choiceList --> list str
# generating clickable buttons
def textChoices(newStory, choiceList):

    # display newStory
    print("\n\n" + newStory + "\n\n")

    # display choices
    x=1
    for choice in choiceList:
        print(x + ". " + choice + "\n") 
        x += 1
    
    # somebody selects a choice! (left for later depending on we decide to present this? clicky clicky)
    # selectedChoice = whatever they end up picking
    try:
        num = int(input("Enter your choice number: "))
        if num < 1 or num > x:
            raise ValueError
        else: 
            selectedChoice = choiceList[num]
    except ValueError:
        print("Please only input numbers for your choice, between " + 1 + " and " + x)  

    # concat choice to newStory --> generate

    openai.api_key = os.getenv("OPENAI_API_KEY")

    story = openai.Completion.create(
        engine="davinci",
        prompt = newStory + selectedChoice,
        temperature=0.7,
        max_tokens=200,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )

    return story