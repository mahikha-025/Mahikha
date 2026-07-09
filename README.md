# 🏠 House Price Prediction Using Linear Regression

## 📌 Project Overview

House Price Prediction is a Machine Learning project that predicts the median house price of a district using various housing-related features from the California Housing Dataset. The project implements the **Linear Regression** algorithm to identify relationships between input features and house prices, enabling accurate price predictions based on historical data.

This project serves as an introduction to supervised machine learning and demonstrates the complete workflow of building, training, and evaluating a regression model using Python and Scikit-learn.

---

## 🎯 Objective

- Build a machine learning model to predict house prices.
- Learn the implementation of Linear Regression.
- Perform data preprocessing and train the model.
- Evaluate prediction accuracy using performance metrics.
- Understand the end-to-end machine learning workflow.

---

## 🛠️ Technologies Used

- Python
- Google Colab / Jupyter Notebook
- Pandas
- NumPy
- Scikit-learn
- Matplotlib

---

## 📂 Dataset

This project uses the **California Housing Dataset**, which is available directly through the Scikit-learn library.

### Features

- MedInc – Median Income
- HouseAge – House Age
- AveRooms – Average Number of Rooms
- AveBedrms – Average Number of Bedrooms
- Population – Population
- AveOccup – Average Occupancy
- Latitude
- Longitude

### Target

- Median House Value

---

## ⚙️ Machine Learning Workflow

1. Import the required libraries.
2. Load the California Housing Dataset.
3. Convert the dataset into a Pandas DataFrame.
4. Explore the dataset.
5. Split the data into training and testing sets.
6. Train the Linear Regression model.
7. Predict house prices using the test dataset.
8. Evaluate the model using MSE and R² Score.
9. Display the prediction results.

---

## 📊 Model Evaluation

The model performance is evaluated using:

- **Mean Squared Error (MSE)**
- **R² Score (Coefficient of Determination)**

These metrics measure how accurately the trained model predicts house prices.

---

## 📁 Project Structure

```
House-Price-Prediction/
│
├── House_Price_Prediction.ipynb
├── README.md
└── requirements.txt
```

---

## ▶️ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/House-Price-Prediction.git
```

Move into the project folder:

```bash
cd House-Price-Prediction
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Project

Open the notebook using:

- Google Colab
- Jupyter Notebook

Run all the cells sequentially to:

- Load the dataset
- Train the model
- Predict house prices
- View evaluation metrics

---

## 📈 Sample Output

```
Mean Squared Error: 0.5559

R² Score: 0.5758

Actual Price: 1.36100
Predicted Price: 0.71912

Actual Price: 2.41300
Predicted Price: 1.76402

Actual Price: 2.00700
Predicted Price: 2.70966
```

*(Output values may vary slightly because of train-test splitting.)*

---

## 💡 Applications

- Real Estate Price Prediction
- Property Value Estimation
- Housing Market Analysis
- Investment Decision Support
- Business Intelligence

---

## 🚀 Future Enhancements

- Use advanced regression algorithms.
- Perform feature engineering.
- Hyperparameter tuning.
- Deploy the model as a web application.
- Add data visualization dashboards.
- Compare multiple machine learning models.

---

## 📚 Libraries Used

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
```

---

## 📄 Requirements

Create a `requirements.txt` file with the following content:

```text
pandas
numpy
matplotlib
scikit-learn
```

---

## 👩‍💻 Author

**Mahikha Cha**

B.Sc. Computer Science with Data Analytics

---

## ⭐ Acknowledgement

The California Housing Dataset is provided by **Scikit-learn** and is widely used for educational purposes in machine learning and data science.

---

## 📜 License

This project is created for educational and learning purposes. Feel free to use and modify it for academic projects.

---

### ⭐ If you found this project useful, don't forget to Star the repository!
