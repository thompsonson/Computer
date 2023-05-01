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
from langchain import OpenAI
from langchain.agents import initialize_agent


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

#query(
#    index,
#    "Write a python class that inherits from the prompt base controller. The class should have the prompt 'you are a python tester, given the message, create a pytest'",
#)

tools = [
    Tool(
        name = "Codebase Index",
        func=lambda q: str(index.query(q)),
        description="useful for when you want to answer questions about the codebase.",
        return_direct=True
    ),
]

# set Logging to DEBUG for more detailed outputs
memory = ConversationBufferMemory(memory_key="chat_history")
llm=OpenAI(temperature=0)
agent_chain = initialize_agent(tools, llm, agent="conversational-react-description", memory=memory, verbose=True)
#print(f"agent_chain: {agent_chain}")

agent_chain.run(input="""You are a python developer. Information about classes and code is available to you via the Codebase Index tool. Find out what the BaseController does and then create a class that inherits from it. The case should have the PROMPT_TEMPLATE 'generate a pydantic model for storing code artefacts'. 
Include all of the code.""")

agent_chain.run(input="""Find a class that inherits from BaseController. Use this case as an example of how it is used.""")

agent_chain.run(input="""Find the pydantic modules used by the class that inherits from BaseController. Use this as an example of how pydantic modules are used.""")

agent_chain.run(input="""Create a class that inherits from BaseController. The case should have the PROMPT_TEMPLATE 'generate a pydantic model for storing code artefacts'.""")

from langchain import OpenAI, SQLDatabase, SQLDatabaseChain

db = SQLDatabase.from_uri("sqlite:///../.db/database.db")
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)
db_chain.run("How many codefunctions are there?")
