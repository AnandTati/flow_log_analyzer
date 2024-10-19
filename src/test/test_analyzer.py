from collections import defaultdict
import os
import sys
sys.path.insert(0, os.getcwd() + '/src')

import unittest

from log_parser import LogParser


class TestLogParserMethods(unittest.TestCase):

    def setUp(self):
        self.valid_lookup_file_name = os.path.join(os.getcwd(), './src/test/test_lookup_valid.csv')
        self.empty_lookup_file_name = os.path.join(os.getcwd(), './src/test/test_lookup_empty.csv')
        self.valid_protocol_map_file_name = os.path.join(os.getcwd(), './src/test/test_protocol_valid.csv')
        self.partial_protocol_map_file_name = os.path.join(os.getcwd(), './src/test/test_protocol_partial.csv')

    def test_analyzer_throw_on_lookup_map(self):
        ''' Should throw when lookup map file is missing '''
        with self.assertRaises(FileNotFoundError) as fnfe:
            flow_log_file_name = os.path.join(os.getcwd(), './src/test/test_flow_empty.log')
            LogParser.analyze(flow_log_file_name, 'invalid_lookup_file_name', self.valid_protocol_map_file_name)
        
        self.assertEqual(str(fnfe.exception), 'Lookup map file missing')
    
    def test_analyzer_throw_on_protocol_map(self):
        ''' Should throw when protocol map file is missing '''
        with self.assertRaises(FileNotFoundError) as fnfe:
            flow_log_file_name = os.path.join(os.getcwd(), './src/test/test_flow_empty.log')
            LogParser.analyze(flow_log_file_name, self.valid_lookup_file_name, 'invalid_protocol_map_file_name')
        
        self.assertEqual(str(fnfe.exception), 'Protocol map file missing')

    def test_analyzer_for_partial_protocol_map(self):
        ''' Should return correct count when protocol map file is partial '''
        flow_log_file_name = os.path.join(os.getcwd(), './src/test/test_flow_invalid_protocol.log')
        tag_count_map, port_count_map = LogParser.analyze(flow_log_file_name, self.valid_lookup_file_name, self.valid_protocol_map_file_name)
        
        expected_tag_count_map = {'INVALID_PROTOCOL': 1, 'sv_P2': 1, 'sv_P1': 2, 'email': 2, 'Untagged': 8}
        self.assertDictEqual(tag_count_map, expected_tag_count_map)

        expected_port_count_map = {'143': {'INVALID_PROTOCOL': 1}, '443': {'tcp': 1}, '23': {'tcp': 1}, '25': {'tcp': 1}, '110': {'tcp': 1}, '993': {'tcp': 1}}
        self.assertDictEqual(port_count_map, expected_port_count_map)
    
    def test_analyze_empty_flow_log(self):
        ''' Should not fail when flow log file is empty and return empty responses '''
        flow_log_file_name = os.path.join(os.getcwd(), './src/test/test_flow_empty.log')
        tag_count_map, port_count_map = LogParser.analyze(flow_log_file_name, self.valid_lookup_file_name, self.valid_protocol_map_file_name)

        expected_tag_count_map = defaultdict(int)
        self.assertDictEqual(tag_count_map, expected_tag_count_map)

        expected_port_count_map = defaultdict()
        self.assertDictEqual(port_count_map, expected_port_count_map)

    def test_analyze(self):
        ''' Should return correct responses for valid flow log file '''
        flow_log_file_name = os.path.join(os.getcwd(), './src/test/test_flow_valid.log')
        tag_count_map, port_count_map = LogParser.analyze(flow_log_file_name, self.valid_lookup_file_name, self.valid_protocol_map_file_name)

        expected_tag_count_map = {'sv_P2': 1, 'sv_P1': 2, 'email': 3, 'Untagged': 8}
        self.assertDictEqual(tag_count_map, expected_tag_count_map)

        expected_port_count_map = {'443': {'tcp': 1}, '23': {'tcp': 1}, '25': {'tcp': 1}, '110': {'tcp': 1}, '993': {'tcp': 1}, '143': {'tcp': 1}}
        self.assertDictEqual(port_count_map, expected_port_count_map)


if __name__ == '__main__':
    unittest.main()