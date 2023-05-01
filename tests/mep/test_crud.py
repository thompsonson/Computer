import pytest
from models.sql.mep import MEP, Committee, Activity
from models.pydantic.mep import MEPIn, MEPOut, CommitteeIn, ActivityIn
from utils.DBAdapter import DBAdapter
from controllers.mep import MEPController

# Create a test database adapter (replace with your test database configuration)
test_db_adapter = DBAdapter()

# Create an MEPController instance for testing
mep_controller = MEPController(db_adapter=test_db_adapter)


def test_mep_crud_operations():
    # Test create_mep
    mep_data = MEPIn(
        name="John Doe", affiliation="Renew Europe Group", involvement="AI Legislation"
    )
    created_mep = mep_controller.create_mep(mep_data)
    assert created_mep.name == "John Doe"

    # Test get_mep
    retrieved_mep = mep_controller.get_mep(created_mep.id)
    assert retrieved_mep.id == created_mep.id
    assert retrieved_mep.name == "John Doe"

    # Test update_mep
    updated_data = MEPIn(
        name="Johnathan Doe",
        affiliation="Renew Europe Group",
        involvement="AI Legislation",
    )
    updated_mep = mep_controller.update_mep(created_mep.id, updated_data)
    assert updated_mep.name == "Johnathan Doe"

    # Test delete_mep
    mep_controller.delete_mep(created_mep.id)
    with pytest.raises(Exception):
        mep_controller.get_mep(created_mep.id)


def test_search_meps():
    # Create test MEPs
    mep_data_1 = MEPIn(
        name="Alice Smith",
        affiliation="Renew Europe Group",
        involvement="AI Legislation",
    )
    mep_data_2 = MEPIn(
        name="Bob Johnson",
        affiliation="Progressive Alliance",
        involvement="Foreign Affairs",
    )
    mep_controller.create_mep(mep_data_1)
    mep_controller.create_mep(mep_data_2)

    # Test search_meps_by_name
    search_results = mep_controller.search_meps_by_name("Alice")
    assert len(search_results) == 1
    assert search_results[0].name == "Alice Smith"

    # Test search_meps_by_affiliation
    search_results = mep_controller.search_meps_by_affiliation("Renew Europe Group")
    assert len(search_results) == 1
    assert search_results[0].affiliation == "Renew Europe Group"

    # Test search_meps_by_involvement
    search_results = mep_controller.search_meps_by_involvement("AI Legislation")
    assert len(search_results) == 1
    assert search_results[0].involvement == "AI Legislation"


# Clean up test MEPs after testing
def teardown_module():
    test_db_adapter.unmanaged_session().query(MEP).delete()
