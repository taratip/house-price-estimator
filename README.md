# Estimating House Price in Boston Area
This project is to estimate house prices in Boston Area (MA, USA) based on the features using publicly available data. 

## Data sources
* The house sales records were scrapped from zillow.com. For the scrapping code, please see [https://github.com/taratip/house-sales-analysis/blob/master/scrapper.py](https://github.com/taratip/house-sales-analysis/blob/master/scrapper.py)
* Get additional features using Zillow API
* [S&P/Case-Shiller MA-Boston Home Price Index](https://fred.stlouisfed.org/series/BOXRSA) 

## Data Analysis
The value of house can be different now as it was in the past. Therefore, the house price needs to be adjusted to the same month.
S&P/Case-Shiller MA-Boston Home Price Index is used to adjust the price, however, it only has the index up to July 2018, whereas the house
sales records I have were up until October 2018. So a time series forecasting using the ARIMA model (AutoRegressive Integrated Moving Average)
was used to predict index for the next 3 months.

Please see the code for Time series analysis at [https://github.com/taratip/house-sales-analysis/blob/master/Home%20Price%20Index.ipynb](https://github.com/taratip/house-sales-analysis/blob/master/Home%20Price%20Index.ipynb)

## Data Preprocessing
### Data exploration and data cleaning
Drop the record which missing some data such as lot size, finished squared ft, bedrooms, bathrooms, and price. For records that missing total
rooms, I filled in by calculating avarage number of total rooms having the same number of bedrooms and bathrooms from the data.
Additional features were created such as price per sqft because each house has different square footage and each neighborhood has different home prices.
This could be an important factor that correlates with the last sold price.

### Neighborhood clustering
There are total 27 neighborhoods in the data. Because there was only one transaction activity in some neighborhoods, I need to cluster the 
neighborhood based on how expensive the price per sqft was and how frequency the sales transactions occurred into three groups:
1. low frequencey
2. low price, high frequency
3. high price, high frequency

### Train and Build Regression Models
After prepared all data, four different models were tests and compared which one provides the best result. The performance of the models were
evaluated by cross-validation. Gradient Boosting Regression has the best result so I would consider this is the final model. 

Model | R squared score
--- | ---
Linear | -1.1774
Decision Tree | 0.3132
Random Forest | 0.3172
Gradient Boosting | 0.3176

For all analysis processes, please see https://github.com/taratip/house-sales-analysis/blob/master/Data%20Analysis.ipynb

## Houses with similar features
K-means Clustering algorithm was used on unlabelled given data to find the patterns and segregate all inputs based on features and the 
prediction is based on which cluster it belonged. The dataset given for Unsupervised Algorithm has 31 features including house features and neighborhoods.

For the clustering analysis, please see https://github.com/taratip/house-sales-analysis/blob/master/Clustering.ipynb

## Web application
After training all models, I created a web application to get an input from user and estimate the house price based on input features using
the final model which is Gradient Boosting Regression. The K-means Clustering is used to get previously sold houses with similar features based on input.
The web application also sends API request to Zillow to get information of these three similar houses.

The code can be found at [https://github.com/taratip/house-price-estimator](https://github.com/taratip/house-price-estimator). The web can be accessed at https://house-price-estimator-tj.herokuapp.com/

## Future
It is obvious that the model I chose did not give accurate prediction as the dataset I have is too few for machine learning. Some of important features 
were not included in the model such crime rate, school system in the area, kitchen, pool, etc. With more features and more data, a better 
prediction can be made. 
