import os
import streamlit as st

import tiktoken

from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

from langchain.prompts import PromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage

from prompts import *


def main():
    # APIキーの設定
    with open("apikey.txt") as f:
        key = f.read()
        os.environ["OPENAI_API_KEY"] = str(key)

    llm = ChatOpenAI(model_name="gpt-4-0125-preview", temperature=0)
    memory = ConversationBufferMemory(return_messages=True)
    chain = ConversationChain(
        llm=llm,
        memory=memory
    )

    encoding = tiktoken.encoding_for_model("gpt-4-0125-preview")

    # prompt = "こんにちは！私の名前は、YUUKIです。"
    # ai_message = chain.run(input=prompt)
    # print("##################")
    # print(ai_message)

    # prompt = "私の名前は、何ですか？答えてください。"
    # ai_message = chain.run(input=prompt)
    # print("##################")
    # print(ai_message)

    # messages = [
    #     SystemMessage(content="You are a helpful assistant."),
    #     HumanMessage(content="こんにちは！私はジョンと言います！"),
    #     AIMessage(content="こんにちは、ジョンさん！どのようにお手伝いできますか？"),
    #     HumanMessage(content="私の名前が分かりますか？")
    # ]

    # result = chain(messages)
    # print('\n####################################################\n')
    # print(result['input'])
    # print("\n----------------------------------------------------\n")
    # print(result['response'])
    # print('\n####################################################\n')


    # prompt = PromptTemplate(
    #     template="""

    #     あなたは、以下の問題文と解答例から、質問に対する解説を行うチャットボットです。

    #     ====== 問題文と解答例 ======
    #     {document}

    #     """,
    #     input_variables=["document", "question"],
    # )




    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content="こんにちは！各設問の解説をしてください。"),
        AIMessage(content=KAISETSU_PROMPT),
        HumanMessage(content="設問2について、もっと詳しく解説してください。")
    ]

    token_size = encoding.encode(SYSTEM_PROMPT)
    print("token_size:", len(token_size))

    token_size = encoding.encode(KAISETSU_PROMPT)
    print("token_size:", len(token_size))

    result = chain.invoke(messages)
    print('\n####################################################\n')
    # print(result['input'])
    print("\n----------------------------------------------------\n")
    print(result['response'])
    print('\n####################################################\n')

    token_size = encoding.encode(result['response'])
    print("token_size:", len(token_size))



if __name__ == "__main__":
    main()