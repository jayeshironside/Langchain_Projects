import os
from dotenv import load_dotenv
# Use the environment variables to retrieve API keys
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from langchain.llms import OpenAI

llm = OpenAI(model_name="text-davinci-003", temperature=0.5)
our_prompt = """"
I love trips, and I have been to 6 countries.
I plan to visit few more soon.

Can you create a post for tweet in 10 words or above?
"""

print(our_prompt)
print(llm(our_prompt)) # Prints the model output 