import time

def time_mpc_execution(function, *args):
    """Measures execution time for a given function."""
    start_time = time.time()
    result = function(*args)
    end_time = time.time()
    print(f"Execution Time: {end_time - start_time:.4f} seconds")
    return result

# Example usage:
if __name__ == "__main__":
    from financial_metrics import calculate_var

    returns = [0.05, 0.04, -0.01]
    time_mpc_execution(calculate_var, returns)
