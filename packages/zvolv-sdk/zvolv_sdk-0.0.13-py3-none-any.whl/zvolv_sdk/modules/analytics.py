import requests

class Analytics:
    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
    
    def search(self, form_id, query):
        """Fetch workspace details from domain."""
        url = f"{self.base_url}/api/v1/analytics/search"
        response = self.session.post(url, json={'formId': form_id, 'query': query})
        if response.status_code == 200:
            resp = response.json()
            if resp.get('error') == False:
                print("search Success")
                return resp['data']
            else:
                print("search Failed")
                print(response.json())

        return response.json()