import pygtk
import gtk.glade

import math
import copy

from metabat import population
from metabat.actors import create_population

from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar

from matplotlib.figure import Figure
from numpy import arange, sin, pi, cos, exp

class MetabatApp(object):

    # zakres czestotliwosci
    freq_range = (0.1, 0.4)

    # dziedzina
    df = (-3.0, 4.0)

    # stale chlodzace
    a=0.9
    g=0.9

    # ilosc nietoperzy
    n=4


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
        self.ax = fig.add_subplot(111)
        self._figarrange = arange(-15.0,15.0,0.01)
        t = self._figarrange
        self._figfunc = cos(t) * exp (sin(t)) * sin(t) / 1.5

        self.canvas = FigureCanvas(fig)
        
        self.vbox = self.wTree.get_widget('vbox2')

        self.vbox.pack_start(self.canvas)
        self.toolbar = NavigationToolbar(self.canvas, self.window)
        self.vbox.pack_start(self.toolbar, False, False)

        self.wTree.get_widget('next_step').connect('clicked', self.next_iter)

        self.window.show_all()
        
        

        def observe(population, f):
            def wrap():
                f()
                text = "Iteration %s\n" % population.step
                for i, bat in enumerate(population.bats):
                    text += "  [%d] = %s\n" % (i, bat)
                text += "  gbest: %s\n" % str(population.gbest)
                self.log.get_buffer().set_text(text)
            return wrap

        bats = create_population(n=self.n, position_unit_vector=1, rndfactor=6)

        self.p = population.Population(
            bats=bats,
            freq_range=self.freq_range,
            sol = self.sol,
            df = self.df,
            a=self.a,
            g=self.g,
            )
        self.p.next = observe(self.p, self.p.next)
        self.p.next()
        self.draw_bats()

    def draw_bats(self):
        self.ax.clear()
        self.ax.plot(self._figarrange, self._figfunc)
        for i, bat in enumerate(self.p.bats):
            self.ax.plot(bat.position, self.sol(bat.position), 'o')
            self.ax.text(bat.position, self.sol(bat.position)+0.04,
                    '%s' % i, {'size': 7})
        self.ax.figure.canvas.draw()

    def next_iter(self, widget):
        self.p.next()
        self.draw_bats()

if __name__ == '__main__':
    app = MetabatApp()
    gtk.main()
