"""  """
import os
import sys

# Add the parent directory of the models package to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import gradio as gr, string
import asyncio
from sqlalchemy import String, Integer
from controllers.controller_ehticalai import BuddhistController, RightSpeechEvaluation


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


def generate_inputs(controller):
    input_mapping = {
        String: gr.inputs.Textbox,
        Integer: gr.inputs.Slider,
    }
    inputs = {}
    model_info = controller.get_model_info()
    for name, column_type in model_info:
        input_type = input_mapping.get(column_type)
        if input_type:
            inputs[name] = input_type(label=name.capitalize())
    return inputs


controller = BuddhistController.for_model_info()  # Instantiate the controller
inputs = generate_inputs(controller)
output_fields = gr.outputs.Textbox(label="Processed data", type="text")

iface = gr.Interface(
    fn=evaluate_right_speech,
    inputs=inputs,
    outputs=output_fields,
    title="Buddhist Right Speech Evaluation",
    description="Evaluate a message based on the Buddhist principles of Right Speech.",
)

iface.launch()
