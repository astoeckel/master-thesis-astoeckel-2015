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

import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import scipy.io as sio

def cm2inch(value):
    return value / 2.54

expected = 5.5
f = lambda x: (1.0  / (1.0 + (x - expected)**2))
xs = np.linspace(0, 10.75, 1000)
ys0 = map(lambda x: x, xs)
ys1 = map(lambda x: math.floor(x), xs)
ysf0 = map(lambda x: f(x), xs)
ysf1 = map(lambda x: f(math.floor(x)), xs)

fig = plt.figure(figsize=(cm2inch(12), cm2inch(7)))
ax = fig.add_subplot(1, 1, 1)
l1 = ax.plot(xs, ys1, color='#000000', dashes=[1, 1], lw=0.5, label="$n^\mathrm{out}(\phi)$")
l2 = ax.plot(xs, ys0, color='#000000', label="$q^\mathrm{out}(\phi)$")
ax.set_yticks(xrange(0, 11))
ax.set_ylim(0, 10)
ax.set_xticks([])
ax.grid(linewidth=0.25, color="#888888")
ax.set_xlabel("Parameter $\phi$")
ax.set_ylabel("Output spike count")

ax2 = ax.twinx()
ax2.set_ylim(0, 1)
l3 = ax2.plot(xs, ysf1, dashes=[1, 1], lw=0.5, color="#3465a4", label="$S(n^\mathrm{out}(\phi))$")
l4 = ax2.plot(xs, ysf0, color="#3465a4", label="$S(q^\mathrm{out}(\phi))$")
ax2.set_ylabel("Student's t distribution $\mathrm{S}(q \mid x_0)$", color="#3465a4")
for tl in ax2.get_yticklabels():
    tl.set_color(color="#3465a4")

lns = l1 + l2 + l3 + l4
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc='lower center', bbox_to_anchor=(0.5, 1.05), ncol=4)

fig.savefig("student_t_step.pdf", format='pdf', bbox_inches='tight')

