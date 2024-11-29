from hashlib import sha256
import random

class ZKP:
    """Zero-Knowledge Proof Protocol for MPC Verification."""
    
    @staticmethod
    def commit(value, nonce=None):
        """
        Generates a cryptographic commitment to a value.
        Args:
            value (int): The value to commit to.
            nonce (int): Optional random nonce. If not provided, a new one is generated.
        Returns:
            tuple: Commitment and nonce.
        """
        if nonce is None:
            nonce = random.randint(1, 1_000_000)
        commitment = sha256(f"{value}:{nonce}".encode()).hexdigest()
        return commitment, nonce

    @staticmethod
    def verify_commitment(commitment, value, nonce):
        """
        Verifies a commitment against a value and nonce.
        Args:
            commitment (str): The original commitment.
            value (int): The value to verify.
            nonce (int): The nonce used in the original commitment.
        Returns:
            bool: True if the commitment is valid, False otherwise.
        """
        recalculated = sha256(f"{value}:{nonce}".encode()).hexdigest()
        return recalculated == commitment

    @staticmethod
    def prove_sum(shares, claimed_sum):
        """
        Simulates a proof that the sum of shares equals the claimed result.
        Args:
            shares (list): List of integer shares.
            claimed_sum (int): The sum to prove.
        Returns:
            bool: True if the proof is valid, False otherwise.
        """
        return sum(shares) == claimed_sum
