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

from __future__ import print_function

import numpy as np
import scipy.misc

train = [
    'objects/00_00_orig.png',
    'objects/01_00_orig.png',
    'objects/02_00_orig.png',
    'objects/03_00_orig.png',
    'objects/04_00_orig.png',
    'objects/05_00_orig.png',
    'objects/06_00_orig.png',
    'objects/07_00_orig.png',
]

noisy = [
    'objects/00_01_noise.png',
    'objects/01_01_noise.png',
    'objects/02_01_noise.png',
    'objects/03_01_noise.png',
    'objects/04_01_noise.png',
    'objects/05_01_noise.png',
    'objects/06_01_noise.png',
    'objects/07_01_noise.png',
]

recalled = [
    'objects/00_02_out.png',
    'objects/01_02_out.png',
    'objects/02_02_out.png',
    'objects/03_02_out.png',
    'objects/04_02_out.png',
    'objects/05_02_out.png',
    'objects/06_02_out.png',
    'objects/07_02_out.png',
]

# Train the binam
binam = None
for fn in train:
    print("Training image", fn)
    im = np.array(scipy.misc.imread(fn), dtype=np.bool).reshape((-1, 1))
    if binam is None:
        binam = np.dot(im, im.T)
    else:
        binam = np.logical_or(binam, np.dot(im, im.T))
binam = np.array(binam, dtype=np.uint16)

# Recall the images
for i, fn in enumerate(noisy):
    print("Recalling image", fn)
    im = scipy.misc.imread(fn)
    orig_shape = im.shape
    im = np.array(im, dtype=np.uint16).reshape((-1, 1)) / 255
    c = np.sum(im)
    out = (np.dot(binam.T, im) >= c).reshape(orig_shape) * 255
    orig = scipy.misc.imread(recalled[i])
    print("False positive count: ", np.sum(out - orig))
    scipy.misc.imsave(recalled[i], out)



