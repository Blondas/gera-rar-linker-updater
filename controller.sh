#!/bin/bash

SRC_DIR_PREFIX="foo/bar"
OUTPUT_DIR="foo/bar"

DBNAME="DBNAME"
TABLE_NAME="your_table_name"
PYTHON_MODULE="linker_uploader"

export DB@DBDFT=$DBNAME

# Connect to the database
db2 connect to $DBNAME
if [$? -ne 0]; then
    echo "Error connecting to the database."
    exit 1
fi

# Run the query
SQL_QUERY="SELECT
    src_tsm_server_name,
    src_tsm_filespace_name,
    scr_tsm_btch_filename,
    status,
    dst_agid_name
FROM $TABLE_NAME limit 1"

QUERY_RESULT=$(db2 -x "$SQL_QUERY" 2>&1)
if [ $? -ne 0 ]; then
    echo "DB2 Error: $QUERY_RESULT"
    db2 terminate
    exit 1
fi

readarray -t QUERY_RESULTS <<< "$DB2_OUTPUT"
if [ ${#RESULTS[@]} -eq 0 ]; then
    echo "No results returned or an error occurred."
    db2 terminate
    exit 1
fi

# Check if the query returned any results
if [ ${#QUERY_RESULTS[@]} -eq 0 ]; then
    echo "No results returned or an error occurred."
    db2 terminate
    exit 1
fi

for row in "${RESULTS[@]}"
do
    # Skip empty lines
    if [ -n "$row" ]; then
        echo "Processing $row"

        read -r src_tsm_server_name src_tsm_filespace_name scr_tsm_btch_filename status dst_agid_name <<< "$row"

        python -m $PYTHON_MODULE \
            --src-directory-prefix $SRC_DIR_PREFIX \
            --output-directory $OUTPUT_DIR \
            --db-src-tsm-server-name "$src_tsm_server_name" \
            --db-src-tsm-filespace-name "$src_tsm_filespace_name" \
            --db-src-tsm-batch-filename "$scr_tsm_btch_filename" \
            --db-status "$status" \
            --dst-agid-name "$dst_agid_name"

        if [ $? -ne 0 ]; then
            echo "Error running Python module for row: $row"
            # Continue with next row rather than exiting
        fi
    fi
done

# Disconnect from the database
db2 terminate

echo "Scrit finished successfully."