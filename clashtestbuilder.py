import sys
import os
import xml.etree.ElementTree as ET
# import copy

src = sys.argv[1]
dst = sys.argv[2]
src = "C:/Scripting/Git/clashTestBuilder/GDK_SSets_SubFolder.xml"
# tmp = "C:/Scripting/Git/clashTestBuilder/template.xml"
dst = "C:/Scripting/Git/clashTestBuilder/ClashTests.xml"
# ((os.path.basename(dst)).split(".")[0]) - get file name
tmp = """<?xml version="1.0" encoding="UTF-8" ?>

<exchange xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://download.autodesk.com/us/navisworks/schemas/nw-exchange-12.0.xsd" units="m" filename="" filepath="">
  <batchtest name="CNEB_ClashTests" internal_name="CNEB_ClashTests" units="m">
    <clashtests>
    </clashtests>
  </batchtest>
</exchange>"""

ttest = """<clashtest name="" test_type="hard" status="new" tolerance="0.0000000000" merge_composites="0">
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

def listElements(rt,element):
  path = "".join(('.//',str(element)))
  elist = []
  if rt.find(path):
    for el in rt.findall(path):
      name = el.get('name')
      elist.append(name)
  # print(vfolders)
  return elist

def ssets(rt):
  ssets = []
  for sset in rt.findall('.//selectionset'):
    value = sset.get('name')
    ssets.append(value)
  return ssets
  
def ctests(rt):
  ctests = []
  for sset in ssets(rt):
    for i in range((ssets(rt)).index(sset),len(ssets(rt))):
      ctest = [sset,ssets(rt)[i]]
      # print(ctest)
      # print(ctest[0], " vs ", ctest[1])
      ctests.append(ctest)
      # print(ctests)
  return ctests

sroot = ET.parse(src).find('.//selectionsets')
droot = ET.fromstring(tmp)

a = droot.find("batchtest")
a.append(sroot.find("selectionsets")) # append selection sets from source file
a.set('name',((os.path.basename(dst)).split(".")[0]))
a.set('internal_name',((os.path.basename(dst)).split(".")[0]))

b = droot.find("batchtest/clashtests")

vfname = listElements(sroot,'viewfolder')[0]
print(vfname)

for vf in sroot.findall('viewfolder'):
    if vf.get('name') == vfname:
        # print(ssets(vf))
        vfroot = vf

nclist = []
for i in range(len(ctests(vfroot))):
  c = ET.fromstring(ttest)
  nname = " ".join((ctests(vfroot)[i][0], "vs", ctests(vfroot)[i][1]))
  # print(nname)
  c.set('name', nname)
  c.find('left/clashselection/locator').text = "/".join(("lcop_selection_set_tree",vfname,ctests(vfroot)[i][0]))
  c.find('right/clashselection/locator').text = "/".join(("lcop_selection_set_tree",vfname,ctests(vfroot)[i][1]))
  nclist.append(ET.tostring(c))
  
for i in nclist:
  b.append(ET.fromstring(nclist[i]))

f = open(dst, "w")
(ET.ElementTree(droot)).write((f),encoding='unicode')
f.close()

# update locators naming with viewfolders:
# - for one folder
# - for each folder
# - for chosen folder sys.argv[3]
# - for chosen folders sys.argv[3]

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