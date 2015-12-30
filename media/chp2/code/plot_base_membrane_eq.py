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

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import scipy.io as sio

def cm2inch(value):
    return value / 2.54

def sim(v0, gIs, EIs, CM, tEnd):
    deltaT = 1e-5
    ts = np.arange(0, tEnd, deltaT)
    vs = np.zeros(len(ts))
    v = v0
    for i in xrange(len(ts)):
        v = v + deltaT * np.sum((EIs - v) * gIs) / CM
        vs[i] = v
    return ts, vs

def plot_sim(v0s, gIs, EIs, Enames, title = "", EeqPos = 0.15, CM = 1.0e-9, tEnd = 0.1):
    gIs = np.array(gIs)
    EIs = np.array(EIs)

    fig = plt.figure(figsize=(cm2inch(5.5), cm2inch(5.5)))
    ax = fig.add_subplot(111)
    for v0 in v0s:
        ts, vs = sim(v0, gIs, EIs, CM, tEnd)
        ax.plot(ts, vs, zorder=0, color='#3465a4')

    Eeq = np.sum(gIs * EIs) / np.sum(gIs)
    ax.plot([0, tEnd], [Eeq, Eeq], ':', color='k')
    ax.annotate(s="$E_{\\mathrm{eq}}$", xy=(tEnd * EeqPos, Eeq),
        verticalalignment="bottom", horizontalalignment="left")
    for i in xrange(len(EIs)):
        ax.plot([0, tEnd], [EIs[i], EIs[i]], '--', color='k', lw=0.5)
        ax.annotate(s=Enames[i], xy=(tEnd * 0.975, EIs[i]),
            verticalalignment="bottom", horizontalalignment="right")

    ax.annotate(s=title, xy=(tEnd * 0.25, 0.03),
            verticalalignment="top", horizontalalignment="left")

    ax.set_xlim(0, tEnd)
    ax.set_ylim(-0.09, 0.08)
    ax.xaxis.set_ticks(np.linspace(0, tEnd, 3))
    ax.yaxis.set_ticks(np.arange(-0.08, 0.12, 0.04))
    ax.set_xlabel("Time $t$ [s]")
    ax.set_ylabel("Membrane potential $u(t)$ [V]")
    return fig


EIs =  [-0.061, 0.06, -0.088]
Enames = [
    "$E_{\\mathrm{Cl}^-}$",
    "$E_{\\mathrm{Na}^+}$",
    "$E_{\\mathrm{K}^+}$"]
v0s = np.linspace(np.min(EIs), np.max(EIs), 3)

plot_sim(v0s, [0.0e-6, 0.00e-6, 0.05e-6], EIs, Enames,
    title="$g_{\\mathrm{K}^+} = 0.05 \, \mu\mathrm{S}$")\
    .savefig("base_membrane_eq1.pdf", format='pdf', bbox_inches='tight')

plot_sim(v0s, [0.00e-6, 0.3e-6, 0.05e-6], EIs, Enames,
    title="$g_{\\mathrm{K}^+} \,\,\, = 0.05 \, \mu\mathrm{S}$\n" +
          "$g_{\\mathrm{Na}^+} = 0.3 \, \mu\mathrm{S}$")\
    .savefig("base_membrane_eq2.pdf", format='pdf', bbox_inches='tight')

plot_sim(v0s, [0.1e-6, 0.0e-6, 0.05e-6], EIs, Enames, EeqPos=0.4,
    title="$g_{\\mathrm{K}^+} \, = 0.05 \, \mu\mathrm{S}$\n" +
          "$g_{\\mathrm{Cl}^-} = 0.1 \, \mu\mathrm{S}$")\
    .savefig("base_membrane_eq3.pdf", format='pdf', bbox_inches='tight')

plot_sim(v0s, [0.05e-6, 0.05e-6, 0.05e-6], EIs, Enames, EeqPos=0.4,
    title="$g_{\\mathrm{K}^+} \,\,\, = 0.05 \, \mu\mathrm{S}$\n" +
          "$g_{\\mathrm{Na}^+} = 0.05 \, \mu\mathrm{S}$\n" +
          "$g_{\\mathrm{Cl}^-} \,\, = 0.05 \, \mu\mathrm{S}$")\
    .savefig("base_membrane_eq4.pdf", format='pdf', bbox_inches='tight')


plt.show()
