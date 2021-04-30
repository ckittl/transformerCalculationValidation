import csv
import datetime
import decimal
import os
import powerfactory

from numpy import arange

"""
This script is meant to control the PowerFactory instance and write out the obtained results into a csv file.
It is designed to be imported into the PowerFactory project and used from within it. Therefore a valid PowerFactory
license as well as the provided project file are needed.
"""

# General information
pBase = 0.4  # Base active power in MW
tapRange = range(-10, 11)  # Range of available tap positions
pRange = arange(-1, 1, decimal.Decimal(0.1))  # Active power range in terms of dimensionless power
resultDirectory = os.path.relpath('../results/powerfactory')  # Where to put result files

# Preparing the writing of results
filename = datetime.datetime.now().strftime("%Y%m%d-%H%M") + '_powerfactory.csv'
filepath = os.path.join(resultDirectory, filename)
if not os.path.exists(filename):
    os.makedirs(filename)

file = open(filepath, 'wt', newline='')
header = ['tapPos', 'p', 'v']
csv_writer = csv.writer(file)
csv_writer.writerow(header)

# Get powerfactory object
app = powerfactory.GetApplication()
project = app.GetActiveProject()
projectName = project.loc_name
app.PrintPlain("Active Project: " + str(project))
ldf = app.GetFromStudyCase("ComLdf")

# Identify the assets in the grid
transformers = app.GetCalcRelevantObjects("2-Wicklungstransformator.ElmTr2")
transformer = transformers[0]
loads = app.GetCalcRelevantObjects("Allgemeine Last.ElmLod")
load = loads[0]
nodes = app.GetCalcRelevantObjects("Knoten_j.ElmTerm")
node = nodes[0]
app.PrintPlain(
    "Using the transformer " + str(transformer) + " and load " + str(load) + ". Observing node voltage at node " + str(
        node))

for tapPos in tapRange:
    # Adjust transformer position
    transformer.SetAttribute("nntap", tapPos)
    for p in pRange:
        # Adjust the active power load of the load
        load.SetAttribute("plini", p * pBase)

        # Perform the load flow calculation
        pfStatus = ldf.Execute()
        if pfStatus != 0:
            app.PrintError("Failure during power flow calculation!")
        v = node.GetAttribute("m:u")

        app.PrintPlain("(tapPos = " + str(tapPos) + ", p = " + str(p) + " MW) --> v = " + str(v))

        # Prepare the output and write it to file
        row = [tapPos, "{0:.1f}".format(p / pBase), v]
        csv_writer.writerow(row)
file.close()
