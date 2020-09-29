import unittest
import sys
import os
import json
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from git_spider_process import *


class TestSpiderProcess(unittest.TestCase):

    def test_parse_input_pipeline(self):
        """Test parsing input for git crawling"""
        test_in = 'test_input.json'
        with open(test_in) as input_json_file:
            input_json_str = input_json_file.read()
            input_json_data = json.loads(input_json_str)
            keywords, proxies, search_type = parse_input_params(input_json_data)
            self.assertIsNotNone(keywords)
            self.assertIsNotNone(proxies)
            self.assertIsNotNone(search_type)

    def test_run_crawler_unicode(self):
        """Test crawling, assert crawler returns a result"""
        result = run_crawler("git \u0394", " ", "wikis")
        self.assertIsNotNone(result)

    def test_output(self):
        """Test outputting to a file"""
        test_out = 'test.json'
        write_result_to_json('{"test": 1}', test_out)
        self.assertTrue(os.path.exists(test_out))
        os.remove(test_out)


if __name__ == '__main__':
    unittest.main()
