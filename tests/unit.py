"""
Unit tests module
"""

import unittest
import math

class MetabatCoreTestCase(unittest.TestCase):
    """
    core metaheuristic bat-like algorithm test case
    """


    def test_actors(self):

        from metabat.actors import Microbat

        actor = Microbat(0,0)
        self.assertEqual(actor.loudness_range, 
                (Microbat.LOUDNESS_MIN, Microbat.LOUDNESS_MAX))

        # test frequency property
        try:
            actor.frequency = Microbat.FREQUENCY_MAX-1
            self.assertEqual(actor.frequency, Microbat.FREQUENCY_MAX-1)
        except ValueError:
            self.fail('Freqency setter failed')

        try:
            actor.frequency = Microbat.FREQUENCY_MAX+1
            self.fail('Frequency limiter failed')
        except ValueError:
            pass


        try:
            actor.frequency = Microbat.FREQUENCY_MAX
            self.assertEqual(actor.frequency, Microbat.FREQUENCY_MAX)
        except ValueError:
            self.fail('Cannot set MAX_FREQUENCY')


        # test loudness property

        try:
            min, max = actor.loudness_range
            actor.loudness = min
            actor.loudness = max
            actor.loudness = min+1
            actor.loudness = max-1
        except ValueError:
            self.fail('Cannot set loudness in defined range')

        min, max = actor.loudness_range

        try:
            actor.loudness = min-1
            self.fail('Loudness limiter failed')
        except ValueError:
            pass

        try:
            actor.loudness = max+1
            self.fail('Loudness limiter failed')
        except ValueError:
            pass



class MetabatPopulation(unittest.TestCase):

    def setUp(self):
        from metabat import population
        from metabat.actors import create_population

        # funkcja wartosciujaca nietoperza
        self.sol = lambda x: math.sin(x.position*math.pi/180.0)
        self.p = population.Population(create_population(10,10),
                (0,100), self.sol)

    def test_best_solution(self):
        print self.p.best_solution
        for i in xrange(0,100):
            self.p.next()
        print self.p.best_solution


