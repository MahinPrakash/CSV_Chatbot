import streamlit as st
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from cryptography.fernet import Fernet

encrypted_key=b'gAAAAABoCkZy6AcjIj_MpvrcyzdHVpYgmG9gLTJxjtNVDtklx6pUGJs9G3asZ1uzc8JgIXNbaPtqyF05TDvYiJVtxktpZLBmGOJTUK1eiZ46fHw70Nq94eEq5797e-VePP-iFTw6sd752z8oClPpzmT1V3uneNdtPfUx1WbfTAQOaElFggdVHeMfW4nNe2xXeJtm4XVW0cfu99n2lFTs9izH7ODOkx7KgvFLc1VUENupXLg4PSNgOn_bCPTTOSIdKFGQGos98ICXjsx6wPYQpY0yoXRd1sM8OYsH0nYTo3A0Fc7YMnChuyY='

key=b'dNxmct5HrAjsG8LsJACGnXElHLVcbzjOgsJgvdfsUck='

fernet = Fernet(key)
decr_api = fernet.decrypt(encrypted_key).decode()

st.title('CSV Chatbot📊')

uploaded_file = st.file_uploader("Upload a CSV file")
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

    

