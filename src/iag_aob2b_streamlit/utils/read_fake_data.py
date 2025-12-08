import json

def read_json_to_df(file_path):
    """
    Reads a JSON file and returns the data as a pandas DataFrame.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        pd.DataFrame: DataFrame containing the JSON data
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return data