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
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import scipy.io as sio

def cm2inch(value):
    return value / 2.54

if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " <FILENAME>")
    sys.exit(1)

data = np.loadtxt(sys.argv[1], delimiter='\t')

fig = plt.figure(figsize=(cm2inch(13.5), cm2inch(7)))
gs = gridspec.GridSpec(2, 1, height_ratios=[6,1])

ax = fig.add_subplot(gs[0])
xs = data[:, 0] * 1000.0 * 1000.0
ax.plot(xs, data[:, 1], '-', dashes=[3, 1], color='k', linewidth=0.5)
ax.plot(xs, data[:, 3], color='#3465a4', linewidth=0.5)
ax.set_xlim([0, 1])
ax.set_xticks([])
ax.set_yticks([0, 1, 2, 3, 4, 5, 6])

l1 = plt.Line2D((0,1),(0,0), linestyle='-', dashes=[3, 1], color='k', linewidth=0.5)
l2 = plt.Line2D((0,1),(0,0), color='#3465a4', linewidth=0.5)
l3 = plt.Line2D((0,1),(0,0), color='k', linewidth=0.5)
ax.legend(
        [l1, l2, l3],
        ["$n^\\mathrm{out}(g_\\mathrm{L})$",
         "$q^\\mathrm{out}(g_\\mathrm{L})$",
         "$p^\\mathrm{out}(g_\\mathrm{L})$"],
         loc='lower center', bbox_to_anchor=(0.5, 1.05), ncol=3)

ax = fig.add_subplot(gs[1])
ax.plot(xs, data[:, 2], color='k', linewidth=0.5)
ax.set_ylim([0, 1])
ax.set_yticks([0, 1])
ax.set_xlim([0, 1])
ax.set_xlabel("Parameter $g_\\mathrm{L}$ [$\\mu$S]")

fig.savefig("sweep_min_apices.pdf", format='pdf', bbox_inches='tight')

