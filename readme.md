# Access8Math Introduction

Access8Math is an NVDA add-on that enhances the user experience when reading and writing mathematical content.

Access8Math offers text-to-speech/Braille functionality for MathML content. MathML is the standard language for describing math structure and content on the web, which enables visually readable math content through a web browser.

Access8Math can also assist in writing and converting LaTeX to MathML. LaTex is a typesetting system which is easy to write and learn. It’s commonly used for representing math formulas.

With Access8Math's reading, writing, and conversion features, visually impaired users can read and write math content with ease. Based on MathML and LaTeX, two common math markups, Access8Math significantly reduces the difficulty of two-way communication between visually impaired and sighted users.

## Reading Features Overview

* Read MathML content in a web browser.
* Read MathType content in Microsoft Word.
* Read a full paragraph that contains text and math content.
* Provide customized speech output rules, including simplified outputs and pauses between math segments.
* Allow customization of math symbol speech output and Braille output.

##  Interaction Features Overview

* Allow navigating between, zooming in, or zooming out of math segments.
* Use NVDA review cursor to read text.
* Provide mathematical meaning of items when interacting.

## Writing Features Overview

* Convert LaTeX/Nemeth to MathML.
* Provide a command menu to facilitate LaTeX input.
* Provide shortcut gestures to facilitate LaTeX input.
* Help moving the editing cursor more efficiently while editing.
* Preview content that includes LaTeX/Nemeth while editing.
* Convert plain text files into accessible HTML files for preview and export.

# Access8Math Description

The Access8Math add-on provides comprehensive math content reading and writing capabilities.

Access8Math offers customizable speech and braille output, and an Interactive Mode to access and understand math content. In Interactive Mode, users can read math content in smaller segments, as well as choosing the size of the segments through keyboard shortcuts. In this way, they can understand the structure and hierarchical relationships of long math content more easily.

Access8Math also provides a command menu to make writing LaTeX easier. Instead of memorizing complex LaTeX syntaxes, users can navigate through the command menu to input math markups..

In addition, users can preview their inputs while editing, which helps users to find and fix syntax errors as soon as possible.

Finally, Access8Math converts text and math content written in LaTeX into visually readable HTML files. Since both text and math content can be displayed together visually, it makes math discussion between visually impaired and sighted people more fluid.

## MathML Examples

Math contents on Wikipedia are written in MathML:

* Quadratic equation: https://en.wikipedia.org/wiki/Quadratic_equation
* Matrix multiplication: https://en.wikipedia.org/wiki/Matrix_multiplication
* Cubic equation: https://en.wikipedia.org/wiki/Cubic_equation

# Access8Math User Guide

## Reading Features

### Language Setting

Select the language in which the math content in Access8Math will be converted in Settings > Reading. If your language is not supported by the system, see the "Adding a new language" paragraph in the "Localization" section of this document.

### Reading Experience Settings

#### Mathematical Structure Analysis

These rules are designed to enhance the reading experience of commonly used mathematical structures. The system analyzes the content according to the MathML structure and mathematical rules, so that the speech outputs and Braille outputs are more consistent with the mathematical meaning. For example, "x^2" will be read as "square of x" instead of "x super 2". 

Enable or disable this functionality by checking the "Analyze mathematical meaning of contents" checkbox in Settings > Reading. Uncheck this option to view the original MathML structure.

This option also changes the given additional information of the mathematical meaning when navigating between math segments in Interactive Mode.

#### Simplified Speech Outputs

When the system analyzes mathematical rules, it will read them out in a simplified way. If there is only one single item in the math content, it can omit the markups before and after while reading, so that it can be understood more efficiently. For example, "\(\frac{1}{2}\)" will be read as "1 over 2" instead of "fraction with numerator 1 and denominator 2 end fraction". 

Enable or disable a simplified rule from the list of checkboxes in Settings > Rules.

#### Pauses Between Segments

Access8Math reads math content with a pause between items to make the math content easier to understand. 

To adjust the pause time between items, set a value from 1 to 100 in Settings > Reading. A smaller value means a shorter pause time and a larger value means a longer pause time.

### Math Reader Settings

Select the source of the math reader in Settings > Math Reader.

* Speech Source: Use Access8Math/MathCAT/Math Player for speech outputs.
* Braille Source: Use Access8Math/MathCAT/Math Player for Braille outputs.
* Interaction Source: Use Access8Math/MathCAT/Math Player for Interactive Mode.

### Customize Math Symbol Speech Outputs and Braille Outputs

In the "Localization" menu, it’s possible to edit the table of math symbols and the table of mathematical rules. For more details, please refer to the "Localization" section of this document.

## Interaction Features

### How to Activate NVDA Interactive Mode?

For speech-oriented users, it is often preferable to listen to a math equation in smaller segments rather than hearing the whole equation at once. If currently in Browse mode, move the cursor over the math content and press the Space or Enter key.

If not in Browse mode:
1. Move the review cursor to the location of the math content. By default, the review cursor follows the system caret so the system cursor can be moved to the math content.
2. Execute the following shortcut: NVDA + Alt + M to interact with the math content.

Once in Interactive Mode, use commands such as the arrow keys to explore an equation. For example, use the left and right arrow to move within an equation, and use the down arrow to explore a segment of the equation.

When finished reading, simply press Esc to return to the document. For more information about reading and navigating in Math Content, see the next section.

### Available Keyboard Controls in Access8Math Interactive Mode

* Down arrow: Reduces the scope of the reading segment.
* Up arrow: Enlarges the scope of the reading segment.
* Left arrow: Go to the previous math segment.
* Right arrow: Go to the next math segment.
* Ctrl + C: Copy the MathML of the object.
* Home key: Reads the entire math content.
* Numeric Keypad 1-9: Use NVDA Review Mode to read the math content (see the Review Mode section of the NVDA User Guide).
* Esc key: Quit Interactive Mode.
* Table navigation: In a math table, use Ctrl + Alt + arrow keys to move up or down a column, left or right a row. The navigation is the same as NVDA table navigation.
* Ctrl + Alt + Left arrow: Move to the left column.
* Ctrl + Alt + Right arrow: Move to the right column.
* Ctrl + Alt + Up arrow: Move to the previous row.
* Ctrl + Alt + Down arrow: Move to the next row.

### Adjust Additional Information for Outputs in Interactive Mode

* Provide auto-generated additional information: In Interactive Mode, the system provides additional information about the number of items when meanings of sub-nodes are not fully defined in a math rule. This feature applies to situations where some MathML markups may have a variable number of sub-nodes, such as tables, matrices, or equations. The system provides additional information like "first column", "second item", and so on, while navigating. If not willing to hear the additional information, uncheck this setting.

* Use an sound effect to indicate that no movement is possible: When checked, a beep sound appears when it’s not possible to move to a new item; when unchecked, the sound will be replaced by the text "no movement".

## Writing Features

### Access8Math Editor

Access8Math editor allows users to write Markdown documents and add resources (such as images, links, etc.) to the editor’s workspace for referencing them in a document.

When exporting documents, Access8Math editor converts Markdown files into HTML files which displays both the text and the math content. The resources in the document will be archived into the output zip file. This allows the exported HTML file to display various types of contents (such as text, math, images, videos, and audios).

For more information on how to use the import and export features, please refer to the "Import and Export'' section of this document.

### Separators

When writing, special characters are used to separate text content from math content. In other words, the content inside the separators is math content written in a specific math markup, while the content outside is general text content.

| Category | Staring Separator | Ending Separator |
| --- | --- | --- |
| LaTeX (Parentheses) | \( | \) |
| LaTeX (Dollar sign) | $ | $ |
| Nemeth (UEB) | _% | _: |
| Nemeth (at) | @ | @ |

Note: It’s possible to change the separators used in LaTeX/Nemeth in the Settings > Document.

### Mixed Content Examples

* LaTeX (Parentheses): The solution to the quadratic equation \(ax^2+bx+c=0\) is \(x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}\).
* LaTeX (Dollar sign): The solution to the quadratic equation $ax^2+bx+c=0$ is $x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}$.
* Nemeth(UEB): The solution to the quadratic equation _%⠁⠭⠘⠆⠐⠬⠃⠭⠬⠉⠀⠨⠅⠀⠴_: is _%⠭⠀⠨⠅⠀⠹⠤⠃⠬⠤⠜⠃⠘⠆⠐⠤⠲⠁⠉⠻⠌⠆⠁⠼_:.
* Nemeth(at): The solution to the quadratic equation @⠁⠭⠘⠆⠐⠬⠃⠭⠬⠉⠀⠨⠅⠀⠴@ is @⠭⠀⠨⠅⠀⠹⠤⠃⠬⠤⠜⠃⠘⠆⠐⠤⠲⠁⠉⠻⠌⠆⠁⠼@.
* MathML: The solution to the quadratic equation <math display="inline"><mi>a</mi><msup><mi>x</mi><mn>2</mn></msup><mo>+</mo><mi>b</mi><mi>x</mi><mo>+</mo><mi>c</mi><mo>=</mo><mn>0</mn></math> is <math display="inline"><mfrac><mrow><mo>−</mo><mi>b</mi><mi>±</mi><msqrt><msup><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mi>a</mi><mi>c</mi></msqrt></mrow><mrow><mn>2</mn><mi>a</mi></mrow></mfrac></math>.

### Command Gestures (Toggle: NVDA + Alt + C)

* Alt + M: Display the markup command menu. In the window, select LaTeX/Nemeth, and press Enter. It will add the LaTeX/Nemeth markups before and after the currently selected text (or at the current editing cursor if no text is selected), and automatically move the editing cursor into the markups.
* Alt + L: Display the LaTeX command menu (virtual menu). In the window, select a LaTeX command item, and press Enter. The corresponding LaTeX syntax will be added to the current editing cursor, and the editing cursor will be moved to the appropriate input point automatically. If the editing cursor is not in the LaTeX area, the starting and ending separators will be added automatically.
* LaTeX Command Menu
    * In this command menu, use the up and down arrow to select items in the list, and use the right and left arrow to enter or quit a sub-menu. The LaTeX command menu contains two levels: categories and LaTeX markups. For example, use the up and down arrow to select a category in the category list, then use the right arrow to enter the LaTeX markup sub-menu to select the LaTeX markup to be inserted.
    * Select any LaTeX command item and press A ~ Z or F1 ~ F12 to set the shortcut gesture.
    * Select any LaTeX command item and press Delete/Backspace to remove the set shortcut gesture.
    * Select any LaTeX command item and press Enter to add the corresponding LaTeX syntax to the current editing cursor.
* Alt + I: Interact with the math block when the editing cursor is over it.
* Alt + H: Show the view command menu (virtual menu) for preview or export. Please refer to the “Import and Export” section for more details.

Note: Enable or disable command gestures at startup in Settings > Writing. Press NVDA + Alt + C in the editing area to enable or disable the command gesture. The shortcut can be changed in the NVDA input gestures.

### Shortcut Gestures (Toggle: NVDA + Alt + S)

When the editing cursor is in the LaTeX block, press A ~ Z or F1 ~ F12 to quickly insert the bound LaTeX, and press Shift + Alphabets, Shift + F1 ~ F12 to read out the bound LaTeX of the shortcut gesture (it’s necessary to set up the shortcut gesture in the LaTeX Command Menu first).

Note: Enable or disable shortcut gestures at startup in Settings > Writing. Press NVDA + Alt + S in the editor to enable or disable shortcut gestures. The shortcut can be changed in the NVDA input gestures.

### Greek Alphabets Gestures (Toggle: NVDA + Alt + G)

When the editing cursor is in the LaTeX block, press a letter key to quickly insert the LaTeX markup of the corresponding Greek letter. See the "Appendix" of this document for Alphabet to Greek Alphabet Table.

### Editing and Navigating Between Blocks 

In Access8Math editor, content separated by separators is treated as different blocks, such as text blocks and math content blocks. The editing cursor can be quickly moved between different blocks using the block navigation.

Take the content "The solution of the quadratic equation \(ax^2+bx+c=0\) is \(x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}\)" as an example, there are two main math content blocks and two text blocks, which can be labeled as Block A, Block B, Block C and Block D:

* Block A: The six words "The solution of the quadratic equation" is one text block.
* Block B: The math block \(ax^2+bx+c=0\) starts with a starting separator and ends with the ending separator after 0.
* Block C: The word "is" is another text block.
* Block D: The second math block \(x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}\) starts with the starting separator and ends with the closing separator after the whole expression.

#### Block Navigation Gestures (Toggle: NVDA + Alt + N)

* Alt + Left arrow: Move to the beginning of the previous block.
* Alt + Down arrow: Read out the content of the current block without moving.
* Alt + Right arrow: Move to the beginning of the next block.
* Alt + Home: Move to the beginning of the current block.
* Alt + End: Move to the end of the current block.
* Alt + Shift + Left arrow: Move to the previous block and select it.
* Alt + Shift + Down arrow: Select the content of the current data block without moving.
* Alt + Shift + Right arrow: Move to the next block and select it.

Note: Enable or disable block navigation gestures at startup in Settings > Writing. Press NVDA + Alt + N in the editor to enable or disable block navigation gestures. The shortcut can be changed in the NVDA input gestures.

#### Block Browse Mode (Toggle: NVDA + Space)

When using the Block Browsing mode, the system will output the mathematical meaning of the content instead of the original math markup of the current block. For example, “\(\frac{1}{2}\) as a decimal is 0.5” will output as "1 over 2 as a decimal is 0.5" instead of “\(\frac{1}{2}\) as a decimal is 0.5”.

Use the following gestures to move the editing cursor and enter the Interactive Mode:

* Left arrow: Move to the beginning of the previous block and read it.
* Right arrow: Move to the beginning of the next block and read it.
* Up arrow: Move to the previous line and read all the blocks in that line.
* Down arrow: Move to the next line and read all the blocks in that line.
* Page Up: Move up ten lines and read all the blocks in this area.
* Page Down: Move down ten lines and read all the blocks in this area.
* Home: Move to the first block of the line where the editing cursor is located.
* End: Move to the last block of the line where the editing cursor is located.

Press Shift with the above keys to select the text.

* Space/Enter: Press Space/Enter when the editing cursor is on a math block to enter the Interactive Mode.

If pressing the following keys only, the editing cursor will jump to the next block of that type. If pressing Shift + the key at the same time, the editing cursor will jump to the previous block of that type:

* L: Move to the next LaTeX block and read it.
* N: Move to the next Nemeth block and read it.
* M: Move to the next MathML block and read it.
* T: Move to the next text block and read it.
* Tab: Move to the next interactive block (Math block) and read it.

Use the following gestures to edit the document:

* Ctrl + X: Cut the contents of the current editing block.
* Ctrl + C: Copy the content of the current editing block.
* Ctrl + V: Paste the content behind the current editing block.
* Delete/Backspace: Delete the content of the current block.

### Import and Export

#### Export a Document

For the “preview” feature  in the Access8Math editor's View menu, it allows users to convert the Markdown document to an HTML document for previewing.

The math content in the Markdown document will be converted to MathML, which allows different users to view it easily (visually or through speech or Braille). As for resources (such as images, videos or audios), they will be converted into appropriate HTML elements and reference the correct resource files. Therefore, the output HTML document can display various types of contents.

For the “export” feature  in the Access8Math editor's View menu, it allows users to save and share the document. Two types of documents will be exported:

* Access8Math Document file (*.a8m): Access8Math Document file can be imported into the editor again for modification.
* Archive file (*.zip): The HTML file in the archive file is the same as the HTML file converted for the preview feature. All users can read this HTML document without install Access8Math.

#### Import a Document

There are two ways to open an Access8Math Document:

* File Explorer: In the File Explorer, select an Access8Math Document and press NVDA + application key or NVDA + Shift + F10 to open a virtual menu. Select “view” or “edit" option to open the document.
* Access8Math Editor: Open any .a8m file by selecting the "Open” option in the “File” menu in the editor.

Note: Configure whether or not the math objects in the exported HTML are independant blocks with the “HTML Math Display'' setting in Settings > File. This setting will affect whether the math objects are read independently or mixed with normal text when navigating with arrow keys to read the whole line in the Browse Mode.

## Virtual Menus

Virtual menus will be presented only as speech and braille outputs. There is no actual visual menu. Select an item in the list by using the up/down arrow. If the menu item has a sub-menu, use the right key to enter the sub-menu; use the left key to exit the sub-menu.

## Localisation

### Adding a New Language

By clicking this option in the “Localisation” menu, languages that are not originally supported by the system can be added. Once added, the newly added language will appear in the "Settings" > "Reading" > "Language" menu. However, the added language is only a copy of the English language template. The speech and Braille outputs need to be defined through "Symbol Dictionary" and "Math Rules" to achieve customized localization.

### Customizing Speech and Braille Outputs for Math Symbols

In the "Tools" > "Access8Math" > "Localization" menu, speech and Braille outputs can be customized. Both speech and Braille outputs are divided into two parts: "Symbol Dictionary" and "Math Rules."

* Symbol Speech Dictionary: Customize how different math symbols are read.
* Math Rules Speech Output: Customize how different math rules are read.
* Symbol Braille Dictionary: Customize how different math symbols are displayed in Braille outputs.
* Math Rules Braille Output: Customize how different math rules are displayed in Braille outputs.

### Editing Symbol Dictionary

Access8Math maps specific symbols to corresponding text/ braille outputs through a dictionary file to solve issues where rare symbols cannot be read by speech synthesizers or where symbols have different meanings between mathematical contexts and general text.

For example, "!" means "factorial" in mathematical content, while in general text it represents emotion. By editing the dictionary file, symbols can be mapped to new alternative texts or Braille outputs to update incorrect outputs..

* Add: Introduce a new symbol entry to the dictionary. After selecting the add button, enter the desired symbol in the dialog box and confirm. Then, the added symbol will appear in the entry list in the Symbol Dictionary dialog.
* Modify: Choose a symbol and edit its alternative text. The system will then read out and display Braille outputs based on the alternative text.
* Remove: Select a symbol and press the remove button to eliminate the chosen entry.
* Restore Default Values: Reset the dictionary to the default entries defined by the system.
* Import: Bring in a symbol dictionary file, which can load exported symbol dictionary files.
* Export: Save the symbol dictionary file to a specified path for sharing or saving.

### Editing Math Rules

Access8Math establishes corresponding mathematical rules for the MathML structure of commonly used math content. When encountering MathML structures that match the rules, the system will read out and display them according to the content defined in the mathematical rules. The speech outputs and Braille outputs can be customized according to the habits of different regions.

* Edit: In the Math Rules dialog, there is a list of mathematical rules. Select any rule and click the "Edit" button to enter the editing dialog. The editable fields of the rule can be divided into two parts, "Serialization Order" and "Mathematical Meaning of Specific Nodes."

  * Serialization Order: In Access8Math, each math rule is divided into several segments, and these segments are output in a specific order. In this section, the output order of specific segments, as well as the text at the beginning, between segments, and at the end can be adjusted. For example, in the fraction rule "mfrac", this rule is divided into five segments. Orders 0, 2, and 4 represent the starting text, the separating text between segments 1 and 3, and the ending text. Each text can be adjusted according to preference. Orders 1 and 3 allow adjustments to the output order of specific segments by the drop-down menu.
  * Mathematical Meaning of Specific Nodes: The mathematical meaning of specific segments of the math rule can be adjusted in this section. Taking the fraction rule "mfrac" as an example, this rule contains two specific segments: the numerator and the denominator. You can change the meaning of each specific segment according to the math rule.

* Example: Verify if a rule is read in the correct way after editing. Clicking the “Example” button will bring up default mathematical content that matches the corresponding mathematical rule. Users can interact with the content to see whether a rule is read in the correct way.
* Restore Default Values: Reset the list of mathematical rules to the initial default values.
* Import: Import a mathematical rules file, which can be used to load exported mathematical rules files.
* Export: Save the mathematical rules file to the specified path for sharing or saving.

If you are interested in localizing symbol dictionaries and mathematical rules, edit them through these two windows, and use the export function to obtain edited files. Then, you can provide these files to the development team through Access8Math GitHub Pull requests or Email (tsengwoody.tw@gmail.com). We would be happy to include your translation in Access8Math.

## Appendix

### LaTeX Menu

| id | latex | category | order | label |
| --- | --- | --- | --- | --- |
| matrix2X2 | \left [ \begin{matrix} {} &{} \\ {} &{} \end{matrix} \right ] | 2-dimension | 0 | matrix (2X2) |
| matrix3X3 | \left [ \begin{matrix} {} &{} &{} \\ {} &{} &{} \\ {} &{} &{} \end{matrix} \right ] | 2-dimension | 1 | matrix (3X3) |
| determinant2X2 | \left  |  \begin{array} {cc} {} &{} \\ {} &{} \end{array} \right  |  | 2-dimension | 2 | determinant (2X2) |
| determinant3X3 | \left  |  \begin{array} {ccc} {} &{} &{} \\ {} &{} &{} \\ {} &{} &{} \end{array} \right  |  | 2-dimension | 3 | determinant (3X3) |
| leftarrow | \leftarrow | arrow | 0 | left arrow |
| rightarrow | \rightarrow | arrow | 1 | right arrow |
| leftrightarrow | \leftrightarrow | arrow | 2 | left right arrow |
| uparrow | \uparrow | arrow | 3 | up arrow |
| downarrow | \downarrow | arrow | 4 | down arrow |
| updownarrow | \updownarrow | arrow | 5 | up down arrow |
| dotproduct | \cdot | calculus | 5 | dot product |
| integral | \int_{}^{}{} \mathrm d | calculus | 1 | integral |
| nabla | \nabla | calculus | 2 | nabla |
| partial | \partial | calculus | 4 | partial derivative |
| prime | \prime | calculus | 3 | derivative |
| differential | \mathrm{d} | calculus | 0 | differential |
| combination | C_{}^{} | combinatorics | 0 | combination |
| permutation | P_{}^{} | combinatorics | 1 | permutation |
| combination-with-repetition | H_{}^{} | combinatorics | 2 | combination with repetition |
| unordered-selection | U_{}^{} | combinatorics | 3 | unordered selection |
| frac | \frac{}{} | common | 0 | fractions |
| sqrt | \sqrt{} | common | 1 | square root |
| root | \sqrt[]{} | common | 2 | root |
| sumupdown | \sum_{}^{} | common | 3 | summation |
| vector | \vec{} | common | 4 | vector |
| limit | \lim_{{} \to {}} | common | 5 | limit |
| logarithm | \log_{} | common | 6 | logarithm |
| arc | \overset{\frown}{} | geometry | 0 | arc |
| triangle | \triangle{} | geometry | 1 | triangle |
| angle | \angle{} | geometry | 2 | angle |
| degree | ^{\circ} | geometry | 3 | degree |
| circ | \circ | geometry | 4 | circle |
| parallel | \parallel | geometry | 5 | parallel |
| perp | \perp | geometry | 6 | perpendicular |
| square | \square{} | geometry | 7 | square |
| small-diamond | \diamond{} | geometry | 8 | small diamond |
| large-diamond | \Diamond{} | geometry | 9 | large diamond |
| because | \because | logic | 0 | because |
| therefore | \therefore | logic | 1 | therefore |
| iff | \iff | logic | 2 | if and only if |
| implies | \implies | logic | 3 | implies |
| impliedby | \impliedby | logic | 4 | implied by |
| times | \times | operator | 0 | times |
| div | \div | operator | 1 | divide |
| pm | \pm | operator | 2 | plus-minus sign |
| modulus | \bmod | operator | 3 | modulus |
| overline | \overline{} | other | 0 | line segment |
| overleftrightarrow | \overleftrightarrow{} | other | 1 | line |
| overrightarrow | \overrightarrow{} | other | 2 | ray |
| binom | \binom{}{} | other | 3 | binomial coefficient |
| simultaneous-equations | \begin{cases} {} &{} \\ {} &{} \end{cases} | other | 4 | simultaneous equations |
| infty | \infty | other | 5 | infty |
| repeating-decimal | 0.\overline{} | other | 6 | repeating decimal |
| ge | \ge | relation | 0 | greater than or equal to |
| le | \le | relation | 1 | less than or equal to |
| ne | \ne | relation | 2 | not equal to |
| approx | \approx | relation | 3 | approximate |
| cong | \cong | relation | 5 | full equal |
| sim | \sim | relation | 6 | similar |
| doteqdot | \doteqdot | relation | 4 | approximately equal to |
| propto | \propto | relation | 7 | proportional to |
| in | \in | set | 0 | belong to |
| notin | \not\in | set | 1 | not belong to |
| ni | \ni | set | 2 | include element |
| notni | \not\ni | set | 3 | not include element |
| subset | \subset | set | 4 | lie in |
| subsetneqq | \subsetneqq | set | 5 | properly lie in |
| not-subset | \not\subset | set | 6 | not lie in |
| supset | \supset | set | 7 | include |
| supsetneqq | \supsetneqq | set | 8 | properly include |
| not-supset | \not\supset | set | 9 | not include |
| cap | \cap | set | 10 | intersection set |
| cup | \cup | set | 11 | union set |
| setminus | \setminus | set | 12 | difference set |
| complement | \complement_{} | set | 13 | complement |
| emptyset | \emptyset | set | 14 | empty set |
| natural-number | \mathbb{N} | set | 15 | natural number |
| real-number | \mathbb{R} | set | 16 | real number |
| forall | \forall | set | 17 | for all |
| exists | \exists | set | 18 | exists |
| sine | \sin{} | trigonometric | 0 | sine |
| cosine | \cos{} | trigonometric | 1 | cosine |
| tangent | \tan{} | trigonometric | 2 | tangent |
| cotangent | \cot{} | trigonometric | 3 | cotangent |
| secant | \sec{} | trigonometric | 4 | secant |
| cosecant | \csc{} | trigonometric | 5 | cosecant |
| arcsine | \arcsin{} | trigonometric | 6 | arcsine |
| arccosine | \arccos{} | trigonometric | 7 | arccosine |
| arctangent | \arctan{} | trigonometric | 8 | arctangent |
| hyperbolic-sine | \sinh{} | trigonometric | 9 | hyperbolic sine |
| hyperbolic-cosine | \cosh{} | trigonometric | 10 | hyperbolic cosine |
| hyperbolic-tangent | \tanh{} | trigonometric | 11 | hyperbolic tangent |
| hyperbolic-cotangent | \coth{} | trigonometric | 12 | hyperbolic cotangent |
| floor | \lfloor  \rfloor | other | 7 | floor |
| ceil | \lceil  \rceil | other | 8 | ceil |

### English Alphabets to Greek Alphabets Table

| English Alphabet | Greek Alphabet | LaTeX |
| --- | --- | --- |
| a | α | \alpha |
| b | β | \beta |
| c | θ | \theta |
| d | δ | \delta |
| e | ε | \epsilon |
| f | φ | \phi |
| g | γ | \gamma |
| h | η | \eta |
| i | ι | \iota |
| k | κ | \kappa |
| l | λ | \lambda |
| m | μ | \mu |
| n | ν | \nu |
| o | ο | \omicron |
| p | π | \pi |
| r | ρ | \rho |
| s | σ | \sigma |
| t | τ | \tau |
| u | υ | \upsilon |
| v | φ | \psi |
| w | ω | \omega |
| x | χ | \chi |
| y | ξ | \xi |
| z | ζ | \zeta |

# Access8Math update log

## Access8Math v4.2 Update

* Added import/export feature for .a8m files.
* Fixed some issues.

## Access8Math v4.1 Update

* Indicate a capital letter using NVDA voice configuration when the node consists of only one uppercase letter.
* Resolved Opening the virtual context menu in the file explorer in Access8Math conflicts with toggling native selection mode in NVDA Browsing mode, as they both use the same gesture (NVDA+Shift+F10).
* Remove outdated setting options.
* Limit the write feature to within the Access8Math editor, notepad only.
* Rewrite readme.

## Access8Math v4.0 Update

* Compatibility with NVDA 2024.1
* Removed legacy code

## Access8Math v3.8 Update

* Added table navigation support (ctrl+alt+arrow keys) for Mtable in interactive mode.
* Added new categories to the LaTeX menu, including Geometry, Combinatorics, Trigonometric Functions, and Calculus.
* Added new items to the LaTeX menu.
* Included the rounding symbol.
* Fixed conversion errors of .1 and > symbols when converting Nemeth to LaTeX.
* Fixed the path error for restoring default files in the math rules dialog.

## Access8Math v3.7 Update

* new feature: Auto-Complete feature in write feature.
* Added "mixed number" rule to the Nemeth to LaTeX translator.
* In Access8Math editor, Added close button on the upper right corner to close the Access8Math editor.
* Fixed SimultaneousEquationsType rule(read feature).
* Fixed "|" symbol don`t convert to text according in Unicode dictionary(read feature).
* Fix issues with Converting ∫ Nemeth Braille to LaTeX.

## Access8Math v3.6 Update

* new feature: Nemeth Braille Input, with the same functionality as LaTeX input. Allows for real-time interactive navigation (Alt+I) during editing and supports outputting HTML+MathML documents.
* new feature: Added Nemeth delimiter UEB/at(@@) for distinguish Nemeth content.
* new feature: You can convert and copy LaTeX from Math object in interactive navigation mode.
* Added the NVDA+Shift+F10 shortcut to open  virtual context menu in the file explorer.
* Fixed and optimized localized UI issues and cleaned localized file format.

## Access8Math v3.5 Update

* Vectors and rays can be distinguished correctly
* Utilizing dialogue to display image, video, or audio resources in an Access8Math HTML document
* Using a new window to open link resources in an Access8Math HTML document
* The MathML namespace is exported when copying MathML from the Math object in interactive navigation mode
* Display font adjustment, find and replace feature in Access8Math editor
* Compatibility with NVDA 2023.1

## Access8Math v3.4 Update

* Speech, Braille, and interactive source move to Preferences -> Settings -> Math Reader category.
* Integrated MathCAT, you can choose what speech, braille, and interactive source(Access8Math/Math Player/MathCAT) you need in Math Reader settings panel when having already installed Math Player/MathCat.
* Used MultiCategorySettingsDialog to collect settings dialog.
* Press NVDA+alt+e open text file with the built-in editor in File Explore.
* In virtual menus, submenu can open by enter
* Implenment MathML menclose tag rule
* new feature: virtual context menu in File Explorer. It can quickly open Access8Math Document to view or edit it(Please read "Access8Math editor and Access8Math Document" section to know detail information)

## Access8Math v3.3 Update

* Add built-in editor using traditional editing area because of windows 11 changed to UIA editing area
* built-in editor new/open/save feature
* Access8Math language initial setting is based on NVDA language setting
* Improved speech and braille display in virtual menus
* Compatibility with NVDA 2022.1
* Fixed marked menu cannot open when document is empty
* Fixed translate LaTeX/AsciiMath feature
* Fixed HTML document rendering problem when HTML document display setting choice text option

## Access8Math v3.2 Update

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

## Access8Math v3.1 Update

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

## Access8Math v3.0 Update

* Write mathematical content in AsciiMath
* Write mathematical content in LaTeX
* Writing mixed content (text content and mathematical content)
* Use shortcut keys to move the cursor to different types of blocks in edit field
* Use command menu to select commands in edit field
* Set shortcuts in the LaTeX command menu
* Review and export content in edit field to HTML

## Access8Math v2.6 Update

* Auto entering interactive mode when showing Access8Math interaction window.
* You can choose how to hint no movement in interactive mode: beep or speech 'no move' two way.
* The content of the current item will be repeated again When there is no movement.

## Access8Math v2.5 Update

* Adding Russian translation of rules and UI. Thanks to the translation work of Futyn-Maker.
* Fixing compound symbol translation failed bug.
* Removing duplicates of lowercase letters and added general uppercases in en unicode.dic(0370~03FF).

## Access8Math v2.3 Update

* Fix bug.

## Access8Math v2.3 Update

* Compatibility with Python3
* refactoring module and fix code style
* Adding one symbol vector rule

## Access8Math v2.2 Update

*fix bug incorrect speech when a single node has more characters.
* Fix compatibility issue in NVDA 2019.2, thanks to pull requests of CyrilleB79.
* Fix bug in unicode dict has duplicate symbols.
* Add translations in French, thanks to the translation work of CyrilleB79.
* Adjust keyboard shortcut.

## Access8Math v2.1 Update

* In "General Settings", you can set whether "Access8Math interaction window" is automatically displayed when entering interactive mode.
* In interactive mode, "interaction window" can be displayed manually via ctrl+m when "interaction window" are not showed.
* Fix multi-language switching bug.
* Add translations in Turkish, thanks to the translation work of cagri (çağrı doğan).
* Compatibility update for nvda 2019.1 check for add-on`s manifest.ini flag.
* Refactoring dialog window source code.

## Access8Math v2.0 Update

* Add multi-language new-adding and customizing settings,and add three windows of "unicode dictionary", "math rule", "New language adding"
* The "unicode dictionary" can customize the reading way of each math symbolic text.
* "math rule" can customize the reading method and preview the modification through the sample button before completed.
* "New language adding" allows adding language not provided in the built-in system. The newly language will be added to the general settings, and multi-language customization can be achieved through reading definition of "unicode dictionary" and "mathematical rules".
* improved in interactive mode, you can use the number keys 7~9 to read sequence text in the unit of line.

## Access8Math v1.5 update log

* In "general setting" dialog box add setting pause time between items. Values from 1 to 100, the smaller the value, the shorter the pause time, and the greater the value, the longer the pause time.
* Fix setting dialog box can't save configure in NVDA 2018.2.

## Access8Math v1.4 update log

* Adjust settings dialog box which divided into "general setting" and "rules setting" dialog box. "General Settings" is the original "Access8Math Settings" dialog box, and "Rule Settings" dialog box is for selecting whether specific rules are enabled.
* New rules
 * vector rule: When there is a "⇀" right above two Identifier, the item is read as "Vector...".
 * frown rule：When there is a " ⌢ " right above two Identifier, the item is read as "frown...".
* Fix bug.

## Access8Math v1.3 update log

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

## Access8Math v1.2 update log

* New rule
 * negative number rule: Read 'negative' rather than 'minus sign' when minus sign in first item or its previous item is certain operator.
 * integer add fraction rule: Read 'add' between integer and fraction when fraction previous item is integer.
* Program architecture improve
 * add sibling class
 * add dynamic generate Complement class
* Fix bug

## Access8Math v1.1 update log

* In navigation mode command, "Ctrl+c" copy object MathML source code.
* Settings dialog box in Preferences:
 * Language: Access8Math reading language on math content.
 * Analyze the mathematical meaning of content: Semantically analyze the math content, in line with specific rules, read in mathematical meaning of that rules.
 * Read defined meaning in dictionary: When the pattern is definied in the dictionary, use dictionary to read the meaning of subpart in the upper layer part.
 * Read of auto-generated meaning: When the pattern is not difined or incomplete in dictionary, use automatic generation function to read the meaning of subpart in the upper layer part.
* Add some simple rule. Single rules are simplified versions of various rules. When the content only has one single item, for better understanding and reading without confusion, you can omit to choose not to read the script before and after the content.
* Update unicode.dic.
* Fix bug.
