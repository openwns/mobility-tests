import openwns
import openwns.node
import rise.Mobility
import rise.Roadmap
import rise.scenario.Manhattan

WNS = openwns.Simulator(simulationModel = openwns.node.NodeSimulationModel())
WNS.maxSimTime = 20.0
WNS.modules.rise.debug.main = True
WNS.outputStrategy = openwns.simulator.OutputStrategy.DELETE

class Car(openwns.node.Node):
    mobility = None

    def __init__(self, name, mobility):
        super(Car, self).__init__(name)
        self.mobility = rise.Mobility.Component(self,
                                                "Mobility Component",
                                                mobility)

# scenario of roadmapTest
streets, crossings = rise.Roadmap.readFromFile("roadmapTest.roadmap")
aMobility = rise.Mobility.Roadmap("manhattan2x3", streets, crossings)

for ii in xrange(50):
    WNS.simulationModel.nodes.append( Car("Car" + str(ii), aMobility) )
    WNS.simulationModel.nodes[-1].mobility.mobility.userVelocityDist.mean = 30

openwns.setSimulator(WNS)
