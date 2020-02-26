# Add no vfolder option
# vfolders by index/slice?
# Add units parameter
# Clash search set against multiple search sets at once (AvB,C,D; BvC,D; DvD)
# def locator() function to create locator string from multiple elements
# Add if no search set case
# *Add option to append new tests
# Add file selection window, change root folder to sfile folder
# Change variable type to expected one
# Add argument detection for batch mode
# Clach multiple folders
# Option without importing search sets (empty <selectionsets></selectionsets> node)

import sys
import os
import xml.etree.ElementTree as ET
import easygui

#Function definitions

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

def locator(lst):
  locator='/'.join(lst)
  return locator

#Argument assignments

if len(sys.argv) <= 1:
  print("--Welcome to Clash Test Builder--")
  print("--Provide required parameters--")
  print()
  print('Select source file containing search sets:')
  src = easygui.fileopenbox()
  sroot = ET.parse(src).find('.//selectionsets')
  print()
  print('Available Viewfolders:')
  for vf in sroot.findall('viewfolder'):
    print(vf.get('name'))
  print()
  vfolders = str(input('Viewfolder name you want to create clash tests for:')) # option for more vfs TBA
  print(vfolders)
  tolerance = str(0.001*float(input('Tolerance (mm):')))
  print('Select output file:')
  dst = easygui.fileopenbox()
  ssappend = input('Do you want to append search sets [y/n]?:').upper()
else:
  src = sys.argv[1] # source xml file with search sets
  sroot = ET.parse(src).find('.//selectionsets')
  dst = sys.argv[2] # destination xml file
  vfolders = sys.argv[3].split(",") # viewfolder list to be processed
  tolerance = str(0.001*float(sys.argv[4])) # add function to set tolerance
  ssappend = sys.argv[4]


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

droot = ET.fromstring(tmp)

a = droot.find("batchtest")
if ssappend == 'Y':
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
  ct = ctests(vf)
  for i in range(len(ct)):
    c = ET.fromstring(ttest)
    nname = " ".join((ct[i][0], "vs", ct[i][1]))
    c.set('name', nname)
    c.set('tolerance', tolerance)
    c.find('left/clashselection/locator').text = "/".join(("lcop_selection_set_tree",vfname,ct[i][0]))
    c.find('right/clashselection/locator').text = "/".join(("lcop_selection_set_tree",vfname,ct[i][1]))
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
