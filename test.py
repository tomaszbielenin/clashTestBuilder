import xml.etree.ElementTree as ET
import copy

s = """<a>
   <b>
    <c>World</c>
   </b>
 </a>"""

tmp = ET.fromstring(s)
b = tmp.find("b")
dupe = copy.deepcopy(b) #copy <c> node
tmp.append(dupe) #insert the new node

print(ET.tostring(tmp))
tree = ET.ElementTree(tmp)
# dst = open("C:/Scripting/Git/clashTestBuilder/output.xml", "w")
tree.write(open("C:/Scripting/Git/clashTestBuilder/output.xml", "w"),encoding='unicode')
