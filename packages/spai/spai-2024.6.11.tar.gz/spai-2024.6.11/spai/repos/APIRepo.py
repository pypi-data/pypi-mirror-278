import requests
import os
from rich import print
import json


class APIRepo:
    def __init__(
        self, url=os.getenv("SPAI_API_URL", "https://spai.test.earthpulse.ai/")
    ):
    # def __init__(self, url=os.getenv("SPAI_API_URL", "http://localhost:8000/")):
        self.url = url
        self.url = self.url if self.url.endswith("/") else self.url + "/"
        if not self.url.startswith("http://") and not self.url.startswith("https://"):
            raise Exception(
                "Invalid URL: " + self.url + "\nIt must start with http:// or https://"
            )

    def format_response(self, response):
        # return (data, error)
        if response.status_code == 200:
            return response.json(), None
        return None, response.json()["detail"]

    def info(self):
        return requests.get(self.url).json()

    def login(self):
        return requests.get(self.url + "auth/login")

    def token(self, code):
        return requests.get(self.url + "auth/token?code=" + code)

    def logout_url(self):
        response = requests.get(self.url + "auth/logout")
        return response.json()["logout_url"]

    def get_headers(self, user):
        return {"Authorization": "Bearer " + user["id_token"]}

    def retrieve_user(self, user):
        response = requests.get(self.url + "auth/me", headers=self.get_headers(user))
        return self.format_response(response)

    def retrieve_projects(self, user):
        return requests.get(
            self.url + "projects", headers=self.get_headers(user)
        ).json()

    def retrieve_project(self, user, project):
        response = requests.get(
            self.url + f"projects/{project}", headers=self.get_headers(user)
        )
        return self.format_response(response)

    def retrieve_project_by_name(self, user, project_name):
        response = requests.get(
            self.url + f"projects?name={project_name}", headers=self.get_headers(user)
        )
        return self.format_response(response)

    def stop_service(self, user, service_id):
        response = requests.post(
            self.url + f"stop/{service_id}",
            headers=self.get_headers(user),
        )
        if response.status_code == 200:
            return response.text
        return "Something went wrong.\n" + response.json()["detail"]

    def stop_service_by_name(self, user, project_id, service_type, service_name):
        response = requests.post(
            self.url
            + f"stop?project={project_id}&type={service_type}&name={service_name}",
            headers=self.get_headers(user),
        )
        return self.format_response(response)

    def get_logs(self, user, service_id):
        response = requests.get(
            self.url + f"logs/{service_id}",
            headers=self.get_headers(user),
        )
        if response.status_code == 200:
            return response.json()
        return "Something went wrong.\n" + response.json()["detail"]

    def delete_project(self, user, project):
        response = requests.delete(
            self.url + f"projects/{project}", headers=self.get_headers(user)
        )
        return self.format_response(response)

    def retrieve_template(self, user, template):
        return requests.get(
            self.url + f"templates?name={template}", headers=self.get_headers(user)
        )

    def deploy_template(self, user, template, variables):
        response = requests.post(
            self.url + f"deploy/template?name={template}",
            json={"variables": variables},
            headers=self.get_headers(user),
        )
        return self.format_response(response)

    def deploy_folder(self, user, zip_path, variables):
        response = requests.post(
            self.url + f"deploy",
            files={"folder": open(zip_path, "rb")},
            data={"variables": json.dumps(variables)},
            headers=self.get_headers(user),
        )
        if response.status_code == 413:
            raise Exception("Your project is too large, it can be a maximum of 100 MB.")
        return self.format_response(response)

    def retrieve_service_by_name_type_project(
        self, user, project_id, service_type, service_name
    ):
        response = requests.get(
            self.url
            + f"services?project={project_id}&type={service_type}&name={service_name}",
            headers=self.get_headers(user),
        )
        return self.format_response(response)

    def retrieve_service(self, user, service_id):
        response = requests.get(
            self.url + f"services/{service_id}",
            headers=self.get_headers(user),
        )
        return self.format_response(response)

    def create_or_retrieve_s3_bucket(self, user, project_name, storage_name):
        response = requests.get(
            self.url
            + f"services/storage/s3?project={project_name}&name={storage_name}",
            headers=self.get_headers(user),
        )
        return self.format_response(response)
