from unittest import TestCase
from fcoder import CoderClient

coder_server_auth_token = "241b2687-e3f2-43b5-826b-cb91e8be6b08"

class TestCoderClient(TestCase):
    def test_code_interpreter(self):
        client = CoderClient(
            server_host="127.0.0.1",
            server_port=8888,
            auth_token=coder_server_auth_token
        )
        result = client.code_interpreter("print('hello')")
        self.assertIn(
            {'text/plain': 'hello\n'},
            result.output
        )

