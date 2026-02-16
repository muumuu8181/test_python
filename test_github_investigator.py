import unittest
from unittest.mock import patch, MagicMock
import json
import io
import sys
import github_investigator

class TestGithubInvestigator(unittest.TestCase):

    def setUp(self):
        # Sample response data
        self.sample_data = {
            "items": [
                {
                    "language": "Python",
                    "stargazers_count": 50,
                    "topics": ["python", "search"]
                },
                {
                    "language": "JavaScript",
                    "stargazers_count": 500,
                    "topics": ["javascript", "web"]
                },
                {
                    "language": "Python",
                    "stargazers_count": 2000,
                    "topics": ["python", "data-science"]
                },
                {
                    "language": None,
                    "stargazers_count": 15000,
                    "topics": []
                }
            ]
        }

    @patch('urllib.request.urlopen')
    def test_search_repositories_and(self, mock_urlopen):
        # Mock response
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(self.sample_data).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        # Call function
        results = github_investigator.search_repositories(['test', 'query'], use_or=False)

        # Verify URL construction
        args, _ = mock_urlopen.call_args
        req = args[0]
        self.assertIn('q=test+query', req.full_url)
        self.assertEqual(results, self.sample_data['items'])

    @patch('urllib.request.urlopen')
    def test_search_repositories_or(self, mock_urlopen):
        # Mock response
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(self.sample_data).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        # Call function
        results = github_investigator.search_repositories(['test', 'query'], use_or=True)

        # Verify URL construction for OR
        args, _ = mock_urlopen.call_args
        req = args[0]
        self.assertIn('q=test+OR+query', req.full_url)
        self.assertEqual(results, self.sample_data['items'])

    def test_classify_results(self):
        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        github_investigator.classify_results(self.sample_data['items'])

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Check language classification
        self.assertIn("Python: 2", output)
        self.assertIn("JavaScript: 1", output)
        self.assertIn("Unknown: 1", output)

        # Check stars classification
        self.assertIn("< 100: 1", output)        # 50
        self.assertIn("100 - 1000: 1", output)   # 500
        self.assertIn("1000 - 10000: 1", output) # 2000
        self.assertIn("> 10000: 1", output)      # 15000

        # Check topics
        self.assertIn("python: 2", output)
        self.assertIn("web: 1", output)

if __name__ == '__main__':
    unittest.main()
