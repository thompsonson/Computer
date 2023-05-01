from typing import Optional

from langchain.schema import HumanMessage
from controllers.agents.baseagent import AgentBase


# UI inspiration from https://github.com/fredliubojin/langchain_gradio/tree/main
class ChatBot(AgentBase):
    def __init__(
        self, tools: dict, llm, memory, verbose: Optional[bool] = False
    ) -> None:
        prompt = "You are a python developer. Information about classes and code is available to you via the Codebase Index tool. What could be done by inheriting the BaseController?"
        super().__init__(tools, prompt, memory, llm, max_iterations=3, verbose=verbose)  # type: ignore

    def get_response(self, selected_model, user_input, conversation_history=""):
        # Get raw chat response
        response = self._agentchain.run(user_input).strip()

        # Iterate through messages in ChatMessageHistory and format the output
        updated_conversation = '<div style="background-color: hsl(30, 100%, 30%); color: white; padding: 5px; margin-bottom: 10px; text-align: center; font-size: 1.5em;">Chat History</div>'
        for i, message in enumerate(self._memory.chat_memory.messages):
            if isinstance(message, HumanMessage):
                prefix = "User: "
                background_color = "hsl(0, 0%, 40%)"  # Dark grey background
                text_color = "hsl(0, 0%, 100%)"  # White text
            else:
                prefix = "Chatbot: "
                background_color = "hsl(0, 0%, 95%)"  # White background
                text_color = "hsl(0, 0%, 0%)"  # Black text
            updated_conversation += f'<div style="color: {text_color}; background-color: {background_color}; margin: 5px; padding: 5px;">{prefix}{message.content}</div>'
        return updated_conversation
