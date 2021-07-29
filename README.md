# KiCad_PartsBox_BOM
Export KiCad v6 (v5?) BOM to be imported into PartsBox as CSV

# Screenshots
![alt text](https://github.com/WhiteChairFromIkea/KiCad_PartsBox_BOM/blob/master/BOM%20menu.png)
![alt text](https://github.com/WhiteChairFromIkea/KiCad_PartsBox_BOM/blob/master/Libre%20calc%20import.png)

# Installation:
For v6:   
1. Copy `kicad_netlist_reader.py` and `PartsBox_BOM.py` to `%userprofile%\Documents\KiCad\5.99\plugins` folder.
   
2. Open sch with eeschema, Tools -> Generate Bill of materials..., click "+", locate `%userprofile%\Documents\KiCad\5.99\plugins\PartsBox_BOM.py`. Edit "Command line" field to end with `%O.csv`, instead of `%O` to add csv file extension for the output file;  

3. Click generate;
 CSV file file will be located inside project folder and shell opened with csv editor.

## Note 1
This repository contains patched `kicad_netlist_reader.py`. At present (2021-Jul-30) this file is not merged to KiCad master, and it is unknown if it will be merged. This file is installed by KiCad installer somewhere, probably in program files dir, together with KiCad stock Schematic editor BOM plugins. In case stock `kicad_netlist_reader.py` is used, flag `REMOVE_DNP_COMPONENTS` will be ignored, and BOM will contain all components, without any exceptions.

## Note 2
Only `Id	Designator Package	Quantity	Designation	Supplier` and `ref` (as per https://partsbox.io/how-to-generate-a-bom-from-kicad.html) columns are necessarry for partsbox import, other collumns inside csv can be customized by editing "PartsBox_BOM.py".

## Note 3
v5 plugins dir (untested): `%appdata%\kicad\scripting\plugins` or `C:\Program Files\KiCad\bin\scripting\plugins`.

## Note 4
Script is based on "# Example: Sorted and Grouped CSV BOM".
