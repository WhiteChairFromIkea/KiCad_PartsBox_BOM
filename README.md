# KiCad_PartsBox_BOM
Export KiCad v5 BOM to be imported into PartsBox as CSV

# Screenshots
![alt text](https://github.com/WhiteChairFromIkea/KiCad_PartsBox_BOM/blob/master/BOM%20menu.png)
![alt text](https://github.com/WhiteChairFromIkea/KiCad_PartsBox_BOM/blob/master/Libre%20calc%20import.png)

# Dependencies:
File "kicad_netlist_reader.py" must be in the same folder as "PartsBox_BOM.py". It can be found inside C:\Program Files\KiCad\bin\scripting\plugins in case of normal installation. It can be copied to %appdata% folder...

# Installation:
 1. Place "PartsBox_BOM.py" inside KiCad 5 plugins folder:   
   a) %appdata%\kicad\scripting\plugins  
   b) copy directly insie C:\Program Files\KiCad\bin\scripting\plugins  
   
 2. Open sch with eeschema, Tools -> Generate Bill of materials..., click "+", locate "kicad_netlist_reader.py". Edit "Command line" field to end with "%O.csv", instead of "%O" to add csv file extension for the output file;  
 3. Click generate;
 CSV file file will be located inside project folder.

# Notes
Only "Id	Designator	Package	Quantity	Designation	Supplier and ref" (as per https://partsbox.io/how-to-generate-a-bom-from-kicad.html) columns are necessarry for partsbox import, other collumns inside csv can be customized by editing "PartsBox_BOM.py" line 64 (personal preferences)...

Script is based on "# Example: Sorted and Grouped CSV BOM".
