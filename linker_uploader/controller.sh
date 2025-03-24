#!/bin/bash

DBNAME="DBNAME"
TABLE_NAME="your_table_name"
db2 connect to $DBNAME

SQL_QUERY="SELECT
    src_tsm_server_name,
    src_tsm_filespace_name,
    scr_tsm_btch_filename,
    status,
    dst_agid_name
FROM $TABLE_NAME"
readarray -t QUERY_RESULTS < <(db2 -x "$SQL_QUERY")
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
        echo "$row"
    fi
done

# Disconnect from the database
db2 terminate

echo "Scrit finished successfully."