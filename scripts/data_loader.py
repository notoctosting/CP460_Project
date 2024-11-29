import json

def load_data(filepath):
    """Loads financial data from a JSON file."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data

def get_all_returns(data):
    """Extracts all returns from the dataset."""
    returns = []
    for institution, metrics in data.items():
        returns.extend(metrics["returns"])
    return returns

# Example usage
if __name__ == "__main__":
    filepath = "../data/sample_data.json"
    data = load_data(filepath)
    all_returns = get_all_returns(data)
    print(f"All Returns: {all_returns}")