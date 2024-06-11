import json
from pathlib import Path
from uuid import uuid4

import pytest
from pydantic.dataclasses import dataclass as validating_dataclass

from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.models.graphql import RecipeRunResponse
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks.mixin.globus import GlobusTransferItem
from dkist_processing_common.tasks.trial_output_data import TransferTrialDataBase
from dkist_processing_common.tests.conftest import FakeGQLClient


@pytest.fixture
def destination_bucket() -> str:
    return "crazy"


@pytest.fixture
def recipe_run_configuration(custom_root_name, custom_dir_name, destination_bucket):
    class GQLClientWithConfiguration(FakeGQLClient):
        def execute_gql_query(self, **kwargs):
            response = super().execute_gql_query(**kwargs)
            if isinstance(response, list):
                if isinstance(response[0], RecipeRunResponse):
                    response[0].configuration = json.dumps(
                        {
                            "trial_root_directory_name": custom_root_name,
                            "trial_directory_name": custom_dir_name,
                            "destination_bucket": destination_bucket,
                        }
                    )
            return response

    return GQLClientWithConfiguration


@pytest.fixture
def dummy_globus_transfer_item() -> GlobusTransferItem:
    return GlobusTransferItem(source_path="foo", destination_path="bar", recursive=True)


@pytest.fixture
def trial_output_task(dummy_globus_transfer_item) -> type[TransferTrialDataBase]:
    class TransferTrialData(TransferTrialDataBase):
        def build_transfer_list(self) -> list[GlobusTransferItem]:

            transfer_list = [dummy_globus_transfer_item]
            return transfer_list

        @property
        def intermediate_task_names(self) -> list[str]:
            return ["FOO"]

    return TransferTrialData


@pytest.fixture
def basic_trial_output_task(
    recipe_run_id, recipe_run_configuration, trial_output_task, tmp_path, mocker
):
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient",
        new=recipe_run_configuration,
    )
    proposal_id = "test_proposal_id"
    with trial_output_task(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        task.scratch = WorkflowFileSystem(
            recipe_run_id=recipe_run_id,
            scratch_base_path=tmp_path,
        )
        task.constants._update({"PROPOSAL_ID": proposal_id})
        yield task, proposal_id
        task._purge()


@validating_dataclass
class OutputFileObjects:
    """File objects returned by complete_trial_output_task"""

    debug_file_obj: bytes
    intermediate_keep_file_obj: bytes
    intermediate_discard_file_obj: bytes
    dataset_inv_file_obj: bytes
    asdf_file_obj: bytes
    quality_data_obj: bytes
    quality_report_file_obj: bytes
    movie_file_obj: bytes


@pytest.fixture
def complete_trial_output_task(
    recipe_run_id, recipe_run_configuration, trial_output_task, tmp_path, mocker
) -> tuple[TransferTrialDataBase, str, OutputFileObjects]:
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient",
        new=recipe_run_configuration,
    )
    proposal_id = "test_proposal_id"
    with trial_output_task(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        task.scratch = WorkflowFileSystem(
            recipe_run_id=recipe_run_id,
            scratch_base_path=tmp_path,
        )
        task.constants._update({"PROPOSAL_ID": proposal_id})

        # Write a debug frame
        debug_file_obj = uuid4().hex.encode("utf8")
        task.write(debug_file_obj, relative_path="debug.ext", tags=[Tag.debug(), Tag.frame()])

        # Write a dataset inventory file
        dataset_inv_file_obj = uuid4().hex.encode("utf8")
        task.write(
            dataset_inv_file_obj,
            relative_path="dataset_inv.ext",
            tags=[Tag.output(), Tag.dataset_inventory()],
        )

        # Write an asdf file
        asdf_file_obj = uuid4().hex.encode("utf8")
        task.write(asdf_file_obj, relative_path="asdf.ext", tags=[Tag.output(), Tag.asdf()])

        # Write quality data
        # quality data is not tagged as OUTPUT
        quality_data_obj = uuid4().hex.encode("utf8")
        task.write(
            quality_data_obj,
            relative_path="quality_data.json",
            tags=Tag.quality_data(),
        )

        # Write a quality report file
        quality_report_file_obj = uuid4().hex.encode("utf8")
        task.write(
            quality_report_file_obj,
            relative_path="quality_report.pdf",
            tags=[Tag.output(), Tag.quality_report()],
        )

        # Write a movie file
        movie_file_obj = uuid4().hex.encode("utf8")
        task.write(movie_file_obj, relative_path="movie.mp4", tags=[Tag.output(), Tag.movie()])

        # Write an intermediate frame that we want to transfer
        intermediate_keep_file_obj = uuid4().hex.encode("utf8")
        task.write(
            intermediate_keep_file_obj,
            relative_path="intermediate.ext",
            tags=[Tag.intermediate(), Tag.frame(), Tag.task("FOO")],
        )

        # Write an intermediate frame that we don't want to transfer
        intermediate_discard_file_obj = uuid4().hex.encode("utf8")
        task.write(
            intermediate_discard_file_obj,
            relative_path="something_else.ext",
            tags=[Tag.intermediate(), Tag.frame(), Tag.task("WHO_CARES")],
        )

        output_file_objects = OutputFileObjects(
            debug_file_obj=debug_file_obj,
            intermediate_keep_file_obj=intermediate_keep_file_obj,
            intermediate_discard_file_obj=intermediate_discard_file_obj,
            dataset_inv_file_obj=dataset_inv_file_obj,
            asdf_file_obj=asdf_file_obj,
            quality_data_obj=quality_data_obj,
            quality_report_file_obj=quality_report_file_obj,
            movie_file_obj=movie_file_obj,
        )

        yield task, proposal_id, output_file_objects
        task._purge()


@pytest.mark.parametrize(
    "custom_root_name, custom_dir_name",
    [
        pytest.param("roor", "foo", id="Custom trial dir name"),
        pytest.param(None, None, id="Default trial dir name"),
    ],
)
def test_format_object_key(basic_trial_output_task, custom_root_name, custom_dir_name):
    """
    :Given: A base task made from TransferTrialDataBase
    :When: Formatting a path into an object key
    :Then: The expected object key is produced and includes a custom dir name if requested
    """
    task, proposal_id = basic_trial_output_task
    expected_root_name = custom_root_name or proposal_id
    expected_dir_name = custom_dir_name or task.constants.dataset_id
    filename = "test_filename.ext"
    path = Path(f"a/b/c/d/{filename}")
    assert task.format_object_key(path) == str(
        Path(expected_root_name, expected_dir_name, filename)
    )


@pytest.mark.parametrize(
    "custom_root_name, custom_dir_name", [pytest.param(None, None, id="Default trial dir name")]
)
def test_build_transfer_list(complete_trial_output_task, dummy_globus_transfer_item):
    """
    Given: A Task based on TransferTrialDataBase with a defined build_transfer_list
    When: Building the full transfer list
    Then: The expected transfer list is returned
    """
    task, *_ = complete_trial_output_task
    transfer_list = task.build_transfer_list()

    assert len(transfer_list) == 1
    assert transfer_list[0] == dummy_globus_transfer_item


@pytest.mark.parametrize(
    "custom_root_name, custom_dir_name", [pytest.param(None, "foo", id="Custom trial dir name")]
)
def test_build_debug_transfer_list(complete_trial_output_task, destination_bucket, custom_dir_name):
    """
    Given: A Task based on TransferTrialDataBase with a tagged DEBUG frame
    When: Building the debug transfer list
    Then: The resulting transfer list has the correct source and destination paths and references the correct frames
    """
    task, proposal_id, output_file_objects = complete_trial_output_task
    debug_file_obj = output_file_objects.debug_file_obj

    transfer_list = task.build_debug_frame_transfer_list()

    assert len(transfer_list) == 1
    transfer_item = transfer_list[0]
    assert transfer_item.source_path == task.scratch.workflow_base_path / "debug.ext"
    expected_destination = Path(
        destination_bucket, proposal_id, custom_dir_name or task.constants.dataset_id, "debug.ext"
    )
    assert transfer_item.destination_path == expected_destination
    with transfer_item.source_path.open(mode="rb") as f:
        assert debug_file_obj == f.read()


@pytest.mark.parametrize(
    "custom_root_name, custom_dir_name", [pytest.param(None, "foo", id="Custom trial dir name")]
)
def test_build_output_asdf_transfer_list(
    complete_trial_output_task, destination_bucket, custom_dir_name
):
    """
    Given: A Task based on TransferTrialDataBase with a tagged output asdf file
    When: Building the output asdf transfer list
    Then: The resulting transfer list has the correct source and destination paths and references the correct frames
    """
    task, proposal_id, output_file_objects = complete_trial_output_task
    asdf_file_obj = output_file_objects.asdf_file_obj

    transfer_list = task.build_output_asdf_transfer_list()

    assert len(transfer_list) == 1
    transfer_item = transfer_list[0]
    assert transfer_item.source_path == task.scratch.workflow_base_path / "asdf.ext"
    expected_destination = Path(
        destination_bucket, proposal_id, custom_dir_name or task.constants.dataset_id, "asdf.ext"
    )
    assert transfer_item.destination_path == expected_destination
    with transfer_item.source_path.open(mode="rb") as f:
        assert asdf_file_obj == f.read()


@pytest.mark.parametrize(
    "custom_root_name, custom_dir_name", [pytest.param(None, "foo", id="Custom trial dir name")]
)
def test_build_output_quality_data_transfer_list(
    complete_trial_output_task, destination_bucket, custom_dir_name
):
    """
    Given: A Task based on TransferTrialDataBase with tagged output quality data
    When: Building the output quality data transfer list
    Then: The resulting transfer list has the correct source and destination paths and references the correct file
    """
    task, proposal_id, output_file_objects = complete_trial_output_task
    quality_data_obj = output_file_objects.quality_data_obj

    transfer_list = task.build_output_quality_data_transfer_list()

    assert len(transfer_list) == 1
    transfer_item = transfer_list[0]
    assert transfer_item.source_path == task.scratch.workflow_base_path / "quality_data.json"
    expected_destination = Path(
        destination_bucket,
        proposal_id,
        custom_dir_name or task.constants.dataset_id,
        "quality_data.json",
    )
    assert transfer_item.destination_path == expected_destination
    with transfer_item.source_path.open(mode="rb") as f:
        assert quality_data_obj == f.read()


@pytest.mark.parametrize(
    "custom_root_name, custom_dir_name", [pytest.param(None, "foo", id="Custom trial dir name")]
)
def test_build_output_quality_report_transfer_list(
    complete_trial_output_task, destination_bucket, custom_dir_name
):
    """
    Given: A Task based on TransferTrialDataBase with a tagged output quality report file
    When: Building the output quality report transfer list
    Then: The resulting transfer list has the correct source and destination paths and references the correct file
    """
    task, proposal_id, output_file_objects = complete_trial_output_task
    quality_report_file_obj = output_file_objects.quality_report_file_obj

    transfer_list = task.build_output_quality_report_transfer_list()

    assert len(transfer_list) == 1
    transfer_item = transfer_list[0]
    assert transfer_item.source_path == task.scratch.workflow_base_path / "quality_report.pdf"
    expected_destination = Path(
        destination_bucket,
        proposal_id,
        custom_dir_name or task.constants.dataset_id,
        "quality_report.pdf",
    )
    assert transfer_item.destination_path == expected_destination
    with transfer_item.source_path.open(mode="rb") as f:
        assert quality_report_file_obj == f.read()


@pytest.mark.parametrize(
    "custom_root_name, custom_dir_name", [pytest.param(None, "foo", id="Custom trial dir name")]
)
def test_build_output_dataset_inventory_transfer_list(
    complete_trial_output_task, destination_bucket, custom_dir_name
):
    """
    Given: A Task based on TransferTrialDataBase with a tagged output dataset inventory file
    When: Building the output dataset inventory transfer list
    Then: The resulting transfer list has the correct source and destination paths and references the correct frames
    """
    task, proposal_id, output_file_objects = complete_trial_output_task
    dataset_inv_file_obj = output_file_objects.dataset_inv_file_obj

    transfer_list = task.build_output_dataset_inventory_transfer_list()

    assert len(transfer_list) == 1
    transfer_item = transfer_list[0]
    assert transfer_item.source_path == task.scratch.workflow_base_path / "dataset_inv.ext"
    expected_destination = Path(
        destination_bucket,
        proposal_id,
        custom_dir_name or task.constants.dataset_id,
        "dataset_inv.ext",
    )
    assert transfer_item.destination_path == expected_destination
    with transfer_item.source_path.open(mode="rb") as f:
        assert dataset_inv_file_obj == f.read()


@pytest.mark.parametrize(
    "custom_root_name, custom_dir_name", [pytest.param(None, "foo", id="Custom trial dir name")]
)
def test_build_output_movie_transfer_list(
    complete_trial_output_task, destination_bucket, custom_dir_name
):
    """
    Given: A Task based on TransferTrialDataBase with a tagged output movie file
    When: Building the output movie transfer list
    Then: The resulting transfer list has the correct source and destination paths and references the correct files
    """
    task, proposal_id, output_file_objects = complete_trial_output_task
    movie_file_obj = output_file_objects.movie_file_obj

    transfer_list = task.build_output_movie_transfer_list()

    assert len(transfer_list) == 1
    transfer_item = transfer_list[0]
    assert transfer_item.source_path == task.scratch.workflow_base_path / "movie.mp4"
    expected_destination = Path(
        destination_bucket, proposal_id, custom_dir_name or task.constants.dataset_id, "movie.mp4"
    )
    assert transfer_item.destination_path == expected_destination
    with transfer_item.source_path.open(mode="rb") as f:
        assert movie_file_obj == f.read()


@pytest.mark.parametrize(
    "custom_root_name, custom_dir_name", [pytest.param("root", None, id="Default trial root name")]
)
def test_build_intermediate_transfer_list(
    complete_trial_output_task, destination_bucket, custom_root_name
):
    """
    Given: A Task based on TransferTrialDataBase with tagged INTERMEDIATE frames
    When: Building the intermediate transfer list
    Then: The resulting transfer list has the correct source and destination paths and references the correct frames
    """
    task, proposal_id, output_file_objects = complete_trial_output_task
    intermediate_file_obj = output_file_objects.intermediate_keep_file_obj

    transfer_list = task.build_intermediate_frame_transfer_list()
    expected_destination_name = "intermediate.ext"
    expected_destination_path = Path(
        destination_bucket, task.format_object_key(Path(expected_destination_name))
    )

    assert len(transfer_list) == 1
    transfer_item = transfer_list[0]
    assert transfer_item.source_path == task.scratch.workflow_base_path / "intermediate.ext"
    assert transfer_item.destination_path == expected_destination_path
    with transfer_item.source_path.open(mode="rb") as f:
        assert intermediate_file_obj == f.read()


@pytest.mark.parametrize(
    "custom_root_name, custom_dir_name", [pytest.param(None, None, id="Default trial dir name")]
)
def test_build_transfer_list_from_tag_list(complete_trial_output_task, destination_bucket):
    """
    Given: A Task based on TransferTrialDataBase with tagged frames
    When: Building a transfer list from lists of tags
    Then: The transfer list is built with correct source and destination paths
    """
    task, proposal_id, output_file_objects = complete_trial_output_task
    debug_file_obj = output_file_objects.debug_file_obj
    intermediate_file_obj = output_file_objects.intermediate_keep_file_obj
    intermediate_file_obj_2 = output_file_objects.intermediate_discard_file_obj

    tag_list_1 = [Tag.frame(), Tag.task("WHO_CARES")]
    tag_list_2 = [Tag.debug()]
    tag_list_3 = [Tag.intermediate()]
    tag_list = [tag_list_1, tag_list_2, tag_list_3]

    transfer_list = task.build_transfer_list_from_tag_lists(tag_list)
    assert len(transfer_list) == 3
    sorted_transfer_list = sorted(transfer_list, key=lambda x: x.source_path.name)

    # This whole structure is nasty. I'm sorry

    # Debug frame
    transfer_item = sorted_transfer_list[0]
    expected_destination_name = "debug.ext"
    expected_destination_path = Path(
        destination_bucket, task.format_object_key(Path(expected_destination_name))
    )
    assert transfer_item.source_path == task.scratch.workflow_base_path / "debug.ext"
    assert transfer_item.destination_path == expected_destination_path
    with transfer_item.source_path.open(mode="rb") as f:
        assert debug_file_obj == f.read()

    # Intermediate frame 1
    transfer_item = sorted_transfer_list[1]
    expected_destination_name = "intermediate.ext"
    expected_destination_path = Path(
        destination_bucket, task.format_object_key(Path(expected_destination_name))
    )
    assert transfer_item.source_path == task.scratch.workflow_base_path / "intermediate.ext"
    assert transfer_item.destination_path == expected_destination_path
    with transfer_item.source_path.open(mode="rb") as f:
        assert intermediate_file_obj == f.read()

    # Intermediate frame 2
    transfer_item = sorted_transfer_list[2]
    expected_destination_name = "something_else.ext"
    expected_destination_path = Path(
        destination_bucket, task.format_object_key(Path(expected_destination_name))
    )
    assert transfer_item.source_path == task.scratch.workflow_base_path / "something_else.ext"
    assert transfer_item.destination_path == expected_destination_path
    with transfer_item.source_path.open(mode="rb") as f:
        assert intermediate_file_obj_2 == f.read()


@pytest.mark.parametrize(
    "custom_root_name, custom_dir_name", [pytest.param(None, None, id="Default trial dir name")]
)
def test_build_transfer_list_from_tag_list_single_list(
    complete_trial_output_task, destination_bucket
):
    """
    Given: A Task based on TransferTrialDataBase with tagged frames
    When: Building a transfer list from a single list of tags
    Then: The transfer list is built with correct source and destination paths
    """
    task, proposal_id, output_file_objects = complete_trial_output_task
    debug_file_obj = output_file_objects.debug_file_obj

    tag_list = [Tag.debug()]

    transfer_list = task.build_transfer_list_from_tag_lists(tag_list)

    assert len(transfer_list) == 1
    transfer_item = transfer_list[0]
    expected_destination_name = "debug.ext"
    expected_destination_path = Path(
        destination_bucket, task.format_object_key(Path(expected_destination_name))
    )
    assert transfer_item.source_path == task.scratch.workflow_base_path / "debug.ext"
    assert transfer_item.destination_path == expected_destination_path
    with transfer_item.source_path.open(mode="rb") as f:
        assert debug_file_obj == f.read()
