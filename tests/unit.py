"""
Unit tests module
"""

import unittest

class MetabatCoreTestCase(unittest.TestCase):
    """
    core metaheuristic bat-like algorithm test case
    """


    def test_actors(self):

        from metabat.actors import Microbat

        actor = Microbat()
        self.assertEqual(actor.frequency, 0)
        self.assertEqual(actor.pulse_rate, 0.0)
        self.assertEqual(actor.loudness_range, 
                (Microbat.LOUDNESS_MIN, Microbat.LOUDNESS_MAX))

        # test frequency property
        try:
            actor.frequency = Microbat.MAX_FREQUENCY-1
            self.assertEqual(actor.frequency, Microbat.MAX_FREQUENCY-1)
        except ValueError:
            self.fail('Freqency setter failed')

        try:
            actor.frequency = Microbat.MAX_FREQUENCY+1
            self.fail('Frequency limiter failed')
        except ValueError:
            pass


        try:
            actor.frequency = Microbat.MAX_FREQUENCY
            self.assertEqual(actor.frequency, Microbat.MAX_FREQUENCY)
        except ValueError:
            self.fail('Cannot set MAX_FREQUENCY')
