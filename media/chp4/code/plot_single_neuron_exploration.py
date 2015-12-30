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

"""
Plots the information for an experiment result as created with ./run.py
"""

import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.io as scio
import os
import sys
import re

# Labels for all possible sweep dimensions (wip)
DIMS = {
    "cM": "Membrane capacitance $C_M$ [nF]",
    "eE": "Excitatory reversal potential $E_\\mathrm{e}$ [mV]",
    "eI": "Inhibitory reversal potential $E_\\mathrm{i}$ [mV]",
    "eL": "Resting potential $E_\\mathrm{L}$ [mV]",
    "eReset": "Reset potential $E_{\\mathrm{reset}}$ [mV]",
    "eTh": "Threshold potential $E_{\\mathrm{Th}}$ [mV]",
    "w": "Synapse weight $w$ [$\\mu\\mathrm{S}$]",
    "gL": "Leak conductivity $g_\\mathrm{L}$ [$\\mu\\mathrm{S}$]",
    "tauE": "Excitatory time constant $\\tau_\\mathrm{e}$ [ms]",
    "tauI": "Inhibitory time constant $\\tau_\\mathrm{i}$ [ms]",
}

SCALES = {
    "cM": 1e9,
    "eE": 1e3,
    "eI": 1e3,
    "eL": 1e3,
    "eReset": 1e3,
    "eTh": 1e3,
    "w": 1e6,
    "gL": 1e6,
    "tauE": 1e3,
    "tauI": 1e3,
}

# Labels for all measures
MEASURES = {
    "Train": "Spike Train",
    "SgSo": "SGSO",
    "SgMo": "SGMO",
}

# Labels for all measures
MEASURE_LABEL = {
    "Train": "$\\mathcal{P}_\\mathrm{st}(\\Phi)$",
    "SgSo": "$\\mathcal{P}_\\mathrm{sgso}(\\Phi)$",
    "SgMo": "$\\mathcal{P}_\\mathrm{sgmo}(\\Phi)$",
}

# Labels for all models
MODELS = {
    "IfCondExp": "LIF",
    "AdIfCondExp": "AdEx"
}

figures = {}

def cm2inch(value):
    return value / 2.54

def match(val, dictionary, prefix="", default="?"):
    for key in dictionary.keys():
        s = prefix + key
        if s in val:
            return dictionary[key]
    return default

if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " <FILENAME>")
    sys.exit(1)

(path, filename) = os.path.split(sys.argv[1])

measure = match(filename, MEASURES)
model = match(filename, MODELS)
dimX = match(filename, DIMS, "X")
dimY = match(filename, DIMS, "Y")
sX = match(filename, SCALES, "X", 1.0)
sY = match(filename, SCALES, "Y", 1.0)
label = match(filename, MEASURE_LABEL)

measure = measure + " evaluation model"
if "Train" in filename:
    N = re.search("_N([0-9]*)", filename).group(1)
    measure = measure + " with $n_\\mathrm{g} = " + N + "$"
title = measure + " (" + model + " neuron)"

print(title, dimX, dimY, sX, sY)

data = scio.loadmat(sys.argv[1])
xs = data['xs'] * sX
ys = data['ys'] * sY
zs = data['zs']

fig = plt.figure(figsize=(cm2inch(10), cm2inch(9.5)))
ax = fig.add_axes([0.0, 0.15, 1.0, 0.85])
ax2 = fig.add_axes([0.0, 0.0, 1.0, 0.05])

cmap = "rainbow"
fmt='%.0f\\%%'

extent = (np.min(xs), np.max(xs), np.min(ys), np.max(ys))
ax.imshow(zs, aspect='auto',origin='lower', extent=extent, cmap=cmap, vmin=0.0, vmax=1.0)


levels = np.linspace(0.0, 1.0, 11)
grid_xs, grid_ys = np.meshgrid(xs, ys)
#CS1 = ax.contourf(grid_xs, grid_ys, zs, levels, cmap=cmap, vmin=0.0, vmax=1.0)
CS2 = ax.contour(grid_xs, grid_ys, zs, levels, linewidths=0.25, colors='k')

#CS2.levels = map(lambda val: fmt % val, levels * 100.0)
#clabels = ax.clabel(CS2, inline=1, fontsize=8)
#[txt.set_bbox(dict(facecolor='white', edgecolor='none', pad=0)) for txt in clabels]
#[txt.set_rotation(0) for txt in clabels]
ax.grid()

ax.set_title(title)
ax.set_xlabel(dimX)
ax.set_ylabel(dimY)

cbar = matplotlib.colorbar.ColorbarBase(ax2, cmap=cmap, orientation='horizontal', ticks=levels)
#	boundaries=levels)
cbar.set_label("Evaluation result " + label)

root, ext = os.path.splitext(sys.argv[1])
fig.savefig(root + ".pdf", format='pdf', bbox_inches='tight')

