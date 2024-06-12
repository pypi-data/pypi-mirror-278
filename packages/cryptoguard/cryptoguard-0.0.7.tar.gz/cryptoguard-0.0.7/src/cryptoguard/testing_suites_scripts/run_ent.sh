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

{ time "$TEST_SUITE_DIR/ent" "$BINARY_FILE" > "$RESULT_DIR/test_ent.log"; } 2> "$RESULT_DIR/time_ent"
echo -e "\nENT" >> "$RESULT_DIR/time"
cat "$RESULT_DIR/time_ent" >> "$RESULT_DIR/time"
rm "$RESULT_DIR/time_ent"

echo "ENT test completed."

