from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI

# Import things that are needed generically
from langchain.agents import initialize_agent, Tool
from langchain.tools import BaseTool
from langchain import LLMMathChain, SerpAPIWrapper

llm = OpenAI(temperature=0)

# tools = load_tools(["serpapi", "llm-math"], llm=llm)

# agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# agent.run("Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?")

# agent.run("What is the square root of 2?")

# agent.run("who coached England's Rugby World Cup winning team and what is the connection to England's Football world cup winning team?")

# agent.run("What is the personal connection between a player in England's Rugby World Cup winning team and a player in England's Football World Cup winning team?")

search = SerpAPIWrapper()
llm_math_chain = LLMMathChain(llm=llm, verbose=True)


class CustomSearchTool(BaseTool):
    name = "Search"
    description = "useful for when you need to answer questions about current events"

    def _run(self, query: str) -> str:
        """Use the tool."""
        return search.run(query)

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("BingSearchRun does not support async")


class CustomCalculatorTool(BaseTool):
    name = "Calculator"
    description = "useful for when you need to answer questions about math"

    def _run(self, query: str) -> str:
        """Use the tool."""
        return llm_math_chain.run(query)

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("BingSearchRun does not support async")


tools = [CustomSearchTool(), CustomCalculatorTool()]

agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

# agent.run("What is the Wolfman language and how does it help us understand the world?")

agent.run(
    """Given the following text, generate a blog post, with the title "ChatGPT needs to learn to use a calculator!" about it. The text should be engaging and amusing.

ChatGPT clearly shows a mastery of the English Language. 
It doesn't appear capable of repeatably generating accurate computation (e.g. with regards to pyhsics auestions about forces on a ball being pushed up a hill).
This leads me to suggest that it isn't an AGI and AGI will only be possible with a collection of tools that can be used to solve problems.
Basically the GPT LLM needs to learn to use a calculator!
"""
)
