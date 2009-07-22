###############################################################################
# This file is part of openWNS (open Wireless Network Simulator)
# _____________________________________________________________________________
#
# Copyright (C) 2004-2009
# Chair of Communication Networks (ComNets)
# Kopernikusstr. 5, D-52074 Aachen, Germany
# phone: ++49-241-80-27910,
# fax: ++49-241-80-22242
# email: info@openwns.org
# www: http://www.openwns.org
# _____________________________________________________________________________
#
# openWNS is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License version 2 as published by the
# Free Software Foundation;
#
# openWNS is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openwns.evaluation import *
import openwns.rng
import openwns
import openwns.node
import openwns.distribution
import rise.Mobility
import rise.Roadmap
import rise.scenario.Manhattan
import constanze.traffic
import constanze.node

WNS = openwns.Simulator(simulationModel = openwns.node.NodeSimulationModel())
WNS.maxSimTime = 20.0
WNS.modules.rise.debug.main = True
WNS.outputStrategy = openwns.simulator.OutputStrategy.DELETE

# The global generator uses a random seed, the traffic will therefore variate
# for every run
WNS.environment.rng = openwns.rng.RNG(useRandomSeed = True)

# Mobility component gets an own RNG with fixed seed. Movement is therefore
# independant from traffic. Disabling below line MUST fail the test
WNS.modules.rise.ownMobilityRNG = openwns.rng.RNG(useRandomSeed = False)

numCars = 5

class Car(openwns.node.Node):
    mobility = None
    load = None

    def __init__(self, name, mobility):
        super(Car, self).__init__(name)
        self.mobility = rise.Mobility.Component(self,
                                                "Mobility Component",
                                                mobility)
        self.load = constanze.node.ConstanzeComponent(self, "carGen")
        
        bindingStub = constanze.node.BindingStub()
        traffic = constanze.traffic.Poisson(0.1, 1E6, 1024)
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
    WNS.simulationModel.nodes.append( Car("Car" + str(ii), aMobility) )

WNS.simulationModel.nodes[0].mobility.mobility.userVelocityDist = openwns.distribution.Uniform(45.0, 55.0)
WNS.simulationModel.nodes[1].mobility.mobility.userVelocityDist = openwns.distribution.Normal(50.0, 15.0)
WNS.simulationModel.nodes[2].mobility.mobility.userVelocityDist = openwns.distribution.Erlang(1.0 / 50.0, 1)
WNS.simulationModel.nodes[3].mobility.mobility.userVelocityDist = openwns.distribution.Poisson(50.0)
WNS.simulationModel.nodes[4].mobility.mobility.userVelocityDist = openwns.distribution.StandardUniform() + 50.0


sourceName = 'rise.scenario.mobility.PositionX'
node = openwns.evaluation.createSourceNode(WNS, sourceName)
node.appendChildren(Separate(by = 'wns.node.Node.id', 
    forAll = xrange(1, numCars), 
    format="wns.node.Node.id%d"))
node.getLeafs().appendChildren(Moments())

sourceName = 'rise.scenario.mobility.PositionY'
node = openwns.evaluation.createSourceNode(WNS, sourceName)
node.appendChildren(Separate(by = 'wns.node.Node.id', 
    forAll = xrange(1, numCars), 
    format="wns.node.Node.id%d"))
node.getLeafs().appendChildren(Moments())

openwns.setSimulator(WNS)
