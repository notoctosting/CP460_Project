import unittest
from scripts.zkp_verification import generate_proof, verify_proof

class TestZKPVerification(unittest.TestCase):
    def test_generate_proof(self):
        proof = generate_proof(0.04, 0.04)
        self.assertTrue(proof)

    def test_verify_proof(self):
        proof = generate_proof(0.04, 0.04)
        verified = verify_proof(proof)
        self.assertTrue(verified)

if __name__ == "__main__":
    unittest.main()
