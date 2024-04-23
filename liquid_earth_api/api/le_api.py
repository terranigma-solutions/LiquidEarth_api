from typing import Union, Optional
import subsurface
from . import utils_api
from ..data.schemas import AddDataPostData, AddNewSpacePostData
from ..modules.rest_client import rest_interface
from ..modules.blob_client import blob_interface


def upload_mesh_to_existing_space(space_name: str, data: subsurface.UnstructuredData, file_name: str,
                                  token: str, grab_link: bool = True) -> Union[bool, dict]:
    # * grab space
    available_projects = get_available_projects(token)
    # ? which type is actually returned here?a
    found_project = utils_api.find_space_item(
        all_projects=available_projects,
        space_name=space_name
    )

    return _upload_mesh_common(data, file_name, found_project, grab_link, token)


def upload_mesh_to_new_space(space_name: str, data: subsurface.UnstructuredData,
                             file_name: str, token: str, grab_link: bool = True) -> Union[bool, dict]:
    found_project = post_create_space(
        AddNewSpacePostData(spaceName=space_name), token)

    return _upload_mesh_common(data, file_name, found_project, grab_link, token)


def get_deep_link(post_data: AddDataPostData, token: str):
    response = rest_interface.get_deep_link(post_data, token)
    return response


# TODO: ? Can we cache this easily?
def get_available_projects(token: str):
    return rest_interface.get_available_projects(token)


def post_create_space(add_new_space: AddNewSpacePostData, token: str) -> dict:
    return rest_interface.post_create_space(add_new_space, token)


def post_add_data_to_space(unstructured_data: subsurface.UnstructuredData, post_data: AddDataPostData, token: str):
    response: dict = rest_interface.post_add_data_to_space(post_data, token)
    uploading_files_response = blob_interface.push_unstructured_data(
        unstructured_data=unstructured_data,
        sas_dict=response
    )
    return uploading_files_response


def _upload_mesh_common(data, file_name, found_project, grab_link, token):
    # * upload data
    post_data = AddDataPostData(
        spaceId=found_project["spaceId"],
        ownerId=found_project["ownerId"],
        dataType="static_mesh",
        fileName=file_name
    )
    post_add_data_to_space(
        unstructured_data=data,
        post_data=post_data,
        token=token
    )
    response = True
    # * Grab link
    if grab_link:
        response = get_deep_link(post_data, token)
    return response
