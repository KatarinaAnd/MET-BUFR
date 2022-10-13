# syno_bufr_2_netcdf.py

**parse_arguments**

Parses arguments:

* -c configuration file

* -t type of station identifier. Either block/wigos/state/ship.

* -st gives the option to specify the stations one wishes to extract. If the stationtype, t = block, the stations have to be specified through "[blockNumber][stationNumber]". If t = state the stations have to be specified through "[stateIdendifier]-[nationalStationNumber]", if t =  wigos the stations have to be specified as "[wigosIdentifierSeries]-[wigosIssuerOfIdentifier]-[wigosIssueNumber]-[wigosLocalIdentifierCharacter]", and if t = ship the stations must be specified as "[shipOrMobileLandIdentifier]".
* 

* -s may specify a timeperiod for which the data should be extracted. Startday should be in the form "YYYY-MM-DD".

* -e Endday should be in the form "YYYY-MM-DD".

* -i

* -a

* -u

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

