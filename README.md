# submission-data-analysis-python

## Folder Structure

The repository contains the following folder structure:

```
├───dashboard
│   ├───main_data.csv
│   └───dashboard.py
├───data
│   ├───data_1.csv
│   └───data_2.csv
├───notebook.ipynb
├───README.md
├───requirements.txt
└───url.txt
```

## Files Description

- `dashboard/main_data.csv`: Contains the main data for the dashboard.
- `dashboard/dashboard.py`: Python script to load and display the main data.
- `data/data_1.csv`: Contains the first dataset.
- `data/data_2.csv`: Contains the second dataset.
- `notebook.ipynb`: Jupyter notebook for data analysis.
- `README.md`: This file, containing information about the project.
- `requirements.txt`: Lists the dependencies required for the project.
- `url.txt`: Stores URLs related to the project.

## Running the Dashboard

To run the dashboard, follow these steps:

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the dashboard using Streamlit:
   ```
   streamlit run dashboard/dashboard.py
   ```
