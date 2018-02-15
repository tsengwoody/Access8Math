# Access8Math v1.1 update log

*	In navigation mode command, "Ctrl+c" copy object MathML source code.
*	Settings dialog box in Preferences:
	*	Language: Access8Math reading language
	*	Analyze the mathematical meaning of content: Semantically analyze the math content, in line with specific rules, read in mathematical meaning of that rules.
	*	Read the meaning of definied pattern in dictionary: When the pattern is definied in the dictionary, use dictionary to read the meaning of subpart in the upper layer part.
	*	Read the meaning of auto-generated: When the pattern is not difined or incomplete in dictionary, use automatic generation function to read the meaning of subpart in the upper layer part.
*	Add some simple rule. Single rules are simplified versions of various rules. When the content only has one single item, for better understanding and reading without confusion, you can omit to choose not to read the script before and after the content.
*	Update unicode.dic
*	Fix bug

# Access8Math ReadMe

This NVDA addon provides the function of reading math content. Although the original NVDA already equipped this feature by applying MathPlayer, some functions still needed to be improved, especially in MathPlayer some language not provided navigation mode.

navigation mode is important to read long math content. It help to understand long math content's structure easily.

Access8Math allows:

*	Read math content written in MathML in web browser(Mozilla Firefox, Microsoft Internet Explorer and Google Chrome).
*	Read Microsoft Word math content written in MathType. (MathPlayer installed only)
*	Navigate the math content by pressing "Space" in math content. Also, you can partially explore the subparts in expression and move or zoom the content between the subpart.
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
*	Settings dialog box:
	*	Language: Access8Math reading language
	*	Analyze the mathematical meaning of content: Semantically analyze the math content, in line with specific rules, read in mathematical meaning of that rules.
	*	Read defined meaning  in dictionary: When the pattern is definied in the dictionary, use dictionary to read the meaning of subpart in the upper layer part.
	*	Read auto-generated meaning: When the pattern is not difined or incomplete in dictionary, use automatic generation function to read the meaning of subpart in the upper layer part.
*	Currently available rules include:
	*	...from...to...
		*	Circle area intergration:
<math xml:lang="en">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <mrow class="MJX-TeXAtom-ORD">
          <mtable columnalign="right left right left right left right left right left right left" rowspacing="3pt" columnspacing="0em 2em 0em 2em 0em 2em 0em 2em 0em 2em 0em" displaystyle="true">
            <mtr>
              <mtd>
                <mrow class="MJX-TeXAtom-ORD">
                  <mi mathvariant="normal">A</mi>
                  <mi mathvariant="normal">r</mi>
                  <mi mathvariant="normal">e</mi>
                  <mi mathvariant="normal">a</mi>
                </mrow>
                <mo stretchy="false">(</mo>
                <mi>r</mi>
                <mo stretchy="false">)</mo>
              </mtd>
              <mtd>
                <mi></mi>
                <mrow class="MJX-TeXAtom-ORD">
                </mrow>
                <mo>=</mo>
                <msubsup>
                  <mo>∫<!-- ∫ --></mo>
                  <mrow class="MJX-TeXAtom-ORD">
                    <mn>0</mn>
                  </mrow>
                  <mrow class="MJX-TeXAtom-ORD">
                    <mi>r</mi>
                  </mrow>
                </msubsup>
                <mn>2</mn>
                <mi>π<!-- π --></mi>
                <mi>t</mi>
                <mspace width="thinmathspace"></mspace>
                <mi>d</mi>
                <mi>t</mi>
              </mtd>
            </mtr>
            <mtr>
              <mtd></mtd>
              <mtd>
                <mi></mi>
                <mrow class="MJX-TeXAtom-ORD">
                </mrow>
                <mo>=</mo>
                <msubsup>
                  <mrow>
                    <mo>[</mo>
                    <mrow>
                      <mo stretchy="false">(</mo>
                      <mn>2</mn>
                      <mi>π<!-- π --></mi>
                      <mo stretchy="false">)</mo>
                      <mrow class="MJX-TeXAtom-ORD">
                        <mfrac>
                          <msup>
                            <mi>t</mi>
                            <mrow class="MJX-TeXAtom-ORD">
                              <mn>2</mn>
                            </mrow>
                          </msup>
                          <mn>2</mn>
                        </mfrac>
                      </mrow>
                    </mrow>
                    <mo>]</mo>
                  </mrow>
                  <mrow class="MJX-TeXAtom-ORD">
                    <mi>t</mi>
                    <mo>=</mo>
                    <mn>0</mn>
                  </mrow>
                  <mrow class="MJX-TeXAtom-ORD">
                    <mi>r</mi>
                  </mrow>
                </msubsup>
              </mtd>
            </mtr>
            <mtr>
              <mtd></mtd>
              <mtd>
                <mi></mi>
                <mrow class="MJX-TeXAtom-ORD">
                </mrow>
                <mo>=</mo>
                <mi>π<!-- π --></mi>
                <msup>
                  <mi>r</mi>
                  <mrow class="MJX-TeXAtom-ORD">
                    <mn>2</mn>
                  </mrow>
                </msup>
                <mo>.</mo>
              </mtd>
            </mtr>
          </mtable>
        </mrow>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle {\begin{aligned}\mathrm {Area} (r)&amp;{}=\int_{0}^{r}2\pi t\,dt\\&amp;{}=\left[(2\pi ){\frac {t^{2}}{2}}\right]_{t=0}^{r}\\&amp;{}=\pi r^{2}.\end{aligned}}}</annotation>
  </semantics>
</math>
	*	...to the ...th power
		*	e to the Xth power of Taylor series(Expand the ideographic way):
<math xml:lang="en">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <msup>
          <mi>e</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mi>x</mi>
          </mrow>
        </msup>
        <mo>=</mo>
        <mn>1</mn>
        <mo>+</mo>
        <mi>x</mi>
        <mo>+</mo>
        <mrow class="MJX-TeXAtom-ORD">
          <mfrac>
            <msup>
              <mi>x</mi>
              <mrow class="MJX-TeXAtom-ORD">
                <mn>2</mn>
              </mrow>
            </msup>
            <mrow>
              <mn>2</mn>
              <mo>!</mo>
            </mrow>
          </mfrac>
        </mrow>
        <mo>+</mo>
        <mrow class="MJX-TeXAtom-ORD">
          <mfrac>
            <msup>
              <mi>x</mi>
              <mrow class="MJX-TeXAtom-ORD">
                <mn>3</mn>
              </mrow>
            </msup>
            <mrow>
              <mn>3</mn>
              <mo>!</mo>
            </mrow>
          </mfrac>
        </mrow>
        <mo>+</mo>
        <mo>⋯<!-- ⋯ --></mo>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle e^{x}=1+x+{\frac {x^{2}}{2!}}+{\frac {x^{3}}{3!}}+\cdots }</annotation>
  </semantics>
</math>
	*	Single fracion
		*	Geometric sequence from 1/2 with common ratio 1/2
<math xml:lang="en">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <mrow class="MJX-TeXAtom-ORD">
          <mfrac>
            <mn>1</mn>
            <mn>2</mn>
          </mfrac>
        </mrow>
        <mo>+</mo>
        <mrow class="MJX-TeXAtom-ORD">
          <mfrac>
            <mn>1</mn>
            <mn>4</mn>
          </mfrac>
        </mrow>
        <mo>+</mo>
        <mrow class="MJX-TeXAtom-ORD">
          <mfrac>
            <mn>1</mn>
            <mn>8</mn>
          </mfrac>
        </mrow>
        <mo>+</mo>
        <mrow class="MJX-TeXAtom-ORD">
          <mfrac>
            <mn>1</mn>
            <mn>16</mn>
          </mfrac>
        </mrow>
        <mo>+</mo>
        <mo>⋯<!-- ⋯ --></mo>
        <mo>=</mo>
        <mrow class="MJX-TeXAtom-ORD">
          <mfrac>
            <mfrac>
              <mn>1</mn>
              <mn>2</mn>
            </mfrac>
            <mrow>
              <mn>1</mn>
              <mo>−<!-- − --></mo>
              <mo stretchy="false">(</mo>
              <mo>+</mo>
              <mrow class="MJX-TeXAtom-ORD">
                <mfrac>
                  <mn>1</mn>
                  <mn>2</mn>
                </mfrac>
              </mrow>
              <mo stretchy="false">)</mo>
            </mrow>
          </mfrac>
        </mrow>
        <mo>=</mo>
        <mn>1.</mn>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle {\frac {1}{2}}+{\frac {1}{4}}+{\frac {1}{8}}+{\frac {1}{16}}+\cdots ={\frac {\frac {1}{2}}{1-(+{\frac {1}{2}})}}=1.}</annotation>
  </semantics>
</math>
	*	Single square root
		*	Regular triangle area A with length a
<math xml:lang="en">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <mi>A</mi>
        <mo>=</mo>
        <mrow class="MJX-TeXAtom-ORD">
          <mfrac>
            <msqrt>
              <mn>3</mn>
            </msqrt>
            <mn>4</mn>
          </mfrac>
        </mrow>
        <msup>
          <mi>a</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mn>2</mn>
          </mrow>
        </msup>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle A={\frac {\sqrt {3}}{4}}a^{2}}</annotation>
  </semantics>
</math>
	*	Single superscript and subscript
		*	Arithmetic progression
<math xml:lang="en">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <munderover>
          <mo>∑<!-- ∑ --></mo>
          <mrow class="MJX-TeXAtom-ORD">
            <mi>i</mi>
            <mo>=</mo>
            <mn>0</mn>
          </mrow>
          <mrow class="MJX-TeXAtom-ORD">
            <mi>n</mi>
            <mo>−<!-- − --></mo>
            <mn>1</mn>
          </mrow>
        </munderover>
        <mo stretchy="false">(</mo>
        <msub>
          <mi>a</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mn>1</mn>
          </mrow>
        </msub>
        <mo>+</mo>
        <mi>i</mi>
        <mi>d</mi>
        <mo stretchy="false">)</mo>
        <mo>=</mo>
        <mrow class="MJX-TeXAtom-ORD">
          <mfrac>
            <mrow>
              <mi>n</mi>
              <mo stretchy="false">(</mo>
              <msub>
                <mi>a</mi>
                <mrow class="MJX-TeXAtom-ORD">
                  <mn>1</mn>
                </mrow>
              </msub>
              <mo>+</mo>
              <msub>
                <mi>a</mi>
                <mrow class="MJX-TeXAtom-ORD">
                  <mi>n</mi>
                </mrow>
              </msub>
              <mo stretchy="false">)</mo>
            </mrow>
            <mn>2</mn>
          </mfrac>
        </mrow>
        <mo>=</mo>
        <mrow class="MJX-TeXAtom-ORD">
          <mfrac>
            <mrow>
              <mi>n</mi>
              <mo stretchy="false">[</mo>
              <mn>2</mn>
              <msub>
                <mi>a</mi>
                <mrow class="MJX-TeXAtom-ORD">
                  <mn>1</mn>
                </mrow>
              </msub>
              <mo>+</mo>
              <mo stretchy="false">(</mo>
              <mi>n</mi>
              <mo>−<!-- − --></mo>
              <mn>1</mn>
              <mo stretchy="false">)</mo>
              <mi>d</mi>
              <mo stretchy="false">]</mo>
            </mrow>
            <mn>2</mn>
          </mfrac>
        </mrow>
        <mo>=</mo>
        <msub>
          <mi>a</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mn>1</mn>
          </mrow>
        </msub>
        <msubsup>
          <mi>C</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mi>n</mi>
          </mrow>
          <mrow class="MJX-TeXAtom-ORD">
            <mn>1</mn>
          </mrow>
        </msubsup>
        <mo>+</mo>
        <mi>d</mi>
        <msubsup>
          <mi>C</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mi>n</mi>
          </mrow>
          <mrow class="MJX-TeXAtom-ORD">
            <mn>2</mn>
          </mrow>
        </msubsup>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle \sum_{i=0}^{n-1}(a_{1}+id)={\frac {n(a_{1}+a_{n})}{2}}={\frac {n[2a_{1}+(n-1)d]}{2}}=a_{1}C_{n}^{1}+dC_{n}^{2}}</annotation>
  </semantics>
</math>

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

# Access8Math v1.1 更新日誌

*	在導航瀏覽時按"Ctrl+c"複製物件MathML原始碼
*	再偏好設定內增加 Access8Math 設定的項目，設定選項對話框，可設定：
	*	語言：Access8Math 的朗讀語言
	*	分析內容的數學意義：將數學內容進行語意分析，符合特定規則時，以該規則的數學意義進行朗讀
	*	讀出字典有定義模式的意義：當字典檔有定義時，使用字典檔讀出提示該項子內容在其上層子內容的意義
	*	讀出自動生成的意義：當字典檔無定義或不完整時，使用自動產生功能讀出提示該項子內容在其上層子內容的意義或項次
*	加入多條簡單規則，簡單規則是各種規則的簡化版，當其內容僅為單一項目時，便可省略前後標記朗讀，以達到更好的理解與閱讀，而亦不致造成混淆
*	更新unicode.dic
*	修正已知問題

# Access8Math 說明

此NVDA addon提供數學內容的閱讀，原先NVDA亦有此功能，但因是調用MathPlayer的功能，部份功能尚顯不足，尤其一些語言未提供導航瀏覽(互動式閱讀部份內容)。

導航瀏覽對於閱讀理解長數學內容相當重要，可協助理解長數學內容的結構。

功能有：

*	可閱讀網頁瀏覽器(Mozilla Firefox, Microsoft Internet Explorer and Google Chrome)上以MathML撰寫的數學內容
*	可閱讀Microsoft Word上以MathType 撰寫的數學內容。(需安裝MathType)
*	在數學內容上按空白鍵可與該數學內容進行導航瀏覽，亦即可部份瀏覽數學內容中的子內容並在子內容間移動或縮放子內容大小
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
*	設定選項對話框，可設定：
	*	語言：Access8Math 的朗讀語言
	*	分析內容的數學意義：將數學內容進行語意分析，符合特定規則時，以該規則的數學意義進行朗讀
	*	讀出字典有定義模式的意義：當字典檔有定義時，使用字典檔讀出提示該項子內容在其上層子內容的意義
	*	讀出自動生成的意義：當字典檔無定義或不完整時，使用自動產生功能讀出提示該項子內容在其上層子內容的意義或項次
*	目前可分析的規則包含：
	*	…從…到…
		*	圓面積積分：
<math xml:lang="zh_TW">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <mrow class="MJX-TeXAtom-ORD">
          <mtable columnalign="right left right left right left right left right left right left" rowspacing="3pt" columnspacing="0em 2em 0em 2em 0em 2em 0em 2em 0em 2em 0em" displaystyle="true">
            <mtr>
              <mtd>
                <mrow class="MJX-TeXAtom-ORD">
                  <mi mathvariant="normal">A</mi>
                  <mi mathvariant="normal">r</mi>
                  <mi mathvariant="normal">e</mi>
                  <mi mathvariant="normal">a</mi>
                </mrow>
                <mo stretchy="false">(</mo>
                <mi>r</mi>
                <mo stretchy="false">)</mo>
              </mtd>
              <mtd>
                <mi></mi>
                <mrow class="MJX-TeXAtom-ORD">
                </mrow>
                <mo>=</mo>
                <msubsup>
                  <mo>∫<!-- ∫ --></mo>
                  <mrow class="MJX-TeXAtom-ORD">
                    <mn>0</mn>
                  </mrow>
                  <mrow class="MJX-TeXAtom-ORD">
                    <mi>r</mi>
                  </mrow>
                </msubsup>
                <mn>2</mn>
                <mi>π<!-- π --></mi>
                <mi>t</mi>
                <mspace width="thinmathspace"></mspace>
                <mi>d</mi>
                <mi>t</mi>
              </mtd>
            </mtr>
            <mtr>
              <mtd></mtd>
              <mtd>
                <mi></mi>
                <mrow class="MJX-TeXAtom-ORD">
                </mrow>
                <mo>=</mo>
                <msubsup>
                  <mrow>
                    <mo>[</mo>
                    <mrow>
                      <mo stretchy="false">(</mo>
                      <mn>2</mn>
                      <mi>π<!-- π --></mi>
                      <mo stretchy="false">)</mo>
                      <mrow class="MJX-TeXAtom-ORD">
                        <mfrac>
                          <msup>
                            <mi>t</mi>
                            <mrow class="MJX-TeXAtom-ORD">
                              <mn>2</mn>
                            </mrow>
                          </msup>
                          <mn>2</mn>
                        </mfrac>
                      </mrow>
                    </mrow>
                    <mo>]</mo>
                  </mrow>
                  <mrow class="MJX-TeXAtom-ORD">
                    <mi>t</mi>
                    <mo>=</mo>
                    <mn>0</mn>
                  </mrow>
                  <mrow class="MJX-TeXAtom-ORD">
                    <mi>r</mi>
                  </mrow>
                </msubsup>
              </mtd>
            </mtr>
            <mtr>
              <mtd></mtd>
              <mtd>
                <mi></mi>
                <mrow class="MJX-TeXAtom-ORD">
                </mrow>
                <mo>=</mo>
                <mi>π<!-- π --></mi>
                <msup>
                  <mi>r</mi>
                  <mrow class="MJX-TeXAtom-ORD">
                    <mn>2</mn>
                  </mrow>
                </msup>
                <mo>.</mo>
              </mtd>
            </mtr>
          </mtable>
        </mrow>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle {\begin{aligned}\mathrm {Area} (r)&amp;{}=\int_{0}^{r}2\pi t\,dt\\&amp;{}=\left[(2\pi ){\frac {t^{2}}{2}}\right]_{t=0}^{r}\\&amp;{}=\pi r^{2}.\end{aligned}}}</annotation>
  </semantics>
</math>
	*	…的…次方
		*	e的x次方泰勒展開式(展開表意方式)：
<math xml:lang="zh_TW">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <msup>
          <mi>e</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mi>x</mi>
          </mrow>
        </msup>
        <mo>=</mo>
        <mn>1</mn>
        <mo>+</mo>
        <mi>x</mi>
        <mo>+</mo>
        <mrow class="MJX-TeXAtom-ORD">
          <mfrac>
            <msup>
              <mi>x</mi>
              <mrow class="MJX-TeXAtom-ORD">
                <mn>2</mn>
              </mrow>
            </msup>
            <mrow>
              <mn>2</mn>
              <mo>!</mo>
            </mrow>
          </mfrac>
        </mrow>
        <mo>+</mo>
        <mrow class="MJX-TeXAtom-ORD">
          <mfrac>
            <msup>
              <mi>x</mi>
              <mrow class="MJX-TeXAtom-ORD">
                <mn>3</mn>
              </mrow>
            </msup>
            <mrow>
              <mn>3</mn>
              <mo>!</mo>
            </mrow>
          </mfrac>
        </mrow>
        <mo>+</mo>
        <mo>⋯<!-- ⋯ --></mo>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle e^{x}=1+x+{\frac {x^{2}}{2!}}+{\frac {x^{3}}{3!}}+\cdots }</annotation>
  </semantics>
</math>
	*	簡單分數
		*	幾何級數從 1/2 開始公共比為 1/2
<math xml:lang="zh_TW">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <mrow class="MJX-TeXAtom-ORD">
          <mfrac>
            <mn>1</mn>
            <mn>2</mn>
          </mfrac>
        </mrow>
        <mo>+</mo>
        <mrow class="MJX-TeXAtom-ORD">
          <mfrac>
            <mn>1</mn>
            <mn>4</mn>
          </mfrac>
        </mrow>
        <mo>+</mo>
        <mrow class="MJX-TeXAtom-ORD">
          <mfrac>
            <mn>1</mn>
            <mn>8</mn>
          </mfrac>
        </mrow>
        <mo>+</mo>
        <mrow class="MJX-TeXAtom-ORD">
          <mfrac>
            <mn>1</mn>
            <mn>16</mn>
          </mfrac>
        </mrow>
        <mo>+</mo>
        <mo>⋯<!-- ⋯ --></mo>
        <mo>=</mo>
        <mrow class="MJX-TeXAtom-ORD">
          <mfrac>
            <mfrac>
              <mn>1</mn>
              <mn>2</mn>
            </mfrac>
            <mrow>
              <mn>1</mn>
              <mo>−<!-- − --></mo>
              <mo stretchy="false">(</mo>
              <mo>+</mo>
              <mrow class="MJX-TeXAtom-ORD">
                <mfrac>
                  <mn>1</mn>
                  <mn>2</mn>
                </mfrac>
              </mrow>
              <mo stretchy="false">)</mo>
            </mrow>
          </mfrac>
        </mrow>
        <mo>=</mo>
        <mn>1.</mn>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle {\frac {1}{2}}+{\frac {1}{4}}+{\frac {1}{8}}+{\frac {1}{16}}+\cdots ={\frac {\frac {1}{2}}{1-(+{\frac {1}{2}})}}=1.}</annotation>
  </semantics>
</math>
	*	簡單方根
		*	正三角型邊長a的面積A
<math xml:lang="zh_TW">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <mi>A</mi>
        <mo>=</mo>
        <mrow class="MJX-TeXAtom-ORD">
          <mfrac>
            <msqrt>
              <mn>3</mn>
            </msqrt>
            <mn>4</mn>
          </mfrac>
        </mrow>
        <msup>
          <mi>a</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mn>2</mn>
          </mrow>
        </msup>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle A={\frac {\sqrt {3}}{4}}a^{2}}</annotation>
  </semantics>
</math>
	*	簡單上下標
		*	等差數列
<math xml:lang="zh_TW">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <munderover>
          <mo>∑<!-- ∑ --></mo>
          <mrow class="MJX-TeXAtom-ORD">
            <mi>i</mi>
            <mo>=</mo>
            <mn>0</mn>
          </mrow>
          <mrow class="MJX-TeXAtom-ORD">
            <mi>n</mi>
            <mo>−<!-- − --></mo>
            <mn>1</mn>
          </mrow>
        </munderover>
        <mo stretchy="false">(</mo>
        <msub>
          <mi>a</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mn>1</mn>
          </mrow>
        </msub>
        <mo>+</mo>
        <mi>i</mi>
        <mi>d</mi>
        <mo stretchy="false">)</mo>
        <mo>=</mo>
        <mrow class="MJX-TeXAtom-ORD">
          <mfrac>
            <mrow>
              <mi>n</mi>
              <mo stretchy="false">(</mo>
              <msub>
                <mi>a</mi>
                <mrow class="MJX-TeXAtom-ORD">
                  <mn>1</mn>
                </mrow>
              </msub>
              <mo>+</mo>
              <msub>
                <mi>a</mi>
                <mrow class="MJX-TeXAtom-ORD">
                  <mi>n</mi>
                </mrow>
              </msub>
              <mo stretchy="false">)</mo>
            </mrow>
            <mn>2</mn>
          </mfrac>
        </mrow>
        <mo>=</mo>
        <mrow class="MJX-TeXAtom-ORD">
          <mfrac>
            <mrow>
              <mi>n</mi>
              <mo stretchy="false">[</mo>
              <mn>2</mn>
              <msub>
                <mi>a</mi>
                <mrow class="MJX-TeXAtom-ORD">
                  <mn>1</mn>
                </mrow>
              </msub>
              <mo>+</mo>
              <mo stretchy="false">(</mo>
              <mi>n</mi>
              <mo>−<!-- − --></mo>
              <mn>1</mn>
              <mo stretchy="false">)</mo>
              <mi>d</mi>
              <mo stretchy="false">]</mo>
            </mrow>
            <mn>2</mn>
          </mfrac>
        </mrow>
        <mo>=</mo>
        <msub>
          <mi>a</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mn>1</mn>
          </mrow>
        </msub>
        <msubsup>
          <mi>C</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mi>n</mi>
          </mrow>
          <mrow class="MJX-TeXAtom-ORD">
            <mn>1</mn>
          </mrow>
        </msubsup>
        <mo>+</mo>
        <mi>d</mi>
        <msubsup>
          <mi>C</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mi>n</mi>
          </mrow>
          <mrow class="MJX-TeXAtom-ORD">
            <mn>2</mn>
          </mrow>
        </msubsup>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle \sum_{i=0}^{n-1}(a_{1}+id)={\frac {n(a_{1}+a_{n})}{2}}={\frac {n[2a_{1}+(n-1)d]}{2}}=a_{1}C_{n}^{1}+dC_{n}^{2}}</annotation>
  </semantics>
</math>

簡單規則是各種規則的簡化版，當其內容僅為單一項目時，便可省略前後標記朗讀，以達到更好的理解與閱讀，而亦不致造成混淆

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
