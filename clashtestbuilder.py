# Add no vfolder option
# Add tolerance arg
# vfolders by index/slice?
# add if for no arg - userinput; args fro setup *.txt
# Add units parameter
# Clash search set against multiple search sets at once (AvB,C,D; BvC,D; DvD)
# def locator() function to create locator string from multiple elements

import sys
import os
import xml.etree.ElementTree as ET

src = sys.argv[1] # source xml file with search sets
dst = sys.argv[2] # destination xml file
vfolders = sys.argv[3].split(",") # viewfolder list to be processed
# tolerance = sys.argv[4] # add function to set tolerance

 
# src = "C:/Scripting/Git/clashTestBuilder/SSets_SubFolder.xml"
# tmp = "C:/Scripting/Git/clashTestBuilder/template.xml"
# dst = "C:/Scripting/Git/clashTestBuilder/ClashTests.xml"
# ((os.path.basename(dst)).split(".")[0]) - get file name
tmp = """<?xml version="1.0" encoding="UTF-8" ?>

<exchange xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://download.autodesk.com/us/navisworks/schemas/nw-exchange-12.0.xsd" units="m" filename="" filepath="">
  <batchtest name="CNEB_ClashTests" internal_name="CNEB_ClashTests" units="m">
    <clashtests>
    </clashtests>
  </batchtest>
</exchange>"""

ttest = """<clashtest name="" test_type="hard" status="new" tolerance="0.0010000000" merge_composites="0">
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
  # Lists 'name' attribute for all elements of given type
  path = "".join(('.//',str(element)))
  elist = []
  if rt.find(path):
    for el in rt.findall(path):
      elist.append(el.get('name'))
  return elist

def ssets(rt):
  # Returns a list of selectionsets in root element
  ssets = []
  for sset in rt.findall('.//selectionset'):
    ssets.append(sset.get('name'))
  return ssets
  
def ctests(rt):
  # Returns a list of ssets coupled for clash test
  ctests = []
  for sset in ssets(rt):
    for i in range((ssets(rt)).index(sset),len(ssets(rt))):
      ctest = [sset,ssets(rt)[i]]
      ctests.append(ctest)
  return ctests

sroot = ET.parse(src).find('.//selectionsets')
droot = ET.fromstring(tmp)

a = droot.find("batchtest")
a.append(sroot) # append selection sets from source file
a.set('name',((os.path.basename(dst)).split(".")[0]))
a.set('internal_name',((os.path.basename(dst)).split(".")[0]))

b = droot.find("batchtest/clashtests")

# vfolders = listElements(sroot,'viewfolder')[0:1] # use slice as an argument maybe
# print(vfolders)

vfroots = []
for vf in sroot.findall('viewfolder'):
    if vf.get('name') in vfolders:
        vfroots.append(vf)        

nclist = []
for vf in vfroots:
  vfname = vf.get('name')
  for i in range(len(ctests(vf))):
    c = ET.fromstring(ttest)
    nname = " ".join((ctests(vf)[i][0], "vs", ctests(vf)[i][1]))
    c.set('name', nname)
    c.find('left/clashselection/locator').text = "/".join(("lcop_selection_set_tree",vfname,ctests(vf)[i][0]))
    c.find('right/clashselection/locator').text = "/".join(("lcop_selection_set_tree",vfname,ctests(vf)[i][1]))
    nclist.append(ET.tostring(c))
    b.append(ET.fromstring(nclist[i]))

f = open(dst, "w")
(ET.ElementTree(droot)).write((f),encoding='unicode')
f.close()

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