from langchain.agents import create_pandas_dataframe_agent
import pandas as pd
from langchain.llms import OpenAI

def query_agent(data, query):

    # Parse the CSV file and create a dataframe from its contents.
    df = pd.read_csv(data)

    llm = OpenAI()

    # Create a pandas dataframe agent
    agent = create_pandas_dataframe_agent(llm, df, verbose=True)

    # Python REPL: A python shell used to evaluating and executing python commands.
    # It takes python code as input and outputs the result. The input python code can be generated from another tool in langchain.
    response = agent.run(query)

    return response