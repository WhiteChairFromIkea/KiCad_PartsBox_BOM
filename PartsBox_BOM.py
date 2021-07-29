"""
    @package
    Generate PartsBox import compatible file.
    
    Warning: THis script requires patched "kicad_netlist_reader.py" file in the same dir as this BOM script.
    
    Usage:
    1) Set "DNP" field to non empty value in order to omit component from the BOM;
    2) Pass "REMOVE_DNP_COMPONENTS" as 3rd argument to omit DNP from BOM;
    3) Edit "kicad_netlist_reader.py" in case other field is used as "Do Not Populate" field (can be any use field).

    Command line:
    python "pathToFile/PartsBox_BOM.py" "%I" "%O.csv" "REMOVE_DNP_COMPONENTS"
    or
    python "pathToFile/PartsBox_BOM.py" "%I" "%O.csv" "LIST_DNP_COMPONENTS"
"""

from __future__ import print_function

# Import the KiCad python helper module and the csv formatter
import kicad_netlist_reader
import csv
import sys

# ref https://gitlab.com/kicad/code/kicad/-/commit/35f9cd2634f419b994178360963a49f5042c4a70 @Jeff Young
# A helper function to convert a UTF8/Unicode/locale string read in netlist for python2 or python3
def fromNetlistText( aText ):
    currpage = sys.stdout.encoding      #the current code page. can be none
    if currpage is None:
        return aText
    if currpage != 'utf-8':
        try:
            return aText.encode('utf-8').decode(currpage)
        except UnicodeDecodeError:
            return aText
    else:
        return aText

def myEqu(self, other):
    """myEqu is a more advanced equivalence function for components which is
    used by component grouping. Normal operation is to group components based
    on their value and footprint.

    In this example of a custom equivalency operator we compare the
    value, the part name (libID) and the footprint.
    """
    result = True
    if self.getValue() != other.getValue():
        result = False
#    elif self.getPartName() != other.getPartName():
#        result = False
    elif self.getFootprint() != other.getFootprint():
        result = False

    return result

# Override the component equivalence operator - it is important to do this before loading the netlist, otherwise all components will have the original equivalency operator.
kicad_netlist_reader.comp.__eq__ = myEqu

# Generate an instance of a generic netlist, and load the netlist tree from the command line option. If the file doesn't exist, execution will stop
net = kicad_netlist_reader.netlist(sys.argv[1])

# Open a file to write to, if the file cannot be opened output to stdout instead
try:
    f = open(sys.argv[2], 'w')
except IOError:
    e = "Can't open output file for writing: " + sys.argv[2]
    print(__file__, ":", e, sys.stderr)
    f = sys.stdout

# Create a new csv writer object to use as the output formatter and write header
out = csv.writer(f, lineterminator='\n', delimiter=';', quotechar='\"', quoting=csv.QUOTE_ALL)
out.writerow(['Id', 'Designator', 'Package', 'Quantity', 'Designation', 'Supplier and ref', 'BLANK', 'DNP?','Footprint', 'lib', 'Comment_sch', 'PartsBox', 'lib descr.', 'Datasheet', 'libpart' ])

# Check if omit DNP components from the BOM. Get all, or only fitted components in groups of matching parts + values. Edit see kicad_netlist_reader.py if other exclude filters are needed
bShowDnpComponents = sys.argv[3]
if(bShowDnpComponents == "REMOVE_DNP_COMPONENTS"):
    grouped = net.groupComponents(net.getInterestingComponents())
else:
    grouped = net.groupComponents()

# Parse component info
for group in grouped:
    refs = ""
    comments_assy = ""

    # Add the reference of every component in the group and keep a reference
    # to the component so that the other data can be filled in once per group
    for component in group:
        c = component
        refs += fromNetlistText( component.getRef() ) + ", "
        cmnt = component.getField("Comment_assy")
        if(cmnt):
            comments_assy += cmnt + ", "

    # Fill in the component groups common data
    out.writerow(["", refs, "", len(group),
        fromNetlistText( c.getValue() ),
        comments_assy,
        "-",
        fromNetlistText( c.getField("DNP") ),
        fromNetlistText( c.getFootprint() ),
        fromNetlistText( c.getLibName() ),
        fromNetlistText( c.getField("Comment_sch") ),
        fromNetlistText( c.getField("PartsBox") ),
        fromNetlistText( c.getDescription() ),
        fromNetlistText( c.getDatasheet() ),
        fromNetlistText( c.getPartName()) ])

# Launch CSV viewer (Libre calc)
import os
os.startfile(sys.argv[2])
# run sys.argv[2]


