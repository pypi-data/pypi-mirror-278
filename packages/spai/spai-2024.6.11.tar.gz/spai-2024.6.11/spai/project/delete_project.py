from ..repos import APIRepo

from .get_project_by_name import get_project_by_name


def delete_project(user, project):
    repo = APIRepo()
    project = get_project_by_name(user, project)
    data, error = repo.delete_project(user, project["id"])
    if error:
        raise Exception("Something went wrong.\n" + error)
    return data
