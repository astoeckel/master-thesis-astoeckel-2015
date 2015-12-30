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

import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.colors as colors
import scipy.io as sio

def cm2inch(value):
    return value / 2.54

if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " <FILENAME1> ... <FILENAME2>")
    sys.exit(1)

fig = plt.figure(figsize=(cm2inch(12.4), cm2inch(4)))
ax = fig.add_subplot(1, 1, 1)

for i in xrange(1, len(sys.argv)):
    data = np.genfromtxt(sys.argv[i], delimiter=',', names=True)
    ax.plot(data['t'] * 1000.0, data['v'] * 1000.0, lw=0.75, color='000000')

    if i == 1:
        tEnd = 30
        tSpikes = data['t'][np.diff(data['gE']) > 1e-10]
        for t in tSpikes:
            ax.plot([t * 1000, t * 1000], [-1000, 1000], ':', color='k', lw=0.25)
        ax.set_xlim(0, tEnd)
        ax.set_ylim(-80, 20)
        ax.set_xlabel("$t$ [ms]")
        ax.set_ylabel("$u(t)$ [mV]")

fig.savefig(sys.argv[1] + ".pdf", format='pdf', bbox_inches='tight')

