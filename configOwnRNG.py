from openwns.evaluation import *
import openwns.rng
import wns.WNS
import wns.Node
import wns.Distribution
import rise.Mobility
import rise.Roadmap
import rise.scenario.Manhattan
import constanze.Constanze
import constanze.Node

WNS = wns.WNS.WNS()
WNS.maxSimTime = 20.0
WNS.modules.rise.debug.main = True
WNS.outputStrategy = wns.WNS.OutputStrategy.DELETE

# The global generator uses a random seed, the traffic will therefore variate
# for every run
WNS.environment.rng = openwns.rng.RNG(useRandomSeed = True)

# Mobility component gets an own RNG with fixed seed. Movement is therefore
# independant from traffic. Disabling below line MUST fail the test
WNS.modules.rise.ownMobilityRNG = openwns.rng.RNG(useRandomSeed = False)

numCars = 5

class Car(wns.Node.Node):
    mobility = None
    load = None

    def __init__(self, name, mobility):
        super(Car, self).__init__(name)
        self.mobility = rise.Mobility.Component(self,
                                                "Mobility Component",
                                                mobility)
        self.load = constanze.Node.ConstanzeComponent(self, "carGen")
        
        bindingStub = constanze.Node.BindingStub()
        traffic = constanze.Constanze.Poisson(0.1, 1E6, 1024)
        self.load.addTraffic(bindingStub, traffic)
                                                
# Manhattan scenario

myManhattan = rise.scenario.Manhattan.Manhattan(rows=10,
                                                columns=10,
                                                blockWidth=200,
                                                blockHeight=200,
                                                streetWidth=30,
                                                velocity=30,
                                                deploymentStrategy="30.03")

aMobility = rise.Mobility.Roadmap("testMobility", myManhattan.streets, myManhattan.crossings)

for ii in xrange(numCars):
    WNS.nodes.append( Car("Car" + str(ii), aMobility) )

WNS.nodes[0].mobility.mobility.userVelocityDist = wns.Distribution.Uniform(45.0, 55.0)
WNS.nodes[1].mobility.mobility.userVelocityDist = wns.Distribution.Normal(50.0, 15.0)
WNS.nodes[2].mobility.mobility.userVelocityDist = wns.Distribution.Erlang(1.0 / 50.0, 1)
WNS.nodes[3].mobility.mobility.userVelocityDist = wns.Distribution.Poisson(50.0)
WNS.nodes[4].mobility.mobility.userVelocityDist = wns.Distribution.StandardUniform() + 50.0


sourceName = 'rise.scenario.mobility.PositionX'
node = openwns.evaluation.createSourceNode(WNS, sourceName)
node.appendChildren(Separate(by = 'wns.node.Node.id', 
    forAll = xrange(numCars), 
    format="wns.node.Node.id%d"))
node.getLeafs().appendChildren(Moments())

sourceName = 'rise.scenario.mobility.PositionY'
node = openwns.evaluation.createSourceNode(WNS, sourceName)
node.appendChildren(Separate(by = 'wns.node.Node.id', 
    forAll = xrange(numCars), 
    format="wns.node.Node.id%d"))
node.getLeafs().appendChildren(Moments())

