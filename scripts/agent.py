import os
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index import download_loader

download_loader("GithubRepositoryReader")

from llama_index.readers.llamahub_modules.github_repo import (
    GithubRepositoryReader,
    GithubClient,
)
from llama_index import GPTSimpleVectorIndex

from langchain.agents import Tool
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain import OpenAI, SQLDatabase
from langchain.agents import initialize_agent


import gradio as gr
from functools import partial

from controllers.agents.chat_documentation_bot import ChatBot
from controllers.tools.CodebaseLookupTool import CodebaseLookupTool


def query(index, query_string, **kwargs):
    "queries the given index"
    print(f"-----------------------\nquery: {query_string}\n------------\n")
    response = index.query(query_string, **kwargs)
    print(f"{response}\n-----------------------\n")
    print(f"response source nodes: {response.source_nodes}\n-----------------------\n")
    print(
        f"response formatted sources: {response.get_formatted_sources}\n-----------------------\n"
    )


if os.path.isfile(".indexes/code_base"):
    index = GPTSimpleVectorIndex.load_from_disk(".indexes/code_base")
else:
    github_client = GithubClient(os.getenv("GITHUB_TOKEN_AGENT"))
    loader = GithubRepositoryReader(
        github_client,
        owner="thompsonson",
        repo="Computer",
        filter_file_extensions=([".py"], GithubRepositoryReader.FilterType.INCLUDE),
        verbose=False,
        concurrent_requests=10,
    )

    docs = loader.load_data(branch="main")
    # alternatively, load from a specific commit:
    # docs = loader.load_data(commit_sha="a6c89159bf8e7086bea2f4305cff3f0a4102e370")

    index = GPTSimpleVectorIndex([])  # .from_documents(docs)
    for doc in docs:
        # print(doc.extra_info)
        index.insert(doc)

    index.save_to_disk(".indexes/code_base")

# query(
#    index,
#    "Write a python class that inherits from the prompt base controller. The class should have the prompt 'you are a python tester, given the message, create a pytest'",
# )

tools = [
    Tool(
        name="Codebase Index",
        func=lambda q: str(index.query(q)),
        description="useful for when you want to answer questions about the codebase.",
        return_direct=True,
    ),
]

# set Logging to DEBUG for more detailed outputs
memory = ConversationBufferMemory(memory_key="chat_history")
llm = OpenAI(temperature=0)
# agent_chain = initialize_agent(tools, llm, agent="conversational-react-description", memory=memory, verbose=True, max_iterations=3)
# agent_chain = initialize_agent(tools, llm, agent="zero-shot-react-description", memory=memory, verbose=True, max_iterations=3)
# print(f"agent_chain: {agent_chain}")
# agent_chain.run(input="""You are a python developer. Information about classes and code is available to you via the Codebase Index tool. Find out what the BaseController does. What could be done when inheriting it?""")
# agent_chain.run(input="""You are a python developer. Information about classes and code is available to you via the Codebase Index tool. What could be done by inheriting the BaseController?""")
# agent_chain.run(input="""Find a class that inherits from BaseController. Use this case as an example of how it is used.""")
# agent_chain.run(input="""Find the pydantic modules used by the class that inherits from BaseController. Use this as an example of how pydantic modules are used.""")
# agent_chain.run(input="""Create a class that inherits from BaseController. The case should have the PROMPT_TEMPLATE 'generate a pydantic model for storing code artefacts'.""")


db = SQLDatabase.from_uri("sqlite:///.db/database.db")
# db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)
# db_chain.run(query="How many functions are there?")
# db_chain.run(query="what is the docstring for the test_html_model function?")
# db_chain.run(query="what is the docstring for the BaseController class?")


cblt = CodebaseLookupTool(db=db, llm=llm)

tools.append(cblt)

agent_chain = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    memory=memory,
    verbose=True,
    max_iterations=5,
)

# agent_chain.run(input="Find the docstring and argument for test_html_model")
# agent_chain.run(input="What are the functions of the HTMLController class?")
# agent_chain.run(input="In markdown format, provide the classess and functions are there in the git project https://github.com/thompsonson/Computer.git?")


def main():
    memory = ConversationBufferMemory(memory_key="chat_history")
    llm = OpenAI(temperature=0)

    tools = [
        Tool(
            name="Codebase Index",
            func=lambda q: str(index.query(q)),
            description="useful for when you want to answer questions about the codebase.",
            return_direct=True,
        ),
    ]
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
    chatbot = ChatBot(tools, llm, memory)  # type: ignore

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
