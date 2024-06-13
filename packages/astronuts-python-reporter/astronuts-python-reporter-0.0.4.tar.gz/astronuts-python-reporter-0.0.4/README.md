# Astronuts Python Reporter

Astronuts Reporter is a powerful tool that generates test reports. It's designed to be easy to use.

## Installation

To install Astronuts Reporter, open your terminal and run the following command:

### Using Pip
```bash
pip install astronuts-python-reporter
```



This command installs Astronuts Reporter as a development dependency in your project.

## Usage

To generate a test report, run the following command in your terminal:

```bash
astronuts-generate
```

This command tells Astronuts Reporter to start generating test reports.

## Integration with Build Scripts

You can also integrate Astronuts Reporter into your build scripts for automatic report generation. 
This can be particularly useful in continuous integration (CI) environments where tests are run automatically.

Add Astronuts Reporter to your requirements.txt file:
```bash
astronuts-python-reporter
```
Then, you can install this dependency in your workflow file (e.g., .yml):
```bash
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
    - name: Generate reports
      run: |
       astronuts-generate
```

In this example, the pytest command runs the tests and generates a JUnit XML report. Astronuts Reporter then uses this report to generate a test report. Whenever your workflow runs the command astronuts-generate, Astronuts Reporter will automatically generate a test report.

### Please note that this library is to be used in conjunction with the Astronuts code quality action. You can download the app from the [Github](https://github.com/marketplace/actions/astronuts-code-quality-action).