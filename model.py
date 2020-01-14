from pcraster import *
from pcraster.framework import *

class PredPreyModel(DynamicModel):
  def __init__(self):
    DynamicModel.__init__(self)
    setclone('clone.map')

  def initial(self):
    # set percentages for prey and predator populations
    percPrey = 0.5
    percPred = 0.5

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


nrOfTimeSteps=100
myModel = PredPreyModel()
dynamicModel = DynamicFramework(myModel,nrOfTimeSteps)
dynamicModel.run()

