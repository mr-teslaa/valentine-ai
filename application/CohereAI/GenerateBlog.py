import os
import time
import cohere
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

# Cohere AI API setup
co = cohere.Client(os.getenv('API_KEY'))

def max_likely(prediction):
    output = prediction.generations[0].text
    return output

# Generate blog posts for each keyword
def generate_letter(gender):
        letter_generate = co.generate(
            model='command',
            prompt= "You are a poet, you are known for your unique romantic, flirting words and today is valentines day. Write one very short sentence within 65 character romantic, loving, caring message for my " + gender,
            max_tokens=70,
            temperature=0.9,
            stop_sequences=["---"]
        )

        letter = max_likely(letter_generate)

        return letter