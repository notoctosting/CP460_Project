def calculate_var(returns, confidence_level=0.95):
    """Calculates Value at Risk (VaR) at the specified confidence level."""
    sorted_returns = sorted(returns)
    var_index = int((1 - confidence_level) * len(sorted_returns))
    return sorted_returns[var_index]

def calculate_sharpe_ratio(returns, risk_free_rate=0.02):
    """Calculates the Sharpe Ratio."""
    avg_return = sum(returns) / len(returns)
    volatility = (sum([(r - avg_return) ** 2 for r in returns]) / len(returns)) ** 0.5
    return (avg_return - risk_free_rate) / volatility

# Example usage:
if __name__ == "__main__":
    returns = [0.05, 0.04, -0.01]
    var = calculate_var(returns)
    sharpe_ratio = calculate_sharpe_ratio(returns)
    print(f"VaR: {var}, Sharpe Ratio: {sharpe_ratio}")
