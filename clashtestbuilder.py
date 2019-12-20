import sys
src = sys.argv[1]
dst = sys.argv[2]
src = "C:/Scripting/Git/clashTestBuilder/GDK_SSets_SubFolder.xml"
# tmp = "C:/Scripting/Git/clashTestBuilder/template.xml"
# dst = "C:/Scripting/Git/clashTestBuilder/output.xml"

import xml.etree.ElementTree as ET
# import copy

sroot = ET.parse(src).find('.//selectionsets')

def listElements(rt,element):
  path = "".join(('.//',str(element)))
  elist = []
  if rt.find(path):
    for el in rt.findall(path):
      name = el.get('name')
      elist.append(name)
  # print(vfolders)
  return elist

# print(listElements(sroot,'viewfolder')[3])

for vf in sroot.findall('viewfolder'):
    if vf.get('name') == listElements(sroot,'viewfolder')[3]:
        ssets = []
        for ss in vf.findall('selectionset'):
            nm = ss.get('name')
            ssets.append(nm)
print(ssets)

ssets = []
for sset in sroot.findall('.//selectionset'):
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
    </clashtests>
  </batchtest>
</exchange>"""

ttest = """<clashtest name="Carriageway vs Carriageway" test_type="hard" status="new" tolerance="0.0000000000" merge_composites="0">
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
      </clashtest>"""

# from lxml import etree
# c = etree.fromstring(ttest)
# ctree = etree.ElementTree(c)
# for e in c.iter():
#     print(ctree.getpath(e))

# droot = ET.parse(dst).getroot()
# print((droot.findall('batchtest/clashtests/clashtest')[2].get('name')))
# dlen = len(droot.findall('batchtest/clashtests/clashtest'))
# print(dlen)

# while dlen < len(ctests):
#     droot[0][0].append(copy.deepcopy(droot[0][0][0]))
droot = ET.fromstring(tmp)
a = droot.find("batchtest")
b = droot.find("batchtest/clashtests")
# c = ET.fromstring(ttest)
d = sroot.find("selectionsets")
# dupe = copy.deepcopy(c) #copy <c> node
a.append(d)
nclist = []
for i in range(len(ctests)):
  c = ET.fromstring(ttest)
  nname = " ".join((ctests[i][0], "vs", ctests[i][1]))
  # print(nname)
  c.set('name', nname)
  c.find('left/clashselection/locator').text = "/".join(("lcop_selection_set_tree",ctests[i][0]))
  c.find('right/clashselection/locator').text = "/".join(("lcop_selection_set_tree",ctests[i][1]))
  nclist.append(ET.tostring(c))
  b.append(ET.fromstring(nclist[i]))



tree = ET.ElementTree(droot)
f = open(dst, "w")
tree.write((f),encoding='unicode')
f.close()

# update locators naming with viewfolders