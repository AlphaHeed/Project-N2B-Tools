# Project-N2B-Tools

Experiments:
The experiments are based on three games. Each game folder contains the games JSON-file and an HTML-file with visualisation of all game rounds.
Each game folder contain experiments on Black Sea and Galicia and in turn these folders contain "Hold" and "Bounce" folders.
Each Hold and Bounce folder contain the games JSON-file that have been edited so that the concerned units hold and bounce respectively.
Each of these files also contain logs from running Sitcheck for both powers (named: Log-<Power>) and the filter output.

Filter:
After running Sitcheck serveral times in the docker container the log is extracted from the Docker Desktop app. 
The filter (FILTER-V6) is executed in the same location as the extracted log (named "Log") and outputs a textfile containing: all actions and probability weights, weight mean value, normalised weight mean value, and standard deviation.

