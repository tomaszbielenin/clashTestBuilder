import sys
# src = sys.argv[1]
# dst = sys.argv[2]
src = "C:/Scripting/Git/clashTestBuilder/CNEB_SearchSets.xml"
# tmp = "C:/Scripting/Git/clashTestBuilder/template.xml"
dst = "C:/Scripting/Git/clashTestBuilder/output.xml"

import xml.etree.ElementTree as ET
import copy

sroot = ET.parse(src).getroot()

ssets = []
for sset in sroot.findall('selectionsets/selectionset'):
    value = sset.get('name')
    ssets.append(value)

# print(ssets)

ctests = []
for sset in ssets:
    for cnt in range(ssets.index(sset),len(ssets)):
        ctest = [sset,ssets[cnt]]
        # print(ctest)
        # print(ctest[0], " vs ", ctest[1])
        ctests.append(ctest)

# print(ctests)

tmp = """<?xml version="1.0" encoding="UTF-8" ?>

<exchange xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://download.autodesk.com/us/navisworks/schemas/nw-exchange-12.0.xsd" units="m" filename="" filepath="">
  <batchtest name="CNEB_ClashTests" internal_name="CNEB_ClashTests" units="m">
    <clashtests>
      <clashtest name="Carriageway vs Carriageway" test_type="hard" status="new" tolerance="0.0000000000" merge_composites="0">
        <linkage mode="none"/>
        <left>
          <clashselection selfintersect="0" primtypes="1">
            <locator>lcop_selection_set_tree/HML - Carriageway</locator>
          </clashselection>
        </left>
        <right>
          <clashselection selfintersect="0" primtypes="1">
            <locator>lcop_selection_set_tree/HML - Carriageway</locator>
          </clashselection>
        </right>
        <rules/>
      </clashtest>
    </clashtests>
  </batchtest>
</exchange>"""

# droot = ET.parse(dst).getroot()
# print((droot.findall('batchtest/clashtests/clashtest')[2].get('name')))
# dlen = len(droot.findall('batchtest/clashtests/clashtest'))
# print(dlen)

# while dlen < len(ctests):
#     droot[0][0].append(copy.deepcopy(droot[0][0][0]))
troot = ET.fromstring(tmp)
b = ET.Element(troot.findall("batchtest/clashtests"))
c = troot.findall("batchtest/clashtests/clashtest")
dupe = ET.Element(copy.deepcopy(c)) #copy <c> node
b.append(dupe) #insert the new node

tree = ET.ElementTree(troot)
tree.write(open("C:/Scripting/Git/clashTestBuilder/output.xml", "w"),encoding='unicode')

# - scrap search set names
# - file name from parameter
# - create test sets
# - create tests
# - append to file
# - save and close