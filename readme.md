# Access8Math ReadMe

This NVDA addon provides the function of reading math content. Although the original NVDA already equipped this feature by applying MathPlayer, some functions still needed to be improved, especially in MathPlayer some language not provided navigation mode.

navigation mode is important to read long math content. It help to understand long math content's structure easily.

## function

Access8Math allows:

*	Read math content written in MathML in web browser(Mozilla Firefox, Microsoft Internet Explorer and Google Chrome).
*	Read Microsoft Word math content written in MathType. (MathPlayer installed only)
*	Pressing "Space" in math content to open "Access8Math interaction window" which contains "interactive" and "copy" button.
	*	interaction: Into math content to navigate and browse. Also, you can partially explore the subparts in expression and move or zoom the content between the subpart.
	*	copy: Copy MathML object source code.
*	In navigation mode, indicate the meaning of subpart in the upper layer part.
*	In navigation mode command：
	*	"Down Arrow": Zoom in on a smaller subpart of the math content.
	*	"Up Arrow": Zoom out to  a larger subpartthe of the math content .
	*	"Left Arrow": Move to the previous math content.
	*	"Right Arrow": Move to the next math content.
	*	"Home": Move back to the top.(Entire math content)	
	*	"Ctrl+c": Copy object MathML source code
	*	"Numpad 1~9": Reading the math content into serialized text using NVDA Reviewing Text.
	*	"ESC": Exit the navigation mode.
*	"Ctrl+Alt+m": Switch the provider between Access8Math and MathPlayer.(MathPlayer installed only)
*	Menu:
	*	General Settings dialog box:
		*	Language: Access8Math reading language
		*	Item interval time: Setting pause time between items. Values from 1 to 100, the smaller the value, the shorter the pause time, and the greater the value, the longer the pause time.
		*	Analyze the mathematical meaning of content: Semantically analyze the math content, in line with specific rules, read in mathematical meaning of that rules.
		*	Read defined meaning  in dictionary: When the pattern is definied in the dictionary, use dictionary to read the meaning of subpart in the upper layer part.
		*	Read auto-generated meaning: When the pattern is not difined or incomplete in dictionary, use automatic generation function to read the meaning of subpart in the upper layer part.
	*	Rule Settings dialog box: select whether specific rules are enabled.
*	"unicode dictionary" allows customizing the reading method for each symbol text.
*	"math rule" allows customizing the reading method for each type of mathematics.
*	"New language adding" allows adding language not provided in the built-in system. The newly language will be added to the "General settings", and multi-language customization can be achieved through reading definition of "unicode dictionary" and "math rule".

## Math Rules

Access8Math establishes 43 mathematical rules according to the mathematical type and logic to decide the reading math method and order. According to different local math reading logic, the math reading text and order can be changed. The method is as follows:

Edit: After entering the "math rule", the window lists 43 math rules. Choose any math rule and select the "Edit" to enter the editing entry.

The "editing entry" can be divided into two major blocks, the "Serialized ordering" and the "Child role".
*	Serialized ordering: Math rule is divided into multiple blocks according to the reading order. In this area, the reading order of child node and the delimitation text of start, inter- and the end can be changed. Taking the fractional rule mfrac as an example, this rule is divided into five reading blocks. The order 0, 2, and 4 represent the initial prompt, the project segmentation prompt, and the end prompt, respectively, and the meanings text can be changed in each field. Order 1 and 3 adjust the reading	sequence of child node which can be changed in the drop-down menu.
*	Child role:  The next-level sub-item of the mathematical rule. Taking the fractional rule mfrac as an example, the rule contains the numerator and the denominator. The sub-content in the upper sub-content meaning can be changed in the child-node role field.

Example: You can check the reading method of this math rule after editing. After clicking, a math content is preset the corresponding math rules for confirming whether the reading method is as expected.

Recover default: Restores the list of math rules to their initial presets.

Import: Import math rules files, which can be used to load math rules files.

Export: Save the math rules file to the specified path to share or keep.

## other

Single rules are simplified versions of various rules. When the content only has one single item, for better understanding and reading without confusion, you can omit to choose not to read the script before and after the content.

Math rules and definitions analyzed by math contents are continuing increasing.

We are now focusing the MathML written in Presentation Markup, because MathML graphical input tools such as word, math type, wiris generated MathML are all in this type.

Math contents in Wiki are all written in MathML.

*	Matrix multiplication: https://en.wikipedia.org/wiki/Matrix_multiplication
*	Cubic function: https://en.wikipedia.org/wiki/Cubic_function

Example

*	Quadratic equation
<math xmlns="http://www.w3.org/1998/Math/MathML"><mfrac><mrow><mo>-</mo><mi>b</mi><mo>&#xB1;</mo><msqrt><msup><mi>b</mi><mn>2</mn></msup><mo>-</mo><mn>4</mn><mi>a</mi><mi>c</mi></msqrt></mrow><mrow><mn>2</mn><mi>a</mi></mrow></mfrac></math>
*	Binomial theorem
<math xml:lang="en">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <mo stretchy="false">(</mo>
        <mn>1</mn>
        <mo>+</mo>
        <mi>x</mi>
        <msup>
          <mo stretchy="false">)</mo>
          <mrow class="MJX-TeXAtom-ORD">
            <mi>α<!-- α --></mi>
          </mrow>
        </msup>
        <mo>=</mo>
        <munderover>
          <mo>∑<!-- ∑ --></mo>
          <mrow class="MJX-TeXAtom-ORD">
            <mi>n</mi>
            <mo>=</mo>
            <mn>0</mn>
          </mrow>
          <mrow class="MJX-TeXAtom-ORD">
            <mi mathvariant="normal">∞<!-- ∞ --></mi>
          </mrow>
        </munderover>
        <mi>C</mi>
        <mo stretchy="false">(</mo>
        <mi>α<!-- α --></mi>
        <mo>,</mo>
        <mi>n</mi>
        <mo stretchy="false">)</mo>
        <msup>
          <mi>x</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mi>n</mi>
          </mrow>
        </msup>
        <mspace width="1em"></mspace>
        <mi mathvariant="normal">∀<!-- ∀ --></mi>
        <mi>x</mi>
        <mo>:</mo>
        <mrow>
          <mo>|</mo>
          <mi>x</mi>
          <mo>|</mo>
        </mrow>
        <mo>&lt;</mo>
        <mn>1</mn>
        <mo>,</mo>
        <mi mathvariant="normal">∀<!-- ∀ --></mi>
        <mi>α<!-- α --></mi>
        <mo>∈<!-- ∈ --></mo>
        <mrow class="MJX-TeXAtom-ORD">
          <mi mathvariant="double-struck">C</mi>
        </mrow>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle (1+x)^{\alpha }=\sum _{n=0}^{\infty }C(\alpha ,n)x^{n}\quad \forall x:\left|x\right|&lt;1,\forall \alpha \in \mathbb {C} }</annotation>
  </semantics>
</math>

Source code: https://github.com/tsengwoody/Access8Math

Please report any bugs or comments, thank you!

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
