import pygtk
import gtk.glade

import math

from metabat import population
from metabat.actors import create_population

from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar

from matplotlib.figure import Figure
from numpy import arange, sin, pi, cos, exp

class MetabatApp(object):
    def __init__(self):
        self.gladefile = 'main.glade'
        self.wTree = gtk.glade.XML(self.gladefile)

        self.window = self.wTree.get_widget('window')
        if self.window:
            self.window.connect('destroy', gtk.main_quit)
        self.canvas = self.wTree.get_widget('canvas')
        self.log = self.wTree.get_widget('log')
        
        
        fig = Figure(figsize=(5,4), dpi=100)
	ax = fig.add_subplot(111)
	t = arange(0.0,3.0,0.01)
	s = cos(2*pi*t) * exp (sin(2*pi*t)) * sin(2*pi*t) / 1.5

	ax.plot(t,s)

        self.canvas = FigureCanvas(fig)
        
        self.vbox = self.wTree.get_widget('vbox1')

	self.vbox.pack_start(self.canvas)
	self.toolbar = NavigationToolbar(self.canvas, self.window)
	self.vbox.pack_start(self.toolbar, False, False)

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
            freq_range=(0,0.3),
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
