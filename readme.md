# Access8Math ReadMe

This NVDA addon provides the function of reading math content. Although the original NVDA already equipped this feature by applying MathPlayer, some functions still needed to be improved, such as not providing or incomplete specific language translation, not providing specific language navigation and browsing and many more.

Navigation interactive mode can segment a math content into smaller partial fragments for speaking, and select the read fragment and method through a series of keyboard key operations. This function can better understand the structure and items of long math content. The hierarchical relationship with the item.

## Reading feature

*	Read math content written in MathML in web browser(Mozilla Firefox, Microsoft Internet Explorer and Google Chrome) or read Microsoft Word math content written in MathType. (MathPlayer installed only)
*	Interaction: Press space or enter on the MathML math object to enter navigation interactive mode. It means you can browse part of the sub-content in the math content and move between sub-contents or zoom the size of the sub-content
*	Pressing "Space" in math content to open "Access8Math interaction window" which contains "interactive" and "copy" button.
	*	interaction: Into math content to navigate and browse. Also, you can partially explore the subparts in expression and move or zoom the content between the subpart.
	*	copy: Copy MathML object source code.
* Text review: Press the numeric keyboard 1-9 during navigation to read the mathematical content of the serialized text word by word and line by line
* Analyze the overall mathematical meaning of the content: analyze the structure of MathML, and when it meets a specific rule, read it aloud in the mathematical meaning of the rule
* Analyze the mathematical meaning of the content item: When navigating and browsing, it will prompt the meaning of the content under its upper content. For example, there are two score items, and moving between them will enroll the item as the denominator or numerator

## navigation interactive mode command：

*	"Down Arrow": Zoom in on a smaller subpart of the math content.
*	"Up Arrow": Zoom out to  a larger subpartthe of the math content .
*	"Left Arrow": Move to the previous math content.
*	"Right Arrow": Move to the next math content.
*	"Home": Move back to the top.(Entire math content)	
*	"Ctrl+c": Copy object MathML source code
*	"Numpad 1~9": Reading the math content into serialized text using NVDA Reviewing Text.
*	"ESC": Exit the navigation mode.

## Writing feature

Writing mixed content (text content and mathematical content):

### write mixed content

Use delimiter(start delimiter "\(" and end delimiter "\)", LaTeX block) to determine the area between the text content and the mathematical content, that is, the data in LaTeX block is mathematical content (LaTeX), and the data outside LaTeX block is text content.

Press alt+h in edit field to convert an HTML document with mixed text data and mathematical data and can be reviewed or exported. The data in the LaTeX block will be converted to MathML for presentation with normal text.

*	review: Open the converted HTML document through a program that opens the .HTML extension by default.
*	export: Pack the converted HTML document into a zip file.

Press alt+m key in edit field to pop up the markup command window, select "LaTeX" and press enter, the LaTeX mark will be insert into before and after the currently selected text (the current cursor when there is no text selected) and the cursor will be automatically moved into it for quick input the content.

Press alt+l key in edit field to pop up the LaTeX command window, select the LaTeX command item to be added and press enter to add the corresponding LaTeX syntax at the current cursor and automatically move the cursor to the appropriate input point for quick Enter the content.

LaTeX command window

* Select the LaTeX command item and press f1~f12 to set the shortcut
* Select the LaTeX command item and press d to remove the shortcut that has been set
* Select the LaTeX command item and press enter to add the corresponding LaTeX syntax at the current cursor

In edit field and the cursor is in the LaTeX block, press alt+i to enter navigation interactive mode

alt+h, alt+i, alt+l, alt+m are write gesture groups. Press alt+w edit field to activate or deactivate write gestures.

Edit cursor block navigation move(toggle:alt+n)

*	In edit field, press alt+left arrow key to move to the start point of the previous data block
*	In edit field, press alt+down key without moving, but only read the content of the current data block
*	In edit field, press alt+right arrow key to move to the start point of the next data block
*	In edit field, press alt+home to move to the start point of the current data block
*	In edit field, press alt+end to move to the end point of the current data block
* In the editing area, press alt+shift+left arrow key to move to the previous data block and select
* In the editing area, press alt+shift+down key to move to the current data block and select
* In the editing area, press alt+shift+right arrow to move to the next data block and select

Press alt+s in edit field to turn on or off the shortcut mode. When the shortcut mode is on, press f1~f12 to quickly insert LaTeX syntax. When the shortcut mode is on, press shift+f1~f12 to read out the LaTeX commands currently bound to the shortcut.

Press NVDA+shift+space in edit field to turn on or off the edit single letter navigation mode. When the edit single letter navigation mode is turned on, you can move the edit cursor with single letter navigation

The following keys by themselves jump edit cursor to the next available block, while adding the shift key causes them to jump edit cursor to the previous block:

*	l: move to the next LaTeX block
*	t: move to the next text block

mixed content example: The solution of the quadratic equation in one variable \(ax^2+bx+c=0\) is \(\frac{-b\pm\sqrt{b^2-4ac}}{2a}\).

## settings

All Access8Math menus are centralized in tools -> Access8Math

### read feature settings

*	General Settings dialog:
	*	Language: Access8Math speaking language
	*	Item interval time: Setting pause time between items. Values from 1 to 100, the smaller the value, the shorter the pause time, and the greater the value, the longer the pause time.
	*	Showing Access8Math interaction window when entering interaction mode: Whether to show "Access8Math interaction window" when pressing the space key on the math object.
	*	Analyze the mathematical meaning of the content: perform semantic analysis on the mathematical content, and when it meets a specific rule, using that rule to speak.
	*	Reading pre-defined meaning in dictionary when navigating in interactive mode: When the pattern is definied in the dictionary, use dictionary to read the meaning of subpart in the upper layer part.
	*	Reading of auto-generated meaning when navigating in interactive mode: When the pattern is not difined or incomplete in dictionary, use automatic generation function to read the meaning of subpart in the upper layer part.
	*	Using a beep to alert no move: When navigating in interactive mode, It will hint by beep. If it is not checked, it will hint by speaking "no move".
	*	Using NVDA+alt+letter to toggle command gesture: Whether shortcut needs to be added with NVDA key when toggle command gesture in edit field
*	Rule Settings dialog box: select whether rules are actived.

### localization

*	"Unicode dictionary" allows customizing the reading method for each symbol text.
*	"Mathematics Rules" allows customizing the reading method for each type of mathematics.
*	"Add a new language" can add languages: that were not originally provided in the built-in. After adding, there will be more newly added language families in the general settings and can be used to define the reading method through the "unicode dictionary" and "mathematics rules" to reach localization

#### Math Rules

Access8Math establishes 46 mathematical rules according to the mathematical type and logic to decide the reading math method and order. According to different local math reading logic, the math reading text and order can be changed. The method is as follows:

Edit: After entering the "math rule", the window lists 46 math rules. Choose any math rule and select the "Edit" to enter the editing entry.

The "editing entry" can be divided into two major blocks, the "Serialized ordering" and the "Child role".
*	Serialized ordering: Math rule is divided into multiple blocks according to the reading order. In this area, the reading order of child node and the delimitation text of start, inter- and the end can be changed. Taking the fractional rule mfrac as an example, this rule is divided into five reading blocks. The order 0, 2, and 4 represent the initial prompt, the project segmentation prompt, and the end prompt, respectively, and the meanings text can be changed in each field. Order 1 and 3 adjust the reading	sequence of child node which can be changed in the drop-down menu.
*	Child role:  The next-level sub-item of the mathematical rule. Taking the fractional rule mfrac as an example, the rule contains the numerator and the denominator. The sub-content in the upper sub-content meaning can be changed in the child-node role field.

Example: You can check the reading method of this math rule after editing. After clicking, a math content is preset the corresponding math rules for confirming whether the reading method is as expected.

Recover default: Restores the list of math rules to their initial presets.

Import: Import math rules files, which can be used to load math rules files.

Export: Save the math rules file to the specified path to share or keep.

## example

Math contents in Wiki are all written by MathML.

*	Quadratic equation: https://en.wikipedia.org/wiki/Quadratic_equation
*	Matrix multiplication: https://en.wikipedia.org/wiki/Matrix_multiplication
*	Cubic function: https://en.wikipedia.org/wiki/Cubic_function

Quadratic equation

*	LaTeX: \(ax^2+bx+c=0\)
*	MathML: <math xmlns="http://www.w3.org/1998/Math/MathML"><mfrac><mrow><mo>-</mo><mi>b</mi><mo>&#xB1;</mo><msqrt><msup><mi>b</mi><mn>2</mn></msup><mo>-</mo><mn>4</mn><mi>a</mi><mi>c</mi></msqrt></mrow><mrow><mn>2</mn><mi>a</mi></mrow></mfrac></math>

github: https://github.com/tsengwoody/Access8Math

Please report any bugs or comments, thank you!

# Access8Math v3.1 Update

*	NVDA+ gestures enable option adjustment and can modify the shortcut keys in the input gesture
*	HTML windows are now presented as virtual menu
*	Fixed an issue where the HTML view cannot be converted when text include "`" character
*	When the number of words in the document is greater than 4096, the content will not be converted to HTML view
*	Added mathematical set LaTeX commands
*	Update alt+m to insert "\(", "\)" LaTeX marks before and after the currently selected text (when there is no selected text, it is the current cursor position)
*	In the General settings, you can choose whether the math content in the exported HTML is presented on a separate line(block/inline)
*	When exporting HTML, save the original text file in the compressed file
*	In the general settings, you can choose to use bracket or money symbol as the LaTeX delimiter
*	In the general settings, , you can choose the source of speech, braille, and interaction(Access8Math/Math Player)
*	Dynamic gesture binding write/block navigate/shortcut gesture
*	Activate/deactivate write/block navigate/shortcut gesture by gesture

# Access8Math v3.0 Update

*	Write mathematical content in AsciiMath
*	Write mathematical content in LaTeX
*	Writing mixed content (text content and mathematical content)
*	Use shortcut keys to move the cursor to different types of blocks in edit field
*	Use command menu to select commands in edit field
*	Set shortcuts in the LaTeX command menu
*	Review and export content in edit field to HTML

# Access8Math v2.6 Update

*	Auto entering interactive mode when showing Access8Math interaction window.
*	You can choose how to hint no movement in interactive mode: beep or speech 'no move' two way.
*	The content of the current item will be repeated again When there is no movement.

# Access8Math v2.5 Update

*	Adding Russian translation of rules and UI. Thanks to the translation work of Futyn-Maker.
*	Fixing compound symbol translation failed bug.
*	Removing duplicates of lowercase letters and added general uppercases in en unicode.dic(0370~03FF).

# Access8Math v2.3 Update

*	Fix bug.

# Access8Math v2.3 Update

*	Compatibility with Python3
*	refactoring module and fix code style
*	Adding one symbol vector rule

# Access8Math v2.2 Update

*fix bug incorrect speech when a single node has more characters.
*	Fix compatibility issue in NVDA 2019.2, thanks to pull requests of CyrilleB79.
*	Fix bug in unicode dict has duplicate symbols.
* Add translations in French, thanks to the translation work of CyrilleB79.
*	Adjust keyboard shortcut.


# Access8Math v2.1 Update

*	In "General Settings", you can set whether "Access8Math interaction window" is automatically displayed when entering interactive mode.
*	In interactive mode, "interaction window" can be displayed manually via ctrl+m when "interaction window" are not showed.
*	Fix multi-language switching bug.
* Add translations in Turkish, thanks to the translation work of cagri (çağrı doğan).
*	Compatibility update for nvda 2019.1 check for add-on`s manifest.ini flag.
*	Refactoring dialog window source code.

# Access8Math v2.0 Update

*	Add multi-language new-adding and customizing settings,and add three windows of "unicode dictionary", "math rule", "New language adding"
*	The "unicode dictionary" can customize the reading way of each math symbolic text.
*	"math rule" can customize the reading method and preview the modification through the sample button before completed.
*	"New language adding" allows adding language not provided in the built-in system. The newly language will be added to the general settings, and multi-language customization can be achieved through reading definition of "unicode dictionary" and "mathematical rules".
*	improved in interactive mode, you can use the number keys 7~9 to read sequence text in the unit of line.

# Access8Math v1.5 update log

*	In "general setting" dialog box add setting pause time between items. Values from 1 to 100, the smaller the value, the shorter the pause time, and the greater the value, the longer the pause time.
*	Fix setting dialog box can't save configure in NVDA 2018.2.

# Access8Math v1.4 update log

*	Adjust settings dialog box which divided into "general setting" and "rules setting" dialog box. "General Settings" is the original "Access8Math Settings" dialog box, and "Rule Settings" dialog box is for selecting whether specific rules are enabled.
*	New rules
	*	vector rule: When there is a "⇀" right above two Identifier, the item is read as "Vector...".
	*	frown rule：When there is a " ⌢ " right above two Identifier, the item is read as "frown...".
*	Fix bug.

	# Access8Math v1.3 update log

*	New rule
	*	positive rule: Read "positive" rather than "plus" when plus sign in first item or its previous item is certain operator.
	*	square rule: When the power is 2, the item is read as "squared".
	*	cubic rule: When the power is 3, the item is read as "cubed".
	*	line rule: When there is "↔" right above two Identifier, the item is read as "Line ...".
	*	line segment rule: When there is "¯" right above two Identifier, the item is read as "Line segement ...".
	*	ray rule: When there is a "→" right above two Identifier, the item is read as "Ray ..."
*	Add interaction window：　Pressing "Space" in math content to open "Access8Math interaction window" which contains "interaction" and "copy" button.
	*	interaction: Into math content to navigate and browse.
	*	copy: Copy MathML object source code.
*	Add zh_CN UI language(.po).
*	Adjust inheritance relationship between rules to ensure proper use of the appropriate rules in conflict.
*	Fix bug.

# Access8Math v1.2 update log

*	New rule
	*	negative number rule: Read 'negative' rather than 'minus sign' when minus sign in first item or its previous item is certain operator.
	*	integer add fraction rule: Read 'add' between integer and fraction when fraction previous item is integer.
*	Program architecture improve
	*	add sibling class
	*	add dynamic generate Complement class
*	Fix bug

# Access8Math v1.1 update log

*	In navigation mode command, "Ctrl+c" copy object MathML source code.
*	Settings dialog box in Preferences:
	*	Language: Access8Math reading language on math content.
	*	Analyze the mathematical meaning of content: Semantically analyze the math content, in line with specific rules, read in mathematical meaning of that rules.
	*	Read defined meaning in dictionary: When the pattern is definied in the dictionary, use dictionary to read the meaning of subpart in the upper layer part.
	*	Read of auto-generated meaning: When the pattern is not difined or incomplete in dictionary, use automatic generation function to read the meaning of subpart in the upper layer part.
*	Add some simple rule. Single rules are simplified versions of various rules. When the content only has one single item, for better understanding and reading without confusion, you can omit to choose not to read the script before and after the content.
*	Update unicode.dic.
*	Fix bug.