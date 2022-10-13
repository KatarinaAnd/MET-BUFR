# syno_bufr_2_netcdf.py

**parse_arguments**

Tar inn argumenter:

-c konfigurasjonsfil

-t type of station identifier. Either block/wigos/state/ship.

-st gir muligheten for å spesifisere stasjoner man ønsker å hente ut. Dersom stationtype (-t) er block, kan man bare skrive inn stasjoner som identifseres med "[blockNumber][stationNumber]". Dersom t = state, må stasjonene skrives inn som  "[stateIdendifier]-[nationalStationNumber]". Dersom t = wigos, må stasjonene skrives inn som "[wigosIdentifierSeries]-[wigosIssuerOfIdentifier]-[wigosIssueNumber]-[wigosLocalIdentifierCharacter]". Dersom t = ship, må stasjonene skrives inn som "[shipOrMobileLandIdentifier]".

-s may specify // -e // -i // -a // -u

**parse_cfg**

**get_files_specified_dates**

**get_files_initialize**

**get_files_update**

**bufr_2_json**

**return_list_of_stations**

**sorting_hat**

**block_and_station**

**wigosnumber**

**stateidentifier**

**shipOrMobileLandStationIdentifier**

**set_encoding**

**saving_grace**

