# Weather forecast accuracy prediction

The aim of this project is to analyze the accuracy of the weather forecast in Trentino thanks to the data about 
observations and predictions collected through *MeteoTrentino* web sites.
Moreover, it is possible to give an estimation of the quantity of rain falling down based on some predictions of other 
parameters.

## Structure

### Files and Folders
- The folder `models` contains the regression model created to predict the quantity of rain and a pickle file with the 
  saved coefficients
- Files for the **data collection**, **preparation** and **storage**
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
    - `computation.py` defines the functions to evaluate the accuracy of the predictions (low, medium, high) and to 
        compute the accuracy per day, station, and type of observation
    - `models.py` defines the regression model to predict the quantity of falling rain
- File for **display for the user**
    - `results.py` returns some accuracies for different stations and the prediction for the rain's quantity






