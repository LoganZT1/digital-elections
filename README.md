# digital-elections
Digitizing historic voter lists and creating shapefiles by geocoding the voters

#### Project Status:
This is an ongoing project. More cities and years will be added in the future.

#### Summary:
The goal of this project is to recreate historical voting precinct maps from voter lists. The voter
lists are found on archive.org, which uses optical character recognition (OCR) to convert it to a
text file. The "ocrcleaner" python script reads this text file and produces a csv file containing a
record for each voter. This csv file is then geocoded by joining it to an address shapefile. The result
gives obvious boundaries for each precinct which is then drawn manually. To replicate, download the 
"full text" option from an archive.org source below and change the "input_text", "output_spreadsheet", and
"log_text" variables in the python script to the desired locations. Shapefiles and screenshots can be found in the subdirectories.

#### Sources:

Newton 1947 Voter List: https://archive.org/details/assessedpollscit1947newt/

Newton Address Shapefile: https://www.newtonma.gov/government/information-technology/gis/gis-data-dictionary