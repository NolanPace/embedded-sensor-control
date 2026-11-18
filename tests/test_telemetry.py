import unittest
from telemetry import parse,simulate,summary
class TelemetryTests(unittest.TestCase):
    def test_parse(self):
        x=parse('100,1.2500,1.1250,0.5800')
        self.assertEqual(x.timestamp_ms,100);self.assertAlmostEqual(x.voltage,1.25)
    def test_invalid(self):
        for line in ('bad','1,2,3,4','3,-1,1,.5','0,1,1,2'):
            with self.assertRaises(ValueError):parse(line)
    def test_reproducible(self):
        a=list(simulate(50,7));b=list(simulate(50,7))
        self.assertEqual(a,b);self.assertEqual(summary(a)['samples'],50)
        self.assertTrue(all(0<=r.control_output<=1 for r in a))
    def test_empty(self):
        self.assertEqual(summary([])['samples'],0)
if __name__=='__main__':unittest.main()
