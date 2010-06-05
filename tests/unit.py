"""
Unit tests module
"""

import unittest
import math


class MetabatPopulation(unittest.TestCase):

    def setUp(self):
        from metabat import population
        from metabat.actors import create_population

        def observe(population, f):
            def wrap():
                print "Iteration %s" % population.step
                for i, bat in enumerate(population.bats):
                    print "  [%d] = %s" % (i, bat)
                f()
                print "  gbest: %s" % str(population.gbest)
                raw_input()
            return wrap


        # funkcja wartosciujaca nietoperza
        #self.sol = lambda x: math.sin(x.position*math.pi/180.0)
<<<<<<< HEAD
        #self.sol = lambda x:math.cos(x.position) * math.exp(math.sin(x.position)) * math.sin(x.position)  / 1.5
        #self.sol = lambda x:(-math.fabs(x.position)+1)
        self.sol = lambda x: (-(x.position-4)*(x.position-2)*(x.position-1)*x.position)
        self.p = population.Population(
            bats=create_population(n=10, position_unit_vector=10),
            freq_range=(0.01,0.3),
=======
        self.sol = lambda x:math.cos(x.position) * math.exp(math.sin(x.position)) * math.sin(x.position)  / 1.5
        #self.sol = lambda x: -1*(x.position-4)*(x.position-2)*(x.position-1)*x.position
        self.p = population.Population(
            bats=create_population(n=10, position_unit_vector=1),
            freq_range=(-0.3,0.3),
>>>>>>> a5b71f2d5da31549d7ea63cf6536d4f2d912d653
            sol = self.sol,
            a=0.9,
            g=0.9,
            )
        self.p.next = observe(self.p, self.p.next)

    def test_best_solution(self):
        print self.p.gbest
        for i in xrange(0,1000):
            self.p.next()
        print self.p.gbest


