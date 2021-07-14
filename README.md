# Weather forecast accuracy prediction

The aim of this project is to analyze the accuracy of the weather forecast in Trentino thanks to the data about 
observations and predictions collected through *MeteoTrentino* web sites.
Moreover, it is possible to give an estimation of the quantity of rain falling down based on some predictions of other 
parameters.

## Structure

### Files and Folders
- The folder `models` contains the regression model created to predict the quantity of rain and a pickle file with the 
  saved coefficients
- Files for the data collection, preparation and storage
    - `prediction.py` defines the class **Previsione** and the functions to store the data about the predictions into a 
      Mysql database
    - `dati_reali.py` defines the class **DatiReali** and the functions to store the data about the observations into a 
      Mysql database
    - `fetch_dati_reali.py` defines the functions to get the data about the predictions from the website, to parse the 
      xml related to them and it stores the data into the database
    - `fetch_dati_reali.py` defines the functions to get the data about the observations from the website, to parse the 
      json related to them and it stores the data into the database
- Files for the data elaboration and preparation for the analysis
    - `modify_previsioni.py` 




