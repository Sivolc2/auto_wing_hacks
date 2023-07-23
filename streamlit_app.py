import mermaid
from pathlib import Path


# New imports
import openpyxl
import streamlit as st

from langchain import SQLDatabase
from langchain.agents import AgentType
from langchain.agents import initialize_agent, Tool
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chains import LLMMathChain, SQLDatabaseChain
from langchain.llms import OpenAI
from langchain.utilities import DuckDuckGoSearchAPIWrapper
from langchain.agents import load_tools
from streamlit_agent.callbacks.capturing_callback_handler import playback_callbacks
from streamlit_agent.clear_results import with_clear_container
from langchain.utilities import GoogleSerperAPIWrapper

from product_search import search_for_products

import pandas as pd
import os

DB_PATH = (Path(__file__).parent / "Chinook.db").absolute()


# New function to run agent with custom prompt
def run_with_prompt(input, tools, llm, prompt):
    prompt + " " + input
    result = llm.run(input, tools=tools)
    return result

SAVED_SESSIONS = {
    "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?": "leo.pickle",
    "What is the full name of the artist who recently released an album called "
    "'The Storm Before the Calm' and are they in the FooBar database? If so, what albums of theirs "
    "are in the FooBar database?": "alanis.pickle",
}
# st.title("🦜 LangChain: Chat with search")
st.set_page_config(
    page_title="Lumos", page_icon="🦜", layout="wide", initial_sidebar_state="collapsed"
)

"# 🦜🔗 Lumos: Revolutionize Your Business"
openai_api_key = st.write(
    os.environ["OPENAI_API_KEY"] == st.secrets["OPENAI_API_KEY"],
)

# Tools setup
llm = OpenAI(temperature=0, openai_api_key=openai_api_key, streaming=True)
llm_math_chain = LLMMathChain.from_llm(llm)
db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")
db_chain = SQLDatabaseChain.from_llm(llm, db)
search_google = GoogleSerperAPIWrapper()
tools = [
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math",
    ),
    Tool(
        name="FooBar DB",
        func=db_chain.run,
        description="useful for when you need to answer questions about FooBar. Input should be in the form of a question containing full context",
    ),
    Tool(
       name="Mermaid",
       func=mermaid.run,
       description="will display the provided mermaid diagram to the user. Input should be a mermaid diagram"
    ),
    Tool(
        name="SearchG",
        func=search_google.run,
        description="useful for when you need to ask with search"
    )
]

mrkl = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True) 

tool_order_prompt = """
The tools should be used in this order for answering questions:
1. SearchG - Use this to search the internet for general information
2. Calculator - Use this for any math calculations 
3. FooBar DB - Use this to look up information in the FooBar database
4. Mermaid - Use this to generate mermaid diagrams
You should follow this order whenever possible when answering the user's questions.
"""

# Existing imports and setup
tabs = st.tabs(["QA", "Product Search"])

with tabs[0]:
    with st.form(key="form"):
        user_input = st.text_input("What type of business do you run?")
        # if not user_input:
        #     user_input = prefilled
        submit_clicked = st.form_submit_button("Submit Inquiry")
        ## Add langchain preprompt?


with tabs[1]:
    products = st.text_input("Enter comma-separated list of products")
    
    if products:
        products = [p.strip() for p in products.split(",")]

        for product in products:
            st.header(product)

            # Get the result from the agent
            # result = mrkl.run(product, tool="Search Google")

            # result = mrkl.run(tool="Search Google")
            result = mrkl.run(f"What are some options to buy {product}?", "SearchG")
            # Assume result is a list of dictionaries for this example
            df = pd.DataFrame(result)

            # Summarize the data as required (this step depends on the structure and nature of your data)
            # df = df.groupby(...).sum()  # Example summarization
            
            file_name = f"{product.replace(' ','_')}.xlsx"

            # Save to Excel
            df.to_excel(file_name, index=False)

            # Display the DataFrame
            st.dataframe(df)

            # Provide download link
            st.download_button(
                label="📥 Download Results",
                data=df.to_excel(index=False, engine='openpyxl'),
                file_name=file_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

output_container = st.empty()
if with_clear_container(submit_clicked):
    output_container = output_container.container()
    output_container.chat_message("user").write(user_input)

    answer_container = output_container.chat_message("assistant", avatar="🦜")
    st_callback = StreamlitCallbackHandler(answer_container)

    # If we've saved this question, play it back instead of actually running LangChain
    # (so that we don't exhaust our API calls unnecessarily)
    answer = run_with_prompt(user_input, tools, mrkl, tool_order_prompt)[0:len(tool_order_prompt)]

    answer_container.write(answer)
