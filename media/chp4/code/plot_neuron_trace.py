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
import matplotlib.colors as colors
import scipy.io as sio

def cm2inch(value):
    return value / 2.54

dataLIF = np.genfromtxt('demo_lif.csv', delimiter=',', names=True)
dataAdEx = np.genfromtxt('demo_adex.csv', delimiter=',', names=True)

tSpikes = np.linspace(5, 65, 13)
tEnd = 80

ELabelsLIF = ["$E_\mathrm{L}$", "$E_\mathrm{e}$", "$E_\mathrm{Th}$"]
ELIF = [-70, 0, -54]

ELabelsAdEx = ["$E_\mathrm{L}$", "$E_\mathrm{e}$", "$E_\mathrm{Th}^\mathrm{exp}$"]
EAdEx = [-70, 0, -54]

fig = plt.figure(figsize=(cm2inch(12.4), cm2inch(12)))

ax = fig.add_subplot(311)
lw = 0.75
for t in tSpikes:
    ax.plot([t, t], [-1000, 1000], ':', color='k', lw=0.25)
for i in xrange(len(ELIF)):
    ax.plot([0, tEnd], [ELIF[i], ELIF[i]], '--', color='k', lw=0.25)
    ax.annotate(s=ELabelsLIF[i], xy=(tEnd * 0.975, ELIF[i]),
        verticalalignment="bottom", horizontalalignment="right")
ax.plot(dataLIF['t'] * 1000.0, dataLIF['v'] * 1000.0, lw=lw, color='#000000')
ax.set_xlim(0, tEnd)
ax.set_ylim(-80, 20)
ax.set_xticklabels([])
ax.set_ylabel("LIF $u(t)$ [mV]")

ax = fig.add_subplot(312)
for t in tSpikes:
    ax.plot([t, t], [-1000, 1000], ':', color='k', lw=0.25)
for i in xrange(len(EAdEx)):
    ax.plot([0, tEnd], [EAdEx[i], EAdEx[i]], '--', color='k', lw=0.25)
    ax.annotate(s=ELabelsAdEx[i], xy=(tEnd * 0.975, EAdEx[i]),
        verticalalignment="bottom", horizontalalignment="right")
ax.plot(dataAdEx['t'] * 1000.0, dataAdEx['v'] * 1000.0, lw=lw, color='#000000')
ax.set_xlim(0, tEnd)
ax.set_ylim(-80, 20)
ax.set_xticklabels([])
ax.set_ylabel("AdEx $u(t)$ [mV]")

ax = fig.add_subplot(313)
for t in tSpikes:
    ax.plot([t, t], [-1000, 1000], ':', color='k', lw=0.25)
ax.plot(dataAdEx['t'] * 1000.0, dataAdEx['gE'] * 1000.0 * 1000.0, lw=lw, color='#000000')

ax.set_xlim(0, tEnd)
ax.set_ylim(0, 0.12)
ax.set_xlabel("Time $t$ [ms]")
ax.set_ylabel("$g_{\mathrm{E}}(t)$ [$\mu$S]")

fig.savefig("lif_vs_adex.pdf", format='pdf', bbox_inches='tight')

