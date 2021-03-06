# Geosimulation Modelling - Course Project

For this project, we are implementing the model described in the following paper:

[Ferreri, L., & Venturino, E. (2013)](https://www.sciencedirect.com/science/article/pii/S1476945X12000736). Cellular automata for contact ecoepidemic processes in predator–prey systems. *Ecological complexity*, *13*, 8-20.

## Notes 

* All outputs of the model without a pathogen are saved into the `output` folder. The folder has to exist already, otherwise Python will throw an error. 
* Correspondingly, outputs of the model where predators can get infected are saved in `outputInfectedPred` and of the model with infected prey - in `outputInfectedPrey`.
