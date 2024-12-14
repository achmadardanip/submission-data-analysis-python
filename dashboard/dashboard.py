import pandas as pd

def load_data(file_path):
    """
    Load data from a CSV file.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    DataFrame: The loaded data as a pandas DataFrame.
    """
    return pd.read_csv(file_path)

def main():
    # Load the main data
    data = load_data('main_data.csv')
    
    # Display the first few rows of the data
    print(data.head())

if __name__ == "__main__":
    main()
