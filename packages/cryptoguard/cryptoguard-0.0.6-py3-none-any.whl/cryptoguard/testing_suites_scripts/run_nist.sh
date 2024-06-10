#!/bin/bash

# Assign positional arguments to variables
BINARY_FILE=$1
RESULT_DIR=$2

# Ensure that the binary file exists
if [ ! -f "$BINARY_FILE" ]; then
    echo "Error: The specified binary file '$BINARY_FILE' does not exist." >&2
    exit 1
fi

# Ensure that the specified directory exists
if [ ! -d "$RESULT_DIR" ]; then
    echo "Error: The specified directory '$RESULT_DIR' does not exist." >&2
    exit 1
fi

# Get the path to the testing suite directory
TEST_SUITE_DIR="$(dirname "$(realpath "$0")")/../testing_suites"

# copy sts-2.1.2/experiments folder to present working directory for NIST program to be able to store the results
cp -r "$TEST_SUITE_DIR/sts-2.1.2/experiments" "."

# Function to clean up the temporary experiments directory
cleanup() {
    rm -rf "./experiments"
}

# Set up a trap to call the cleanup function on exit
trap cleanup EXIT

# create input file for the NIST testing suite
# [0] Input File
# User Prescribed Input File
# Enter 0 if you DO NOT want to apply all of the statistical tests to each sequence and 1 if you DO.
# Parameter Adjustments (0 to continue)
# How many bitstreams?
# [1] Binary - Each byte in data file contains 8 bits of data

cat <<EOL > $RESULT_DIR/nist_input.txt
0
$BINARY_FILE
1
0
100
1
EOL

# Run the NIST test suite
{ time "$TEST_SUITE_DIR/sts-2.1.2/assess" 1000000 < "$RESULT_DIR/nist_input.txt"; } 2> "$RESULT_DIR/time_nist"

# Log the timing results
echo -e "\nNIST" >> "$RESULT_DIR/time"
cat "$RESULT_DIR/time_nist" >> "$RESULT_DIR/time"
rm "$RESULT_DIR/time_nist"

# Copy the final analysis report to the result directory
cp "./experiments/AlgorithmTesting/finalAnalysisReport.txt" "$RESULT_DIR/test_nist.log"

echo "NIST test completed."

