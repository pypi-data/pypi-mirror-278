import subprocess
import sys
import os


def run_pytest():
    subprocess.run(['pytest', '--cov=.', '--cov-report=xml:coverage/coverage.xml'], check=True)
    subprocess.run(['pytest', '--junitxml=test-reports/report.xml'], check=True)


library_directory = os.path.dirname(os.path.abspath(__file__))
custom_file_path = os.path.join(library_directory, 'transform_pytest_report.py')


def transform_report():
    subprocess.run(
        ['python3', custom_file_path, 'test-reports/report.xml', 'test-reports/astronuts_report.xml'],
        check=True)


def main():
    try:
        run_pytest()
        transform_report()
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
