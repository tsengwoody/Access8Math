#Access8Math ReadMe

This NVDA addon provides the function of reading math content. Although the original NVDA already equipped this feature by applying MathPlayer, some functions still needed to be improved, especially reading math content in Chinese.

Access8Math allows:

*	Read math content Written in MathML in web browser(Mozilla Firefox, Microsoft Internet Explorer and Google Chrome).
*	Navigate the math content by pressing "Space" in math content. Also, you can partially explore the subparts in expression and move or zoom the content between the subpart.
*	In navigation mode, indicate the meaning of subpart in the upper layer part.
*	In navigation mode command：
	*	"Down Arrow": Zoom out the current math content into smaller subpart.
	*	"Up Arrow": Zoom in the current math content into larger subpart. 
	*	"Left Arrow": Move to the previous math content.
	*	"Right Arrow": Move to the next math content.
	*	"Home": Move back to the top.(Entire math content)	
	*	"End": Move to the last and least subpart.
	*	"Numpad 1~9": Reading the math content into serialized text using NVDA Reviewing Text.
	*	"ESC": Exit the navigation mode.
*	"Ctrl+Alt+M": Switch the mode between Access8Math and MathPlayer.(MathPlayer installed only)

Math rules and definitions analyzed by math contents are continuing increasing.

We are now focusing the MathML written in Presentation Markup, because MathML graphical input tools such as word, math type, wiris generated MathML are all in this type.

Math contents in Wiki are all written in MathML.

*	Matrix multiplication: https://en.wikipedia.org/wiki/Matrix_multiplication
*	Cubic function: https://en.wikipedia.org/wiki/Cubic_function

Source code: https://github.com/tsengwoody/Access8Math

Please report any bugs or comments, thank you!

# Access8Math 說明

此NVDA addon提供數學內容的閱讀，原先NVDA亦有此功能，但因是調用MathPlayer的功能，部份功能尚顯不足，尤其在中文方式的閱讀上

功能有：

*	可閱讀網頁瀏覽器(Mozilla Firefox, Microsoft Internet Explorer and Google Chrome)上以MathML撰寫的數學內容
*	在數學內容上按空白鍵可與該數學內容進行導航瀏覽，亦即可部份瀏覽數學內容中的子內容並在子內容間移動或縮放子內容大小
*	在導航瀏覽時會提示該項子內容在其上層子內容的意義
*	在導航瀏覽時按鍵：
	*	向下鍵縮小當前數學內容成更小的子內容
	*	向上鍵放大當前數學內容成更大的子內容
	*	向左鍵向前一項數學內容
	*	向右鍵向後一項數學內容
	*	home鍵回到最頂層(完整數學內容)
	*	end鍵進入最後一項的最小部份
	*	數字鍵盤1-9：使用NVDA Reviewing Text方式閱讀序列化的數學內容
	*	esc鍵退出導航瀏覽模式
*	ctrl+alt+M：可在Access8Math與MathPlayer間切換(有安裝MathPlayer才能切換)

數學內容解析數學規則意義持續增加中

目前先針對以Presentation Markup寫成的MathML處理，因word、math type、wiris等MathML圖形化輸入工具產生的MathML皆為此型態

維基百科上的數學內容皆以MathML寫成

*	矩陣乘法：https://zh.wikipedia.org/zh-tw/%E7%9F%A9%E9%99%A3%E4%B9%98%E6%B3%95
*	三次方程：https://zh.wikipedia.org/zh-tw/%E4%B8%89%E6%AC%A1%E6%96%B9%E7%A8%8B

原始碼：https://github.com/tsengwoody/Access8Math

歡迎提出見意與bug回報，謝謝！

# NVDA Add-on Scons Template #

This package contains a basic template structure for NVDA add-on development, building, distribution and localization.
For details about NVDA add-on development please see the [NVDA Developer Guide](http://www.nvda-project.org/documentation/developerGuide.html).
The NVDA addon development/discussion list [is here](http://www.freelists.org/list/nvda-addons)

Copyright (C) 2012-2014 nvda addon team contributors.

This package is distributed under the terms of the GNU General Public License, version 2 or later. Please see the file COPYING.txt for further details.

## Features

This template provides the following features you can use to help NVDA add-on development:

*	Automatic add-on package creation, with naming and version loaded from a centralized build variables file (buildVars.py).
*	Manifest file creation using a template (manifest.ini.tpl). Build variables are replaced on this template.
*	Compilation of gettext mo files before distribution, when needed.
- To generate a gettext pot file, please run scons pot. A **addon-name.pot** file will be created with all gettext messages for your add-on. You need to check the buildVars.i18nSources variable to comply with your requirements.
*	Automatic generation of manifest localization files directly from gettext po files. Please make sure buildVars.py is included in i18nFiles.
*	Automatic generation of HTML documents from markdown (.md) files, to manage documentation in different languages.

## Requirements

You need the following software to use this code for your NVDA add-ons development:

- a Python distribution (2.7 or greater is recommended). Check the [Python Website](http://www.python.org) for Windows Installers.
- Scons - [Website](http://www.scons.org/) - version 2.1.0 or greater. Install it using **easy_install** or grab an windows installer from the website.
- GNU Gettext tools, if you want to have localization support for your add-on - Recommended. Any Linux distro or cygwin have those installed. You can find windows builds [here](http://gnuwin32.sourceforge.net/downlinks/gettext.php).
- Markdown-2.0.1 or greater, if you want to convert documentation files to HTML documents. You can [Download Markdown-2.0.1 installer for Windows](https://pypi.python.org/pypi/Markdown/2.0.1) or get it using `easy_install markdown`.


## Usage

### To create a new NVDA add-on, taking advantage of this template: ###

- Create an empty folder to hold the files for your add-on.
- Create an **addon** folder inside this new folder. Inside **addon* folder, create needed folders for the add-on modules (e.g. appModules, synthDrivers, etc.). An add-on may have one or more module folders.
- Copy the **buildVars.py** file, the manifest.ini.tpl file, the manifest-translated.ini.tpl, **SCONSTRUCT**, site_scons, .gitignore and .gitattributes files to the created folder.
- In the **buildVars.py** file, change variable **addon_info** with your add-on's information (name, summary, description, version, author and url).
- Put your code in the usual folders for NVDA extension, under the **addon** folder. For instance: globalPlugins, synthDrivers, etc.
- Gettext translations must be placed into addon\locale\<lang>/LC_MESSAGES\nvda.po. 

### To manage documentation files for your addon: ###

- Copy the **readme.md** file for your add-on to the first created folder, where you copied **buildVars.py**. You can also copy **style.css** to improve the presentation of HTML documents.
- Documentation files (named **readme.md**) must be placed into addon\doc\<lang>/.

### To package the add-on for distribution: ###

- Open a command line, change to the folder that has the **SCONSTRUCT** file (usually the root of your add-on development folder) and run the **scons** command. The created add-on, if there were no errors, is placed in the current directory.
- You can further customize variables in the **buildVars.py** file.

Note that this template only provides a basic add-on structure and build infrastructure. You may need to adapt it for your specific needs.

If you have any issues please use the NVDA addon list mentioned above.
