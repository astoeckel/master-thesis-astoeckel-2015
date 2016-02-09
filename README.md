Design Space Exploration of Associative Memories using Spiking Neurons with Respect to Neuromorphic Hardware Implementations
============================================================================================================================

[Download PDF from GitHub (v1.2)](https://github.com/hbp-sanncs/master-thesis-astoeckel-2015/releases/download/v1.2/master_astoecke_design_space_exploration_2015.pdf)

Abstract
--------

Artificial neural networks are well-established models for key functions of
biological brains, such as low-level sensory processing and memory. In
particular, networks of artificial spiking neurons emulate the time dynamics,
high parallelisation and asynchronicity of their biological counterparts. Large
scale hardware simulators for such networks – *neuromorphic* computers – are
developed as part of the Human Brain Project, with the ultimate goal to gain
insights regarding the neural foundations of cognitive processes.

In this thesis, we focus on one key cognitive function of biological brains,
associative memory. We implement the well-understood Willshaw model for
artificial spiking neural networks, thoroughly explore the design space for the
implementation, provide fast design space exploration software and evaluate our
implementation in software simulation as well as neuromorphic hardware.

Thereby we provide an approach to manually or automatically infer viable
parameters for an associative memory on different hardware and software
platforms. The performance of the associative memory was found to vary
significantly between individual neuromorphic hardware platforms and numerical
simulations. The network is thus a suitable benchmark for neuromorphic systems.

Build
-----

The LaTeX document was built ontop of TeXLive on Fedora 23. It uses `biber` for
bibliography management and `latexmk` for building. You can build a PDF version
of the thesis with the following series of commands:
````bash
git clone --recursive https://github.com/hbp-sanncs/master-thesis-astoeckel-2015/
cd master-thesis-astoeckel-2015 && make
````

Figures, scripts and data
-------------------------

All figures can be found in the `media` folder. The SVG source code of most figures
is stored in the `source` folder. The figures can be edited using the free vector
graphics editor Inkscape. Scripts and programms used for the generation of
the figures can be found in the corresponding `code` folders. Some scripts for the
generation of figures can be found in the [PyNAM](https://github.com/hbp-sanncs/pynam/tree/master/misc)
project.


License
-------

In its entirety, this document is licensed under a
[Creative Commons Attribution-No Derivatives 4.0 International License](http://creativecommons.org/licenses/by-nd/4.0/).
Individual figures – unless an external source is explicitly specified – are
licensed under a
[Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).
They may – in addition to what is permitted by copyright law – be reused and
modified for any purpose, as long as a reference to this document is provided.

The *Smart Thesis* template used in this document was written by Jan Philip
Göpfert and Andreas Stöckel and is inspired by the *Classic Thesis* template
developed by André Miede. The source code of this document and all
described software tools are available at: https://github.com/hbp-sanncs/

Author
------

This master thesis was written by Andreas Stöckel in 2015 at Bielefeld University in
the [Cognitronics and Sensor Systems Group](http://www.ks.cit-ec.uni-bielefeld.de/)
which is part of the [Human Brain Project, SP 9](https://www.humanbrainproject.eu/neuromorphic-computing-platform).

