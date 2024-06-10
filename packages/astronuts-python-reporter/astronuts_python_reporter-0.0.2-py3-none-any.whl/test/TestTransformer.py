import unittest

from src import transform_pytest_report


def create_sample_test_report():
    # Test report content
    test_report_content = """<?xml version="1.0" encoding="utf-8"?>
    <testsuites>
        <testsuite name="pytest" errors="0" failures="0" skipped="0" tests="2" time="0.047"
                   timestamp="2024-06-06T16:24:59.952184" hostname="Surajs-MacBook-Pro.local">
            <testcase classname="test.test_sample.TestSample" name="test_add" time="0.002"/>
            <testcase classname="test.test_sample_new" name="test_add" time="0.001"/>
        </testsuite>
    </testsuites>"""

    # Create a sample test report file
    with open('sample_test_report.xml', 'w') as f:
        f.write(test_report_content)

    # Return the path to the test report file
    return './sample_test_report.xml'


def create_sample_files():
    input_file = create_sample_test_report()

    # Create a sample output file (it can be empty)
    with open('./sample_output.xml', 'w') as f:
        pass

    # Return the paths to the input and output files
    return input_file, './sample_output.xml'


class TestTransformReport(unittest.TestCase):

    def setUp(self):
        self.input_file, self.output_file = create_sample_files()

    def test_transform_report(self):
        # Call the function with the test input and output files
        transform_pytest_report.transform_report(self.input_file, self.output_file)

        # Now, open the output file and check if it has been written correctly
        with open(self.output_file, 'r') as f:
            content = f.read()
            # Add your assertions here based on what you expect in the output file
            self.assertIn('<testExecutions version="1">', content)
