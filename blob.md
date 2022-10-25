# syno_bufr_2_netcdf.py

**parse_arguments**

Parses arguments:

* -c configuration file

* -t type of station identifier. Either block/wigos/state/ship.

* -st gives the option to specify the stations one wishes to extract. If the stationtype, t = block, the stations have to be specified through "[blockNumber][stationNumber]". If t = state the stations have to be specified through "[stateIdendifier]-[nationalStationNumber]", if t =  wigos the stations have to be specified as "[wigosIdentifierSeries]-[wigosIssuerOfIdentifier]-[wigosIssueNumber]-[wigosLocalIdentifierCharacter]", and if t = ship the stations must be specified as "[shipOrMobileLandIdentifier]".

* -s may specify a timeperiod for which the data should be extracted. Startday should be in the form "YYYY-MM-DD".

* -e Endday should be in the form "YYYY-MM-DD".

* -i downloads all data available in folder (default).

* -a downloads data from all stations within the specified station type (default).

* -u reads the latest date available in output folder, and updates the stations to current date.

**parse_cfg**

reads the config file

**get_files_specified_dates**

if -s and -e is true, then it will return the files from the input folder which contains data from the timespace specified.

**get_files_initialize**

if -s and -e is false, then this function returns all the available data (for the specified station type) in the input folder.

**get_files_update**

if -u is true, then this function will read the latest available data in the output folder, and return the available data from that date from the input folder.

**bufr_2_json**

converts bufr to json, using the bufr_dump bash function.

**return_list_of_stations**

Returns the list of stations available either within the specifies period or of all the files within the input-folder.

**sorting_hat**


**block_and_station**

**wigosnumber**

**stateidentifier**

**shipOrMobileLandStationIdentifier**

**set_encoding**

**saving_grace**

