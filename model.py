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

    # create maps with that percentage of pred/prey present
    self.prey = uniform(1) < percPrey
    self.pred = uniform(1) < percPred
    self.report(self.prey, 'output/preyInit')
    self.report(self.pred, 'output/predInit')

  def dynamic(self):
    # find all locations with both predator and prey
    both = pcrand(self.pred, self.prey)
    self.report(both, 'output/both')

    # predators reproduce at these locations
    self.pred = (window4total(scalar(both)) + scalar(both)) >= 1
    self.report(self.pred, 'output/pred')
    
    # find all surviving prey
    survive = pcrand(self.prey, ~both)

    # all survivors reproduce
    self.prey = (window4total(scalar(survive)) + scalar(survive)) >= 1
    self.report(self.prey, 'output/prey')

#define number of Time Steps

nrOfTimeSteps=100

#define proportion (prey and predator) step size

propstepSize=0.01

# Open file to save results

f= open("DataPreyPredator_propstep_"+str(propstepSize)+".txt","w+")
f.write("PercPrey-Ini,PercPred-Ini,PercPrey-Final,PercPred-Final"+"\n")

for percPrey in np.arange(0,1,propstepSize):
    
    for percPred in np.arange(0,1,propstepSize):
        myModel = PredPreyModel()
        dynamicModel = DynamicFramework(myModel,nrOfTimeSteps)
        dynamicModel.run()

        preyEq = readmap("output/prey0000."+str(nrOfTimeSteps))
        predEq = readmap("output/pred0000."+str(nrOfTimeSteps))

        # compute calculations 
    
        PercPreyFinal= maptotal(scalar(preyEq==1))/(200*200)
        PercPredFinal= maptotal(scalar(predEq!=0))/(200*200)
        # Writting individial results into the file - Initial and final conditions are saved

        f.write(str(float(percPrey)) + "," + str(float(percPred)) + "," + str(float(PercPreyFinal)) + "," + str(float(PercPredFinal))+"\n")
        print(str(float(percPrey)) + "," + str(float(percPred)) + "," + str(float(PercPreyFinal)) + "," + str(float(PercPredFinal))+"\n")
             
f.close()
