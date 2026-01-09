# Mixed Bedrock Alluvial LEM Guides
Two jupyter notebook guides on how to run 1D and 2D tests on the shared stream power model (SSPM) and SPACE. 
These are landscape evolution models that capture the effects of bedrock incision 
and sediment transport. Based on model tests used for Thompson & Whipple (2026) (In preparation).

For a simpler tutorial for SSPM see:
https://landlab.readthedocs.io/en/latest/tutorials/landscape_evolution/erosion_deposition/shared_stream_power.html

__Installation__
This tutorial uses Landlab. Instructions for instalation can be found at:
https://landlab.readthedocs.io/en/latest/installation.html

__Usage__
To run SSPM, use the shared_stream_power_shared.ipynb notebook.
To run SPACE, use the space_shared.ipynb notebook.

All outputs from these notebooks will be stored in ./output.
RunSSPM.py and TestSPACE.py are modules used to set up test objects for the notebooks.
They can be modified to change plotting or test setup.
DictionariesSSPM.py and DictionariesSPACE.py include previously used groups of parameters
used for research, and are included as an example resource.

__Contact__
For questions or contributions, contact Annie: annt@uoregon.edu

__License__
Licensed by MIT License

