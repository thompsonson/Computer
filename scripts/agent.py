import os

from llama_index import download_loader

download_loader("GithubRepositoryReader")

from llama_index.readers.llamahub_modules.github_repo import (
    GithubRepositoryReader,
    GithubClient,
)
from llama_index import GPTSimpleVectorIndex


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
    github_client = GithubClient(os.getenv("GITHUB_TOKEN"))
    loader = GithubRepositoryReader(
        github_client,
        owner="thompsonson",
        repo="Computer",
        filter_file_extensions=([".py"], GithubRepositoryReader.FilterType.INCLUDE),
        verbose=False,
        concurrent_requests=10,
    )

    docs = loader.load_data(branch="html")
    # alternatively, load from a specific commit:
    # docs = loader.load_data(commit_sha="a6c89159bf8e7086bea2f4305cff3f0a4102e370")

    index = GPTSimpleVectorIndex([])  # .from_documents(docs)
    for doc in docs:
        # print(doc.extra_info)
        index.insert(doc)

    index.save_to_disk(".indexes/code_base")

query(
    index,
    "Write a python class that inherits from the prompt base controller. The class should have the prompt 'you are a python tester, given the message, create a pytest'",
)
