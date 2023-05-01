from langchain import OpenAI, SQLDatabase
from langchain.agents import initialize_agent
from langchain.agents import Tool
from langchain.chains.conversation.memory import ConversationBufferMemory


import gradio as gr
from functools import partial

from controllers.agents.chat_documentation_bot import ChatBot
from controllers.tools.CodebaseLookupTool import CodebaseLookupTool


def main():
    memory = ConversationBufferMemory(memory_key="chat_history")
    llm = OpenAI(temperature=0)

    tools = []
    #        Tool(
    #            name="Codebase Index",
    #            func=lambda q: str(index.query(q)),
    #            description="useful for when you want to answer questions about the codebase.",
    #            return_direct=True,
    #        ),
    #    ]
    db = SQLDatabase.from_uri("sqlite:///.db/database.db")
    cblt = CodebaseLookupTool(db=db, llm=llm)
    tools.append(cblt)

    user_input = gr.components.Textbox(
        lines=3,
        label="Enter your message",
    )

    output_history = gr.outputs.HTML(
        label="Updated Conversation",
    )
    chatbot = ChatBot(tools, llm, memory, verbose=True)  # type: ignore

    inputs = [
        # api_key_input,
        # model_selection,
        user_input,
    ]

    iface = gr.Interface(
        fn=partial(chatbot.get_response, chatbot),
        inputs=inputs,
        outputs=[output_history],
        title="LiveQuery GPT-4",
        description="A simple chatbot using GPT-4 and Gradio with conversation history",
        allow_flagging="never",
    )

    iface.launch()


if __name__ == "__main__":
    main()
