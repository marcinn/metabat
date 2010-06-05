import pygtk
import gtk.glade

import math

from metabat import population
from metabat.actors import create_population

class MetabatApp(object):
    def __init__(self):
        self.gladefile = 'main.glade'
        self.wTree = gtk.glade.XML(self.gladefile)

        self.window = self.wTree.get_widget('window')
        if self.window:
            self.window.connect('destroy', gtk.main_quit)
        self.canvas = self.wTree.get_widget('canvas')
        self.log = self.wTree.get_widget('log')

        self.wTree.get_widget('next_step').connect('clicked', self.next_iter)

        self.window.show_all()

        def observe(population, f):
            def wrap():
                text = "Iteration %s\n" % population.step
                for i, bat in enumerate(population.bats):
                    text += "  [%d] = %s\n" % (i, bat)
                f()
                text += "  gbest: %s\n" % str(population.gbest)
                self.log.get_buffer().set_text(text)
            return wrap

        self.sol = lambda x:math.cos(x.position) * math.exp(math.sin(x.position)) * math.sin(x.position)  / 1.5
        self.p = population.Population(
            bats=create_population(n=10, position_unit_vector=1),
            freq_range=(-0.3,0.3),
            sol = self.sol,
            a=0.9,
            g=0.9,
            )
        self.p.next = observe(self.p, self.p.next)
        self.p.next()

    def next_iter(self, widget):
        self.p.next()

if __name__ == '__main__':
    app = MetabatApp()
    gtk.main()
