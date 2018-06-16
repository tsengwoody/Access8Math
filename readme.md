# Access8Math ReadMe

This NVDA addon provides the function of reading math content. Although the original NVDA already equipped this feature by applying MathPlayer, some functions still needed to be improved, especially in MathPlayer some language not provided navigation mode.

navigation mode is important to read long math content. It help to understand long math content's structure easily.

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
*	Single rules are simplified versions of various rules. When the content only has one single item, for better understanding and reading without confusion, you can omit to choose not to read the script before and after the content.

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

# Access8Math v1.5 update log

*	In "general setting" dialog box add setting pause time between items. Values from 1 to 100, the smaller the value, the shorter the pause time, and the greater the value, the longer the pause time.
*	Fix setting dialog box can't save configure.

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

# Access8Math 說明

此NVDA addon提供數學內容的閱讀，原先NVDA亦有此功能，但因是調用MathPlayer的功能，部份功能尚顯不足，尤其一些語言未提供導航瀏覽(互動式閱讀部份內容)。

導航瀏覽對於閱讀理解長數學內容相當重要，可協助理解長數學內容的結構。

功能有：

*	可閱讀網頁瀏覽器(Mozilla Firefox, Microsoft Internet Explorer and Google Chrome)上以MathML撰寫的數學內容
*	可閱讀Microsoft Word上以MathType 撰寫的數學內容。(需安裝MathType)
*	在數學內容上按空白鍵後開啟「Access8Math 互動視窗」，視窗內含有「互動」、「複製」按鈕。
	*	互動：與該數學內容進行導航瀏覽，亦即可部份瀏覽數學內容中的子內容並在子內容間移動或縮放子內容大小
	*	複製：複製物件MathML原始碼
*	在導航瀏覽時會提示該項子內容在其上層子內容的意義
*	在導航瀏覽時按鍵：
	*	向下鍵縮小當前數學內容成更小的子內容
	*	向上鍵放大當前數學內容成更大的子內容
	*	向左鍵向前一項數學內容
	*	向右鍵向後一項數學內容
	*	home鍵回到最頂層(完整數學內容)
	*	"Ctrl+c": 複製物件MathML原始碼
	*	數字鍵盤1-9：使用NVDA Reviewing Text方式閱讀序列化的數學內容
	*	esc鍵退出導航瀏覽模式
*	ctrl+alt+m：可在Access8Math與MathPlayer間切換閱讀器(有安裝MathPlayer才能切換)

*	功能表：
	*	「一般設定」對話框，可設定：
		*	語言：Access8Math 朗讀數學內容的語言
		*	項目間隔時間：設定項目間停頓時間，數值從1到100，數值愈小表示停頓時間愈短，反之數值愈大表示停頓時間愈長。
*	分析內容的數學意義：將數學內容進行語意分析，符合特定規則時，以該規則的數學意義進行朗讀
		*	讀出字典有定義模式的意義：當字典檔有定義時，使用字典檔讀出提示該項子內容在其上層子內容的意義
		*	讀出自動生成的意義：當字典檔無定義或不完整時，使用自動產生功能讀出提示該項子內容在其上層子內容的意義或項次
	*	「規則設定」對話框：可選擇特定規則是否啟用的設定。
*	簡單規則：簡單規則是各種規則的簡化版，當其內容僅為單一項目時，便可省略前後標記朗讀，以達到更好的理解與閱讀，而亦不致造成混淆

數學內容解析數學規則意義持續增加中

目前先針對以Presentation Markup寫成的MathML處理，因word、math type、wiris等MathML圖形化輸入工具產生的MathML皆為此型態

維基百科上的數學內容皆以MathML寫成

*	矩陣乘法：https://zh.wikipedia.org/zh-tw/%E7%9F%A9%E9%99%A3%E4%B9%98%E6%B3%95
*	三次方程：https://zh.wikipedia.org/zh-tw/%E4%B8%89%E6%AC%A1%E6%96%B9%E7%A8%8B

*	例子
	*	一元二次方程解：
<math xmlns="http://www.w3.org/1998/Math/MathML"><mfrac><mrow><mo>-</mo><mi>b</mi><mo>&#xB1;</mo><msqrt><msup><mi>b</mi><mn>2</mn></msup><mo>-</mo><mn>4</mn><mi>a</mi><mi>c</mi></msqrt></mrow><mrow><mn>2</mn><mi>a</mi></mrow></mfrac></math>
	*	二項式定理：
<math xml:lang="zh_TW">
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

原始碼：https://github.com/tsengwoody/Access8Math

歡迎提出見意與bug回報，謝謝！

# Access8Math v1.5 更新日誌

*	在「一般設定」新增項與項間停頓時間設定。數值從1到100，數值愈小表示停頓時間愈短，反之數值愈大表示停頓時間愈長。
*	更新 unicode.dic

# Access8Math v1.4 更新日誌

*	調整設定選項對話框，分為「一般設定」、「規則設定」對話框。「一般設定」為原先「Access8Math 設定」對話框，「規則設定」對話框則為可選擇特定規則是否啟用的設定。
*	新規則
	*	向量規則：當兩個Identifier的正上方有「⇀」時，將其項讀為「向量……」
	*	弧度規則：當兩個Identifier的正上方有「⌢」時，將其項讀為「弧……」
*	修正已知問題

# Access8Math v1.3 更新日誌

*	新規則
	*	正規則：當「+」在首項或其前項為<mo></mo>標記時，將「+」讀為「正」而非「加」
	*	平方規則：當次方數為2時，將其讀為「…的平方」
	*	立方規則：當次方數為3時，將其項讀為「…的立方」
	*	直線規則：當兩個Identifier的正上方有「↔」時，將其項讀為「直線……」
	*	線段規則：當兩個Identifier的正上方有「¯」時，將其項讀為「線段……」
	*	射線規則：當兩個Identifier的正上方有「→」時，將其項讀為「射線……」
*	新增互動視窗：在數學內容上按空白鍵後開啟「Access8Math 互動視窗」，視窗內含有「互動」、「複製」按鈕。
	*	互動：進入數學內容導航瀏覽
	*	複製：複製物件MathML原始碼
*	多國語言新增 zh_CN 的語言
*	調整規則間繼承關係，確保規則衝突時，能正確使用適合的規則
*	修正已知問題

# Access8Math v1.2 更新日誌

*	新規則
	*	負規則：當「-」在首項或其前項為<mo></mo>標記時，將「-」讀為「負」而非「減」
	*	帶分數：當分數前項為數字時，將數字與分數間讀為「又」
*	程式架構優化
	*	加入「sibling」的類別
	*	加入動態產生「反向」 nodetype的類別
*	修正已知問題

# Access8Math v1.1 更新日誌

*	在導航瀏覽時按"Ctrl+c"複製物件MathML原始碼
*	再偏好設定內增加 Access8Math 設定的項目，設定選項對話框，可設定：
	*	語言：Access8Math 朗讀數學內容的語言
	*	分析內容的數學意義：將數學內容進行語意分析，符合特定規則時，以該規則的數學意義進行朗讀
	*	讀出字典有定義模式的意義：當字典檔有定義時，使用字典檔讀出提示該項子內容在其上層子內容的意義
	*	讀出自動生成的意義：當字典檔無定義或不完整時，使用自動產生功能讀出提示該項子內容在其上層子內容的意義或項次
*	加入多條簡單規則，簡單規則是各種規則的簡化版，當其內容僅為單一項目時，便可省略前後標記朗讀，以達到更好的理解與閱讀，而亦不致造成混淆
*	更新unicode.dic
*	修正已知問題
