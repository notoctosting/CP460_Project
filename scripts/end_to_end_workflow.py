from data_loader import load_data, get_all_returns
from financial_metrics import (
    calculate_var_secure, calculate_sharpe_ratio, calculate_expected_shortfall,
    calculate_portfolio_beta, calculate_correlation
)
from mpc_protocol import secure_average, secure_variance
import matplotlib.pyplot as plt
import time

def end_to_end_workflow():
    """
    Runs the entire MPC-based financial metrics workflow with advanced metrics.
    """
    from mpyc.runtime import mpc
    mpc.run(mpc.start())

    try:
        # Load data
        filepath = "../data/sample_data.json"
        data = load_data(filepath)
        all_returns = get_all_returns(data)
        market_returns = data["Market_Index"]["returns"]

        print("\n=== Secure Financial Metrics ===")

        # Compute Secure Average
        avg_return = secure_average(all_returns)
        print(f"Secure Average Return: {avg_return:.6f}")

        # Compute Secure Variance and Volatility
        variance = secure_variance(all_returns, avg_return)
        volatility = variance ** 0.5
        print(f"Secure Variance: {variance:.6f}")
        print(f"Secure Volatility: {volatility:.6f}")

        # Compute Secure Value at Risk (VaR)
        var = calculate_var_secure(all_returns)
        print(f"Secure Value at Risk (VaR): {var:.6f}")

        # Compute Expected Shortfall (ES)
        es = calculate_expected_shortfall(all_returns)
        print(f"Expected Shortfall (ES): {es:.6f}")

        # Compute Portfolio Beta
        beta = calculate_portfolio_beta(all_returns, market_returns)
        print(f"Portfolio Beta: {beta:.6f}")

        # Compute Correlation with Market
        correlation = calculate_correlation(all_returns, market_returns)
        print(f"Correlation with Market: {correlation:.6f}")

        # Visualize the distribution of returns
        visualize_returns(all_returns)

    finally:
        mpc.run(mpc.shutdown())

def visualize_returns(returns):
    """
    Plots the return distribution.
    """
    plt.hist(returns, bins=20, alpha=0.7, color='blue', edgecolor='black')
    plt.title('Portfolio Return Distribution')
    plt.xlabel('Return')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    end_to_end_workflow()