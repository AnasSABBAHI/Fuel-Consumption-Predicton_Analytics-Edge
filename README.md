# Tractor Fuel Consumption Prediction

##  Project Summary
This project aims to predict fuel consumption for tractors based on operational and geographical data. By analyzing factors such as tractor model, agricultural tool used, operating speed, and parcel characteristics, we can build a predictive model. This model can help farmers optimize fuel usage, improve operational efficiency, and detect anomalies such as fuel theft.

##  Objectives
- To perform Exploratory Data Analysis (EDA) to understand the relationships between different features and fuel consumption.
- To engineer relevant features from raw trajectory and geographical data.
- To build and train a supervised machine learning model to predict fuel consumption (in Liters).
- To evaluate the model's performance using the Mean Absolute Error (MAE) metric.
- To create a clean, reproducible repository suitable for a data science student portfolio.

##  Data Description
The dataset is composed of three main sources:
1.  **`interventions_train.csv`**: The main dataset containing records of agricultural interventions.
2.  **`trajets_train/`**: A folder of CSV files, where each file details the GPS trajectory (time, latitude, longitude, speed) of a single intervention.
3.  **`Parcelles/`**: A folder of CSV files, with each file defining the geographical boundaries (latitude, longitude) of a parcel of land.

**Key Features:**
- `Machine`, `Puissance`: Tractor model and its power.
- `Outil`, `Largeur`: The agricultural tool used and its width.
- `Operation`: The type of agricultural operation (e.g., soil work, seeding).
- `Parcelle`: The identifier for the parcel of land.
- `Consommation (L)`: The target variable, representing total fuel consumed.

##  Dependencies
This project uses standard Python data science libraries. A `requirements.txt` file is provided to install the exact dependencies.

- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- geopy
- shapely
- pyproj

##  How to Run the Project
1.  **Clone the Repository:**
    ```bash
    git clone <https://github.com/AnasSABBAHI/Fuel-Consumption-Predicton_Analytics-Edge>
    cd fuel-consumption-prediction
    ```

2.  **Set up the Environment:**
    It is recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Place Data:**
    Ensure your data files (`interventions_train.csv`, `trajets_train/` folder, `Parcelles/` folder) are placed inside the `data/` directory.

4.  **Run the Notebooks:**
    Launch Jupyter Notebook or JupyterLab and run the notebooks in order:
    - `notebooks/1_data_preprocessing_and_eda.ipynb`
    - `notebooks/2_model_training_and_prediction.ipynb`
    - You can also explore `notebooks/exploratory_parcel_visualization.ipynb`.

## 📈 Expected Outputs
- The preprocessing notebook will generate cleaned and merged data.
- The training notebook will train a `GradientBoostingRegressor` model and output its performance metrics.
- If test data is provided, the notebook will generate a `predictions.csv` file with the model's predictions.

## 📊 Interpretation of Results

The final model, a Gradient Boosting Regressor, is trained on the full dataset to make predictions. Initial analysis shows that **Duree_mn** (duration) and **Distance_km** have the strongest positive correlation with fuel consumption, which is expected. Features like **Puissance** (power) also show a moderate positive correlation, while **Largeur** (tool width) has a strong negative correlation, suggesting wider tools may lead to more efficient, less fuel-intensive operations per unit of area. The model's performance should be judged by the MAE on an independent test set.
