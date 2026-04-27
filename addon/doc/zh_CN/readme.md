# Access8Math 概述

Access8Math 是一个 NVDA add-on，可以提升用户在阅读和书写数学内容时的体验。

Access8Math 提供 MathML 内容的语音与盲文支持。它也提供交互模式，让用户可以用较小的片段探索数学内容，并更容易理解其结构与层级关系。

Access8Math 也可以协助编写 LaTeX 并转换为 MathML。LaTeX 是一种易于编写与学习的排版系统，常用于表示数学公式。Access8Math 也提供指令菜单、预览支持与导出功能，让数学编辑与分享更加实用。

通过对无障碍数学阅读与高效率数学书写的支持，Access8Math 让视障用户与视力正常的用户之间的数学沟通更加容易。

## 阅读功能概览

* 读取浏览器中 MathML 的内容。
* 读取 Microsoft Word 中 MathType 的内容。
* 完整读出段落中的文字内容与数学内容。
* 自定义朗读规则提升阅读体验（简化朗读规则、项目与项目间停顿等）。
* 可自定义数学符号如何语音报读与盲文输出。

## 交互功能概览

* 移动、放大或缩小数学片段以利阅读。
* 使用 NVDA 检阅光标阅读文字。
* 移动时提示该元素的数学意义。

## 书写功能概览

* 可将 LaTeX/Nemeth 转为 MathML。
* 提供用以辅助输入 LaTeX 的指令菜单
* 提供用以辅助输入 LaTeX 的快捷手势。
* 在编辑时协助更有效地移动编辑光标。
* 在编辑时实时阅读含有 LaTeX/Nemeth 的内容。
* 将纯文字文件转换为可访问的 HTML 文件并进行预览和导出。

## 目录

* 阅读功能
* 交互功能
* 书写功能
* 虚拟菜单
* 本地化
* 附录

## MathML 范例

维基百科上的数学内容即是以 MathML 写成：

* 一元二次方程式：https://zh.wikipedia.org/wiki/一元二次方程
* 矩阵乘法：https://zh.wikipedia.org/zh-tw/%E7%9F%A9%E9%99%A3%E4%B9%98%E6%B3%95
* 三次方程式：https://zh.wikipedia.org/zh-tw/%E4%B8%89%E6%AC%A1%E6%96%B9%E7%A8%8B

# Access8Math 用户手册

## 阅读功能操作

### 语言设置

在「设置」 > 「阅读」菜单中可选择 Access8Math 中数学内容转换的语言。如果发现系统未支持你的语言，请参阅文件「本地化」章节中，「加入新语言」段落。

### 阅读体验设置

#### 数学结构分析

此类规则是为了提高常用数学结构的阅读体验而设计，系统会依据 MathML 结构与数学规则将内容进行处理，让语音朗读与盲文显示更符合数学意义。例如：「x^2」将报读为「x 的平方」而非「x 上标 2」。

你可以在「设置」 >「 阅读」中的「分析内容的数学意义」的复选框勾选是否启用。反之，如想查看原始的 MathML 结构时，则需将此选项取消勾选。

此选项同时也会改变交互模式下移动时提示内容在上下文中数学意义的信息。

#### 简化朗读

当系统解析数学规则时，会将规则简化朗读，若数学内容仅为单一项目时，便可省略朗读前后标记，以达到更快速的理解与阅读效率，而亦不致造成混淆。例如：「\(\frac{1}{2}\)」将朗读为「2 分之 1」而不是「分数 2 分之 1 结束分数」。
若要调整相关简化规则是否启用，你可以在「设置」 > 「规则」中的复选框列表中选择某项简化规则是否启用。

#### 项目间隔时间

Access8Math 报读数学内容时，会在项目与项目之间停顿，让数学内容更容易理解。

若要调整数学内容项目与项目间报读停顿的时间，你可以在「设置」 >「阅读」中设置从 1 到 100 的数值，数值愈小表示停顿时间愈短，相反数值愈大表示停顿时间愈长。

### 数学阅读器设置

在「设置」>「数学阅读器」中可选择数学阅读器的来源。

* 语音来源：选择使用 Access8Math 或 MathCAT 或 Math Player 进行语音朗读。
* 盲文来源：选择使用 Access8Math 或 MathCAT 或 Math Player 进行盲文显示。
* 交互来源：选择使用 Access8Math 或 MathCAT 或 Math Player 进行交互模式。

### 自定义数学符号语音报读与盲文输出

在「本地化」菜单中，可以编辑数学符号表与数学规则表，详细说明请参阅文件「本地化」章节。

## 交互功能操作

### 如何进入 NVDA 交互模式

对于以语音为主的用户，通常希望在较小的片段中听取算式，而非一次听完整个算式。如果你正在浏览模式下，只需将光标移到数学内容上，然后按下空格键或 Enter 键即可。

如果你不在浏览模式下：
1. 将检阅光标移到数学内容的位置。预设情况下，检阅光标会跟随系统光标移动，因此你可以通过移动系统光标到数学内容上。
1. 执行以下快捷键：NVDA + Alt + M，即可进入交互模式与数学内容交互。

进入交互模式后，你可以使用方向键等指令来探索算式。例如，你可以使用左右方向键在算式内移动，并使用向下键进入分式以探索算式中的某一部分。

完成阅读后，只需按下 Esc 键即可返回文件。有关在数学内容中读取和导览的更多信息，请参考下个章节。

### Access8Math 可用于交互模式的键盘指令

* 向下键：缩小阅读片段含概的范围。
* 向上键：放大阅读片段含概的范围。
* 向左键：向前一项数学内容。
* 向右键：向后一项数学内容。
* Ctrl + C：复制对象的 MathML。
* Home 键：阅读片段的范围为整个数学内容。
* 数字键盘 1-9：使用 NVDA 检阅模式阅读数学内容（请参见 NVDA 用户指南的检阅模式章节）。
* Esc 键：退出交互模式。
* 表格导航：在数学表格中，可使用 Ctrl + Alt + 方向键，往上或下一列，往左或右一行移动，与 NVDA 的表格导航相同。
            * Ctrl + Alt + 向左键：移到左一栏。
	* Ctrl + Alt + 向右键：移到右一栏。
	* Ctrl + Alt + 向上键：移到上一列。
	* Ctrl + Alt + 向下键：移到下一列。

### 调整交互模式的朗读与提示方式

* 在交互模式读出自动产生的意义：在交互模式下，当数学规则的子节点角色字段无法完整定义时，系统会读出项数的信息。这项功能适用于某些 MathML 的标签可能具有不定数量节点的情况，例如表格、矩阵、方程式，在移动时，系统会读出类似「第一栏」、「第二项」等提示。如果用户不希望听到这些提示，可将此项设置取消勾选。
* 在交互模式下使⽤⾳效来提⽰无法移动：勾选时，当交互模式下无法移动到新项目上时发出哔哔声；未勾选时则将以语音「无移动」提示。

## 书写功能操作

### Access8Math 编辑器

Access8Math 提供了一套编辑器功能，他可以书写 Markdown 文件，且当有额外资源（如图片、链接等）时可将资源置于编辑器工作空间内并进行引用。

编辑器的导出功能会将 markdown 文件转换为 HTML 文件，其文字和数学内容均能以视觉方式完整显示，此外，导出功能会将文件内引用的资源放入输出的压缩文件中。因此，转出的 HTML 文件可呈现一般文字、数学、图片、视频与音频等内容。

有关更多导入与导出的操作请参阅本文件「导入与导出」章节。

### 分隔符

在书写时，一些特殊的字符会被作为分隔符，以区分文字内容与数学内容，换句话说，在分隔符内的数据为以特定数学标记编写的数学内容，在分隔符外的则为一般文字内容。

| 类别 | 开始标记 | 结束标记 |
| --- | --- | --- |
| LaTeX(括号) | \( | \) |
| LaTeX(美元符号) | $ | $ |
| Nemeth(UEB) | _% | _: |
| Nemeth(at) | @ | @ |

备注：你可以在「设置」 > 「文件」中选择 LaTeX/Nemeth 使用的分隔符号。

### 综合内容范例

* LaTeX（括号）：一元二次方程式 \(ax^2+bx+c=0\) 的解为 \(x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}\) 。
* LaTeX（美元符号）：一元二次方程式 $ax^2+bx+c=0$ 的解为 $x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}$ 。
* Nemeth(UEB)：一元二次方程式 _%⠁⠭⠘⠆⠐⠬⠃⠭⠬⠉⠀⠨⠅⠀⠴_: 的解为 _%⠭⠀⠨⠅⠀⠹⠤⠃⠬⠤⠜⠃⠘⠆⠐⠤⠲⠁⠉⠻⠌⠆⠁⠼_: 。
* Nemeth(at)：一元二次方程式 @⠁⠭⠘⠆⠐⠬⠃⠭⠬⠉⠀⠨⠅⠀⠴@ 的解为 @⠭⠀⠨⠅⠀⠹⠤⠃⠬⠤⠜⠃⠘⠆⠐⠤⠲⠁⠉⠻⠌⠆⠁⠼@ 。
* MathML：一元二次方程式 <math display="inline"><mi>a</mi><msup><mi>x</mi><mn>2</mn></msup><mo>+</mo><mi>b</mi><mi>x</mi><mo>+</mo><mi>c</mi><mo>=</mo><mn>0</mn></math> 的解为 <math display="inline"><mfrac><mrow><mo>−</mo><mi>b</mi><mi>±</mi><msqrt><msup><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mi>a</mi><mi>c</mi></msqrt></mrow><mrow><mn>2</mn><mi>a</mi></mrow></mfrac></math> 。

### 指令手势（开关：NVDA + Alt + C）

* Alt + M：显示标记指令菜单，选择 LaTeX/Nemeth 按下 Enter 键，即会在当前所选文字前后（无选择文字时为当前编辑光标处）加入 LaTeX/Nemeth 标记，并会自动将编辑光标移入其内，以快速输入内容。
* Alt + L：显示 LaTeX 指令菜单（虚拟菜单），选择要加入的 LaTeX 指令项目按下 Enter 键，即会在当前编辑光标处加入对应的 LaTeX 语法，并会自动将编辑光标移入适当输入点，以快速输入内容（若编辑光标未在 LaTeX 区内会自动加上开始与结束标记）。
* LaTeX 指令窗口操作
    * 在此指令菜单中可通过上下键选择列表项目，并通过左右键在不同层级列表中移动。LaTeX 指令菜单包含类别与 LaTeX 标记两个层级，用户可通过上下键先于类别列表中选择分类后再使用向右键进入 LaTeX 标记层选择想插入的 LaTeX 。
    * 选到任意 LaTeX 指令项目按下英文字母 A ~ Z 或 F1 ~ F12 设置快捷手势。
    * 选到任意 LaTeX 指令项目按下 Delete/Backspace 移除已设置的快捷手势。
    * 选到任意 LaTeX 指令项目按下 Enter 在当前编辑光标处加入对应的 LaTeX 语法。
* Alt + I：编辑光标停在数学区块上时，可与该数学区块进行交互。
* Alt + H：显示用于预览或导出的查看指令菜单（虚拟菜单）。详细信息请参阅「导入与导出」章节。

备注：在「设置」>「书写」中内可选择启动时是否启用指令手势，编辑区中按 NVDA + Alt + C 可启用或停用指令手势，并可于 NVDA 的输入手势中变更。

### 快捷手势（开关：NVDA + Alt + S）

当编辑光标在 LaTeX 区块时，按下英文字母 A ~ Z 或 F1 ~ F12 可快速插入绑定的 LaTeX。按 Shift + 字母、Shift + F1 ~ F12 可读出该快捷手势当下绑定的 LaTeX。（需先于 LaTeX 指令菜单中设置快捷手势）

备注：在「设置」>「书写」中可选择启动时是否启用快捷手势，编辑区中按 NVDA + Alt + S 可启用或停用快捷手势，可于输入手势中变更。

### 希腊字母手势（开关：NVDA + Alt + G）

当编辑光标在 LaTeX 区块时，按字母可快速插入对应的希腊字母 LaTeX 。字母与希腊字母对照表请参阅本文件之「附录」。

### 区块编辑与导航

在 Access8Math 编辑器中，通过分隔符隔开的内容会被视为不同的区块，常见的区块分别为文字区块与数学内容区块。你可以通过区块导航快速地在不同类型的区块之间移动编辑光标。

以「一元二次方程式 \(ax^2+bx+c=0\) 的解为 \(x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}\)」此内容为例，有两个主要的数学内容区块以及两个文字区块，我们可以将它们标示为 A 区块、B 区块、C 区块与 D 区块：

* A 区块：「一元二次方程式」这七个字为文字区块。
* B 区块：从  \(ax^2+bx+c=0\) 的起始括号 \( 开始，结束于 0 后面的结束括号 \)。
* C 区块：「的解为」这三个字为文字区块。
* D 区块：从  \(x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}\) 的起始括号 \( 开始，结束于整个表示式的结束括号  \)。

#### 区块导航手势（开关：NVDA + Alt + N）

* Alt + 向左键：移动到上一个数据区块的开始点。
* Alt + 向下键：不移动仅读出当前数据区块的内容。
* Alt + 向右键：移动到下一个数据区块的开始点。
* Alt + Home：移动到当前数据区块的开始点。
* Alt + End：移动到当前数据区块的结束点。
* Alt + Shift + 向左键：移动到上一个数据区块并选取。
* Alt + Shift + 向下键：不移动仅选取当前数据区块的内容。
* Alt + Shift + 向右键：移动到下一个数据区块并选取。

备注：在「设置」>「书写」内可选择启动时是否启用区块导航手势，编辑区中按 NVDA + Alt + N 可启用或停用区块导航手势，可于输入手势中变更。

#### 区块浏览模式（开关：NVDA + Space）

当区块浏览模式打开时，编辑光标移动到数学区块的语音/盲文输出会是数学文字化内容而非原始的数学标记。例如："\(\frac{1}{2}\) 的小数表示为 0.5" 会输出为 "2 分之 1 的小数表示为 0.5" 而非 "\(\frac{1}{2}\) 的小数表示为 0.5"。

可用以下按键手势移动编辑光标与进入交互模式：

* 向左键：移动到上一个数据区块的开始点并读出。
* 向右键：移动到下一个数据区块的开始点并读出。
* 向上键：移动到上一行并读出该行所有区块的内容。
* 向下键：移动到下一行并读出该行所有区块的内容。
* Page Up：往上移动十行并读出该行所有区块的内容。
* Page Down：往下移动十行并读出该行所有区块的内容。
* Home：移动到编辑光标所在行的第一个区块。
* End：移动到编辑光标所在行的最后一个区块。

以上编辑光标移动按键加上 Shift 键则会一并选取文字。

* Space/Enter：编辑光标停在数学区块上时按下 Space/Enter 可进入交互模式。

下列的按键，若仅按该单一键，编辑光标会跳至其对应的后一个类型的区块，若同时按 Shift + 该单一按键，编辑光标会跳至前一个类型的区块：

* L：移到下一个 LaTeX 区块并读出。
* N：移到下一个 Nemeth 区块并读出。
* M：移到下一个 MathML 区块并读出。
* T：移到下一个文字区块并读出。
* Tab：移动到下一个可交互区块（数学区块）并读出。

可用以下按键手势编辑文件：

* Ctrl + X：剪下当前编辑光标区块。
* Ctrl + C：复制当前编辑光标区块。
* Ctrl + V：于当前编辑光标区块后贴上内容。
* Delete/Backspace：删除当前编辑光标区块。

### 导入与导出

#### 导出文件

Access8Math 编辑器的查看菜单内的预览功能可以将 Markdown 文件转换为 HTML 文件进行预览。

Markdown 文件中的数学区块会转换为 MathML，用户可以用不同的方式阅读（视觉阅读、语音听读、盲文点显器呈现)。而文件中所引用的资源（链接、图片、视频与音频等）也会转换成适当的 HTML 元素并正确指向资源文件。因此，转出的 HTML 文件可呈现一般文字、数学、图片、视频与音频等内容。

Access8Math 编辑器的查看菜单内的导出功能让用户可以保存与分享文件。用户选择导出路径与文件名后，导出功能将以相同文件名输出两种文件：

* Access8Math Document 文件 (*.a8m)： Access8Math Document 文件可以再次导入编辑器中进行修改。
* 压缩文件 (*.zip)：压缩文件中的 HTML 文件与预览所转换出的 HTML 文件相同，用户无需安装 Access8Math 即可阅读这个文件。

例如导出路径为 `D:\`，文件名为 `test`，Access8Math 将产生 `D:\test.a8m` 与 `D:\test.zip`。用户可以解压缩 `test.zip` 并打开 `index.html` 来查看文件，HTML 文件中的数学内容将以 MathML 显示。

#### 导入文件

打开 Access8Math Document 的方式：

* 文件资源管理器：在文件资源管理器内选取了一个 Access8Math Document 后，可按下 NVDA + 应用程序键或 NVDA + Shift + F10 打开虚拟菜单，并选择“查看”或“编辑”文件。
* Access8Math 编辑器：在 Access8Math 编辑器的文件菜单中，选择“打开”即可打开 .a8m 文件。

备注：在「设置」>「文件」中的「HTML 数学显示」，可选择导出后的 Access8Math Document 内的 HTML 中数学对象是否为独立区块。效果为在浏览模式上下方向键移动报读整行内容时，数学对象是否独立读出或与一般文字混合读出。

## 虚拟菜单

虚拟菜单将仅以语音朗读和盲文显示菜单项目的方式呈现，而不会以视觉化方式呈现。用户需通过向上键/向下键在列表中选择项目，如果菜单项目有子菜单，可使用向右键进入子菜单；使用向左键退出子菜单。
 
## 本地化

### 加入新语言

可加入原先系统未提供的语言，加入后于「设置」 > 「阅读」 > 「语言」菜单内会多出刚新增的语系，但新增的语系仅是英文语系的副本，你必需通过「符号字典」与「数学规则」定义语音朗读与盲文输出来达成本地化。

### 自定义数学符号语音报读与输出方式

在「工具」 > 「Access8Math」> 「本地化」菜单中可自定义语音朗读与盲文显示，语音朗读与盲文显示内皆分为「符号字典」与「数学规则」两部份。

* 符号读音字典：可自定义各项符号文字的语音朗读。
* 数学规则读音：可自定义各数学类型的语音朗读。
* 符号盲文字典：可自定义各项符号文字的盲文显示。
* 数学规则盲文：可自定义各数学类型的盲文显示。

### 符号字典编辑

Access8Math 通过字典档定义符号对应替代文字／盲文码，以解决罕见符号语音合成器无法朗读或符号在数学情境中与一般文字中有明显差异的问题。例如，「!」在数学内容中意义为「阶乘」，而在一般文字中则表示情感。通过字典档的编辑与新增，可以将原始符号对应到新的替代文字/盲文码，以修正错误的语音朗读与盲文显示。

* 新增：增加一笔符号字典纪录，按下加入按钮后在加入符号对话框中可输入要新增的符号并按确认，此时在符号字典对话框中的纪录列表上就能看到新增的符号。
* 修改：选择一笔符号字典纪录并在替代文字输入值后，Access8Math 遇到此符号即会以对应的替代文字语音朗读与盲文显示该符号。
* 移除：选择一笔符号字典纪录后按下移除按钮可删除选定的符号字典纪录。
* 还原预设值：将字典档列表还原到预设 Access8Math 定义的符号字典纪录。
* 导入：将符号字典文件导入，可用于载入导出的符号字典文件。
* 导出：将符号字典文件储存于指定路径，以利分享或保存符号字典文件。

### 数学规则编辑

Access8Math 将常用数学内容的 MathML 结构，建立对应的数学规则，当遇到符合规则的 MathML 结构时，系统会依据数学规则所定义的内容来语音朗读与盲文显示，依据各地区的习惯不同，用户可自定义语音朗读与盲文输出，方法如下：

* 编辑：进入「数学规则」后，对话框内有数学规则列表，选择任一规则可选择「编辑按钮」进入编辑条目。规则的「编辑条目」可分为两大区块，分别是「序列化顺序」与「节点数学意义」。

  * 序列化顺序：依据数学规则划分数个区段，在此区域可变更规则区段的输出顺序及开始、项目间与结束的文字提示。以分数规则 mfrac 为例，此规则分为五个输出区段，顺序 0、2 和 4 分别代表起始提示、项目区隔提示与结束提示，可在各字段中输入变更自己习惯的输出，而顺序 1 与 3 则可通过下拉式菜单调整区段输出的先后次序。
  * 节点数学意义：可编辑该数学规则特定区段的数学意义。以分数规则 mfrac 为例，此项规则就包含分子与分母两项，而在节点字段中，可以变更此节点在其上下文中的数学意义。

* 范例：可先行查阅确认编辑修改后对此类型的数学规则读法。点击后会出现一个预设好符合该对应数学规则的数学内容，供确认对此类型的数学规则读法是否符合预期。
* 还原预设值：将数学规则列表还原到初始预设值。
* 导入：将数学规则文件导入，可用于载入导出的数学规则文件。
* 导出：将数学规则文件储存于指定路径，以利分享或保存数学规则文件。

如果你有兴趣进行符号字典、数学规则的本地化工作，你可以通过这两个对话框编辑符号字典与数学规则，并通过「导出本地化文件」功能导出一份压缩文件。接着，你可以通过 Access8Math GitHub Pull Requests 或 Email 将此文件提供给开发团队，我们很乐意将其加入 Access8Math 中。

## 附录

### LaTeX 菜单

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

### 英文字母到希腊字母表

| 英文字母 | 希腊字母 | LaTeX |
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

# Access8Math 更新日志

## Access8Math v4.5 更新日志

* 新增 HTML 色彩配置设置，可用于预览与导出输出。
* 重构数学提供者与书写层，改善套件结构与可维护性。
* 移除未使用的网页模板与依赖的相容性模块，并整理导入路径。

## Access8Math v4.2 更新日志

* 加入导出/导入 a8m 文件功能。
* 修正一些问题。

## Access8Math v4.1 更新日志

* 当节点仅包含一个大写字母时，使用 NVDA 语音配置指示大写字母。
* 解决了 Access8Math 在文件资源管理器中打开虚拟上下文菜单与 NVDA 在浏览模式下切换本机选择模式冲突的问题，因为它们都使用相同的手势 (NVDA+Shift+F10)。
* 删除过时的设置选项。
* 限制仅在 Access8Math 编辑器、记事本中才能使用书写功能。
* 重新编写说明文件。


较早版本的更新内容请参阅 [changelog.md](changelog.md)。
