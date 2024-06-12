import requests

class SharedVariableClient:
    def __init__(self, base_url="http://localhost:5000/"):
        self.base_url = base_url

    def get_variable(self, name):
        try:
            response = requests.get(self.base_url, params={'name': name}, timeout=5)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error getting variable: {e}")
            return None

    def set_variable(self, name, value):
        try:
            data = f"{name}={value}"
            response = requests.post(self.base_url, data=data, timeout=5)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error setting variable: {e}")

    def delete_variable(self, name):
        try:
            response = requests.delete(self.base_url, params={'name': name}, timeout=5)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error deleting variable: {e}")

    def change_port(self, port):
        """Change the port used by the client.

        Args:
            port (int): The new port number.

        Returns:
            None
        """
        self.base_url = f"http://localhost:{port}/"
