import requests

class SharedVariableClient:
    """
    A client for managing shared variables through a HTTP server.

    Args:
        base_url (str): The base URL of the server. Defaults to "http://localhost:5000/".

    Methods:
        get_variable(name): Retrieves the value of the specified variable.
        set_variable(name, value): Sets or adds a variable.
        delete_variable(name): Deletes the specified variable.
        change_port(port): Changes the port used by the client.
    """
    
    def __init__(self, base_url="http://localhost:5000/"):
        self.base_url = base_url

    def get_variable(self, name):
        """Retrieve the value of the specified variable.

        Args:
            name (str): The name of the variable.

        Returns:
            str: The value of the variable or an error message.
        """
        try:
            response = requests.get(self.base_url, params={'name': name})
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            return f"Error: {e}"

    def set_variable(self, name, value):
        """Set or add a variable.

        Args:
            name (str): The name of the variable.
            value (str): The value of the variable.

        Returns:
            str: Success message or an error message.
        """
        try:
            data = f"{name}={value}"
            response = requests.post(self.base_url, data=data)
            response.raise_for_status()
            return "Variable set successfully."
        except requests.RequestException as e:
            return f"Error: {e}"

    def delete_variable(self, name):
        """Delete a specific variable.

        Args:
            name (str): The name of the variable to delete.

        Returns:
            str: Success message or an error message.
        """
        try:
            response = requests.delete(self.base_url, params={'name': name})
            response.raise_for_status()
            return "Variable deleted successfully."
        except requests.RequestException as e:
            return f"Error: {e}"

    def change_port(self, port):
        """Change the port used by the client.

        Args:
            port (int): The new port number.

        Returns:
            None
        """
        self.base_url = f"http://localhost:{port}/"
