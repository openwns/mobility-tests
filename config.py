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

import openwns
import openwns.evaluation.default
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
# Manhattan scenario

myManhattan = rise.scenario.Manhattan.Manhattan(rows=10,
                                                columns=10,
                                                blockWidth=200,
                                                blockHeight=200,
                                                streetWidth=30,
                                                velocity=30,
                                                deploymentStrategy="30.03")

aMobility = rise.Mobility.Roadmap("testMobility", myManhattan.streets, myManhattan.crossings)

for ii in xrange(50):
    WNS.simulationModel.nodes.append( Car("Car" + str(ii), aMobility) )
    WNS.simulationModel.nodes[-1].mobility.mobility.userVelocityDist.mean = 30

openwns.evaluation.default.installEvaluation(WNS)

openwns.setSimulator(WNS)
