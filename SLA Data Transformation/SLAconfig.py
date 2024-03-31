"""
Python script to read in the CI Name and Remedy Contract ID from asset_contract_list.csv then cross-reference the
Contract ID with Contract IDs in master_reference.csv. Output SLA.cfg with the CI Name and corresponding referenced
values from SLA_October2021.csv
If Contract ID is not found in master_reference.csv, a default value of 1111100,80000,170000 is set.
"""
import csv
import os
import sys

# Global Variables
ENCODING = 'latin-1'  # to prevent UTF-8 read errors because of latin characters
ASSET_LIST_FILE = 'asset_contract_list.csv'
MASTER_REFERENCE = 'master_reference.csv'
OUTPUT_FILE = 'SLA.cfg'


def main():
    """
    Reads both given CSV files and writes new SLA.cfg file with CI Name=Day,Hour Start,Hour End format.

    Preconditions:
    - asset_contract_list.csv has two header lines
    - all characters in each CSV conform to latin-1 encoding (applicable to company names)
    """
    default_reference_values = ["1111100", "80000", "170000"]

    if not os.path.isfile(ASSET_LIST_FILE) or not os.path.isfile(MASTER_REFERENCE):
        print("One or both input files do not exist.")
        sys.exit(1)

    with open(ASSET_LIST_FILE, 'r', encoding=ENCODING) as asset_list, \
            open(MASTER_REFERENCE, 'r', encoding=ENCODING) as master_reference, \
            open(OUTPUT_FILE, 'w', newline='') as output:

        asset_reader = csv.reader(asset_list)
        reference_reader = csv.reader(master_reference)
        output_writer = csv.writer(output)

        # Read the headers of the CSV files
        next(asset_reader)
        next(asset_reader)  # Two header rows in asset_contract_list.csv
        next(reference_reader)

        # Assign column indices
        asset_col_index = 3  # Contract ID in asset_contract_list
        reference_col_index = 0  # Contract ID in reference file
        reference_indices = [2, 3, 4]  # Corresponding to Days, Hour Start and Hour End

        # Iterate over each line in asset_contract_list
        for asset_row in asset_reader:
            asset_col_value = asset_row[asset_col_index]
            reference_found = False

            # Iterate over each line in reference data to find a match
            for reference_row in reference_reader:
                reference_col_value = reference_row[reference_col_index]
                if reference_col_value == asset_col_value:
                    referenced_values = [reference_row[i] for i in reference_indices]
                    output_writer.writerow([asset_row[0] + "=" + referenced_values[0]] + referenced_values[1:])
                    reference_found = True
                    break

            if not reference_found:
                output_writer.writerow(
                    [asset_row[0] + "=" + default_reference_values[0]] + default_reference_values[1:])

            # Reset the file pointer to the beginning of master_reference.csv for each asset_row
            master_reference.seek(0)
            next(reference_reader)  # Skip the header row

    print("Output file generated successfully.")


def test_output_line_count():

    # Count the number of lines in the asset file
    with open(ASSET_LIST_FILE, 'r', encoding=ENCODING) as asset_list:
        asset_line_count = sum(1 for _ in asset_list) - 2

    # Count the number of lines in the output file
    with open(OUTPUT_FILE, 'r', encoding=ENCODING) as output:
        output_line_count = sum(1 for _ in output)

    # Compare the line counts and assert equality
    assert output_line_count == asset_line_count, "Line counts do not match"

    print("Output line count test passed!")


if __name__ == '__main__':
    main()
    test_output_line_count()
