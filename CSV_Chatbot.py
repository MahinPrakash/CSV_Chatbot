import streamlit as st
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from cryptography.fernet import Fernet

encrypted_key=b'gAAAAABn_luBgcX90Fj1ELxPBLuwkfd448Z8s65ecZ3xKRLZ9wS4qHslz-JJnocepy--f4ki6Z5urqz8RdE_r3zSZPCEuwFWqrbGEu5jWVHBX1fESer09zMWAZBJnvRFIUL_jzO3xwpyuw_6N8ptYoFLV_n6HUEEpzHMOriYQjtH_Nj0X4aaoihLlpbdvJbYhwtY-pFnjmHJanb9KKNwtN2b6fSVFnVjtfWEmbfkc0YheZAGRMtVyYwnOP242Fm8UEdg1vrZxJ7ouNE_01E3RdPvW0Dr1OcejMFo26e3D0kw1HJbFKIUps4='

key=b'NHXeNPE94HFUOlfUif_StMUW5FGWo1kKb8BN3mTlJNU='

fernet = Fernet(key)
decr_api = fernet.decrypt(encrypted_key).decode()

st.title('CSV Chatbot📊')

uploaded_file = st.file_uploader("Upload a data file")
if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    st.dataframe(dataframe)
    dataframe.to_csv(uploaded_file.name,index=False)

user_prompt=st.text_input('Enter your Prompt')
if st.button("Ask"):
    llm = ChatOpenAI(model='gpt-4.1',temperature=0.0,api_key=decr_api)
    
    with st.spinner(text="Analyzing your data"):
        agent = create_csv_agent(
            llm,
            uploaded_file.name,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            handle_parsing_errors=True,
            allow_dangerous_code=True
        )
    
        response = agent.run(user_prompt)
    
    st.title('Response:-')
    st.info(response)

    

