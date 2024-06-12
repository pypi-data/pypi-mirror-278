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

function log2 {
    local x=0
    for (( y=$1-1 ; $y > 0; y >>= 1 )) ; do
        let x=$x+1
    done
    echo $x
}

COUNT_BYTES=$(<"${BINARY_FILE}" wc -c)
COUNT_LOG_BYTES=$(log2 $COUNT_BYTES)

PR_STEPS=5
MIN_PR=$(( COUNT_LOG_BYTES - PR_STEPS - 1 ))
MAX_PR=$(( MIN_PR + PR_STEPS ))

{ time (cat "$BINARY_FILE" | "$TEST_SUITE_DIR/pr" stdin64 -tlmin "$MIN_PR" -tlmax "$MAX_PR" -e 0.1 > "$RESULT_DIR/test_practrand.log"); } 2> "$RESULT_DIR/time_pr"
echo -e "\nPractRand" >> "$RESULT_DIR/time"
cat "$RESULT_DIR/time_pr" >> "$RESULT_DIR/time"
rm "$RESULT_DIR/time_pr"

echo "PractRand test completed."

