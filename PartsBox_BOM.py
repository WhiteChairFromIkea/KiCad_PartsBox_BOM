#
# Example python script to generate a BOM from a KiCad generic netlist
#
# Example: Sorted and Grouped CSV BOM
#

# 2019-11-22 Not working grouping by Comment_assy field!!!!
#2020-02-03 ' Fixed Not working grouping by Comment_assy field, added "REMOVE_DNP_COMPONENTS" as third argument. use anything els as 3rd argument to list all components.

"""
    @package
    Generate a Tab delimited list (csv file type).
    Components are sorted by ref and grouped by value with same footprint
    Fields are (if exist)
    'Ref', 'Qnty', 'Value', 'Cmp name', 'Footprint', 'Description', 'Vendor'

    Command line:
    python "pathToFile/PartsBox_BOM.py" "%I" "%O.csv" "REMOVE_DNP_COMPONENTS"
    or
    python "pathToFile/PartsBox_BOM.py" "%I" "%O.csv" "LIST_DNP_COMPONENTS"
"""

# Import the KiCad python helper module and the csv formatter
import kicad_netlist_reader
import csv
import sys

# Generate an instance of a generic netlist, and load the netlist tree from
# the command line option. If the file doesn't exist, execution will stop
net = kicad_netlist_reader.netlist(sys.argv[1])
bShowDnpComponents = sys.argv[3]

# Open a file to write to, if the file cannot be opened output to stdout
# instead
try:
    f = open(sys.argv[2], 'w')
except IOError:
    e = "Can't open output file for writing: " + sys.argv[2]
    print(__file__, ":", e, sys.stderr)
    f = sys.stdout

# Create a new csv writer object to use as the output formatter
out = csv.writer(f, lineterminator='\n', delimiter=';', quotechar='\"', quoting=csv.QUOTE_ALL)

# Output a set of rows for a header providing general information
# out.writerow(['Source:', net.getSource()])
# out.writerow(['Date:', net.getDate()])
# out.writerow(['Tool:', net.getTool()])
# out.writerow( ['Generator:', sys.argv[0]] )
# out.writerow(['Component Count:', len(net.components)])
# out.writerow("\n")
#out.writerow(['Ref', 'Qnty', 'Value', 'Cmp name', 'Footprint', 'Description', 'Vendor'])
out.writerow(['Id', 'Designator', 'Package', 'Quantity', 'Designation', 'Supplier and ref', 'BLANK', 'DNP?','Footprint', 'lib', 'Comment_sch', 'PartsBox', 'lib descr.', 'Datasheet', 'libpart' ])

# Get all of the components in groups of matching parts + values
# (see ky_generic_netlist_reader.py)
grouped = net.groupComponents()

# Output all of the component information
for group in grouped:
    refs = ""
    comments_assy = ""
    dnp = ""

    # Add the reference of every component in the group and keep a reference
    # to the component so that the other data can be filled in once per group
    for component in group:
        if(bShowDnpComponents == "REMOVE_DNP_COMPONENTS"):
            dnp = component.getField("DNP")
        else:
            dnp = ""
        if(not dnp):
            refs += component.getRef() + ", "
            cmnt = component.getField("Comment_assy")
            if(cmnt):
                comments_assy += cmnt + ", "
#        print(refs)
#        print(comments_assy)
            c = component
#        print(c.getField("Comment_assy"))

    # Fill in the component groups common data
    out.writerow(["", refs, "", len(group), c.getValue(), comments_assy, "-", c.getField("DNP"), c.getFootprint(), c.getLibName(), c.getField("Comment_sch"), c.getField("PartsBox"), c.getDescription(), c.getDatasheet(), c.getPartName()])

import os
os.startfile(sys.argv[2])
# run sys.argv[2]


