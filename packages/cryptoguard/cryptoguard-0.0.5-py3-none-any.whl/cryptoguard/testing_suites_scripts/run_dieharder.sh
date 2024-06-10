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

{ time while :; do cat $BINARY_FILE || exit; done | dieharder -a -g 200 | head -n 26 > "$RESULT_DIR/test_dieharder.log"; } 2> "$RESULT_DIR/time_dieharder"
echo -e "\nDieharder" >> "$RESULT_DIR/time"
cat "$RESULT_DIR/time_dieharder" >> "$RESULT_DIR/time"
rm "$RESULT_DIR/time_dieharder"

echo "Dieharder test completed."

