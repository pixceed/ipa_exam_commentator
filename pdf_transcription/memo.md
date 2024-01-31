# 画像形式のPDFをOCRで文字起こし

## 参考

<https://qiita.com/masa1124/items/198ceea22becdf311f31>

## インストール

``` bash
!pip install pyocr
!sudo apt-get install -y tesseract-ocr libtesseract-dev tesseract-ocr-jpn
```

下記のコマンドを実行してjpnと表示されたらインストール成功

``` bash
!tesseract --list-langs
```
