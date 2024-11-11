# CP460_Project
# Secure Multi-Party Computation for Privacy-Preserving Financial Metrics

## Overview
This project implements Secure Multi-Party Computation (MPC) for calculating key financial metrics such as Value at Risk (VaR), Sharpe Ratio, and Maximum Drawdown while preserving the privacy of each participating party’s data. Optionally, it includes Zero-Knowledge Proofs (ZKP) for verifiability.

## Installation
To set up the environment:
```bash
python3 -m venv mpc_env
source mpc_env/bin/activate
pip install -r requirements.txt
```

## Usage
Run the example notebook examples/example_run.ipynb to see the complete workflow or use the scripts as follows:

1. Load sample data with data_loader.py.
2. Use mpc_protocol.py to initialize and execute the MPC.
3. Compute financial metrics with financial_metrics.py.
4. Run tests in tests/ to validate functionality.