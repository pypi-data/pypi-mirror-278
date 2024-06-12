#!/usr/bin/python3

import sys
import argparse
import os
import subprocess
import time
from datetime import timedelta
import select

# Testing suite names
TESTING_SUITES = [
    'ENT',
    'PractRand',
    'SmallCrush',
    'Crush',
    'Alphabit',
    'Rabbit',
    'Dieharder',
    'NIST']

# Testing setting options
TESTING_SETTING_OPTIONS = {
    'Light': {TESTING_SUITES[0], TESTING_SUITES[1], TESTING_SUITES[2]},  # ENT, PractRand, TestU01 SmallCrush
    'Recommended': {TESTING_SUITES[0], TESTING_SUITES[1], TESTING_SUITES[6], TESTING_SUITES[7]},
    'All': set(TESTING_SUITES),
    'Custom': set()
}

def print_testing_settings():
    """Prints the available testing settings."""
    print("\n        T E S T I N G   S E T T I N G S")
    print("        _______________________________\n")
    for setting_num, setting_name in enumerate(TESTING_SETTING_OPTIONS.keys(), start=1):
        testing_suites = TESTING_SETTING_OPTIONS[setting_name]
        if len(testing_suites) == 0:
            print(f"    {('[' + str(setting_num) + '] ' + setting_name).ljust(20)}")
        else:
            print(f"    {('[' + str(setting_num) + '] ' + setting_name).ljust(20)} ({', '.join(suite for suite in TESTING_SETTING_OPTIONS[setting_name])})")
    print()

def print_testing_suites():
    """Prints the available testing suites."""
    print()
    print("\n        T E S T I N G   S U I T E S")
    print("        ___________________________\n")
    for num, suite in enumerate(TESTING_SUITES, start=1):
        # print the suite nums/names in two columns
        if num % 2 == 0:
            print(f"[{num}] {suite:<20}")
        else:
            print(f"    [{num}] {suite:<20}", end='')
            if num == len(TESTING_SUITES):
                print()
    print()

def handle_setting_input():
    """Handles user input for selecting a testing setting."""
    print_testing_settings()
    while True:
        try:
            # Get the selected setting from the user
            setting_num = input("   Please select testing setting (number): ")
            
            setting_num = int(setting_num) - 1
            if setting_num not in range(len(TESTING_SETTING_OPTIONS)):
                raise ValueError
            return setting_num
        except ValueError:
            print(f"   Invalid setting number. Please choose a number between 1 and {len(TESTING_SETTING_OPTIONS)} inclusive.")
        except KeyboardInterrupt:
            print("\n   Exiting the script...")
            sys.exit(0)

def handle_custom_setting_input(binary_setting=None):
    """Handles user input for custom setting binary representation."""
    # If the binary setting is provided, check if it is valid
    if binary_setting:
        if not all(char in '01' for char in binary_setting) or len(binary_setting) != len(TESTING_SUITES):
            print(f"Error: The binary setting must be a binary number with exactly {len(TESTING_SUITES)} digits (0 or 1).")
            sys.exit(1)
        return binary_setting
    else:
        # Print the available testing suites
        print_testing_suites()
        while True:
            try:
                # Get the binary input from the user
                print("   Enter a 0 or 1 to indicate whether or not the numbered statistical\n   testing suite should be applied.\n")
                print(f"    {''.join(str(i) for i in range(1, len(TESTING_SUITES) + 1))}")
                setting_input = input("    ")

                # Check if the input is a binary number with the correct number of digits
                if not all(char in '01' for char in setting_input) or len(setting_input) != len(TESTING_SUITES):
                    print(f"   Error: Please enter a binary number with exactly {len(TESTING_SUITES)} digits (0 or 1).")
                else:
                    return setting_input
            except KeyboardInterrupt:
                print("\n   Exiting the script...")
                sys.exit(0)

def handle_selected_setting(setting_index, binary_setting=None):
    """Handles the selected testing setting and returns the binary representation of the tests to run."""
    setting_name = list(TESTING_SETTING_OPTIONS.keys())[setting_index]
    # If the setting is Custom, handle the custom setting input
    if setting_name == 'Custom':
        return handle_custom_setting_input(binary_setting)
    # Else return the binary representation of the selected setting
    else:
        return ''.join('1' if suite in TESTING_SETTING_OPTIONS[setting_name] else '0' for suite in TESTING_SUITES)

def handle_directory_input():
    """Handles user input for specifying the directory to store the results in."""
    print("\n        R E S U L T   D I R E C T O R Y")
    print("        _______________________________\n")
    while True:
        try:
            result_dir = input("   Please specify directory name to store results in (ENTER for pwd): ")
            if not result_dir:
                return os.getcwd()
            if os.path.exists(result_dir):
                os.rmdir(result_dir)
            try:
                os.makedirs(result_dir)
                return result_dir
            except OSError:
                print(f"   Error: Could not create directory '{result_dir}'. Please try again.")
        except KeyboardInterrupt:
            print("\n   Exiting the script...")
            sys.exit(0)

def print_elapsed_time(start_time):
    """Prints the elapsed time since the start of the script."""
    elapsed_time = time.time() - start_time
    print(f"   Elapsed time: {str(timedelta(seconds=elapsed_time))}", end='\r')        

def run_testing_suites(binary_file_path, handled_binary_setting, result_dir):
    """Runs the testing suites with the specified binary file and setting."""
    try:
        # Count the total number of tests to run and create a progress bar
        total_tests = handled_binary_setting.count('1')

        # Iterate over the testing suites and run the selected ones
        for suite_index, suite in enumerate(TESTING_SUITES):
            if handled_binary_setting[suite_index] == '1':
                # Get the directory of the currently executing script
                script_dir = os.path.dirname(os.path.realpath(__file__))
                testing_suites_scripts_path = os.path.join(script_dir, f"testing_suites_scripts/run_{suite.lower()}.sh")
                args = [testing_suites_scripts_path, binary_file_path, result_dir]

                # Initialize start time for the process
                start_time = time.time()

                # Run the testing suite script
                process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                # Continuously print the elapsed time
                print(f"\n   Running the {suite} testing suite...")

                while process.poll() is None:
                    print_elapsed_time(start_time)

                # Print the final elapsed time after the process finishes
                print_elapsed_time(start_time)
                print()  # Move to the next line after the elapsed time

                # Wait for the process to finish and get the exit code
                process.wait()
                exit_code = process.returncode

                # Check if the process exited with an error
                if exit_code != 0:
                    print(f"An error occurred while running the {suite} script.")

    # Handle any exceptions that occur while running the script
    except subprocess.CalledProcessError as e:
        print("An error occurred while running the script:", e)
        print("Error output:", e.stderr)
    except KeyboardInterrupt:
        print("\n   Exiting the script...")
        sys.exit(0)

def handle_parsed_args(parser, parsed_args):
    """Handles the parsed command-line arguments."""

    # If the -l flag is used, print the available testing suites and exit
    if parsed_args.list_suites:
        print_testing_suites()
        sys.exit(0)

    # Check if the binary file is provided
    if parsed_args.binary_file:

        # Handle the testing setting input
        setting_index = handle_setting_input() if parsed_args.setting is None else parsed_args.setting - 1

        # Check if the binary input flag is used with the Custom setting
        if parsed_args.binary_setting and setting_index != list(TESTING_SETTING_OPTIONS.keys()).index('Custom'):
            print("Error: The --binary-setting (-i) flag can only be used with the Custom setting.")
            sys.exit(1)

        # Handle the selected setting
        input_binary_setting = parsed_args.binary_setting if setting_index == list(TESTING_SETTING_OPTIONS.keys()).index('Custom') else None
        handled_binary_setting = handle_selected_setting(setting_index, input_binary_setting)

        # Handle the result directory input
        result_dir = handle_directory_input() if parsed_args.directory is None else parsed_args.directory
        os.makedirs(result_dir, exist_ok=True)

        # Run the testing suites
        run_testing_suites(parsed_args.binary_file.name, handled_binary_setting, result_dir)
    else:
        parser.print_help()

def main(args=None):
    """Main function to parse command-line arguments and execute the script."""
    parser = argparse.ArgumentParser(description="cryptoguard is a Python package designed for conducting comprehensive testing of random number generators. It provides a collection of testing suites that evaluate the statistical properties and reliability of random number sequences.")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('-l', '--list-suites', action='store_true', help="List all available testing suites")
    parser.add_argument('-b', '--binary-file', type=argparse.FileType('rb'), help="Binary file to test")
    parser.add_argument('-s', '--setting', type=int, choices=range(1, len(TESTING_SETTING_OPTIONS) + 1), help="Testing setting number (" + ", ".join(f"{idx}: {key}" for idx, key in enumerate(TESTING_SETTING_OPTIONS.keys(), start=1)) + ")")
    parser.add_argument('-i', '--binary-setting', type=str, help="Binary representation of the tests to run (only for Custom setting)")
    parser.add_argument('-d', '--directory', type=str, help="Directory to store the results (will be created if it doesn't exist)")

    # Parse the command-line arguments
    if args is None:
        args = sys.argv[1:]

    # Handle the parsed arguments
    parsed_args = parser.parse_args(args)
    handle_parsed_args(parser, parsed_args)

if __name__ == "__main__":
    main()
