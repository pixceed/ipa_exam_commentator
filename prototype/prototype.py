import os
import streamlit as st

from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

from langchain.schema import AIMessage, HumanMessage, SystemMessage

from prompts import *


def main():

    # APIキーの設定
    with open("apikey.txt") as f:
        key = f.read()
        os.environ["OPENAI_API_KEY"] = str(key)

    # UI用の会話履歴を初期化
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # st.session_state.messages = [
    #     SystemMessage(content=SYSTEM_PROMPT),
    #     HumanMessage(content="こんにちは！各設問の解説をしてください。"),
    #     AIMessage(content=KAISETSU_PROMPT)
    # ]
    st.session_state.messages = [
        SystemMessage(content=SYSTEM_PROMPT)
    ]


    if "memory_messages" not in st.session_state:
        st.session_state.memory_messages = []

    # if len(st.session_state.memory_messages) == 0:
    #     st.session_state.memory_messages.append({"role": "assistant", "content": KAISETSU_PROMPT})

    llm = ChatOpenAI(model_name="gpt-4-0125-preview", temperature=0)
    memory = ConversationBufferMemory(return_messages=True)
    chain = ConversationChain(
        llm=llm,
        memory=memory
    )

    st.title("IPA EXAM TutorBot")

    # UI用の会話履歴を表示
    for message in st.session_state.memory_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # UI周り
    prompt = st.chat_input("質問してね")

    if prompt:
        # 会話を追加
        st.session_state.messages.append(
            HumanMessage(content=prompt)
        )
        st.session_state.memory_messages.append(
            {"role": "user", "content": prompt}
        )
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("考え中..."):
                result = chain.invoke(st.session_state.messages)
                st.markdown(result['response'])
        
            # 会話を追加
            st.session_state.messages.append(
                AIMessage(content=result['response'])
            )
            st.session_state.memory_messages.append(
                {"role": "assistant", "content": result['response']}
            )


if __name__ == "__main__":
    main()