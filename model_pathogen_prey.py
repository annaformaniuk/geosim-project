from pcraster import *
from pcraster.framework import *
import numpy as np

class PredPreyModel(DynamicModel):
  def __init__(self):
    DynamicModel.__init__(self)
    # set clone directly:
    # size 200x200, cell size 1, west coord: 0, north coord: 200
    setclone(200, 200, 1, 0, 200)

  def initial(self):
    # percentage of infected prey
    percInf = 0.5

    # create maps with that percentage of total pred/prey present
    prey = uniform(1) < percPrey
    self.pred = uniform(1) < percPred

    # infect some of the prey
    infPrey = pcrand(uniform(1) < percInf, prey)
    # create a nominal prey map, consisting of infected prey (with the value of 2,
    # sound prey (1), and empty cells (0)
    self.prey = ifthenelse(infPrey, nominal(2), ifthenelse(prey, nominal(1), nominal(0)))

    self.report(self.prey, 'outputInfectedPrey/preyInit')
    self.report(self.pred, 'outputInfectedPrey/predInit')

  def dynamic(self):
    # find locations of all prey, infect neighbours, define the sound ones
    allPrey = self.prey != 0
    infPrey = pcrand(window4total(scalar(self.prey == 2)) >=1, allPrey)
    soundPrey = pcrand(allPrey, ~infPrey)

    # find all locations with both predator and prey
    both = pcrand(self.pred, allPrey)
    self.report(both, 'outputInfectedPrey/both')

    # predators reproduce at these locations
    self.pred = (window4total(scalar(both)) + scalar(both)) >= 1
    self.report(self.pred, 'outputInfectedPrey/pred')
    
    # find all surviving prey
    surviveInfected = pcrand(infPrey, ~both)
    surviveSound = pcrand(soundPrey, ~both)

    # sound prey reproduces in own cell and neighbourhood, infected only in own cell
    reprSoundPrey = (window4total(scalar(surviveSound)) + scalar(surviveSound)) >= 1
    reprInfPrey = (scalar(surviveInfected) >= 1)

    # save and report the nominal map
    self.prey = ifthenelse(reprInfPrey, nominal(2), ifthenelse(reprSoundPrey, nominal(1), nominal(0)))
    self.report(self.prey, 'outputInfectedPrey/prey')

#define number of Time Steps

nrOfTimeSteps=100

# define proportion (prey and predator) step size

propstepSize=0.01

# Open file to save results

f= open("testDataInfectedPrey_propstep_"+str(propstepSize)+".txt","w+")
f.write("PercPrey-Ini,PercPred-Ini,PercPrey-Final,PercPred-Final"+"\n")

# set percentages for prey and predator populations

for percPrey in np.arange(0,1,propstepSize):
  for percPred in np.arange(0,1,propstepSize):
    myModel = PredPreyModel()
    dynamicModel = DynamicFramework(myModel,nrOfTimeSteps)
    dynamicModel.run()

    # extract information from the map
    
    preyEq = readmap("outputInfectedPrey/prey0000."+str(nrOfTimeSteps))
    predEq = readmap("outputInfectedPrey/pred0000."+str(nrOfTimeSteps))

    print("outputInfectedPrey/prey0000."+str(nrOfTimeSteps))

    # compute calculations 
    
    PercPredFinal= maptotal(scalar(preyEq==1))/(200*200)
    PercPreyFinal= maptotal(scalar(predEq!=0))/(200*200)

    # Writting individial results into the file - Initial and final conditions are saved

    f.write(str(float(percPrey)) + "," + str(float(percPred)) + "," + str(float(PercPreyFinal)) + "," + str(float(PercPredFinal))+"\n")
    print(str(float(percPrey)) + "," + str(float(percPred)) + "," + str(float(PercPreyFinal)) + "," + str(float(PercPredFinal))+"\n")

# close file
f.close()
