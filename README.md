# Flow Log Analyzer

The **Flow Log Analyzer** is a simple tool designed to parse network [flow log file] and analyze specific port and protocol combinations. This tool tags certain port/protocol combinations and counts the occurrences of each in the logs.

## Features

- **Port/Protocol Tagging:** Tags specific port and protocol combinations based on user-defined rules.
- **Log Counting:** Counts the number of log entries for each tagged port/protocol combination.
- **Customizable Tagging Rules:** Users can define their own port and protocol combinations for tagging.
- **Simple Reporting:** Outputs a summary report of how many times each combination was found in the log.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.8+ (Make sure you're using Python 3.12 if that's your setup)
- `pip` (Python package manager)

### Assumptions

1. Tool works with Flow log file version 2 only.
2. Following input file contents are not validated
   - [Flow log file] contents.
   - Lookup map csv file contents.
   - Protocol map file contents.
3. dstport and protocol number in flow log file are assumed to be valid numbers.
4. Protocol number out of [valid protocol]
can be handled in following ways
   1. Raise exception: This option would help in investigation during develoment.
   2. Log the error and continue: This option would allow to proceed development and investigate the issue later via log files.
   3. Capture the value as INVALID value and continue: This option is similar to prev option. In this option, the issues are immediately visible in the output and allows to continue with development and pinpoint the issue during investigation via output.
   > **NOTE**: For current implementation 3rd option is selected.

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/<username>/flow_log_analyzer.git
    cd flow_log_analyzer
    ```

2. Set up a virtual environment (optional but recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Usage

1. Place your log file in the `data/` directory, and update the path to the log file in the `log_parser.py` script inside the `main()` function.

2. Define the port/protocol combinations you want to tag in a CSV file, such as `src/data/lookup.csv`. Here’s an example format for the file:

    ```csv
    dstport,protocol,tag 
    25,tcp,sv_P1
    68,udp,sv_P2
    ```

3. Run the analyzer:

    ```bash
    python3 src/log_parser.py
    ```

4. The tool will output the count of each tagged combination. For example:

    ```
    Reading lookup and protocol map files
    Parsing Flow Log file
    Completed parsing Flow Log file
    ```

    After completion of the execution, a `/out` folder will be created in the `/root` folder and that folder will have 2 files.
    1. `tag_count.csv`
    2. `port_count.csv`

### Running Unit Tests

To ensure the functionality of the Flow Log Analyzer, unit tests have been provided. Here's how to run them:

1. Install `unittest` if not already available (though it's part of the standard library in Python):

    ```bash
    pip install unittest
    ```

2. Run the tests:

    ```bash
    python3 -m unittest src.test.test_analyzer -v
    ```

    This will run all tests from the `src/test/test_analyzer.py` file.

3. If all tests pass, you will see output like:

    ```
    ......
    ----------------------------------------------------------------------
    Ran 5 tests in 0.005s

    OK
    ```
[Flow Log File]: https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html
[valid protocol]: https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml