from mpc_protocol import secure_average, secure_variance, scale_to_fixed, scale_to_float, secure_sum
from data_loader import load_data, get_all_returns
from zkp_protocol import ZKP

from mpyc.runtime import mpc
from mpc_protocol import scale_to_fixed, scale_to_float, SecInt32
from pysnark.runtime import PrivVal, snark
from pysnark.hash import snarkhash


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

    Args:
        returns (list): List of portfolio returns.
        confidence_level (float): Confidence level for ES (default 95%).

    Returns:
        float: Securely computed Expected Shortfall.
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

    Args:
        portfolio_returns (list): Portfolio returns.
        market_returns (list): Market index returns.

    Returns:
        float: Portfolio Beta.
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

    Args:
        data1, data2 (list): Datasets to calculate correlation for.

    Returns:
        float: Correlation coefficient.
    """
    avg1 = secure_average(data1)
    avg2 = secure_average(data2)

    covariance = secure_sum(
        [(x - avg1) * (y - avg2) for x, y in zip(data1, data2)]
    ) / len(data1)

    variance1 = secure_variance(data1, avg1)
    variance2 = secure_variance(data2, avg2)

    return covariance / (variance1 ** 0.5 * variance2 ** 0.5)




def zkp_verify_average(returns):
    """
    Securely computes the average using PySNARK and verifies correctness with ZKP.
    Args:
        returns (list): List of portfolio returns.
    Returns:
        float: Securely computed average.
    """
    # Convert values to PySNARK private values
    private_values = [PrivVal(v) for v in returns]

    # Compute the sum of private values
    total_sum = sum(private_values)

    # Compute the average
    avg = total_sum / len(private_values)

    # ZKP verification (commitment to total_sum)
    snarkhash(total_sum)  # Creates a commitment to the computed sum

    # Return the average
    return avg.val


def zkp_secure_sum(values):
    """
    Securely computes the sum of a list of values using PySNARK.
    """
    # Convert values to PySNARK private values
    private_values = [PrivVal(v) for v in values]

    # Compute the secure sum
    total_sum = sum(private_values)

    # ZKP verification for the sum
    snarkhash(total_sum)  # Generate commitment to sum for verification

    # Return the sum
    return total_sum.val


if __name__ == "__main__":
    # Load returns
    filepath = "../data/sample_data.json"
    data = load_data(filepath)
    all_returns = get_all_returns(data)

    # Calculate secure metrics with ZKP verification
    avg_return = zkp_verify_average(all_returns)
    secure_sum = zkp_secure_sum(all_returns)

    print(f"Secure Average Return with ZKP: {avg_return}")
    print(f"Secure Sum with ZKP: {secure_sum}")