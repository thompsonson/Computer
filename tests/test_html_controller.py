""" Test for the html controller """

import pytest
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.pydantic.html import HtmlModel as pydantic_html
from models.sql.html import HtmlFile as sql_html, Image as sql_image, Base

from controllers.prompts.html import HtmlController

from utils.DBAdapter import DBAdapter


# Pydantic models
def test_html_model():
    html_model = pydantic_html(
        html="<html><head><title>Test</title></head><body><h1>Test</h1></body></html>",
        filename="test.html",
        images=[
            {"image_name": "image1.png", "image_prompt": "A beautiful landscape"},
            {"image_name": "image2.png", "image_prompt": "A city skyline at night"},
        ],  # type: ignore
    )
    assert html_model.filename == "test.html"
    assert len(html_model.images) == 2


def test_html_model_validation_error():
    with pytest.raises(ValidationError):
        pydantic_html(
            html="",
            filename="",
            images=[],
        )


def test_image_model_validation_error():
    with pytest.raises(ValidationError):
        pydantic_html(
            html="html",
            filename="filename",
            images=[{"image_name": "", "image_prompt": ""}],  # type: ignore
        )


# SQLAlchemy models
@pytest.fixture(scope="module")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def test_html_file(db_session):
    html_file = sql_html(
        html="<html><head><title>Test</title></head><body><h1>Test</h1></body></html>",
        filename="test.html",
    )
    db_session.add(html_file)
    db_session.commit()
    fetched_html_file = (
        db_session.query(sql_html).filter_by(filename="test.html").first()
    )
    assert fetched_html_file.filename == "test.html"


def test_image(db_session):
    html_file = db_session.query(sql_html).filter_by(filename="test.html").first()
    image = sql_image(
        image_name="image1.png",
        image_prompt="A beautiful landscape",
        html_id=html_file.id,
    )
    db_session.add(image)
    db_session.commit()
    fetched_image = (
        db_session.query(sql_image).filter_by(image_name="image1.png").first()
    )
    assert fetched_image.image_name == "image1.png"


@pytest.mark.asyncio
async def test_html_controller():
    print("running the test_html_controller")
    db_adapter = DBAdapter()
    session = db_adapter.unmanaged_session()

    html_controller = HtmlController(
        message="Create a simple webpage about cats with a header and a paragraph.",
        session=session,
    )
    print("below is the output_parser")
    print(html_controller._output_parser)
    print(html_controller)
    # html_file = await html_controller.process_message()
    # assert isinstance(html_file, sql_html)
    # assert "<html>" in html_file.html_content
    # assert "cats" in html_file.html_content
    # assert len(html_file.images) > 0

    # Clean up the created record
    # session.delete(html_file)
    # session.commit()
