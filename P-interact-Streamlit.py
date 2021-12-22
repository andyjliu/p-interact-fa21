import asyncio
import streamlit as st 
import chronological
import openai
import os
import time
import aiofiles as aiof
from PIL import Image
img = Image.open("p-interact-group.jpg")

#zac running with zac's secret:
import json


import os
import openai

# Load your API key from an environment variable or secret management service
#openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = ""
response = openai.Completion.create(engine="davinci", prompt="This is a test", max_tokens=5)

print('success')
# Stop Debug Logger Spam
chronological.logger.remove(None)
output = "outputs/story_output" + str(time.time()) + ".txt"

# var to save the current tldr, called in generateStory
current_tldr = ""

def third_person():
    pass

#moving freqneyc penalty from 0.5-->0.3, temp from 0.5-->0.3
async def generate(prompt, max_tokens=100, temperature=0.3, top_p=1, frequency_penalty=0.3, stop=["\n\n"]):
    result = await chronological.cleaned_completion(prompt,
                                                    max_tokens=max_tokens,
                                                    engine="davinci",
                                                    temperature=temperature,
                                                    top_p=top_p,
                                                    frequency_penalty=frequency_penalty,
                                                    stop=stop)
    return result


async def init_story():
    #Zac 12-3-2021 user input to choose genre
    #I think I forgot/don't understand how the prompt reading is working/I need to change it because its reading text file names, so maybe it needs to load the text file then I add the genre as an additiona line?
    #if genre input use:
    # genre_id = st.text_input('Please Input a Genre (or NA for no Genre)')
    #if no genre input use:
    #genre_id = 'na'
    prompt_id = 'example_prompt'
    # else:
    #     genre_prompt = 'This is the beginning of a '+ genre_id + ' story: ' 
    #     #probably needs a line break here
    #     # Default prompt
    #     prompt_id = ''
    #     prompt_id = genre_prompt + prompt_id
    #     print('test', prompt_id)
    #     #generates a new text file with the prompt id
    #     file_name = prompt_id+'.txt'
    #     print(file_name)
    #     file_path = 'prompts\\'
    #     completeName = os.path.join(file_path, file_name)
    #     print(completeName)
    #     text_file = open(completeName, 'w')
        


    # User input to choose prompt

    # you call the Chronology functions, awaiting the ones that are marked await
    # read_prompt() looks in prompts/ directory for a text file. Pass in file name only, not extension.
    # Example: prompts/hello-world.txt -> read_prompt('hello-world')
    prompt = chronological.read_prompt(prompt_id)
    result = await generate(prompt)

    story = prompt + ' ' + result

    # Return Initial Story
    return story


# generate summary state of most recently generated story
# take from tldr? maybe add more methods later. Maybe add the table method.
# when updating summary state to get new tldr feed it new input story and old tldr story
# use update_tldr for initial generation as well as updating
# some way of s
# newStory --> str
# firstStory --> bool
# tldrSummary --> str
# added updating current_tldr variable
async def update_tldr(newStory, firstStory=True, tldrSummary=""):

    if firstStory:
        tldrUpdated = openai.Completion.create(
            engine="davinci",
            prompt=newStory + "\n\n" + "tl;dr:",
            temperature=0.3,
            max_tokens=200,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        firstStory = False
        current_tldr = tldrUpdated

    else:

        tldrUpdated = openai.Completion.create(
            engine="davinci",
            prompt=tldrSummary + "\n\n" + newStory + "\n\n" + "tl;dr:",
            temperature=0.3,
            max_tokens=200,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        current_tldr = tldrUpdated

    return tldrUpdated


# separate out the story generation into separate function,     done
# have it take tldr as input,                                   done
# update tldr with function,                                    done   
# and output new tldr iteratively                               done

def generateStory():
    
    # update tldr with update_tldr
    update_tldr(init_story, firstStory=False, tldrSummary=current_tldr)
    
    return current_tldr


async def options_generator(prompt):
    results = []
    # Generate 4 story options
    for i in range(4):
        #param test moving temp from 0.5 --> .3, and 0.5-->0.3 freqencuy pentalty
        results.append(generate(prompt, max_tokens=50, temperature=0.3,
                       frequency_penalty=0.3, stop=["\n\n\n\n\n"]))
    choices = await chronological.gather(*results)
    return choices

# you can name this function anything you want, the name "logic" is arbitrary
async def game():
    header = st.container()

    dataset = st.container()
    features = st.container()
    modelTraining = st.container()


    my_page = st.sidebar.radio('Page Navigation', ['page 1', 'page 2', 'page 3'])

    if my_page == 'page 1':
        with header:
            title_one = st.title("Welcome to our PAI project")
            st.image(img, caption='Meet the team: Nolan, Maymuunah, Andy, David, and Zac')
            #st.markdown('The goal of our project is...')
            
    if my_page == 'page 2':
        st.title('Let\'s Play')
        old_text = ""
        #user_input = int(st.text_input('Please Select an option number'))

        story = await init_story() # we took out await
        # - FOR ANDY stuck on await
        st.markdown("<p style=font-size:18px><b>" + story + "</b></p>", unsafe_allow_html = True)
        count = 0
        #st.button("Begin Game", key=None, help=None, on_click=None, args=None, kwargs=None)
        while True: # code comes from game function
            count += 1
            #st.text_input('Please enter a number for story')
            
            choices = await options_generator(story) # we took out await

            x = 1
            for choice in choices:
                st.markdown(str(x) + ". " + choice + "\n")
                x += 1
            try:
                user_input = int(st.text_input("Enter your choice number: ", key=count))
                time.sleep(3)
                # - 1 because choosing 1 is really choosing 0
                num = user_input - 1
                if num < 0 or num > x:
                    selected_choice = 1 # override
                else:
                    selected_choice = choices[num]
            except ValueError:
                print("Please only input numbers for your choice, between 1 and 4")
            # Generate Chapter
            # moving temperature from 0.7-->0.3, frequency penalty from 0.5--->0.3
            result = await generate(story + selected_choice, max_tokens=200, temperature=0.3, frequency_penalty=0.3) # we took out await

            # Return Chapter
            story += result
            st.markdown( "<p style=font-size:18px><b>" + story + "</b></p>", unsafe_allow_html = True)
    if my_page == 'page 3':
        st.title("Thank you for visting our PAI Project!")
        st.markdown('To learn more about PAI (Project AI) please check out https://www.p-ai.org/')

# invoke the Chronology main fn to run the async logic
chronological.main(game)

