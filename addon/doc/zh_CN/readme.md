# Access8Math 说明

此NVDA addon提供数学内容的阅读，原先NVDA亦有此功能，但因是调用MathPlayer的功能，部份功能尚显不足，尤其一些语言未提供导航浏览(交互式阅读部份内容)。

导航浏览对于阅读理解长数学内容相当重要，可协助理解长数学内容的结构。

## 功能

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
	*	数字键盘1-9：使用NVDA Reviewing Text方式阅读串行化的数学内容
	*	esc键退出导航浏览模式
*	ctrl+alt+m：可在Access8Math与MathPlayer间切换阅读器(有安装MathPlayer才能切换)

## 菜单

*	「一般设定」对话框，可设定：
	*	语言：Access8Math 朗读数学内容的语言
	*	项目间隔时间：设定项目间停顿时间，数值从1到100，数值愈小表示停顿时间愈短，反之数值愈大表示停顿时间愈长。
	*	分析内容的数学意义：将数学内容进行语意分析，符合特定规则时，以该规则的数学意义进行朗读
	*	读出字典有定义模式的意义：当字典文件有定义时，使用字典文件读出提示该项子内容在其上层子内容的意义
	*	读出自动生成的意义：当字典文件无定义或不完整时，使用自动产生功能读出提示该项子内容在其上层子内容的意义或项次
*	「规则设定」对话框：可选择特定规则是否启用的设定。
*	「unicode 字典」可客制设定各项符号文字的报读方式。
*	「数学规则」可客制设定各数学类型的报读方式。
*	「加入新语言」可加入原先于内建未提供的语言，加入后于一般设定内会多出刚新增的语系并可再透过「unicode 字典」与「数学规则」定义读法达到多国语言客制化设定

## 数学规则

Access8Math将常用数学式依据类型与逻辑，建立43项数学规则，程序依据这套规则判别数学式的念法与念读顺序，依据各地习惯不同，可以变更数学念读顺序与念法，方法如下：

编辑: 进入"数学规则"后，小窗口列有43项数学规则，选则任一规则可选择"编辑按钮"进入编辑条目。

规则的"编辑条目"可分为两大区块，分别是串行化顺序与子节点角色。
	*	串行化顺序：将数学规则依据念读顺序划分多个区块，在此区域可变更规则子项目的念读顺序及开始、项目间与结束的分隔文字，以分数规则mfrac为例，此规则分为五个念读顺序，顺序0、2和4分别代表起始提示、项目区隔提示与结束提示，可在各字段中输入变更自己习惯的念法，而顺序1与3则可调整子节点念读的先后，可于下拉式选单中变更顺序。
	*	子节点角色：为该数学规则的下一阶层子项目，以分数规则mfrac为例，此项规则就包含分子与分母两项，而在子节点字段中，可以变更该项子内容在其上层子内容的意义文字，。

范例：可先行查阅确认编辑修改后对此类型的数学规则读法。点击后会出现一个预设好符合该对应数学规则的数学内容，供确认对此类型的数学规则读法是否符合预期。

还原默认值：将数学规则列表还原到初始默认值。

汇入：将数学规则档案汇入，可用于加载数学规则档案。

汇出：将数学规则档案储存于指定路径，以利分享或保存数学规则档案。

## 其他

	简单规则：简单规则是各种规则的简化版，当其内容仅为单一项目时，便可省略前后标记朗读，以达到更好的理解与阅读，而亦不致造成混淆

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

# Access8Math v2.3 更新日志

*	相容于 Python3
*	重构模块与修正程序代码风格
*	加入单符号向量规则

# Access8Math v2.2 更新日志

*	修政单一节点有多字符时无法正确报读
*	修政设定窗口的兼容性问题，可兼容 NVDA 2019.2，感谢 CyrilleB79 的 pull requests 
*	修政 unicode 有重复符号时的处理
*	加入法语的翻译，感谢 CyrilleB79 的翻译工作
*	新增与修政部份接口快捷键设定

# Access8Math v2.1 更新日志

*	在「一般设定」中，可设定进入互动模式时，是否一并自动显示「Access8Math 互动窗口」
*	在互动模式中，当无显示互动窗口时，可透过 ctrl+m 来手动显示互动窗口
*	修政多国语言切换问题
*	加入土耳其语的翻译，感谢 Cagri(Çağrı Doğan) 的翻译工作
*	兼容性更新，针对 NVDA 2019.1 对附加组件 manifest 标示的检查
*	重构对话窗口原始码

# Access8Math v2.0 更新日志

*	加入多国语系新增与客制化设定功能，新增三个窗口「unicode 字典」、「数学规则」、「加入新语言」
*	unicode 字典可客制设定各项符号文字的报读方式。
*	数学规则可客制设定各数学类型的报读方式并可于修改完成前透过范例的按钮先行查阅修改的效果。
*	加入新语言可加入原先于内建未提供的语言，加入后于一般设定内会多出刚新增的语系并可再透过「unicode 字典」与「数学规则」定义读法达到多国语言客制化设定
*	优化在互动模式下，可使用数字键7~9以行为单位阅读序列文字

# Access8Math v1.5 更新日志

*	在「一般设定」新增项与项间停顿时间设定。数值从1到100，数值愈小表示停顿时间愈短，反之数值愈大表示停顿时间愈长。
*	更新 unicode.dic

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
