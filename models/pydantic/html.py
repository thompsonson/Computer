""" pydantic model for html controller """

from typing import List
from pydantic import BaseModel, Field, constr


class Image(BaseModel):
    """Represents an image with its name and associated prompt."""

    image_name: constr(min_length=1) = Field(..., description="The name of the image file.")  # type: ignore
    image_prompt: constr(min_length=1) = Field(..., description="The prompt used for generating the image.")  # type: ignore


class HtmlModel(BaseModel):
    """Represents an HTML file with its content, filename, and related images."""

    html: constr(min_length=1) = Field(..., description="HTML content as a string, all linebreaks must be represented a \n")  # type: ignore
    filename: constr(min_length=1) = Field(..., description="The filename of the HTML file")  # type: ignore
    images: List[Image] = Field(
        ..., description="A list of images with their respective names and prompts."
    )
