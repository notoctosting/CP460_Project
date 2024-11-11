import json

def load_data(filepath):
    """Loads financial data from a JSON file."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data

# Example usage:
if __name__ == "__main__":
    data = load_data('../data/sample_data.json')
    print(data)