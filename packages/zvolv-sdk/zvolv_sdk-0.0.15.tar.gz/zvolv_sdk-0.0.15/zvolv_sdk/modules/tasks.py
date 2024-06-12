import requests

from elasticsearch_dsl import Search as ESearch
from ..models.task import Task

class Tasks:
    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        self.workspace_instance = None
    
    def get(self, id):
        """Get form details from id"""
        url = f"{self.base_url}/api/v1/tasks/{id}"
        response = self.session.get(url)
        if response.status_code == 200:
            resp = response.json()
            if resp.get('error') == False and resp['data']['elements']:
                return Task(**resp['data']['elements'][0])
            else:
                print("Form get Failed")
                print(response.json())

        return response.json()
    
    def search(self, searchObj: ESearch):
        """Search tasks"""

        # Accept only elasticsearch-dsl Search object as searchObj
        if not isinstance(searchObj, ESearch):
            raise ValueError("searchObj field should be an instance of elasticsearch-dsl Search object")

        query = searchObj.to_dict()
        url = f"{self.base_url}/api/v1/analytics/search"
        response = self.session.post(url, json={'isTask': True, 'query': query})
        if response.status_code == 200:
            resp = response.json()
            if resp.get('error') == False and resp['data']['elements']:
                return resp['data']
            else:
                print("Form search Failed")
                print(response.json())

        return response.json()
    
    def put(self, task: Task):
        """Update existing task"""
        # task should be a valid Task model
        if not isinstance(task, Task):
            raise ValueError("task field should be an instance of Task model")
        # id or uuid field is required in the task model to update the task
        if not task.id and not task.uuid:
            raise ValueError("id or uuid field is required to update the task")
        url = f"{self.base_url}/api/v1/tasks"
        print(task.model_dump(exclude_none=True, exclude_unset=True))
        response = self.session.put(url, json=task.model_dump(exclude_none=True, exclude_unset=True))
        if response.status_code == 200:
            resp = response.json()
            if resp.get('error') == False:
                return resp
            else:
                print("Form put Failed")
                print(response.json())

        return response.json()
    
    def post(self, task: Task):
        """Create a new task"""
        if not isinstance(task, Task):
            raise ValueError("task field should be an instance of Task model")
        url = f"{self.base_url}/api/v1/tasks"
        response = self.session.post(url, json=task.model_dump(exclude_none=True, exclude_unset=True))
        if response.status_code == 200:
            resp = response.json()
            if resp.get('error') == False:
                return resp
            else:
                print("Form post Failed")
                print(response.json())

        return response.json()