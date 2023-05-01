from unittest.mock import MagicMock
import pytest
from controllers.prompts.mep_extract import MEPExtractController
from controllers.mep import MEPController
from models.pydantic.mep import MEPIn
from models.sql.mep import MEP
from utils.DBAdapter import DBAdapter
from langchain.llms import OpenAI
from langchain.output_parsers import PydanticOutputParser
from sqlalchemy.orm import Session


# Define the mep_controller fixture
@pytest.fixture
def mep_controller():
    # Create an instance of MEPController
    return MEPController(db_adapter=DBAdapter())


# Define the mep_extract_controller fixture
@pytest.fixture
def mep_extract_controller():
    # Create an instance of MEPExtractController
    user_input = "Salima YENBOU.Renew Europe Group.Member.E-mail.Twitter.Facebook.Instagram.France. . - Renaissance (France).Date of birth :.14-03-1971.,. Aubervilliers.Home Salima YENBOU.Member.AFET.Committee on Foreign Affairs.DROI.Subcommittee on Human Rights.PEGA.Committee of Inquiry to investigate the use of Pegasus and equivalent surveillance spyware.DMED.Delegation to the Parliamentary Assembly of the Union for the Mediterranean.Substitute.CULT.Committee on Culture and Education.DPAL.Delegation for relations with Palestine.Most recent activities.EU Action Plan against Trafficking in Cultural Goods (debate) \n. . . .FR.20-04-2023.P9_CRE-PROV(2023)04-20(4-162-0000).Contributions to plenary debates.The crackdown on the right to education and education rights activists in Afghanistan, including the case of Matiullah Wesa \n. . . .FR.19-04-2023.P9_CRE-PROV(2023)04-19(3-376-0000).Contributions to plenary debates.JOINT MOTION FOR A RESOLUTION on the universal decriminalisation of homosexuality in the light of recent developments in Uganda.19-04-2023.RC-B9-0219/2023.Motions for resolutions.PDF\n.(185 KB).DOC\n.(55 KB).Home.Main parliamentary activities. .Contributions to plenary debates. .Reports - as rapporteur. .Reports - as shadow rapporteur. .Opinions - as shadow rapporteur. .Motions for resolutions. .Oral questions.Other parliamentary activities. .Questions for written answer (including answers).Curriculum vitae.Declarations.Assistants.Meetings. .Past meetings.History of parliamentary service. .9th parliamentary term.Contact.Bruxelles.Parlement européenBât. WILLY BRANDT02M10560, rue Wiertz / Wiertzstraat 60B-1047 Bruxelles/Brussel.Telephone\n. \n. \n.0032 2 28 45740.Fax\n. \n. \n.0032 2 28 49740.Strasbourg.Parlement européenBât. WINSTON CHURCHILLM020541, avenue du Président Robert SchumanCS 91024F-67070 Strasbourg Cedex.Telephone\n. \n. \n.0033 3 88 1 75740.Fax\n. \n. \n.0033 3 88 1 79740.Share this page:.Share this page on Facebook.Share this page on Twitter.Share this page on LinkedIn.Share this page on Whatsapp.Sign up for email updates.Subscribe to the RSS feed.MEPs.Political groups.Group of the European People's Party (Christian Democrats).Group of the Progressive Alliance of Socialists and Democrats in the European Parliament.Renew Europe Group.Group of the Greens/European Free Alliance.European Conservatives and Reformists Group.Identity and Democracy Group.The Left group in the European Parliament - GUE/NGL.Non-attached Members."

    return MEPExtractController(message=user_input)


@pytest.mark.asyncio
async def test_parse_mep_data_without_llm():
    # Sample input simulating a user query
    page_content = "John Doe.Renew Europe Group.Member.E-mail.Twitter.Facebook.Instagram.Country. . - Party (Country).Date of birth :.01-01-1980.,. City.Home John Doe.Member."

    # Expected output
    expected_output = {
        "name": "John Doe",
        "affiliation": "Renew Europe Group",
        "committees": ["Member"],
        "activities": ["E-mail", "Twitter", "Facebook", "Instagram"],
    }

    # Create an instance of MEPController
    mep_controller = MEPController(db_adapter=DBAdapter())

    # Create a mock object to replace the MEPExtractController instance
    mock_mep_extract_controller = MagicMock()
    # Set the return value of the process_message method of the mock object
    mock_mep_extract_controller.process_message.return_value = expected_output

    # Use the mock object to replace the MEPExtractController instance in the parse_mep_data method
    # mep_controller.MEPExtractController = MagicMock(return_value=mock_mep_extract_controller)

    # Call the function and get the output
    output = mep_controller.parse_mep_data(
        page_content, mep_extract_controller=mock_mep_extract_controller
    )

    # Assert that the output matches the expected output
    assert output["name"] == expected_output["name"]  # type: ignore
    assert output["affiliation"] == expected_output["affiliation"]  # type: ignore
    assert output["committees"] == expected_output["committees"]  # type: ignore
    assert output["activities"] == expected_output["activities"]  # type: ignore


# Sample input with missing committees and activities
@pytest.mark.parametrize(
    "page_content, expected_output",
    [
        (
            """
        Salima YENBOU.Renew Europe Group.Member.E-mail.Twitter.Facebook.Instagram.France. . - Renaissance (France).Date of birth :.14-03-1971.,. Aubervilliers.Home Salima YENBOU.Member.AFET.Committee on Foreign Affairs.DROI.Subcommittee on Human Rights.PEGA.Committee of Inquiry to investigate the use of Pegasus and equivalent surveillance spyware.DMED.Delegation to the Parliamentary Assembly of the Union for the Mediterranean.Substitute.CULT.Committee on Culture and Education.DPAL.Delegation for relations with Palestine.Most recent activities.EU Action Plan against Trafficking in Cultural Goods (debate) \n. . . .FR.20-04-2023.P9_CRE-PROV(2023)04-20(4-162-0000).Contributions to plenary debates.The crackdown on the right to education and education rights activists in Afghanistan, including the case of Matiullah Wesa \n. . . .FR.19-04-2023.P9_CRE-PROV(2023)04-19(3-376-0000).Contributions to plenary debates.JOINT MOTION FOR A RESOLUTION on the universal decriminalisation of homosexuality in the light of recent developments in Uganda.19-04-2023.RC-B9-0219/2023.Motions for resolutions.PDF\n.(185 KB).DOC\n.(55 KB).Home.Main parliamentary activities. .Contributions to plenary debates. .Reports - as rapporteur. .Reports - as shadow rapporteur. .Opinions - as shadow rapporteur. .Motions for resolutions. .Oral questions.Other parliamentary activities. .Questions for written answer (including answers).Curriculum vitae.Declarations.Assistants.Meetings. .Past meetings.History of parliamentary service. .9th parliamentary term.Contact.Bruxelles.Parlement européenBât. WILLY BRANDT02M10560, rue Wiertz / Wiertzstraat 60B-1047 Bruxelles/Brussel.Telephone\n. \n. \n.0032 2 28 45740.Fax\n. \n. \n.0032 2 28 49740.Strasbourg.Parlement européenBât. WINSTON CHURCHILLM020541, avenue du Président Robert SchumanCS 91024F-67070 Strasbourg Cedex.Telephone\n. \n. \n.0033 3 88 1 75740.Fax\n. \n. \n.0033 3 88 1 79740.MEPs.Political groups.Group of the European People's Party (Christian Democrats).Group of the Progressive Alliance of Socialists and Democrats in the European Parliament.Renew Europe Group.Group of the Greens/European Free Alliance.European Conservatives and Reformists Group.Identity and Democracy Group.The Left group in the European Parliament - GUE/NGL.Non-attached Members.See also.Visits.Live sessions.Legislative Observatory.The President of Parliament.European Parliament.News.MEPs.About Parliament.Plenary.Committees.Delegations.Contact.Sitemap.Legal notice.Privacy policy.Accessibility
        """,
            {
                "name": "Salima YENBOU",
                "affiliation": "Renew Europe Group",
                "committees_populated": True,
                "activities_populated": True,
            },
        ),
        (
            "",
            {
                "name": "",
                "affiliation": "",
                "committees_populated": False,
                "activities_populated": False,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_parse_mep_data_various_scenarios(
    page_content, expected_output, mep_controller: MEPController
):
    # Call the function and get the output
    output = await mep_controller.parse_mep_data(page_content)

    # Assert that the output matches the expected output
    assert output["name"] == expected_output["name"]
    assert output["affiliation"] == expected_output["affiliation"]
    assert bool(output["committees"]) == expected_output["committees_populated"]
    assert bool(output["activities"]) == expected_output["activities_populated"]


# Integration Test
@pytest.mark.asyncio
async def test_integration_parse_mep_data(mep_controller: MEPController):
    # Sample input simulating a user query

    # Call the function and get the output
    parsed_data = await mep_controller.parse_mep_data("overridden", mep_extract_controller)  # type: ignore

    # Assert that the parsed data contains the expected information
    assert parsed_data["name"] == "Salima YENBOU"
    assert parsed_data["affiliation"] == "Renew Europe Group"
    # Additional assertions for committees, activities, etc.
