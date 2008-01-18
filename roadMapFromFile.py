import wns.WNS
import wns.Node
import rise.Mobility
import rise.Roadmap
import rise.scenario.Manhattan

WNS = wns.WNS.WNS()
WNS.maxSimTime = 20.0
WNS.modules.rise.debug.main = True
WNS.outputStrategy = wns.WNS.OutputStrategy.DELETE

class Car(wns.Node.Node):
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
    WNS.nodes.append( Car("Car" + str(ii), aMobility) )
    WNS.nodes[-1].mobility.mobility.userVelocityDist.mean = 30


