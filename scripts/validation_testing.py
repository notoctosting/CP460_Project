from data_loader import load_data, get_all_returns
from financial_metrics import (
    calculate_var_secure, calculate_sharpe_ratio, calculate_expected_shortfall
)

# Plaintext counterparts for secure computations
def plaintext_var(returns, confidence_level=0.95):
    """
    Calculates Value at Risk (VaR) in plaintext.
    """
    sorted_returns = sorted(returns)
    var_index = int((1 - confidence_level) * len(sorted_returns))
    return sorted_returns[var_index]

def plaintext_expected_shortfall(returns, confidence_level=0.95):
    """
    Calculates Expected Shortfall (ES) in plaintext.
    """
    sorted_returns = sorted(returns)
    var_index = int((1 - confidence_level) * len(sorted_returns))
    tail_returns = sorted_returns[:var_index]
    return sum(tail_returns) / len(tail_returns)

def plaintext_sharpe_ratio(returns, risk_free_rate=0.02):
    """
    Calculates Sharpe Ratio in plaintext.
    """
    avg_return = sum(returns) / len(returns)
    variance = sum((x - avg_return) ** 2 for x in returns) / len(returns)
    volatility = variance ** 0.5
    if abs(volatility) < 1e-10:
        return None
    return (avg_return - risk_free_rate) / volatility

# Validation testing
if __name__ == "__main__":
    # Load data
    filepath = "../data/sample_data.json"
    data = load_data(filepath)
    all_returns = get_all_returns(data)

    # Compute secure results
    print("\n=== Secure Computations ===")
    var_secure = calculate_var_secure(all_returns)
    es_secure = calculate_expected_shortfall(all_returns)
    sharpe_secure = calculate_sharpe_ratio(all_returns)
    print(f"Secure VaR: {var_secure}")
    print(f"Secure ES: {es_secure}")
    print(f"Secure Sharpe Ratio: {sharpe_secure}")

    # Compute plaintext results
    print("\n=== Plaintext Computations ===")
    var_plaintext = plaintext_var(all_returns)
    es_plaintext = plaintext_expected_shortfall(all_returns)
    sharpe_plaintext = plaintext_sharpe_ratio(all_returns)
    print(f"Plaintext VaR: {var_plaintext}")
    print(f"Plaintext ES: {es_plaintext}")
    print(f"Plaintext Sharpe Ratio: {sharpe_plaintext}")

    # Compare results
    print("\n=== Comparison ===")
    print(f"VaR Difference: {abs(var_secure - var_plaintext):.6f}")
    print(f"ES Difference: {abs(es_secure - es_plaintext):.6f}")
    print(f"Sharpe Ratio Difference: {abs(sharpe_secure - sharpe_plaintext):.6f}")
