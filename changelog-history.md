# Access8Math Changelog History

## 4.2

* Added import/export feature for .a8m files.
* Fixed some issues.

## 4.1

* Indicate a capital letter using NVDA voice configuration when the node consists of only one uppercase letter.
* Resolved Opening the virtual context menu in the file explorer in Access8Math conflicts with toggling native selection mode in NVDA Browsing mode, as they both use the same gesture (NVDA+Shift+F10).
* Remove outdated setting options.
* Limit the write feature to within the Access8Math editor, notepad only.
* Rewrite readme.

## 4.0

* Compatibility with NVDA 2024.1
* Removed legacy code

## 3.8

* Added table navigation support (ctrl+alt+arrow keys) for Mtable in interactive mode.
* Added new categories to the LaTeX menu, including Geometry, Combinatorics, Trigonometric Functions, and Calculus.
* Added new items to the LaTeX menu.
* Included the rounding symbol.
* Fixed conversion errors of .1 and > symbols when converting Nemeth to LaTeX.
* Fixed the path error for restoring default files in the math rules dialog.

## 3.7

* new feature: Auto-Complete feature in write feature.
* Added "mixed number" rule to the Nemeth to LaTeX translator.
* In Access8Math editor, Added close button on the upper right corner to close the Access8Math editor.
* Fixed SimultaneousEquationsType rule(read feature).
* Fixed "|" symbol don`t convert to text according in Unicode dictionary(read feature).
* Fix issues with Converting ∫ Nemeth Braille to LaTeX.

## 3.6

* new feature: Nemeth Braille Input, with the same functionality as LaTeX input. Allows for real-time interactive navigation (Alt+I) during editing and supports outputting HTML+MathML documents.
* new feature: Added Nemeth delimiter UEB/at(@@) for distinguish Nemeth content.
* new feature: You can convert and copy LaTeX from Math object in interactive navigation mode.
* Added the NVDA+Shift+F10 shortcut to open  virtual context menu in the file explorer.
* Fixed and optimized localized UI issues and cleaned localized file format.

## 3.5

* Vectors and rays can be distinguished correctly
* Utilizing dialogue to display image, video, or audio resources in an Access8Math HTML document
* Using a new window to open link resources in an Access8Math HTML document
* The MathML namespace is exported when copying MathML from the Math object in interactive navigation mode
* Display font adjustment, find and replace feature in Access8Math editor
* Compatibility with NVDA 2023.1

## 3.4

* Speech, Braille, and interactive source move to Preferences -> Settings -> Math Reader category.
* Integrated MathCAT, you can choose what speech, braille, and interactive source(Access8Math/Math Player/MathCAT) you need in Math Reader settings panel when having already installed Math Player/MathCat.
* Used MultiCategorySettingsDialog to collect settings dialog.
* Press NVDA+alt+e open text file with the built-in editor in File Explore.
* In virtual menus, submenu can open by enter
* Implenment MathML menclose tag rule
* new feature: virtual context menu in File Explorer. It can quickly open Access8Math Document to view or edit it(Please read "Access8Math editor and Access8Math Document" section to know detail information)

## 3.3

* Add built-in editor using traditional editing area because of windows 11 changed to UIA editing area
* built-in editor new/open/save feature
* Access8Math language initial setting is based on NVDA language setting
* Improved speech and braille display in virtual menus
* Compatibility with NVDA 2022.1
* Fixed marked menu cannot open when document is empty
* Fixed translate LaTeX/AsciiMath feature
* Fixed HTML document rendering problem when HTML document display setting choice text option

## 3.2

* New feature "`" to separate data blocks, the blocks enclosed by "`" are AsciiMath data
* New feature editing-shortcut for browse navigation mode cut (ctrl+x), copy (ctrl+c), paste (ctrl+v), delete (delete/back space)
* New feature moving-shortcut for browse navigation mode move between interactive data blocks (tab), move between AsciiMath data blocks (a)
* Change move cursor way in browse navigation mode - move cursor way with up, down, left and right arrow keys and read out the contents of the data block after the movement.
* When the cursor moves in the browse navigation mode, the math data block will read the serialized textual content of math instead of the source code
* When the cursor is in the math data block in the browse navigation mode, press the space or enter key to interact with the math data block.
* New feature English letters as shortcut keys that can be setted
* New feature greek alphabet shortcut gesture
* Shortcut key input is only apply in the LaTeX area
* set using audio or speech indicate to switching of browse navigation mode
* The LaTeX command menu can be opened in the text area and insert LaTeX separators when LaTeX command inserting
* New feature translation menu, which can convert the LaTeX/AsciiMath data format of the block where the cursor is located. It belongs to the command gesture group. When the cursor is in the LaTeX/AsciiMath block, press alt+t to open the translation menu (in the browse navigation mode, ctrl+t)
* New feature batch menu, which can convert the entire document LaTeX/AsciiMath data format to each other, and can convert the LaTeX separator between brackets and dollar. It belongs to the command gesture group. Press alt+b to open the batch menu
* Added MathML block type, support alt+i, single letter navigation "m", tab movement in browse navigation mode
* New feature braille custom-defined math rules and unicode dictionary, which are the same as speech
* The exported HTML can show with markdown
* The exported HTML is added page title and file name by notepad window title.

## 3.1

* HTML windows are now presented as virtual menu
* Fixed an issue where the HTML view cannot be converted when text include "`" character
* When the number of words in the document is greater than 4096, the content will not be converted to HTML view
* Added mathematical set LaTeX commands
* Update alt+m to insert "\(", "\)" LaTeX marks before and after the currently selected text (when there is no selected text, it is the current cursor position)
* In the General settings, you can choose whether the math content in the exported HTML is presented on a separate line(block/inline)
* When exporting HTML, save the original text file in the compressed file
* In the general settings, you can choose to use bracket or money symbol as the LaTeX delimiter
* In the general settings, you can choose the source of speech, braille, and interaction(Access8Math or Math Player)
* Activate/deactivate write/block navigate/shortcut gesture by gesture
* switch the source of speech/braille/interact source by gesture(Access8Math or Math Player)

## 3.0

* Write mathematical content in AsciiMath
* Write mathematical content in LaTeX
* Writing mixed content (text content and mathematical content)
* Use shortcut keys to move the cursor to different types of blocks in edit field
* Use command menu to select commands in edit field
* Set shortcuts in the LaTeX command menu
* Review and export content in edit field to HTML

## 2.6

* Auto entering interactive mode when showing Access8Math interaction window.
* You can choose how to hint no movement in interactive mode: beep or speech 'no move' two way.
* The content of the current item will be repeated again When there is no movement.

## 2.5

* Adding Russian translation of rules and UI. Thanks to the translation work of Futyn-Maker.
* Fixing compound symbol translation failed bug.
* Removing duplicates of lowercase letters and added general uppercases in en unicode.dic(0370~03FF).

## 2.3

* Fix bug.

## 2.3

* Compatibility with Python3
* refactoring module and fix code style
* Adding one symbol vector rule

## 2.2

*fix bug incorrect speech when a single node has more characters.
* Fix compatibility issue in NVDA 2019.2, thanks to pull requests of CyrilleB79.
* Fix bug in unicode dict has duplicate symbols.
* Add translations in French, thanks to the translation work of CyrilleB79.
* Adjust keyboard shortcut.

## 2.1

* In "General Settings", you can set whether "Access8Math interaction window" is automatically displayed when entering interactive mode.
* In interactive mode, "interaction window" can be displayed manually via ctrl+m when "interaction window" are not showed.
* Fix multi-language switching bug.
* Add translations in Turkish, thanks to the translation work of cagri (çağrı doğan).
* Compatibility update for nvda 2019.1 check for add-on`s manifest.ini flag.
* Refactoring dialog window source code.

## 2.0

* Add multi-language new-adding and customizing settings,and add three windows of "unicode dictionary", "math rule", "New language adding"
* The "unicode dictionary" can customize the reading way of each math symbolic text.
* "math rule" can customize the reading method and preview the modification through the sample button before completed.
* "New language adding" allows adding language not provided in the built-in system. The newly language will be added to the general settings, and multi-language customization can be achieved through reading definition of "unicode dictionary" and "mathematical rules".
* improved in interactive mode, you can use the number keys 7~9 to read sequence text in the unit of line.

## 1.5

* In "general setting" dialog box add setting pause time between items. Values from 1 to 100, the smaller the value, the shorter the pause time, and the greater the value, the longer the pause time.
* Fix setting dialog box can't save configure in NVDA 2018.2.

## 1.4

* Adjust settings dialog box which divided into "general setting" and "rules setting" dialog box. "General Settings" is the original "Access8Math Settings" dialog box, and "Rule Settings" dialog box is for selecting whether specific rules are enabled.
* New rules
 * vector rule: When there is a "⇀" right above two Identifier, the item is read as "Vector...".
 * frown rule：When there is a " ⌢ " right above two Identifier, the item is read as "frown...".
* Fix bug.

## 1.3

* New rule
 * positive rule: Read "positive" rather than "plus" when plus sign in first item or its previous item is certain operator.
 * square rule: When the power is 2, the item is read as "squared".
 * cubic rule: When the power is 3, the item is read as "cubed".
 * line rule: When there is "↔" right above two Identifier, the item is read as "Line ...".
 * line segment rule: When there is "¯" right above two Identifier, the item is read as "Line segement ...".
 * ray rule: When there is a "→" right above two Identifier, the item is read as "Ray ..."
* Add interaction window：　Pressing "Space" in math content to open "Access8Math interaction window" which contains "interaction" and "copy" button.
 * interaction: Into math content to navigate and browse.
 * copy: Copy MathML object source code.
* Add zh_CN UI language(.po).
* Adjust inheritance relationship between rules to ensure proper use of the appropriate rules in conflict.
* Fix bug.

## 1.2

* New rule
 * negative number rule: Read 'negative' rather than 'minus sign' when minus sign in first item or its previous item is certain operator.
* integer add fraction rule: Read 'add' between integer and fraction when fraction previous item is integer.
* Program architecture improve
 * add sibling class
 * add dynamic generate Complement class
* Fix bug

## 1.1

* In navigation mode command, "Ctrl+c" copy object MathML source code.
* Settings dialog box in Preferences:
 * Language: Access8Math reading language on math content.
 * Analyze the mathematical meaning of content: Semantically analyze the math content, in line with specific rules, read in mathematical meaning of that rules.
 * Read defined meaning in dictionary: When the pattern is definied in the dictionary, use dictionary to read the meaning of subpart in the upper layer part.
 * Read of auto-generated meaning: When the pattern is not difined or incomplete in dictionary, use automatic generation function to read the meaning of subpart in the upper layer part.
* Add some simple rule. Single rules are simplified versions of various rules. When the content only has one single item, for better understanding and reading without confusion, you can omit to choose not to read the script before and after the content.
* Update unicode.dic.
* Fix bug.
