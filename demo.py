import pygtk
import gtk.glade
import gobject

import math
import copy

from metabat import population
from metabat.actors import create_population

from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar

from matplotlib.figure import Figure
from numpy import arange, sin, pi, cos, exp, power, ndarray, array


FUNC = lambda t: (cos(t) * exp (sin(t)) * sin(t)) / 1.5

class MetabatApp(object):

    # zakres czestotliwosci
    freq_range = (0.01, 0.1)

    # dziedzina
    df = (-3.0, 4.0)

    # stale chlodzace
    a=0.9
    g=0.9

    # ilosc nietoperzy
    n=4


    def __init__(self, func):

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

        self.sol = func
        self._figfunc = array([func(i) for i in t])

        self.canvas = FigureCanvas(fig)
        
        self.vbox = self.wTree.get_widget('vbox2')

        self.vbox.pack_start(self.canvas)
        self.toolbar = NavigationToolbar(self.canvas, self.window)
        self.vbox.pack_start(self.toolbar, False, False)

        self.wTree.get_widget('next_step').connect('clicked', self.next_iter)
        self.wTree.get_widget('btn_play').connect('clicked', self.play)
        self.wTree.get_widget('btn_stop').connect('clicked', self.stop)
        self.wTree.get_widget('btn_reset').connect('clicked', self.reset)
        self.wTree.get_widget('sb_batsnum').set_value(self.n)
        self.wTree.get_widget('sb_freqfrom').set_value(self.freq_range[0])
        self.wTree.get_widget('sb_freqto').set_value(self.freq_range[1])
        self.wTree.get_widget('sb_domainfrom').set_value(self.df[0])
        self.wTree.get_widget('sb_domainto').set_value(self.df[1])
        self.wTree.get_widget('bt_applysettings').connect('clicked', self.change_config)
        self.statusbar = self.wTree.get_widget('statusbar')

        self.window.show_all()
        self.initialize()
        

    def initialize(self):

        self._play = False
        def observe(population, f):
            def wrap():
                f()
                text = "Iteration %s\n" % population.step
                for i, bat in enumerate(population.bats):
                    text += "  [%d] = %s\n" % (i, bat)
                text += "  gbest: %s\n" % str(population.gbest)
                self.log.get_buffer().set_text(text)
                ctx = self.statusbar.get_context_id('global')
                self.statusbar.push(ctx, 'Avg loudness: %.4f   pbest: %s   gbest: %s' % \
                        (population.average_loudness, str(population.pbest), str(population.gbest)))
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
        self.ax.plot((self.df[0], self.df[0]), (-1,1), color="red")
        self.ax.plot((self.df[1], self.df[1]), (-1,1), color="red")
        self.ax.plot(self._figarrange, self._figfunc, color="blue")
        for i, bat in enumerate(self.p.bats):
            self.ax.plot(bat.position, self.sol(bat.position), 'o')
            self.ax.text(bat.position, self.sol(bat.position)+0.04,
                    '%s' % i, {'size': 7})
        self.ax.figure.canvas.draw()

    def next_iter(self, widget):
        self.p.next()
        self.draw_bats()

    def play(self, widget):
        self._play = True
        gobject.timeout_add(60, self.play_frame)

    def reset(self, widget):
        self.initialize()

    def stop(self, widget):
        self._play = False

    def play_frame(self):
        if self._play:
            self.p.next()
            self.draw_bats()
            self.log.queue_draw()
            return True
        return False

    def change_config(self, widget):
        self.n = int(self.wTree.get_widget('sb_batsnum').get_value())
        self.freq_range=self.wTree.get_widget('sb_freqfrom').get_value(),\
                self.wTree.get_widget('sb_freqto').get_value()
        self.df=self.wTree.get_widget('sb_domainfrom').get_value(),\
                self.wTree.get_widget('sb_domainto').get_value()
                
        self.wTree.get_widget('sb_freqto').set_value(self.freq_range[1])
        self.initialize()
    

if __name__ == '__main__':
    app = MetabatApp(FUNC)
    gtk.main()
