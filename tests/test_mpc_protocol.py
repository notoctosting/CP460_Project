import unittest
from scripts.mpc_protocol import initialize_mpc, compute_mpc_average

class TestMPCProtocol(unittest.TestCase):
    def test_compute_mpc_average(self):
        initialize_mpc()
        values = [0.05, 0.04, -0.01]
        avg = compute_mpc_average(values)
        self.assertAlmostEqual(avg, 0.0267, places=3)
        mpc.shutdown()

if __name__ == "__main__":
    unittest.main()
