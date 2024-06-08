import subprocess
import sys


def run_pytest():
    subprocess.run(['pytest', '--cov=src', '--cov-report=xml:coverage/coverage.xml'], check=True)
    subprocess.run(['pytest', '--junitxml=test-reports/report.xml'], check=True)


def transform_report():
    subprocess.run(
        ['python3', 'transform_pytest_report.py', 'test-reports/report.xml', 'test-reports/astronuts_report.xml'],
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
