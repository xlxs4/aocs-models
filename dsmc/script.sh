#!/bin/bash

# Define the base URL
base_url="https://goce-ds.eo.esa.int/oads/data/GOCE_Telemetry"

# Define the range of files to download
start=12
end=23

# Define the output CSV file
output_file="combined.csv"

# Initialize a variable to track the first file
first_file=1

# Loop over the range
for ((i=start; i<=end; i++))
do
  # Pad the number with leading zeros to a length of 2
  padded_num=$(printf '%02d' $i)

  # Define the file name, filling in the number
  filename="GO_CONS_T_CAT290${padded_num}_20090317T090419_20090326T103259_0001.TGZ"

  # Define the csv name
  csv_filename="CAT290${padded_num}.csv"

  # Download the file with curl
  curl "${base_url}/${filename}" \
    -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8' \
    -H 'Accept-Language: en-GB,en;q=0.9' \
    -H 'Connection: keep-alive' \
    -H 'Cookie: JSESSIONID=9C11089B1F4BE89356571BA486618E78; _shibsession_64656661756c7468747470733a2f2f676f63652d64732e656f2e6573612e696e742f73686962626f6c657468=_b469d3c61cb47544136ed133925308ce; _saml_idp=ZW9pYW0taWRwLmVvLmVzYS5pbnQ%3D' \
    -H 'Referer: https://goce-ds.eo.esa.int/oads/access/collection/GOCE_Telemetry/searchbyfilename' \
    -H 'Sec-Fetch-Dest: document' \
    -H 'Sec-Fetch-Mode: navigate' \
    -H 'Sec-Fetch-Site: same-origin' \
    -H 'Sec-Fetch-User: ?1' \
    -H 'Sec-GPC: 1' \
    -H 'Upgrade-Insecure-Requests: 1' \
    -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' \
    -H 'sec-ch-ua: "Not.A/Brand";v="8", "Chromium";v="114", "Brave";v="114"' \
    -H 'sec-ch-ua-mobile: ?0' \
    -H 'sec-ch-ua-platform: "macOS"' \
    --compressed \
    --output "${filename}"

  # Extract the file
  tar -xzf "${filename}"

  # Handle the CSV files differently depending on whether they're the first file or not
  if ((i==start))
  then
    # For the first file, keep all columns
    csv_files+="${csv_filename} "
  else
    # For all other files, keep only the second column
    cut -d',' -f2 "${csv_filename}" > "${csv_filename}_modified.csv"
    csv_files+="${csv_filename}_modified.csv "
  fi
done

# Combine all CSV files horizontally
paste -d, $csv_files > $output_file

# Remove all the CSV files except from the combined one
find . -type f -name "*.csv" ! -name "$output_file" -exec rm {} \;

# Remove the download artifacts
rm *.TGZ *.HDR
