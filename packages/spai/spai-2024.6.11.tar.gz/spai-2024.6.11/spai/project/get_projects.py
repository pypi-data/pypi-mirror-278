from ..repos import APIRepo


def get_projects(user):
    repo = APIRepo()
    projects = repo.retrieve_projects(user)
    return [project["name"] for project in projects]
