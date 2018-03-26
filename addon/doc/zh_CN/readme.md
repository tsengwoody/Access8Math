# Access8Math 说明

此NVDA addon提供数学内容的阅读，原先NVDA亦有此功能，但因是调用MathPlayer的功能，部份功能尚显不足，尤其一些语言未提供导航浏览(交互式阅读部份内容)。

导航浏览对于阅读理解长数学内容相当重要，可协助理解长数学内容的结构。

功能有：

*	可阅读网页浏览器(Mozilla Firefox, Microsoft Internet Explorer and Google Chrome)上以MathML撰写的数学内容
*	可阅读Microsoft Word上以MathType 撰写的数学内容。(需安装MathType)
*	在数学内容上按空格键后开启「Access8Math 互动窗口」，窗口内含有「互动」、「复制」按钮。
	*	互动：与该数学内容进行导航浏览，亦即可部份浏览数学内容中的子内容并在子内容间移动或缩放子内容大小
	*	复制：复制对象MathML原始码
*	在导航浏览时会提示该项子内容在其上层子内容的意义
*	在导航浏览时按键：
	*	向下键缩小当前数学内容成更小的子内容
	*	向上键放大当前数学内容成更大的子内容
	*	向左键向前一项数学内容
	*	向右键向后一项数学内容
	*	home键回到最顶层(完整数学内容)
	*	"Ctrl+c": 复制对象MathML原始码
	*	数字键盘1-9：使用NVDA Reviewing Text方式阅读序列化的数学内容
	*	esc键退出导航浏览模式
*	ctrl+alt+m：可在Access8Math与MathPlayer间切换阅读器(有安装MathPlayer才能切换)

*	菜单：
	*	「一般设定」对话框，可设定：
		*	语言：Access8Math 朗读数学内容的语言
		*	分析内容的数学意义：将数学内容进行语意分析，符合特定规则时，以该规则的数学意义进行朗读
		*	读出字典有定义模式的意义：当字典文件有定义时，使用字典文件读出提示该项子内容在其上层子内容的意义
		*	读出自动生成的意义：当字典文件无定义或不完整时，使用自动产生功能读出提示该项子内容在其上层子内容的意义或项次
	*	「规则设定」对话框：可选择特定规则是否启用的设定。
*	简单规则：简单规则是各种规则的简化版，当其内容仅为单一项目时，便可省略前后标记朗读，以达到更好的理解与阅读，而亦不致造成混淆

数学内容解析数学规则意义持续增加中

目前先针对以Presentation Markup写成的MathML处理，因word、math type、wiris等MathML图形化输入工具产生的MathML皆为此型态

维基百科上的数学内容皆以MathML写成

*	矩阵乘法：https://zh.wikipedia.org/zh-tw/%E7%9F%A9%E9%99%A3%E4%B9%98%E6%B3%95
*	三次方程：https://zh.wikipedia.org/zh-tw/%E4%B8%89%E6%AC%A1%E6%96%B9%E7%A8%8B

*	例子
	*	一元二次方程解：
<math xmlns="http://www.w3.org/1998/Math/MathML"><mfrac><mrow><mo>-</mo><mi>b</mi><mo>&#xB1;</mo><msqrt><msup><mi>b</mi><mn>2</mn></msup><mo>-</mo><mn>4</mn><mi>a</mi><mi>c</mi></msqrt></mrow><mrow><mn>2</mn><mi>a</mi></mrow></mfrac></math>
	*	二项式定理：
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

原始码：https://github.com/tsengwoody/Access8Math

欢迎提出见意与bug回报，谢谢！

# Access8Math v1.4 更新日志

*	调整设定选项对话框，分为「一般设定」、「规则设定」对话框。「一般设定」为原先「Access8Math 设定」对话框，「规则设定」对话框则为可选择特定规则是否启用的设定。
*	新规则
	*	向量规则：当两个Identifier的正上方有「⇀」时，将其项读为「向量……」
	*	弧度规则：当两个Identifier的正上方有「⌢」时，将其项读为「弧……」
*	修正已知问题

# Access8Math v1.3 更新日志

*	新规则
	*	正规则：当「+」在首项或其前项为<mo></mo>标记时，将「+」读为「正」而非「加」
	*	平方规则：当次方数为2时，将其读为「…的平方」
	*	立方规则：当次方数为3时，将其项读为「…的立方」
	*	直线规则：当两个Identifier的正上方有「↔」时，将其项读为「直线……」
	*	线段规则：当两个Identifier的正上方有「¯」时，将其项读为「线段……」
	*	射线规则：当两个Identifier的正上方有「→」时，将其项读为「射线……」
*	新增互动窗口：在数学内容上按空格键后开启「Access8Math 互动窗口」，窗口内含有「互动」、「复制」按钮。
	*	互动：进入数学内容导航浏览
	*	复制：复制对象MathML原始码
*	多国语言新增 zh_CN 的语言
*	调整规则间继承关系，确保规则冲突时，能正确使用适合的规则
*	修正已知问题

# Access8Math v1.2 更新日志

*	新规则
	*	负规则：当「-」在首项或其前项为<mo></mo>标记时，将「-」读为「负」而非「减」
	*	带分数：当分数前项为数字时，将数字与分数间读为「又」
*	程序架构优化
	*	加入「sibling」的类别
	*	加入动态产生「反向」 nodetype的类别
*	修正已知问题

# Access8Math v1.1 更新日志

*	在导航浏览时按"Ctrl+c"复制对象MathML原始码
*	再偏好设定内增加 Access8Math 设定的项目，设定选项对话框，可设定：
	*	语言：Access8Math 朗读数学内容的语言
	*	分析内容的数学意义：将数学内容进行语意分析，符合特定规则时，以该规则的数学意义进行朗读
	*	读出字典有定义模式的意义：当字典文件有定义时，使用字典文件读出提示该项子内容在其上层子内容的意义
	*	读出自动生成的意义：当字典文件无定义或不完整时，使用自动产生功能读出提示该项子内容在其上层子内容的意义或项次
*	加入多条简单规则，简单规则是各种规则的简化版，当其内容仅为单一项目时，便可省略前后标记朗读，以达到更好的理解与阅读，而亦不致造成混淆
*	更新unicode.dic
*	修正已知问题
