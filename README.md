# Weather forecast accuracy in Trentino

The aim of this project is to analyze the accuracy of the weather forecast in Trentino thanks to the data about 
observations and predictions collected through *OpenDataTrentino* web sites.
Moreover, it is possible to give an estimation of the quantity of rain falling down based on some predictions of other 
parameters.

## Structure

### Files and Folders
- The folder `models` contains the regression model created to predict the quantity of rain and a pickle file with the 
  saved coefficients
- Files for the **data collection**, **preparation** and **storage**
    - `station_anagrafica.py` defines the functions to, given the url with stations information and the name of the file 
      that will contain stations names, extract stations codes, names and save them
    - `prediction.py` defines the class *Previsione* and the functions to store the data about the predictions into a 
      Mysql database
    - `dati_reali.py` defines the class *DatiReali* and the functions to store the data about the observations into a 
      Mysql database
    - `fetch_dati_reali.py` defines the functions to get the data about the predictions from the website, to parse the 
      xml related to them, and it stores the data into the database
    - `fetch_dati_reali.py` defines the functions to get the data about the observations from the website, to parse the 
      json related to them, and it stores the data into the database
- Files for the **data elaboration** and **preparation** for the analysis
    - `read_data.py` reads data stored into the databese and computes the time ranges for the collected data
    - `modify_previsioni.py` defines the functions to compute some preliminary computations on predictions data to prepare 
      them for the comparison with the observations
    - `modify_dati_reali.py` defines the functions to compute some preliminary computations on observations data to prepare 
      them for the comparison with the predictions
    - `join_df.py` matches data from predictions and observations marking if there is correspondence between them
    - `write_data.py` stores the modified and joint data into new tables in the database
- Files for **data analysis** and **statistics**
    - `computation.py` evaluates the accuracy of the predictions (low, medium, high) and
        computes the accuracy per day, station, and type of observation
    - `models.py` defines the regression model to predict the quantity of falling rain
- File for **display for the user**
    - `results.py` returns some accuracies for different stations and the prediction for the rain's quantity
    
## Execution

### Requirements to run the script `results.py`

1) `Python 3.8` or more
2) `MySql`
3) Python packages (listed in the file *requirements.txt*)
4) It is recommended to create and activate a virtual environment in the project's folder

- Inside the virtual environment install the required packages with the command:
    `pip install -r requirements.txt`
  
- NB: to run other parts of the project it is necessary to have also `Spark`. The MySQL Connector/J (the official JDBC 
  driver for MySQL) is needed to use `PySpark` on your machine and to connect to the database. It is stored in the folder
  `JDBC_connector`

### Execution of the script `results.py`

Run the python script `results.py` to simulate the prediction of falling rain for tomorrow or to compute the accuracy
of some measures in specific stations given some parameters, which can be set:
* `-rain_acc`:
    - 0 -> if you want to get rain prediction
    - 1 -> if you want to get accuracies for a particular station
* if `-rain_acc` is 0:
    - `-temp_min` -> insert a float indicating the minimum temperature predicted
    - `-temp_max` -> insert a float indicating the maximum temperature predicted
    - `-rain_prob`:
        - 0 if predicted rain probability is < 25%
        - 1 if predicted rain probability is 25%-50%
        - 2 if predicted rain probability is 50%-75%
        - 3 if predicted rain probability is > 75%
    - `-rain_int`:
        - 0 if predicted rain intensity is low
        - 1 if predicted rain intensity is medium
        - 2 if predicted rain intensity is high
    - `-wind_speed`:
        - 0 if predicted wind speed is < 0.5 m/s
        - 1 if predicted wind speed is 0.5-4 m/s
        - 2 if predicted wind speed is 4-8 m/s 
*Example: python3 results.py -rain_acc 0 -temp_min 20 -temp_max 25 -rain_prob 3 -rain_int 2 -wind_speed 0
* if `rain_acc` is 1:
    - `-localita` -> insert the name of a station
        List of possible stations to insert: 
        - ala
        - aldeno
        - arco
        - canazei
        - castello tesino
        - cavalese
        - daone
        - grigno
        - levico
        - mezzano
        - passo pian delle fugazze
        - peio
        - pergine valsugana
        - pinzolo
        - rabbi
        - rovereto
        - san lorenzo in banale
        - torbole
        - trento
    - `-type`:
        - 0 to get accuracy for everything
        - 1 to get accuracy for rain intensity
        - 2 to get accuracy for wind intensity and speed
        - 3 to get accuracy for min and max temperature
*Example: python3 results.py -rain_acc 1 -localita "trento" -type 3
    
### Web app
Through the following link you can browse through the application that shows you the previous results 
https://PCIDJP27XLCXNFR7.anvil.app/SPKJ7RZXFW5E4UXBLRAFA55C    











