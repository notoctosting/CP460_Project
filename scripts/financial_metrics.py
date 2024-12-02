from mpc_protocol import secure_average, secure_variance, scale_to_fixed, scale_to_float, secure_sum
from data_loader import load_data, get_all_returns

from mpyc.runtime import mpc
from mpc_protocol import scale_to_fixed, scale_to_float, SecInt32



def calculate_var_secure(returns, confidence_level=0.95):
    """
    Securely calculates Value at Risk (VaR) using MPC.
    """
    fixed_returns = scale_to_fixed(returns)
    secure_returns = [SecInt32(r) for r in fixed_returns]

    # Secure sorting (simulate for now)
    sorted_returns = mpc.run(mpc.output(mpc.sorted(secure_returns)))

    # Calculate index for VaR
    var_index = int((1 - confidence_level) * len(sorted_returns))
    secure_var_fixed = sorted_returns[var_index]

    return scale_to_float(secure_var_fixed)

def calculate_sharpe_ratio(returns, risk_free_rate=0.02):
    """
    Securely calculates the Sharpe Ratio.
    """
    avg_return = secure_average(returns)
    variance = secure_variance(returns, avg_return)
    volatility = variance ** 0.5  # Volatility = sqrt(variance)

    if abs(volatility) < 1e-10:  # Handle near-zero volatility
        print("Volatility is near zero; Sharpe Ratio cannot be computed.")
        return None

    return (avg_return - risk_free_rate) / volatility

def calculate_expected_shortfall(returns, confidence_level=0.95):
    """
    Securely computes the Expected Shortfall (ES) for a portfolio.
    """
    fixed_returns = scale_to_fixed(returns)
    secure_returns = [SecInt32(r) for r in fixed_returns]

    # Secure sorting
    sorted_returns = mpc.sorted(secure_returns)

    # Compute the index for VaR
    var_index = int((1 - confidence_level) * len(sorted_returns))

    # Secure slicing of returns below the VaR threshold
    tail_returns = sorted_returns[:var_index]

    # Securely compute the sum of tail losses
    total_tail_loss = mpc.run(mpc.output(mpc.sum(tail_returns)))
    avg_tail_loss = total_tail_loss // len(tail_returns)

    # Convert back to floating-point
    return scale_to_float(avg_tail_loss)

def plaintext_expected_shortfall(returns, confidence_level=0.95):
    sorted_returns = sorted(returns)
    var_index = int((1 - confidence_level) * len(sorted_returns))
    tail_returns = sorted_returns[:var_index]
    return sum(tail_returns) / len(tail_returns)

def calculate_portfolio_beta(portfolio_returns, market_returns):
    """
    Calculates Portfolio Beta as Covariance(portfolio, market) / Variance(market).
    """
    avg_portfolio = secure_average(portfolio_returns)
    avg_market = secure_average(market_returns)

    # Secure covariance
    covariance = secure_sum(
        [(p - avg_portfolio) * (m - avg_market) for p, m in zip(portfolio_returns, market_returns)]
    ) / len(portfolio_returns)

    # Secure variance of market returns
    market_variance = secure_variance(market_returns, avg_market)

    return covariance / market_variance

def calculate_correlation(data1, data2):
    """
    Calculates the correlation between two datasets.
    """
    avg1 = secure_average(data1)
    avg2 = secure_average(data2)

    covariance = secure_sum(
        [(x - avg1) * (y - avg2) for x, y in zip(data1, data2)]
    ) / len(data1)

    variance1 = secure_variance(data1, avg1)
    variance2 = secure_variance(data2, avg2)

    return covariance / (variance1 ** 0.5 * variance2 ** 0.5)



# if __name__ == "__main__":
#     # Load returns
#     filepath = "../data/sample_data.json"
#     data = load_data(filepath)
#     all_returns = get_all_returns(data)

#     print("\n=== Secure Financial Metrics ===")
#     # Calculate Value at Risk (VaR)
#     secure_var = calculate_var_secure(all_returns)
#     print(f"Secure VaR (95%): {secure_var:.6f}")

#     # Calculate Expected Shortfall (ES)
#     secure_es = calculate_expected_shortfall(all_returns)
#     print(f"Secure Expected Shortfall (95%): {secure_es:.6f}")

#     # Calculate Sharpe Ratio
#     secure_sharpe = calculate_sharpe_ratio(all_returns)
#     print(f"Secure Sharpe Ratio: {secure_sharpe:.6f}")

#     # Calculate Portfolio Beta
#     portfolio_returns = all_returns["Portfolio"]
#     market_returns = all_returns["Market"]

#     secure_beta = calculate_portfolio_beta(portfolio_returns, market_returns)
#     print(f"Secure Portfolio Beta: {secure_beta:.6f}")

