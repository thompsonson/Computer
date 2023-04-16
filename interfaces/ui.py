"""  """
import os
import sys

# Add the parent directory of the models package to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from controllers.controller_ehticalai import BuddhistController, RightSpeechEvaluation
import asyncio
import gradio as gr
import os
import sys


def format_right_speech_evaluation(evaluation: RightSpeechEvaluation) -> str:
    formatted_output = f"""
    Truthfulness: {evaluation.truthfulness}
    Kindness: {evaluation.kindness}
    Constructiveness: {evaluation.constructiveness}
    Absence of False Speech: {evaluation.absence_of_false_speech}
    Absence of Malicious Speech: {evaluation.absence_of_malicious_speech}
    Absence of Harsh Speech: {evaluation.absence_of_harsh_speech}
    Absence of Idle Chatter: {evaluation.absence_of_idle_chatter}

    Rationale: {evaluation.rationale}
    """
    return formatted_output


async def evaluate_right_speech_async(message: str) -> str:
    controller = BuddhistController(message)
    evaluation = await controller.process_message()
    if evaluation:
        formatted_output = format_right_speech_evaluation(evaluation)
        return formatted_output
    else:
        return "An error occurred while processing the message."


def evaluate_right_speech(message: str) -> str:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(evaluate_right_speech_async(message))
    loop.close()
    return result


input_text = gr.inputs.Textbox(lines=5, label="Enter a message to evaluate")
output_text = gr.outputs.Textbox(label="Right Speech Evaluation")

iface = gr.Interface(
    fn=evaluate_right_speech,
    inputs=input_text,
    outputs=output_text,
    title="Buddhist Right Speech Evaluation",
    description="Evaluate a message based on the Buddhist principles of Right Speech.",
    allow_flagging=False,  # Disable flagging
)

iface.launch()
