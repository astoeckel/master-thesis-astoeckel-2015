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

f = lambda x, l: 0.5 * (1.0 + (l * x) / (1.0 + l * abs(x)))
xs = np.linspace(-10, 10, 100)
ys0 = map(lambda x: f(x, 0.01), xs)
ys1 = map(lambda x: f(x, 0.1), xs)
ys2 = map(lambda x: f(x, 1.0), xs)
ys3 = map(lambda x: f(x, 10.0), xs)

fig = plt.figure(figsize=(cm2inch(5.5), cm2inch(5.5)))
ax = fig.add_subplot(1, 1, 1)
ax.plot(xs, ys0, color='#000000', label="$\\tau = 0.01$")
ax.plot(xs, ys1, color='#000000', dashes=[3, 1], label="$\\tau = 0.1$")
ax.plot(xs, ys2, color='#000000', dashes=[1, 1], label="$\\tau = 1$")
ax.plot(xs, ys3, color='#000000', dashes=[3, 3], label="$\\tau = 10$")
ax.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
ax.grid(linewidth=0.25, color="#888888")
ax.set_xlabel("$x$")
ax.set_ylabel("$\\mathrm{L}(x \mid x_0, \\tau)$")

ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.05), ncol=2)

#fig.savefig("long_tail_sigmoid_1.pdf", format='pdf', bbox_inches='tight')


xs = np.linspace(-75, -40, 100)
ys0 = map(lambda x: f(x + 50, 0.1), xs)
ys1 = map(lambda x: 1 - f(x + 50, 0.1), xs)

fig = plt.figure(figsize=(cm2inch(5.5), cm2inch(5.5)))
ax = fig.add_subplot(1, 1, 1)
ax.plot(xs, ys0, color='#000000', label="$p_1$")
ax.plot(xs, ys1, color='#000000', dashes=[3, 1], label="$p_0$")
ax.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
ax.set_xticks([-70, -50, -40])
ax.set_xticklabels(["$E_\\mathrm{L}$", "$E_\\mathrm{Th}^\\mathrm{eff}$", "$E_\\mathrm{e}$"])
ax.grid(linewidth=0.25, color="#888888")
ax.set_xlabel("$u_\\mathrm{max}$")

ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.05), ncol=2)

fig.savefig("long_tail_sigmoid_2.pdf", format='pdf', bbox_inches='tight')

