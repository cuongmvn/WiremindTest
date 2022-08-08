# WiremindTest
The EDA is presented in notebook with the same name.
The dashboard_app.py is a prototype using dash library, which gives the time series data given a train route.
To run the app, install the necessary requirements and run command
'''
python dashboard_app.py
'''
Then access the default local address (http://127.0.0.1:8050/).
![alt text](https://github.com/cuongmvn/WiremindTest/blob/main/demo.jpg?raw=true)
![alt text](https://github.com/cuongmvn/WiremindTest/blob/main/demo1.jpg?raw=true)
# The Approach or Overview of Analysis Report:

1. I take broad views inspection of the whole dataset, (analysing the data of all train in full-year time scale).
2. then after that I go deeper into smaller time cycle, influence of holidays and 
3. finally inspect each train route and make individual train report.

# Conclusion:

The EDA cover almost all variable, except the 3 variable about similar trains during 2,4 and 12 hours time windows haven't got detailed analysis and visualization.
The analysis focus on demand and price, there are many remarks about observed patterns, outliers, hypotheses and the mention of potential use for future prediction from data.
# Work summary:

There are 3 types of works that was done during this report:
1. Data Cleaning and Feature Engineering:

    This is done with pandas as the test requirement

2. Visualization:

    In early draft seaborn and matplotlib is used frequently.
    Later I decided to make illustration with plotly for more dynamic presentation
    Finally an app_dashboard.py is created which is a simple dashboard solution using dash library developed by plotly.

3. Analysis:

    This part is actually very time consuming and with better understanding of the data, I have to come back to step 1 and 2 for better process.

# What can be done further:

1. Inspect each train route
2. Plotting moving average on time series
3. Do statistical test on the time series
4. More well designed visualization
...