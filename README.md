SpaceX Falcon 9 First Stage Landing Prediction
Project Overview
This project is part of the IBM Data Science Professional Certificate Capstone. The goal is to predict whether the first stage of the SpaceX Falcon 9 rocket will land successfully. Since the first stage's reuse significantly reduces the cost of space launches (from over $165M to ~$62M), predicting landing success is crucial for estimating launch costs.

Methodology
The project follows the standard data science lifecycle:

Data Collection: Using the SpaceX API and Web Scraping from Wikipedia.

Data Wrangling: Cleaning the data, handling missing values, and creating a binary "Class" column (1 for success, 0 for failure).

Exploratory Data Analysis (EDA): Using SQL and Visualization libraries (Pandas, Seaborn, Matplotlib) to find patterns.

Interactive Visual Analytics: Building maps with Folium and an interactive dashboard with Plotly Dash.

Predictive Analysis (Machine Learning): Training and comparing Logistic Regression, SVM, Decision Tree, and KNN models.

Key Results
Best Model: The Decision Tree and SVM models typically yielded the highest accuracy (~83.3% on the test set).

Insights: Launch site KSC LC-39A shows the highest success rate, and success rates have improved significantly as payload mass and experience increased over time.

Repository Structure
data_collection_api.ipynb: Extracting data via API.

web_scraping.ipynb: Extracting data from Wikipedia.

eda_sql.ipynb: Running SQL queries for data insights.

eda_viz.ipynb: Visualizing trends with Seaborn/Matplotlib.

interactive_map_folium.ipynb: Geographic analysis of launch sites.

plotly_dash_app.py: Code for the interactive dashboard.

machine_learning_prediction.ipynb: Final model training and evaluation.

Requirements
Python 3.x

Pandas, NumPy, Scikit-learn

Folium, Plotly, Dash

Seaborn, Matplotlib

How to add this to GitHub:
Go to your repository on GitHub.

Click Add file > Create new file.

Name it README.md.

Paste the content above.

Click Commit changes.
