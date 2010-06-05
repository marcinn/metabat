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

    # zakres czestotliwosci
    freq_range = (-0.3, 0.3)

    # stale chlodzace
    a=0.9
    g=0.9

    # ilosc nietoperzy
    n=10

    def __init__(self):

        self.sol = lambda x:math.cos(float(x)) * math.exp(math.sin(float(x))) * math.sin(float(x))  / 1.5
       

        self.gladefile = 'main.glade'
        self.wTree = gtk.glade.XML(self.gladefile)

        self.window = self.wTree.get_widget('window')
        if self.window:
            self.window.connect('destroy', gtk.main_quit)
        self.canvas = self.wTree.get_widget('canvas')
        self.log = self.wTree.get_widget('log')
        
        
        fig = Figure(figsize=(5,4), dpi=100)
	ax = fig.add_subplot(111)
	t = arange(-15.0,15.0,0.01)
	s = cos(t) * exp (sin(t)) * sin(t) / 1.5

	ax.plot(t,s)
        self.ax = ax

        self.canvas = FigureCanvas(fig)
        
        self.vbox = self.wTree.get_widget('vbox2')

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

        self.p = population.Population(
            bats=create_population(n=self.n, position_unit_vector=1),
            freq_range=self.freq_range,
            sol = self.sol,
            a=self.a,
            g=self.g,
            )
        self.p.next = observe(self.p, self.p.next)
        self.p.next()
        self.bg = self.ax.figure.canvas.copy_from_bbox(self.ax.bbox)
        self.draw_bats()

    def draw_bats(self):
        canvas = self.ax.figure.canvas
        canvas.restore_region(self.bg)
        for bat in self.p.bats:
            self.ax.plot(bat.position, self.sol(bat.position), 'o')
        canvas.draw()
        canvas.blit(self.ax.bbox)

    def next_iter(self, widget):
        self.p.next()
        self.draw_bats()

if __name__ == '__main__':
    app = MetabatApp()
    gtk.main()
