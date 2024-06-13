import unittest
from unittest.mock import patch, MagicMock
from ffm.embeddings import FFMEmbeddings

class TestFFMEmbeddings(unittest.TestCase):

    @patch('ffm.embeddings.base.requests.post')
    def test_embed_documents(self, mock_post):
        # Mock response from the API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"embedding": [0.1, 0.2, 0.3]},
                {"embedding": [0.4, 0.5, 0.6]}
            ]
        }
        mock_post.return_value = mock_response

        embeddings = FFMEmbeddings(base_url="http://localhost:12345", api_key="test_key")
        texts = ["This is a test.", "Another test."]
        result = embeddings.embed_documents(texts)

        self.assertEqual(result, [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])

    @patch('ffm.embeddings.base.requests.post')
    def test_embed_query(self, mock_post):
        # Mock response from the API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"embedding": [0.1, 0.2, 0.3]}
            ]
        }
        mock_post.return_value = mock_response

        embeddings = FFMEmbeddings(base_url="http://localhost:12345", api_key="test_key")
        text = "This is a test query."
        result = embeddings.embed_query(text)

        self.assertEqual(result, [0.1, 0.2, 0.3])

if __name__ == '__main__':
    unittest.main()
