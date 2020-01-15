--About Clash Test Builder--

Clash Test Builder is na app that automates clash test building for Navisworks Manage clash detective.
Algorithm creates pairs from all search sets in selected viewfolder from exported search set source file(round robin style).

--Installation--

Copy clashtestbuilder parent folder with all child items to your local drive.

--Usage--

Clash Test Builder will only work from its parent folder.
To create output file with clash tests run command prompt, drag and drop clashtestbuilder.exe and provide all parameters.

Syntax:
clashtestbuilder.exe <src_path> <dst> <viewfolder>

src: source file path
dst: output file path
veiwfolder: viewfolder name (including quotation marks)

Example:
C:\scripting\clashtestbuilder\clashtestbuilder.exe "C:\Navisworks\SearchSets\SearchSets.xml" "C:\Navisworks\ClashTests\ClashTests.xml" "MyViewFolder"

--Credits & Source Code--

Author: Tomasz Bielenin
You can check source code (Python) on https://github.com/tomaszbielenin/clashTestBuilder
All comments and ideas for further development are welcomed.

