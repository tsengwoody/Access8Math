# Access8Math ReadMe

This NVDA addon provides the function of reading math content. Although the original NVDA already equipped this feature by applying MathPlayer, some functions still needed to be improved, especially in MathPlayer some language not provided navigation mode.

navigation mode is important to read long math content. It help to understand long math content's structure easily.

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
*	"Ctrl+Alt+m": Switch the provider between Access8Math and MathPlayer.(MathPlayer installed only)
*	"Ctrl+Alt+l": Switch the language between en, zh_CN, zh_TW.

Math rules and definitions analyzed by math contents are continuing increasing.

We are now focusing the MathML written in Presentation Markup, because MathML graphical input tools such as word, math type, wiris generated MathML are all in this type.

Math contents in Wiki are all written in MathML.

*	Matrix multiplication: https://en.wikipedia.org/wiki/Matrix_multiplication
*	Cubic function: https://en.wikipedia.org/wiki/Cubic_function

Quadratic equation

<math xmlns="http://www.w3.org/1998/Math/MathML"><mfrac><mrow><mo>-</mo><mi>b</mi><mo>&#xB1;</mo><msqrt><msup><mi>b</mi><mn>2</mn></msup><mo>-</mo><mn>4</mn><mi>a</mi><mi>c</mi></msqrt></mrow><mrow><mn>2</mn><mi>a</mi></mrow></mfrac></math>

Source code: https://github.com/tsengwoody/Access8Math

Please report any bugs or comments, thank you!

# Access8Math 說明

此NVDA addon提供數學內容的閱讀，原先NVDA亦有此功能，但因是調用MathPlayer的功能，部份功能尚顯不足，尤其一些語言未提供導航瀏覽(互動式閱讀部份內容)。

導航瀏覽對於閱讀理解長數學內容相當重要，可協助理解長數學內容的結構。

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
*	ctrl+alt+m：可在Access8Math與MathPlayer間切換閱讀器(有安裝MathPlayer才能切換)
*	ctrl+alt+l：可在英文、中文(中國)、中文(台灣)間切換語言。

數學內容解析數學規則意義持續增加中

目前先針對以Presentation Markup寫成的MathML處理，因word、math type、wiris等MathML圖形化輸入工具產生的MathML皆為此型態

維基百科上的數學內容皆以MathML寫成

*	矩陣乘法：https://zh.wikipedia.org/zh-tw/%E7%9F%A9%E9%99%A3%E4%B9%98%E6%B3%95
*	三次方程：https://zh.wikipedia.org/zh-tw/%E4%B8%89%E6%AC%A1%E6%96%B9%E7%A8%8B

一元二次方程解

<math xmlns="http://www.w3.org/1998/Math/MathML"><mfrac><mrow><mo>-</mo><mi>b</mi><mo>&#xB1;</mo><msqrt><msup><mi>b</mi><mn>2</mn></msup><mo>-</mo><mn>4</mn><mi>a</mi><mi>c</mi></msqrt></mrow><mrow><mn>2</mn><mi>a</mi></mrow></mfrac></math>

原始碼：https://github.com/tsengwoody/Access8Math

歡迎提出見意與bug回報，謝謝！
