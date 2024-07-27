import re

input_text = "OCR/fullinput.txt"
output_spreadsheet = "OCR/output.csv"
log_text = "OCR/log.txt"

output = open(output_spreadsheet, 'w')
output.write('wp,ward,precinct,address,city,state\n')
output.close() #initializes output file before writing

ward_precinct_pattern = re.compile(r'(\d+)-(\d+)')
strict_ward_precinct_pattern = re.compile(r'^(\d+)-(\d+)$')
alternate_wp_pattern = re.compile(r'Ward\s+(\d+)\s+Precinct\s+(\d+)')
street_pattern = re.compile(r'\b(\w+)\s+(Avenue|Boulevard|Circle|Court|Drive|Lane|Park|Parkway|Place|Road|Street|Terrace|Way)\b')
streets_to_suffixes = {
    "Avenue": "AVE",
    "Boulevard": "BLVD",
    "Circle": "CIR",
    "Court": "CT",
    "Drive": "DR",
    "Lane": "LN",
    "Park": "PARK",
    "Parkway": "PKWY",
    "Place": "PL",
    "Road": "RD",
    "Street": "ST",
    "Terrace": "TER",
    "Way": "WAY",
}
street_number_pattern = re.compile(r'^(\d+)\s.*[a-zA-Z].*')

max_ward = 7 #adjust as needed
max_precinct = 6 #adjust as needed
location = "Newton, Massachusetts" #adjust as needed

with open(input_text, 'r') as input, open(output_spreadsheet, 'a') as output, open(log_text, 'w') as log:
    #initialize variables
    ward = '1'
    precinct = '1'
    street_number = '0'
    street = ""
    suffix = ""
    while True:
        try:
            line = input.readline()
            if not line:
                break

            ward_precinct_match = ward_precinct_pattern.search(line)
            alternate_wp_match = alternate_wp_pattern.search(line)
            strict_ward_precinct_match = strict_ward_precinct_pattern.search(line)
            street_match = street_pattern.search(line)
            street_number_match = street_number_pattern.match(line)

            if strict_ward_precinct_match or (ward_precinct_match and street_match) or alternate_wp_match:
                #quality check before writing
                #increasing_ward = int(ward_precinct_match.group(1)) > int(ward)
                #increasing_precinct = int(ward_precinct_match.group(2)) > int(precinct)
                #same_ward = int(ward_precinct_match.group(1)) == int(ward)
                #precinct_one = int(ward_precinct_match.group(2)) == 1
                #((increasing_ward and precinct_one) or (increasing_precinct and same_ward)) and
                if strict_ward_precinct_match:
                    if int(strict_ward_precinct_match.group(1)) <= max_ward and int(strict_ward_precinct_match.group(2)) <= max_precinct and int(strict_ward_precinct_match.group(1)) >= (int(ward) - 1):
                        ward = strict_ward_precinct_match.group(1)
                        precinct = strict_ward_precinct_match.group(2)
                if ward_precinct_match:
                    if int(ward_precinct_match.group(1)) <= max_ward and int(ward_precinct_match.group(2)) <= max_precinct and int(ward_precinct_match.group(1)) >= (int(ward) - 1):
                        ward = ward_precinct_match.group(1)
                        precinct = ward_precinct_match.group(2)
                if alternate_wp_match:
                    if int(alternate_wp_match.group(1)) <= max_ward and int(alternate_wp_match.group(2)) <= max_precinct and int(alternate_wp_match.group(1)) >= (int(ward) - 1):    
                        ward = alternate_wp_match.group(1)
                        precinct = alternate_wp_match.group(2)
                else:
                    log.write(f"did not update wp from line: {line.strip()}\n")
            if street_match:
                #street = f"{street_match.group(1)} {street_match.group(2)}"
                street = street_match.group(1).upper()
                suffix = streets_to_suffixes[street_match.group(2)]
            if street_number_match:
                street_number = street_number_match.group(1)
                wp = ward + precinct
                output.write(wp + ',' + ward + ',' + precinct + ',' + street_number + ' ' + street + ' ' + suffix + ', ' + location + '\n')
        except UnicodeDecodeError:
            log.write(f"Skipping line due to parsing error: {line.strip()}\n")
            continue
