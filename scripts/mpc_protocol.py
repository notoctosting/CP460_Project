from mpyc.runtime import mpc

def initialize_mpc():
    """Initializes the MPyC environment."""
    mpc.start()

def compute_mpc_average(values):
    """Securely computes the average of a list of values using MPC."""
    shares = [mpc.input(value) for value in values]
    avg = mpc.run(mpc.output(sum(shares) / len(shares)))
    return avg

# Example usage:
if __name__ == "__main__":
    initialize_mpc()
    values = [0.05, 0.04, -0.01]  # Example returns
    avg_return = compute_mpc_average(values)
    print(f"Average Return (MPC): {avg_return}")
    mpc.shutdown()