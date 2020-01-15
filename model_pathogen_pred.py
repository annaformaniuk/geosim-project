from pcraster import *
from pcraster.framework import *

class PredPreyModel(DynamicModel):
  def __init__(self):
    DynamicModel.__init__(self)
    # set clone directly:
    # size 200x200, cell size 1, west coord: 0, north coord: 200
    setclone(200, 200, 1, 0, 200)

  def initial(self):
    # set percentages for prey and predator populations
    percPrey = 0.1
    percPred = 0.1
    # percentage of infected predators
    percInf = 0.2

    # create maps with that percentage of total pred/prey present
    self.prey = uniform(1) < percPrey
    pred = uniform(1) < percPred

    # infect some of the predators
    infPred = pcrand(uniform(1) < percInf, pred)
    # create a nominal predators map, consisting of infected predators (with the value of 2),
    # sound predators (1), and empty cells (0)
    self.pred = ifthenelse(infPred, nominal(2), ifthenelse(pred, nominal(1), nominal(0)))

    self.report(self.prey, 'outputInfectedPred/preyInit')
    self.report(self.pred, 'outputInfectedPred/predInit')

  def dynamic(self):
    # find locations of all predators, infect neighbours, define the sound ones
    allPred = self.pred != 0
    infPred = pcrand(window4total(scalar(self.pred == 2)) >=1, allPred)
    soundPred = pcrand(allPred, pcrnot(infPred))

    # find locations where infected or sound predators catch prey
    infEats = pcrand(infPred, self.prey)
    soundEats = pcrand(soundPred, self.prey)
    # find all locations with both predator and prey
    both = pcrand(infEats, soundEats)
    self.report(both, 'outputInfectedPred/both')

    # predators reproduce at these locations: sound ones in own cell and neighbourhood,
    # infected ones only in own cell
    reprSoundPred = (window4total(scalar(soundEats)) + scalar(soundEats)) >= 1
    reprInfPred = (scalar(infEats) >= 1)

    # save and report the nominal map
    self.pred = ifthenelse(reprInfPred, nominal(2), ifthenelse(reprSoundPred, nominal(1), nominal(0)))
    self.report(self.pred, 'outputInfectedPred/pred')
    
    # find all surviving prey
    survive = pcrand(self.prey, ~both)

    # all survivors reproduce
    self.prey = (window4total(scalar(survive)) + scalar(survive)) >= 1
    self.report(self.prey, 'outputInfectedPred/prey')


nrOfTimeSteps=100
myModel = PredPreyModel()
dynamicModel = DynamicFramework(myModel,nrOfTimeSteps)
dynamicModel.run()

