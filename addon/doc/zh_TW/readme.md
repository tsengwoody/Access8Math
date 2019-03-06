# Access8Math 說明

此NVDA addon提供數學內容的閱讀，原先NVDA亦有此功能，但因是調用MathPlayer的功能，部份功能尚顯不足，尤其一些語言未提供導航瀏覽(互動式閱讀部份內容)。

導航瀏覽對於閱讀理解長數學內容相當重要，可協助理解長數學內容的結構。

## 功能

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

## 功能表

*	「一般設定」對話框，可設定：
	*	語言：Access8Math 朗讀數學內容的語言
	*	項目間隔時間：設定項目間停頓時間，數值從1到100，數值愈小表示停頓時間愈短，反之數值愈大表示停頓時間愈長。
	*	分析內容的數學意義：將數學內容進行語意分析，符合特定規則時，以該規則的數學意義進行朗讀
	*	讀出字典有定義模式的意義：當字典檔有定義時，使用字典檔讀出提示該項子內容在其上層子內容的意義
	*	讀出自動生成的意義：當字典檔無定義或不完整時，使用自動產生功能讀出提示該項子內容在其上層子內容的意義或項次
*	「規則設定」對話框：可選擇特定規則是否啟用的設定。
*	「unicode 字典」可客製設定各項符號文字的報讀方式。
*	「數學規則」可客製設定各數學類型的報讀方式。
*	「加入新語言」可加入原先於內建未提供的語言，加入後於一般設定內會多出剛新增的語系並可再透過「unicode 字典」與「數學規則」定義讀法達到多國語言客製化設定

## 數學規則

Access8Math將常用數學式依據類型與邏輯，建立43項數學規則，程式依據這套規則判別數學式的唸法與唸讀順序，依據各地習慣不同，可以變更數學唸讀順序與唸法，方法如下：

編輯: 進入"數學規則"後，小視窗列有43項數學規則，選則任一規則可選擇"編輯按鈕"進入編輯條目。

規則的"編輯條目"可分為兩大區塊，分別是序列化順序與子節點角色。
	*	序列化順序：將數學規則依據唸讀順序劃分多個區塊，在此區域可變更規則子項目的唸讀順序及開始、項目間與結束的分隔文字，以分數規則mfrac為例，此規則分為五個唸讀順序，順序0、2和4分別代表起始提示、項目區隔提示與結束提示，可在各欄位中輸入變更自己習慣的唸法，而順序1與3則可調整子節點唸讀的先後，可於下拉式選單中變更順序。
	*	子節點角色：為該數學規則的下一階層子項目，以分數規則mfrac為例，此項規則就包含分子與分母兩項，而在子節點欄位中，可以變更該項子內容在其上層子內容的意義文字，。

範例：可先行查閱確認編輯修改後對此類型的數學規則讀法。點擊後會出現一個預設好符合該對應數學規則的數學內容，供確認對此類型的數學規則讀法是否符合預期。

還原預設值：將數學規則列表還原到初始預設值。

匯入：將數學規則檔案匯入，可用於載入數學規則檔案。

匯出：將數學規則檔案儲存於指定路徑，以利分享或保存數學規則檔案。

## 其他

	簡單規則：簡單規則是各種規則的簡化版，當其內容僅為單一項目時，便可省略前後標記朗讀，以達到更好的理解與閱讀，而亦不致造成混淆

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

# Access8Math v2.1 更新日誌

*	在「一般設定」中，可設定進入互動模式時，是否一併自動顯示「Access8Math 互動視窗」
*	在互動模式中，當無顯示互動視窗時，可透過 ctrl+m 來手動顯示互動視窗
*	修政多國語言切換問題
*	加入土耳其語的翻譯，感謝 Cagri(Çağrı Doğan) 的翻譯工作
*	相容性更新，針對 NVDA 2019.1 對附加元件 manifest 標示的檢查
*	重構對話視窗原始碼

# Access8Math v2.0 更新日誌

*	加入多國語系新增與客製化設定功能，新增三個視窗「unicode 字典」、「數學規則」、「加入新語言」
*	unicode 字典可客製設定各項符號文字的報讀方式。
*	數學規則可客製設定各數學類型的報讀方式並可於修改完成前透過範例的按鈕先行查閱修改的效果。
*	加入新語言可加入原先於內建未提供的語言，加入後於一般設定內會多出剛新增的語系並可再透過「unicode 字典」與「數學規則」定義讀法達到多國語言客製化設定
*	優化在互動模式下，可使用數字鍵7~9以行為單位閱讀序列文字

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
