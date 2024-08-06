# Access8Math 簡介

Access8Math 是一個 NVDA add-on，可以提升使用者在閱讀和書寫數學內容時的體驗。

在閱讀方面，Access8Math 附加元件能夠完整存取以 MathML 格式撰寫的數學內容。MathML 是 Web 中表示數學內容的標準語言，透過瀏覽器能夠完整顯示視覺可讀的數學內容。

在書寫方面，Access8Math 能夠協助撰寫 LaTeX 並轉換為 MathML。LaTeX 是一種易於撰寫和學習的標記系統，常用於表示數學內容。

透過 Access8Math 的閱讀、書寫與轉換功能，讓視障者在輸入與輸出數學內容更加便利。基於 MathML 與 LaTeX 這兩個通用的數學標記並搭配 Access8Math 的使用，可以顯著降低視障者與明眼者之間雙向溝通的難度。

## 閱讀功能概覽

* 讀取瀏覽器中 MathML 的內容。
* 讀取 Microsoft Word 中 MathType 的內容。
* 完整讀出段落中的文字內容與數學內容。
* 客製化朗讀規則提升閱讀體驗（簡化朗讀規則、項目與項目間停頓等）。
* 可自訂數學符號如何語音報讀與點字輸出。

## 互動功能概覽

* 移動、放大或縮小數學片段以利閱讀。
* 使用 NVDA 檢閱游標閱讀文字。
* 移動時提示該元素的數學意義。

## 書寫功能概覽

* 可將 LaTeX/Nemeth 轉為 MathML。
* 提供用以輔助輸入 LaTeX 的指令選單
* 提供用以輔助輸入 LaTeX 的快捷手勢。
* 在編輯時協助更有效地移動編輯游標。
* 在編輯時即時閱讀含有 LaTeX/Nemeth 的內容。
* 將純文字文件轉換為可訪問的 HTML 文件並進行預覽和匯出。

# Access8Math 說明

Access8Math 附加元件提供了全面的數學內容閱讀與書寫功能。

在閱讀方面，Access8Math 提供了可自訂的語音朗讀和點字輸出，並透過互動模式功能，讓使用者可存取與理解數學內容。互動模式可將數學內容切分成較小的片段進行閱讀，使用者可透過鍵盤操作自主選擇閱讀的片段大小，從而更順暢地理解長篇數學內容的結構和層級關係。

在書寫方面，Access8Math 提供了可快速操作的指令選單，使得輸入 LaTeX 更加容易。在輸入時，使用者無需記憶複雜的 LaTeX 語言，只需透過指令選單輕鬆點選即可完成輸入任務。

此外，在輸入的過程中，使用者能即時檢視其輸入的 LaTeX 語法是否正確，協助使用者發現並修正語法上的錯誤。

最後，Access8Math 能將文字與以 LaTeX 方式撰寫的數學內容轉換為視覺可讀的 HTML 文件。由於文字和數學內容均能以視覺方式完整顯示，這使得視障者與明眼者進行數學交流和討論變得非常即時和流暢。

## MathML 範例

維基百科上的數學內容即是以 MathML 寫成：

* 一元二次方程式：https://zh.wikipedia.org/wiki/一元二次方程
* 矩陣乘法：https://zh.wikipedia.org/zh-tw/%E7%9F%A9%E9%99%A3%E4%B9%98%E6%B3%95
* 三次方程式：https://zh.wikipedia.org/zh-tw/%E4%B8%89%E6%AC%A1%E6%96%B9%E7%A8%8B

# Access8Math 使用者手冊

## 閱讀功能操作

### 語言設定

在「設定」 > 「閱讀」選單中可選擇 Access8Math 中數學內容轉換的語言。如果發現系統未支援你的語言，請參閱文件「本地化」章節中，「加入新語言」段落。

### 閱讀體驗設定

#### 數學結構分析

此類規則是為了提高常用數學結構的閱讀體驗而設計，系統會依據 MathML 結構與數學規則將內容進行處理，讓語音朗讀與點字顯示更符合數學意義。例如：「x^2」將報讀為「x 的平方」而非「x 上標 2」。

你可以在「設定」 >「 閱讀」中的「分析內容的數學意義」的核取方塊勾選是否啟用。反之，如想查看原始的 MathML 結構時，則需將此選項取消勾選。

此選項同時也會改變互動模式下移動時提示內容在上下脈絡中數學意義的資訊。

#### 簡化朗讀

當系統解析數學規則時，會將規則簡化朗讀，若數學內容僅為單一項目時，便可省略朗讀前後標記，以達到更快速的理解與閱讀效率，而亦不致造成混淆。例如：「\(\frac{1}{2}\)」將朗讀為「2 分之 1」而不是「分數 2 分之 1 結束分數」。
若要調整相關簡化規則是否啟用，你可以在「設定」 > 「規則」中的核取方塊列表中選擇某項簡化規則是否啟用。

#### 項目間隔時間

Access8Math 報讀數學內容時，會在項目與項目之間停頓，讓數學內容更容易理解。

若要調整數學內容項目與項目間報讀停頓的時間，你可以在「設定」 >「閱讀」中設定從 1 到 100 的數值，數值愈小表示停頓時間愈短，相反數值愈大表示停頓時間愈長。

### 數學閱讀器設定

在「設定」>「數學閱讀器」中可選擇數學閱讀器的來源。

* 語音來源：選擇使用 Access8Math 或 MathCAT 或 Math Player 進行語音朗讀。
* 點字來源：選擇使用 Access8Math 或 MathCAT 或 Math Player 進行點字顯示。
* 互動來源：選擇使用 Access8Math 或 MathCAT 或 Math Player 進行互動模式。

### 自訂數學符號語音報讀與點字輸出

在「本地化」選單中，可以編輯數學符號表與數學規則表，詳細說明請參閱文件「本地化」章節。

## 互動功能操作

### 如何進入 NVDA 互動模式

對於以語音為主的使用者，通常希望在較小的片段中聽取算式，而非一次聽完整個算式。如果你正在瀏覽模式下，只需將游標移到數學內容上，然後按下空格鍵或 Enter 鍵即可。

如果你不在瀏覽模式下：
1. 將檢閱游標移到數學內容的位置。預設情況下，檢閱游標會跟隨系統游標移動，因此你可以透過移動系統游標到數學內容上。
1. 執行以下快速鍵：NVDA + Alt + M，即可進入互動模式與數學內容互動。

進入互動模式後，你可以使用方向鍵等指令來探索算式。例如，你可以使用左右方向鍵在算式內移動，並使用向下鍵進入分式以探索算式中的某一部分。

完成閱讀後，只需按下 Esc 鍵即可返回文件。有關在數學內容中讀取和導覽的更多資訊，請參考下個章節。

### Access8Math 可用於互動模式的鍵盤指令

* 向下鍵：縮小閱讀片段含概的範圍。
* 向上鍵：放大閱讀片段含概的範圍。
* 向左鍵：向前一項數學內容。
* 向右鍵：向後一項數學內容。
* Ctrl + C：複製物件的 MathML。
* Home 鍵：閱讀片段的範圍為整個數學內容。
* 數字鍵盤 1-9：使用 NVDA 檢閱模式閱讀數學內容（請參見 NVDA 用戶指南的檢閱模式章節）。
* Esc 鍵：退出互動模式。
* 表格導航：在數學表格中，可使用 Ctrl + Alt + 方向鍵，往上或下一列，往左或右一行移動，與 NVDA 的表格導航相同。
            * Ctrl + Alt + 向左鍵：移到左一欄。
	* Ctrl + Alt + 向右鍵：移到右一欄。
	* Ctrl + Alt + 向上鍵：移到上一列。
	* Ctrl + Alt + 向下鍵：移到下一列。

### 調整互動模式的朗讀與提示方式

* 在互動模式讀出自動產生的意義：在互動模式下，當數學規則的子節點角色欄位無法完整定義時，系統會讀出項數的資訊。這項功能適用於某些 MathML 的標籤可能具有不定數量節點的情況，例如表格、矩陣、方程式，在移動時，系統會讀出類似「第一欄」、「第二項」等提示。如果使用者不希望聽到這些提示，可將此項設定取消勾選。
* 在互動模式下使⽤⾳效來提⽰無法移動：勾選時，當互動模式下無法移動到新項目上時發出嗶嗶聲；未勾選時則將以語音「無移動」提示。

## 書寫功能操作

### Access8Math 編輯器

Access8Math 提供了一套編輯器功能，他可以書寫 Markdown 文件，且當有額外資源（如圖片、連結等）時可將資源置於編輯器工作空間內並進行引用。

編輯器的匯出功能會將 markdown 文件轉換為 HTML 文件，其文字和數學內容均能以視覺方式完整顯示，此外，匯出功能會將文件內引用的資源放入輸出的壓縮檔內。因此，轉出的 HTML 文件可呈現一般文字、數學、圖片、影片與音樂等內容。

有關更多匯入與會出的操作請參閱本文件「匯入與匯出」章節。

### 分隔符

在書寫時，一些特殊的字元會被作為分隔符，以區分文字內容與數學內容，換句話說，在分隔符內的資料為以特定數學標記撰寫的數學內容，在分隔符外的則為一般文字內容。

| 類別 | 開始標記 | 結束標記 |
| --- | --- | --- |
| LaTeX(括號) | \( | \) |
| LaTeX(錢號) | $ | $ |
| Nemeth(UEB) | _% | _: |
| Nemeth(at) | @ | @ |

備註：你可以在「設定」 > 「文件」中選擇 LaTeX/Nemeth 使用的分隔符號。

### 綜合內容範例

* LaTeX（括號）：一元二次方程式 \(ax^2+bx+c=0\) 的解為 \(x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}\) 。
* LaTeX（錢號）：一元二次方程式 $ax^2+bx+c=0$ 的解為 $x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}$ 。
* Nemeth(UEB)：一元二次方程式 _%⠁⠭⠘⠆⠐⠬⠃⠭⠬⠉⠀⠨⠅⠀⠴_: 的解為 _%⠭⠀⠨⠅⠀⠹⠤⠃⠬⠤⠜⠃⠘⠆⠐⠤⠲⠁⠉⠻⠌⠆⠁⠼_: 。
* Nemeth(at)：一元二次方程式 @⠁⠭⠘⠆⠐⠬⠃⠭⠬⠉⠀⠨⠅⠀⠴@ 的解為 @⠭⠀⠨⠅⠀⠹⠤⠃⠬⠤⠜⠃⠘⠆⠐⠤⠲⠁⠉⠻⠌⠆⠁⠼@ 。
* MathML：一元二次方程式 <math display="inline"><mi>a</mi><msup><mi>x</mi><mn>2</mn></msup><mo>+</mo><mi>b</mi><mi>x</mi><mo>+</mo><mi>c</mi><mo>=</mo><mn>0</mn></math> 的解為 <math display="inline"><mfrac><mrow><mo>−</mo><mi>b</mi><mi>±</mi><msqrt><msup><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mi>a</mi><mi>c</mi></msqrt></mrow><mrow><mn>2</mn><mi>a</mi></mrow></mfrac></math> 。

### 編輯手勢操作

#### 指令手勢（開關：NVDA + Alt + C）

* Alt + M：顯示標記指令選單，選擇 LaTeX/Nemeth 按下 Enter 鍵，即會在當前所選文字前後（無選擇文字時為當前編輯游標處）加入 LaTeX/Nemeth 標記，並會自動將編輯游標移入其內，以快速輸入內容。
* Alt + L：顯示 LaTeX 指令選單（虛擬選單），選擇要加入的 LaTeX 指令項目按下 Enter 鍵，即會在當前編輯游標處加入對應的 LaTeX 語法，並會自動將編輯游標移入適當輸入點，以快速輸入內容（若編輯游標未在 LaTeX 區內會自動加上開始與結束標記）。
* LaTeX 指令視窗操作
    * 在此指令選單中可透過上下鍵選擇列表項目，並透過左右鍵在不同層級列表中移動。LaTeX 指令選單包含類別與 LaTeX 標記兩個層級，使用者可透過上下鍵先於類別列表中選擇分類後再使用向右鍵進入 LaTeX 標記層選擇想插入的 LaTeX 。
    * 選到任意 LaTeX 指令項目按下英文字母 A ~ Z 或 F1 ~ F12 設定快捷手勢。
    * 選到任意 LaTeX 指令項目按下 Delete/Backspace 移除已設定的快捷手勢。
    * 選到任意 LaTeX 指令項目按下 Enter 在當前編輯游標處加入對應的 LaTeX 語法。
* Alt + I：編輯游標停在數學區塊上時，可與該數學區塊進行互動。

備註：在「設定」>「書寫」中內可選擇啟動時是否啟用指令手勢，編輯區中按 NVDA + Alt + C 可啟用或停用指令手勢，並可於 NVDA 的輸入手勢中變更。

#### 快捷手勢（開關：NVDA + Alt + S）

當編輯游標在 LaTeX 區塊時，按下英文字母 A ~ Z 或 F1 ~ F12 可快速插入綁定的 LaTeX。按 Shift + 字母、Shift + F1 ~ F12 可讀出該快捷手勢當下綁定的 LaTeX。（需先於 LaTeX 指令選單中設定快捷手勢）

備註：在「設定」>「書寫」中可選擇啟動時是否啟用快捷手勢，編輯區中按 NVDA + Alt + S 可啟用或停用快捷手勢，可於輸入手勢中變更。

#### 希臘字母手勢（開關：NVDA + Alt + G）

當編輯游標在 LaTeX 區塊時，按字母可快速插入對應的希臘字母 LaTeX 。字母與希臘字母對照表請參閱本文件之「附錄」。

#### 區塊編輯與導航

在 Access8Math 編輯器中，透過分隔符隔開的內容會被視為不同的區塊，常見的區塊分別為文字區塊與數學內容區塊。你可以透過區塊導航快速地在不同類型的區塊之間移動編輯游標。

以「一元二次方程式 \(ax^2+bx+c=0\) 的解為 \(x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}\)」此內容為例，有兩個主要的數學內容區塊以及兩個文字區塊，我們可以將它們標示為 A 區塊、B 區塊、C 區塊與 D 區塊：

* A 區塊：「一元二次方程式」這七個字為文字區塊。
* B 區塊：從  \(ax^2+bx+c=0\) 的起始括號 \( 開始，結束於 0 後面的結束括號 \)。
* C 區塊：「的解為」這三個字為文字區塊。
* D 區塊：從  \(x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}\) 的起始括號 \( 開始，結束於整個表示式的結束括號  \)。

##### 區塊導航手勢（開關：NVDA + Alt + N）

* Alt + 向左鍵：移動到上一個資料區塊的開始點。
* Alt + 向下鍵：不移動僅讀出當前資料區塊的內容。
* Alt + 向右鍵：移動到下一個資料區塊的開始點。
* Alt + Home：移動到當前資料區塊的開始點。
* Alt + End：移動到當前資料區塊的結束點。
* Alt + Shift + 向左鍵：移動到上一個資料區塊並選取。
* Alt + Shift + 向下鍵：不移動僅選取當前資料區塊的內容。
* Alt + Shift + 向右鍵：移動到下一個資料區塊並選取。

備註：在「設定」>「書寫」內可選擇啟動時是否啟用區塊導航手勢，編輯區中按 NVDA + Alt + N 可啟用或停用區塊導航手勢，可於輸入手勢中變更。

##### 區塊瀏覽模式（開關：NVDA + Space）

當區塊瀏覽模式開啟時，編輯游標移動到數學區塊的語音/點字輸出會是數學文字化內容而非原始的數學標記。例如："\(\frac{1}{2}\) 的小數表示為 0.5" 會輸出為 "2 分之 1 的小數表示為 0.5" 而非 "\(\frac{1}{2}\) 的小數表示為 0.5"。

可用以下按鍵手勢移動編輯游標與進入互動模式：

* 向左鍵：移動到上一個資料區塊的開始點並讀出。
* 向右鍵：移動到下一個資料區塊的開始點並讀出。
* 向上鍵：移動到上一行並讀出該行所有區塊的內容。
* 向下鍵：移動到下一行並讀出該行所有區塊的內容。
* Page Up：往上移動十行並讀出該行所有區塊的內容。
* Page Down：往下移動十行並讀出該行所有區塊的內容。
* Home：移動到編輯游標所在行的第一個區塊。
* End：移動到編輯游標所在行的最後一個區塊。

以上編輯游標移動按鍵加上 Shift 鍵則會一併選取文字。

* Space/Enter：編輯游標停在數學區塊上時按下 Space/Enter可進入互動模式。

下列的按鍵，若僅按該單一鍵，編輯游標會跳至其對應的後一個類型的區塊，若同時按 Shift + 該單一按鍵，編輯游標會跳至前一個類型的區塊：

* L：移到下一個 LaTeX 區塊並讀出。
* N：移到下一個 Nemeth 區塊並讀出。
* M：移到下一個 MathML 區塊並讀出。
* T：移到下一個文字區塊並讀出。
* Tab：移動到下一個可互動區塊（數學區塊）並讀出。

可用以下按鍵手勢編輯文件：

* Ctrl + X：剪下當前編輯游標區塊。
* Ctrl + C：複製當前編輯游標區塊。
* Ctrl + V：於當前編輯游標區塊後貼上內容。
* Delete/Backspace：刪除當前編輯游標區塊。

### 匯入與匯出

#### 匯出文件

Access8Math 編輯器的檢視選單內的預覽功能可以將 Markdown 文件轉換為 HTML 文件進行預覽。

Markdown 文件中的數學區塊會轉換為 MathML，使用者可以用不同的方式閱讀（視覺閱讀、語音聽讀、點字摸讀)。而文件中所引用的資源（連結、圖片、影片與音樂等）也會轉換成適當的 HTML 元素並正確指向資源檔。因此，轉出的 HTML 文件可呈現一般文字、數學、圖片、影片與音樂等內容。

Access8Math 編輯器的檢視選單內的匯出功能讓使用者可以保存與分享文件。匯出功能將輸出兩種檔案：

*  Access8Math Document 檔 (*.a8m)： Access8Math Document 檔可以再次匯入編輯器中進行修改。
* 壓縮檔 (*.zip)：壓縮檔中的 HTML 文件與預覽所轉換出的 HTML 文件相同，使用者無需安裝 Access8Math 即可閱讀這個文件。

#### 匯入文件

開啟 Access8Math Document 的方式：

* 檔案總管：在檔案總管內選取了一個 Access8Math Document 後，可按下 NVDA + 快顯鍵或 NVDA + Shift + F10 開啟虛擬路徑功能表，並選擇檢視或編輯檔案。
* Access8Math 編輯器：在 Access8Math 編輯器的檔案選單內，選擇開啟舊檔功能即可開啟 .a8m 檔。

備註：在「設定」>「文件」中的「HTML 數學顯示」，可選擇匯出後的 Access8Math Document 內的 HTML 中數學物件是否為獨立區塊。效果為在瀏覽模式上下方向鍵移動報讀整行內容時，數學物件是否獨立讀出或與一般文字混合讀出。

## 虛擬選單

虛擬選單將僅以語音朗讀和點字顯示選單項目的方式呈現，而不會以視覺化方式呈現。使用者需透過向上鍵/向下鍵在列表中選擇項目，如果選單項目有子選單，可使用向右鍵進入子選單；使用向左鍵退出子選單。
 
## 本地化

### 加入新語言

可加入原先系統未提供的語言，加入後於「設定」 > 「閱讀」 > 「語言」選單內會多出剛新增的語系，但新增的語系僅是英文語系的副本，你必需透過「符號字典」與「數學規則」定義語音朗讀與點字輸出來達成多國語言客製。

### 自訂數學符號語音報讀與輸出方式

在「工具」 > 「Access8Math」> 「本地化」選單中可自定義語音朗讀與點字顯示，語音朗讀與點字顯示內皆分為「符號字典」與「數學規則」兩部份。

* 符號讀音字典：可客製化各項符號文字的語音朗讀。
* 數學規則讀音：可客製化各數學類型的語音朗讀。
* 符號點字字典：可客製化各項符號文字的點字顯示。
* 數學規則點字：可客製化各數學類型的點字顯示。

### 符號字典編輯

Access8Math 透過字典檔定義符號對應替代文字／點字碼，以解決罕見符號語音合成器無法朗讀或符號在數學情境中與一般文字中有明顯差異的問題。例如，「!」在數學內容中意義為「階乘」，而在一般文字中則表示情感。透過字典檔的編輯與新增，可以將原始符號對應到新的替代文字/點字碼，以修正錯誤的語音朗讀與點字顯示。

* 新增：增加一筆符號字典紀錄，按下加入按鈕後在加入符號對話框中可輸入要新增的符號並按確認，此時在符號字典對話框中的紀錄列表上就能看到新增的符號。
* 修改：選擇一筆符號字典紀錄並在替代文字輸入值後，Access8Math 遇到此符號即會以對應的替代文字語音朗讀與點字顯示該符號。
* 移除：選擇一筆符號字典紀錄後按下移除按鈕可刪除選定的符號字典紀錄。
* 還原預設值：將字典檔列表還原到預設 Access8Math 定義的符號字典紀錄。
* 匯入：將符號字典檔案匯入，可用於載入匯出的符號字典檔案。
* 匯出：將符號字典檔案儲存於指定路徑，以利分享或保存符號字典檔案。

### 數學規則編輯

Access8Math 將常用數學內容的 MathML 結構，建立對應的數學規則，當遇到符合規則的 MathML 結構時，系統會依據數學規則所定義的內容來語音朗讀與點字顯示，依據各地區的習慣不同，使用者可自訂語音朗讀與點字輸出，方法如下：

* 編輯：進入「數學規則」後，對話框內有數學規則列表，選擇任一規則可選擇「編輯按鈕」進入編輯條目。規則的「編輯條目」可分為兩大區塊，分別是「序列化順序」與「節點數學意義」。

  * 序列化順序：依據數學規則劃分數個區段，在此區域可變更規則區段的輸出順序及開始、項目間與結束的文字提示。以分數規則 mfrac 為例，此規則分為五個輸出區段，順序 0、2 和 4 分別代表起始提示、項目區隔提示與結束提示，可在各欄位中輸入變更自己習慣的輸出，而順序 1 與 3 則可透過下拉式選單調整區段輸出的先後次序。
  * 節點數學意義：可編輯該數學規則特定區段的數學意義。以分數規則 mfrac 為例，此項規則就包含分子與分母兩項，而在節點欄位中，可以變更此節點在其脈絡中的數學意義。

* 範例：可先行查閱確認編輯修改後對此類型的數學規則讀法。點擊後會出現一個預設好符合該對應數學規則的數學內容，供確認對此類型的數學規則讀法是否符合預期。
* 還原預設值：將數學規則列表還原到初始預設值。
* 匯入：將數學規則檔案匯入，可用於載入匯出的數學規則檔案。
* 匯出：將數學規則檔案儲存於指定路徑，以利分享或保存數學規則檔案。

如果你有興趣進行符號字典、數學規則的本地化工作，你可以透過這兩個對話框編輯符號字典與數學規則，並透過「匯出本地化檔案」功能匯出一份壓縮檔。接著，你可以透過 Access8Math GitHub Pull Requests 或 Email 將此檔案提供給開發團隊，我們很樂意將其加入 Access8Math 中。

## 附錄

### LaTeX 選單

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

### 英文字母到希臘字母對照表

| 英文字母 | 希臘字母 | LaTeX |
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

# Access8Math 日誌

## Access8Math v4.1 更新日誌

* 當節點僅包含一個大寫字母時，使用 NVDA 語音配置指示大寫字母。
* 解決了 Access8Math 在檔案總管中開啟虛擬上下文功能表與 NVDA 在瀏覽模式下切換本機選擇模式衝突的問題，因為它們都使用相同的手勢 (NVDA+Shift+F10)。
* 刪除過時的設定選項。
* 限制僅在 Access8Math 編輯器、記事本中才能使用書寫功能。
* 重新撰寫說明文件。

## Access8Math v4.0 更新日誌

* 相容於 NVDA 2024.1
* 移除遺留冗餘程式碼

## Access8Math v3.8 更新日誌

* 互動模式中對 Mtable 可使用表格導覽(ctrl+alt+方向鍵)
* 新增 LaTeX 選單類別，包括幾何學、排列組合、三角函數與微積分類別
* 新增 LaTeX 選單項目
* 加入取整符號
* 修正 Nemeth 轉 LaTeX 時 .1 與 > 符號轉換錯誤
* 修正數學規則對話框還原預設檔的路徑錯誤

## Access8Math v3.7 更新日誌

* 新功能：在書寫功能中新增 LaTeX 自動補齊功能。
* 在 Nemeth 轉 LaTeX 中，新增帶分數規則
* 在 Access8Math 編輯器中，右上角新增關閉按鈕，按下可關閉 Access8Math 編輯器
* 修正聯立方成式規則（閱讀功能）
* 修正“|”符號不會根據 Unicode 字典轉換為文字。（閱讀功能）
* 修正 ∫ Nemeth 點字轉換 LaTeX 錯誤

## Access8Math v3.6 更新日誌

* 新功能：nemeth 點字輸入，與 LaTeX 輸入有相同功能，編輯時可即時互動導覽(alt+i)、可輸出 HTML+MathML 文件。
* 新功能：加入 Nemeth 分隔符 UEB/at(@@) 以區分 Nemeth 內容。
* 新功能：在互動導航模式下從 Math 物件轉換並複製 LaTeX
* 在檔案總管中開啟虛擬路徑位置功能表快速鍵增加 NVDA+shift+f10
* 修正與優化本地化 UI  問題

## Access8Math v3.5 更新日誌

* 可以正確區分向量和射線
* Access8Math HTML 文件中使用對話框顯示圖片、影片、聲音資源
* Access8Math HTML 文件中使用新視窗開啟連結資源
* 在互動導航模式下從 Math 物件複製 MathML 時加上 MathML 命名空間
* Access8Math 編輯器新增顯示字型調整、尋找與取代功能
* 相容於 NVDA 2023.1

## Access8Math v3.4 更新日誌

* 語音、點字、互動來源設定選項移到偏號->設定->數學閱讀器內
* 整合 MathCAT，當已安裝了 Math Player/MathCat 時，您可以在數學閱讀器設定中選擇您需要的語音、點字和交互來源（Access8Math/Math Player/MathCAT）。
* 使用 MultiCategorySettingsDialog 蒐集設定對話框。
* 按 NVDA+alt+e 在檔案總管中使用內建編輯器打開文字文件。
* 在虛擬選單中的子功能表可透過 enter 展開
* 實做 MathML menclose tag 規則
* 新功能：在檔案總管中的虛擬路徑位置功能表。它可快速開啟檢視或編輯 Access8Math 文件。(請閱讀 Access8Math Document 章節以了解詳細信息)

## Access8Math v3.3 更新日誌

* 新增內建傳統編輯區的編輯器，因應 windows 11 的 UIA 編輯區
* 內建編輯器新增、開啟舊檔、儲存功能
* Access8Math 語言初始設定根據 NVDA 語言設定
* 相容於 NVDA 2022.1
* 修正當文件為空時無法開啟標記指令選單
* 修政轉換 LaTeX/AsciiMath 功能
* 修正 HTML 文件顯示設定選「文字」選項時 HTML 文件渲染問題

## Access8Math v3.2 更新日誌

* 新增可使用「`」來分隔資料區塊，「`」括起來的區塊為 AsciiMath 資料
* 新增瀏覽導航模式編輯快速鍵 - 剪下(ctrl+x)、複製(ctrl+c)、貼上(ctrl+v)、刪除(delete/back space)
* 新增瀏覽導航模式移動快速鍵 - 在可互動之資料區塊間移動(tab)、在 AsciiMath 資料區塊間移動(a)
* 調整瀏覽導航模式移動快速鍵 - 上下左右鍵移動游標方式並讀出移動後資料區塊內容
* 瀏覽導航模式游標移動時，數學資料區塊會讀出數學文字化內容而非原始語法
* 瀏覽導航模式游標停在數學資料區塊上時可按下 space 或 enter 鍵與該數學資料區塊互動導航
* 新增英文字母為可設定之快捷按鍵
* 新增希臘字母快捷手勢
* 快捷按鍵輸入僅在 LaTeX 區有效
* 可設定以音效或語音提示瀏覽導航模式的切換
* LaTeX 指令選單在文字區時可開啟並在插入時加上 LaTeX 分隔符
* 新增轉譯選單，可將游標所停留在的區塊 LaTeX/AsciiMath 資料格式互轉。屬於命令手勢組，當游標停留在 LaTeX/AsciiMath 區塊時，按下 alt+t 可開啟轉譯選單（在瀏覽導航模式下為 ctrl+t）
* 新增批次選單，可將整份文件 LaTeX/AsciiMath 資料格式互轉、可將 LaTeX 分隔符在括號與錢號間轉譯。屬於命令手勢組，按下 alt+b 可開啟批次選單
* 新增 MathML 區塊類型，支援 alt+i，書寫導航模式下直接報讀與單鍵 m, tab 移動
* 新增點字自訂義數學規則與 unicode 字典，與語音相同
* 匯出的 HTML 可呈現 markdown 語法
* 匯出的 HTML 依據記事本視窗標題加入頁面標題與檔案名稱

## Access8Math v3.1 更新日誌

* HTML 視窗改以虛擬選單呈現
* 修正當文件中有「`」時無法正常轉 HTML 檢視
* 修正當文件字數大於 4096 後的內容無轉 HTML 檢視
* 新增常用集合 LaTeX 指令
* 更新 alt+m 在當前所選文字前後（無選擇文字時為當前游標處）插入「\(」、「\)」 LaTeX 標記
* 在一般設定中可選擇匯出的 HTML 中數學內容是否獨立一行呈現
* 匯出 HTML 時將原始文字檔一併存到壓縮包內
* 在一般設定中可選擇用括號或錢字號作為 LaTeX 分隔符
* 在一般設定中可選擇語音、點字、互動的來源（Access8Math 或 Math Player）
* 透過手勢啟用或停用書寫手勢、區塊導航手勢、快捷手勢
* 透過手勢切換語音、點字、互動來源（Access8Math 或 Math Player）

## Access8Math v3.0 更新日誌

* 以 LaTeX 書寫數學內容
* 以 AsciiMath 書寫數學內容
* 書寫綜合內容（文字內容與數學內容）
* 在編輯區內容以快捷鍵移動游標至不同類型區塊
* 在編輯區內容使用指令功能表選擇指令
* 在 LaTeX 指令功能表設定快捷
* 在編輯區內檢視與匯出內容成 HTML

## Access8Math v2.6 更新日誌

* 開啟互動視窗後會自動進入互動模式
* 可以選擇在互動模式下如何提示「無移動」的方式：提示音或語音「無移動」兩種，在一般設定內有多一個「使用提示音來警告無移動」的選項
* 無移動時會再重複報讀一次當前項的內容

## Access8Math v2.5 更新日誌

* 加入俄語的翻譯，感謝 Futyn-Maker 的翻譯工作
* 修正複合符號翻譯失敗的問題
* 移除在 en unicode.dic 內重複的小寫字母並加入大寫字母(0370~03FF)

## Access8Math v2.4 更新日誌

* 修正已知問題

## Access8Math v2.3 更新日誌

* 相容於 Python3
* 重構模組與修正程式碼風格
* 加入單符號向量規則

## Access8Math v2.2 更新日誌

* 修政單一節點有多字元時無法正確報讀
* 修政設定視窗的相容性問題，可相容 NVDA 2019.2，感謝 CyrilleB79 的 pull requests 
* 修政 unicode 有重複符號時的處理
* 加入法語的翻譯，感謝 CyrilleB79 的翻譯工作
* 新增與修政部份介面快速鍵設定

## Access8Math v2.1 更新日誌

* 在「一般設定」中，可設定進入互動模式時，是否一併自動顯示「Access8Math 互動視窗」
* 在互動模式中，當無顯示互動視窗時，可透過 ctrl+m 來手動顯示互動視窗
* 修政多國語言切換問題
* 加入土耳其語的翻譯，感謝 Cagri(Çağrı Doğan) 的翻譯工作
* 相容性更新，針對 NVDA 2019.1 對附加元件 manifest 標示的檢查
* 重構對話視窗原始碼

## Access8Math v2.0 更新日誌

* 加入多國語系新增與客製化設定功能，新增三個視窗「unicode 字典」、「數學規則」、「加入新語言」
* unicode 字典可客製設定各項符號文字的報讀方式。
* 數學規則可客製設定各數學類型的報讀方式並可於修改完成前透過範例的按鈕先行查閱修改的效果。
* 加入新語言可加入原先於內建未提供的語言，加入後於一般設定內會多出剛新增的語系並可再透過「unicode 字典」與「數學規則」定義讀法達到多國語言客製化設定
* 優化在互動模式下，可使用數字鍵7~9以行為單位閱讀序列文字

## Access8Math v1.5 更新日誌

* 在「一般設定」新增項與項間停頓時間設定。數值從1到100，數值愈小表示停頓時間愈短，反之數值愈大表示停頓時間愈長。
* 更新 unicode.dic

## Access8Math v1.4 更新日誌

* 調整設定選項對話框，分為「一般設定」、「規則設定」對話框。「一般設定」為原先「Access8Math 設定」對話框，「規則設定」對話框則為可選擇特定規則是否啟用的設定。
* 新規則
	* 向量規則：當兩個Identifier的正上方有「⇀」時，將其項讀為「向量……」
	* 弧度規則：當兩個Identifier的正上方有「⌢」時，將其項讀為「弧……」
* 修正已知問題

## Access8Math v1.3 更新日誌

* 新規則
	* 正規則：當「+」在首項或其前項為<mo></mo>標記時，將「+」讀為「正」而非「加」
	* 平方規則：當次方數為2時，將其讀為「…的平方」
	* 立方規則：當次方數為3時，將其項讀為「…的立方」
	* 直線規則：當兩個Identifier的正上方有「↔」時，將其項讀為「直線……」
	* 線段規則：當兩個Identifier的正上方有「¯」時，將其項讀為「線段……」
	* 射線規則：當兩個Identifier的正上方有「→」時，將其項讀為「射線……」
* 新增互動視窗：在數學內容上按空白鍵後開啟「Access8Math 互動視窗」，視窗內含有「互動」、「複製」按鈕。
	* 互動：進入數學內容互動導航
	* 複製：複製物件MathML原始碼
* 多國語言新增 zh_CN 的語言
* 調整規則間繼承關係，確保規則衝突時，能正確使用適合的規則
* 修正已知問題

## Access8Math v1.2 更新日誌

* 新規則
	* 負規則：當「-」在首項或其前項為<mo></mo>標記時，將「-」讀為「負」而非「減」
	* 帶分數：當分數前項為數字時，將數字與分數間讀為「又」
* 程式架構優化
	* 加入「sibling」的類別
	* 加入動態產生「反向」 nodetype的類別
* 修正已知問題

## Access8Math v1.1 更新日誌

* 在互動導航時按"Ctrl+c"複製物件MathML原始碼
* 再偏好設定內增加 Access8Math 設定的項目，設定選項對話框，可設定：
	* 語言：Access8Math 朗讀數學內容的語言
	* 分析內容的數學意義：將數學內容進行語意分析，符合特定規則時，以該規則的數學意義進行朗讀
	* 讀出字典有定義模式的意義：當字典檔有定義時，使用字典檔讀出提示該項子內容在其上層子內容的意義
	* 讀出自動生成的意義：當字典檔無定義或不完整時，使用自動產生功能讀出提示該項子內容在其上層子內容的意義或項次
* 加入多條簡單規則，簡單規則是各種規則的簡化版，當其內容僅為單一項目時，便可省略前後標記朗讀，以達到更好的理解與閱讀，而亦不致造成混淆
* 更新unicode.dic
* 修正已知問題
