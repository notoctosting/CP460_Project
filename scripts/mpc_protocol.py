from mpyc.runtime import mpc
from data_loader import load_data, get_all_returns

# Define a secure integer type with a bit length of 32
SecInt32 = mpc.SecInt(32)  # Secure 32-bit integer type

# Scaling factor for fixed-point arithmetic
SCALING_FACTOR = 10**4

def initialize_mpc():
    """Initializes the MPyC environment."""
    mpc.run(mpc.start())

def shutdown_mpc():
    """Shuts down the MPyC environment."""
    mpc.run(mpc.shutdown())

def scale_to_fixed(values):
    """Scales floating-point values to fixed-point integers."""
    return [int(value * SCALING_FACTOR) for value in values]

def scale_to_float(value):
    """Scales fixed-point integers back to floating-point numbers."""
    return value / SCALING_FACTOR

def secure_average(values):
    """Securely computes the average of a list of values."""
    fixed_values = scale_to_fixed(values)
    secure_values = [SecInt32(value) for value in fixed_values]
    shares = [mpc.input(value, senders=[0]) for value in secure_values]
    secure_shares = [s[0] for s in shares]
    total_fixed = mpc.run(mpc.output(mpc.sum(secure_shares)))
    avg_fixed = total_fixed // len(secure_shares)
    return scale_to_float(avg_fixed)

def secure_variance(values, mean):
    """
    Securely computes the variance of a list of values.

    Variance formula: sum((x - mean)^2) / n
    """
    fixed_values = scale_to_fixed(values)
    fixed_mean = int(mean * SCALING_FACTOR)
    secure_values = [SecInt32(value) for value in fixed_values]
    shares = [mpc.input(value, senders=[0]) for value in secure_values]
    secure_shares = [s[0] for s in shares]

    # Compute sum of squared deviations
    squared_differences = [(x - fixed_mean) ** 2 for x in secure_shares]
    total_squared_differences = mpc.run(mpc.output(mpc.sum(squared_differences)))

    # Divide by n and adjust scaling factor
    variance_fixed = total_squared_differences // len(secure_shares)
    variance = scale_to_float(variance_fixed) / SCALING_FACTOR  # Adjust scaling for squared values
    return variance

def secure_sum(values):
    """Securely computes the sum of a list of values."""
    fixed_values = scale_to_fixed(values)
    secure_values = [SecInt32(value) for value in fixed_values]
    shares = [mpc.input(value, senders=[0]) for value in secure_values]
    secure_shares = [s[0] for s in shares]
    total_fixed = mpc.run(mpc.output(mpc.sum(secure_shares)))
    return scale_to_float(total_fixed)

# Example usage
if __name__ == "__main__":
    initialize_mpc()
    try:
        example_returns = [0.05, 0.03, -0.01, 0.04, 0.02, 0.01, -0.01, 0.01, 0.03]

        # Compute secure average and variance
        avg_return = secure_average(example_returns)
        variance = secure_variance(example_returns, avg_return)

        print(f"Average Return (MPC): {avg_return}")
        print(f"Variance (MPC): {variance}")
    finally:
        shutdown_mpc()
