from data_loader import load_data, get_all_returns
from validation_testing import (
    plaintext_var, plaintext_expected_shortfall, plaintext_sharpe_ratio
)
from financial_metrics import (
    calculate_var_secure, calculate_expected_shortfall, calculate_sharpe_ratio
)
from mpc_protocol import secure_average, secure_variance
import time
import random
import matplotlib.pyplot as plt

def generate_large_dataset(size):
    """Generates a large dataset of random returns for testing."""
    return [random.uniform(-0.05, 0.05) for _ in range(size)]

def time_function(func, *args):
    """
    Times the execution of a function and returns its result and execution time.
    """
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    execution_time = end - start
    print(f"Execution Time: {execution_time:.6f} seconds")
    return result, execution_time

def performance_scalability_test():
    """
    Tests the scalability of secure computations with increasing dataset sizes.
    """
    dataset_sizes = [100, 1000, 5000]
    secure_times = []
    plaintext_times = []
    for size in dataset_sizes:
        large_dataset = generate_large_dataset(size)
        print(f"\n=== Testing with Dataset Size: {size} ===")

        print("\nSecure Average:")
        _, avg_time = time_function(secure_average, large_dataset)

        print("\nSecure Variance:")
        avg_return = secure_average(large_dataset)
        _, var_time = time_function(secure_variance, large_dataset, avg_return)

        print("\nSecure Value at Risk (VaR):")
        _, var_time = time_function(calculate_var_secure, large_dataset)

        print("\nSecure Expected Shortfall (ES):")
        _, es_time = time_function(calculate_expected_shortfall, large_dataset)

        print("\nSecure Sharpe Ratio:")
        _, sharpe_time = time_function(calculate_sharpe_ratio, large_dataset)

        print("\nPlaintext Computations:")

        print("\nPlaintext Value at Risk (VaR):")
        _, var_time = time_function(plaintext_var, large_dataset)

        print("\nPlaintext Expected Shortfall (ES):")
        _, es_time = time_function(plaintext_expected_shortfall, large_dataset)

        print("\nPlaintext Sharpe Ratio:")
        _, sharpe_time = time_function(plaintext_sharpe_ratio, large_dataset)

        print("\n=== Comparison of Secure and Plaintext Computations ===")
        compare_secure_and_plaintext(large_dataset)

        # add times to lists
        secure_times.append(avg_time + var_time + es_time + sharpe_time)
        plaintext_times.append(var_time + es_time + sharpe_time)

    plot_scaling(dataset_sizes, secure_times, plaintext_times)



def plot_scaling(dataset_sizes, secure_times, plaintext_times):
    """
    Plots the scalability of secure computations.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(dataset_sizes, secure_times, label="Secure Computations", marker="o", color="blue")
    plt.plot(dataset_sizes, plaintext_times, label="Plaintext Computations", marker="x", color="orange")
    plt.yscale("log")  # Log scale for better visualization of large differences
    plt.xlabel("Dataset Size")
    plt.ylabel("Execution Time (seconds, log scale)")
    plt.title("Performance Scaling of Secure vs. Plaintext Computations")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.show()

def compare_secure_and_plaintext(returns):
    """
    Compare secure and plaintext computations for validation.
    """
    # Secure computations
    var_secure = calculate_var_secure(returns)
    es_secure = calculate_expected_shortfall(returns)
    sharpe_secure = calculate_sharpe_ratio(returns)

    # Plaintext computations
    var_plaintext = plaintext_var(returns)
    es_plaintext = plaintext_expected_shortfall(returns)
    sharpe_plaintext = plaintext_sharpe_ratio(returns)

    # Print comparisons
    print("\n=== Comparison of Results ===")
    print(f"VaR: Secure = {var_secure}, Plaintext = {var_plaintext}")
    print(f"ES: Secure = {es_secure}, Plaintext = {es_plaintext}")
    print(f"Sharpe Ratio: Secure = {sharpe_secure}, Plaintext = {sharpe_plaintext}")



if __name__ == "__main__":
    performance_scalability_test()
