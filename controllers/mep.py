from typing import List, Dict
from bs4 import BeautifulSoup
import requests

from langchain.document_loaders import UnstructuredURLLoader

from controllers.prompts.mep_extract import MEPExtractController

from models.sql.mep import MEP, Committee, Activity
from models.pydantic.mep import MEPIn, MEPOut, CommitteeIn, ActivityIn
from utils.DBAdapter import DBAdapter


class MEPController:
    def __init__(self, db_adapter: DBAdapter):
        self.db_adapter = db_adapter

    def get_mep(self, mep_id: int) -> MEPOut:
        """
        Get a MEP by ID.

        Args:
            mep_id (int): The ID of the MEP to retrieve.

        Returns:
            MEPOut: The MEP data.
        """
        session = self.db_adapter.unmanaged_session()
        try:
            mep = session.query(MEP).filter(MEP.id == mep_id).one()
            return MEPOut.from_orm(mep)
        finally:
            session.close()

    def create_mep(self, mep_data: MEPIn) -> MEPOut:
        """
        Create a new MEP.

        Args:
            mep_data (MEPIn): The MEP data to create.

        Returns:
            MEPOut: The created MEP data.
        """
        session = self.db_adapter.unmanaged_session()
        try:
            mep = MEP(**mep_data.dict())
            session.add(mep)
            session.commit()
            session.refresh(mep)
            return MEPOut.from_orm(mep)
        finally:
            session.close()

    def update_mep(self, mep_id: int, mep_data: MEPIn) -> MEPOut:
        """
        Update an existing MEP by ID.

        Args:
            mep_id (int): The ID of the MEP to update.
            mep_data (MEPIn): The new MEP data.

        Returns:
            MEPOut: The updated MEP data.
        """
        session = self.db_adapter.unmanaged_session()
        try:
            mep = session.query(MEP).filter(MEP.id == mep_id).one()
            for key, value in mep_data.dict().items():
                setattr(mep, key, value)
            session.commit()
            return MEPOut.from_orm(mep)
        finally:
            session.close()

    def delete_mep(self, mep_id: int) -> None:
        """
        Delete a MEP by ID.

        Args:
            mep_id (int): The ID of the MEP to delete.
        """
        session = self.db_adapter.unmanaged_session()
        try:
            mep = session.query(MEP).filter(MEP.id == mep_id).one()
            session.delete(mep)
            session.commit()
        finally:
            session.close()

    def create_committee(self, committee: CommitteeIn) -> Committee:
        """
        Create a new committee.

        Args:
            committee (CommitteeIn): The committee data to create.

        Returns:
            Committee: The created committee.
        """
        with self.db_adapter.unmanaged_session() as session:
            new_committee = Committee(name=committee.name)
            session.add(new_committee)
            session.commit()
            session.refresh(new_committee)
        return new_committee

    def create_activity(self, activity: ActivityIn) -> Activity:
        """
        Create a new activity.

        Args:
            activity (ActivityIn): The activity data to create.

        Returns:
            Activity: The created activity.
        """
        with self.db_adapter.unmanaged_session() as session:
            new_activity = Activity(description=activity.description)
            session.add(new_activity)
            session.commit()
            session.refresh(new_activity)
        return new_activity

    def _extract_member_urls(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch the URL: {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        member_list = soup.find("div", {"class": "erpl_member-list"})

        if not member_list:
            return []

        member_urls = []

        for member in member_list.find_all("a", {"class": "erpl_member-list-item-content"}):  # type: ignore
            member_url = member["href"]
            member_urls.append(member_url)

        return member_urls

    async def parse_mep_data(
        self, page_content: str, mep_extract_controller=None
    ) -> Dict[str, List[str]]:
        """
        Parses the page content of a Member of the European Parliament (MEP) to extract relevant information.

        The function creates an instance of the MEPExtractController with the provided page content as the message.
        It then uses the MEPExtractController to process the page content and extract information such as the MEP's
        name, affiliation, committees, and activities.

        Args:
            page_content (str): The content of the MEP's page, provided as a string.

        Returns:
            Dict[str, List[str]]: A dictionary containing the extracted information, with keys such as
            "name", "affiliation", "committees", and "activities", and corresponding values as lists of strings.
        """
        if mep_extract_controller is None:
            # Create an instance of MEPExtractController with the page_content as the message
            mep_extract_controller = MEPExtractController(message=page_content)

        # Use the MEPExtractController to process the page content and obtain the parsed data
        parsed_data = await mep_extract_controller.process_message()  # type: ignore

        # Extract the relevant fields from the parsed data
        result = {
            "name": parsed_data.name,  # type: ignore
            "affiliation": parsed_data.affiliation,  # type: ignore
            "committees": [committee.name for committee in parsed_data.committees],  # type: ignore
            "activities": [activity.description for activity in parsed_data.activities],  # type: ignore
        }

        return result

    def fetch_and_store_meps(self):
        """
        Fetches MEPs data from the web, parses it, and stores it in the database.
        """
        url = "https://www.europarl.europa.eu/meps/en/search/advanced?name=&countryCode=FR"
        member_urls = self._extract_member_urls(url)

        loader = UnstructuredURLLoader(urls=member_urls)
        data = loader.load()

        # remove unwanted text
        social_media = [
            "Facebook",
            "Twitter",
            "Flickr",
            "LinkedIn",
            "YouTube",
            "Instagram",
            "Pinterest",
            "Snapchat",
            "Reddit",
        ]

        for entry in data:
            entry.page_content = entry.page_content.replace("\t", ".")
            entry.page_content = entry.page_content.replace("\n\n", ".")
            entry.page_content = entry.page_content.replace("\r\n", ".")
            entry.page_content = entry.page_content.replace(".\n", ".")
            for x in range(1, 11):
                entry.page_content = entry.page_content.replace(".\n", ".")
                entry.page_content = entry.page_content.replace("  ", " ")
                entry.page_content = entry.page_content.replace("..", ".")
            for social in social_media:
                entry.page_content = entry.page_content.replace(
                    f"Check out Parliament on {social}.", ""
                )
                entry.page_content = entry.page_content.replace(
                    f"Share this page on {social}.", ""
                )
            entry.page_content = entry.page_content.replace(
                "Sign up for email updates.", ""
            )
            entry.page_content = entry.page_content.replace(
                f"Subscribe to the RSS feed.", ""
            )
            entry.page_content = entry.page_content.replace(f"Share this page:.", "")

        for document in data:
            parsed_data = self.parse_mep_data(document.page_content)  # type: ignore
            mep_in = MEPIn(
                name=parsed_data["name"],  # type: ignore
                affiliation=parsed_data["affiliation"],  # type: ignore
                source_url=document.metadata["source"],
            )
            mep = self.create_mep(mep_data=mep_in)

            for committee_name in parsed_data["committees"]:  # type: ignore
                committee_in = CommitteeIn(name=committee_name)
                committee = self.create_committee(committee=committee_in)

            for activity_description in parsed_data["activities"]:  # type: ignore
                activity_in = ActivityIn(description=activity_description)
                activity = self.create_activity(activity=activity_in)

    def search_meps(self, query: str) -> List[MEPOut]:
        """
        Searches for MEPs based on a query.

        Args:
            query: A search query to find MEPs.

        Returns:
            A list of MEPOut instances that match the search query.
        """
        raise NotImplementedError

    def search_meps_by_name(self, name: str) -> List[MEPOut]:
        """Search for MEPs by name."""
        session = self.db_adapter.unmanaged_session()
        try:
            meps = session.query(MEP).filter(MEP.name.ilike(f"%{name}%")).all()
            return [MEPOut.from_orm(mep) for mep in meps]
        finally:
            session.close()

    def search_meps_by_affiliation(self, affiliation: str) -> List[MEPOut]:
        """Search for MEPs by political affiliation."""
        session = self.db_adapter.unmanaged_session()
        try:
            meps = (
                session.query(MEP)
                .filter(MEP.affiliation.ilike(f"%{affiliation}%"))
                .all()
            )
            return [MEPOut.from_orm(mep) for mep in meps]
        finally:
            session.close()

    def search_meps_by_involvement(self, involvement: str) -> List[MEPOut]:
        """Search for MEPs by involvement in specific topics."""
        session = self.db_adapter.unmanaged_session()
        try:
            meps = (
                session.query(MEP)
                .filter(MEP.involvement.ilike(f"%{involvement}%"))
                .all()
            )
            return [MEPOut.from_orm(mep) for mep in meps]
        finally:
            session.close()
