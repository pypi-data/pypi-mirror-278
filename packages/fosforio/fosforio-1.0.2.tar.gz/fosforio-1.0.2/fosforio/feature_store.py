import os
import requests
import tempfile
import shutil

class FeastFeatureStore:
    def get_feature_store(self, feature_store_name, project_id):
        try:
            from feast import FeatureStore
            headers = {
                "accept": "application/json",
                "X-Project-Id": project_id,
                'X-Auth-Userid': os.getenv("userId"),
                'X-Auth-Username': os.getenv("userId"),
                'X-Auth-Email': os.getenv("userId"),
            }
            base_url = "http://refract-common-service:5000/refract/common/api"
            url = f"{base_url}/v1/get_feature_store?feature_store_name={feature_store_name}"
            response = requests.get(url=url, headers=headers, verify=False)
            if response.status_code == 403:
                final_dict = response.json()
                error_message = final_dict.get('error', 'Authorization error')
                raise AuthorizationException(error_message)

            temp_dir = tempfile.mkdtemp()
            yaml_path = os.path.join(temp_dir, "feature_store.yaml")
            if response.status_code == 200:
                with open(yaml_path, 'wb') as f:
                    f.write(response.content)
                store = FeatureStore(repo_path=temp_dir)
                shutil.rmtree(temp_dir, ignore_errors=True)
                return store

        except Exception as e:
            shutil.rmtree(temp_dir, ignore_errors=True)
            print(f"Error: {e}")


class AuthorizationException(Exception):
    def __init__(self, message="Authorization error"):
        self.message = message
        super().__init__(self.message)
