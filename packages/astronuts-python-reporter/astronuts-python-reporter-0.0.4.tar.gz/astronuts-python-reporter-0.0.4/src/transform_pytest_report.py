import xml.etree.ElementTree as ET
import os
import sys


def convert_classname_to_filepath(classname):
    # Split the classname by dots
    parts = classname.split('.')
    # Remove the last part (which is typically the class name)
    parts.pop()
    # Convert each part to lowercase
    parts = [part.lower() for part in parts]
    # Join the parts with slashes and append ".py"
    filepath = '/'.join(parts) + '.py'
    return filepath


def transform_report(test_input_file, test_output_file):
    try:
        tree = ET.parse(test_input_file)
        root = tree.getroot()

        current_path = os.getcwd()

        # Create the root for the new SonarQube report
        sonar_root = ET.Element('testExecutions', version='1')

        for testsuite in root.iter('testsuite'):
            for testcase in testsuite.findall('testcase'):

                classname = testcase.get('classname', '')
                name = testcase.get('name', '')
                time = testcase.get('time', '0')

                # Convert class name to file path (assuming the test module structure)
                if classname != '':
                    file_path = convert_classname_to_filepath(classname)
                else:
                    file_path = classname.replace('.', '/') + '.py'

                test_exec = ET.SubElement(sonar_root, 'file', path=f'{current_path}/{file_path}')
                test_case = ET.SubElement(test_exec, 'testCase', name=f'{classname}.{name}',
                                          duration=f'{time.split(".")[0]}')

                # Check for failure
                failure = testcase.find('failure')
                if failure is not None:
                    ET.SubElement(test_case, 'failure', message=failure.get('message', ''),
                                  stacktrace=failure.text or '')

        # Write the transformed report
        os.makedirs(os.path.dirname(test_output_file), exist_ok=True)
        with open(test_output_file, 'wb') as f:
            tree = ET.ElementTree(sonar_root)
            tree.write(f, encoding='utf-8', xml_declaration=True)

        print(f'Transformed report written to {test_output_file}')
    except Exception as e:
        print(f'Error transforming report: {e}')


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python transform_pytest_report.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    transform_report(input_file, output_file)
