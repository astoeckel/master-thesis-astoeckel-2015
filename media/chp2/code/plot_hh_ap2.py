#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   PyNAM -- Python Neural Associative Memory Simulator and Evaluator
#   Copyright (C) 2015 Andreas Stöckel
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pyNN.nest as sim

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.colors as colors
import scipy.io as sio

def cm2inch(value):
    return value / 2.54

sim.setup(timestep=0.001, min_delay=0.1)

EIs =  [-61.0, 60.0, -88.0]
Enames = [
    "$E_{\\mathrm{Cl}^-}$",
    "$E_{\\mathrm{Na}^+}$",
    "$E_{\\mathrm{K}^+}$"]
ELeak = -70.0

tEnd = 10

cellparams = {
        'gbar_Na'   : 20.0,
        'gbar_K'    : 6.0,
        'g_leak'    : 0.1,
        'cm'        : 0.2,
        'v_offset'  : ELeak,
        'e_rev_Na'  : EIs[1],
        'e_rev_K'   : EIs[2],
        'e_rev_leak': ELeak,
        'e_rev_E'   : EIs[1],
        'e_rev_I'   : EIs[2],
        'tau_syn_E' : 0.2,
        'tau_syn_I' : 2.0,
        'i_offset'  : 0.0,
}

#vs = np.linspace(-75.0, EIs[0] + 5, 3)
vs = [-80.0, -61.0, -60.0]
neurons = [sim.create(sim.HH_cond_exp(**cellparams)) for _ in vs]
for i in xrange(len(vs)):
    neurons[i].record(["v"])
    neurons[i].initialize(v=vs[i])

sim.run(tEnd)

fig = plt.figure(figsize=(cm2inch(12.4), cm2inch(7)))
ax = fig.add_subplot(111)

#cmap = plt.cm.rainbow
#cmap = colors.LinearSegmentedColormap.from_list('blues', ['#729fcf', '#3465a4',
#        '#193a6b'])
lss = ['--', ':', '-']
#colors = iter(cmap(np.linspace(0, 1, len(vs))))
colors = iter(['#204a87'] * 3)
for i in xrange(len(vs)):
    data = neurons[i].get_data()
    signal_names = [s.name for s in data.segments[0].analogsignalarrays]
    vm = data.segments[0].analogsignalarrays[signal_names.index('v')]
    ax.plot(vm.times, vm, lss[i], color=next(colors),
            label="$u(0) = " + str(int(vs[i])) + "$ mV")

for i in xrange(len(EIs)):
    ax.plot([0, tEnd], [EIs[i], EIs[i]], '--', color='k', lw=0.5)
    ax.annotate(s=Enames[i], xy=(tEnd * 0.975, EIs[i]),
        verticalalignment="bottom", horizontalalignment="right")

ax.legend(loc='lower center', bbox_to_anchor=(0.45, 1.05), ncol=3)
ax.set_xlim(0, tEnd)
ax.set_ylim(-100, 80)
ax.set_xlabel("Time $t$ [ms]")
ax.set_ylabel("Membrane potential $u(t)$ [mV]")

fig.savefig("hh_ap2.pdf", format='pdf', bbox_inches='tight')

sim.end()

