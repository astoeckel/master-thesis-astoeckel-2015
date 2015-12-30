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

tEnd = 16.0

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

neuron1 = sim.create(sim.HH_cond_exp(**cellparams))
neuron1.record(["v"])
neuron1.initialize(v=cellparams["e_rev_leak"])

neuron2 = sim.create(sim.HH_cond_exp(**cellparams))
neuron2.record(["v"])
neuron2.initialize(v=cellparams["e_rev_leak"])


spike_times = [2.0]
spike_source = sim.Population(1, sim.SpikeSourceArray(spike_times=spike_times))

sim.Projection(spike_source, neuron1, sim.OneToOneConnector(),
                            sim.StaticSynapse(weight=0.076, delay=0.1),
                            receptor_type='excitatory'),
sim.Projection(spike_source, neuron2, sim.OneToOneConnector(),
                            sim.StaticSynapse(weight=0.0755, delay=0.1),
                            receptor_type='excitatory'),


sim.run(tEnd)

data1 = neuron1.get_data()
data2 = neuron2.get_data()

signal_names = [s.name for s in data1.segments[0].analogsignalarrays]

fig = plt.figure(figsize=(cm2inch(12.4), cm2inch(7)))
ax = fig.add_subplot(111)

vm1 = data1.segments[0].analogsignalarrays[signal_names.index('v')]
vm2 = data2.segments[0].analogsignalarrays[signal_names.index('v')]
ax.plot(vm1.times, vm1, color='#204a87', zorder=1, label="Action potential")
ax.plot(vm2.times, vm2, color='#3465a4', lw=0.75, zorder=0, label="Failed initiation")

for i in xrange(len(EIs)):
    ax.plot([0, tEnd], [EIs[i], EIs[i]], '--', color='k', lw=0.5)
    ax.annotate(s=Enames[i], xy=(tEnd * 0.975, EIs[i]),
        verticalalignment="bottom", horizontalalignment="right")
for t in spike_times:
    ax.plot([t, t], [-1000, 1000], ':', color='k', lw=0.5)

ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.05), ncol=2)
ax.set_xlim(0, tEnd)
ax.set_ylim(-100, 80)
ax.set_xlabel("Time $t$ [ms]")
ax.set_ylabel("Membrane potential $u(t)$ [mV]")

fig.savefig("hh_ap.pdf", format='pdf', bbox_inches='tight')

sim.end()

