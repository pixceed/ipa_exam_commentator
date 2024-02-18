import os
import tempfile
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image
import pyocr

# PDFファイルのパス
pdf_path = "pdf_transcription/input/2023r05a_sc_pm_qs_1.pdf"

# アウトプットディレクトリのパス
output_dir = "pdf_transcription/output"

# 一時ディレクトリを作成し、自動削除を無効にする
temp_dir = tempfile.mkdtemp(dir='/tmp')

# pyocrの準備
tools = pyocr.get_available_tools()
tool = tools[0]

# PDFを画像変換し、一時ディレクトリに保存
convert_from_path(
    pdf_path,
    output_folder=temp_dir,
    fmt='jpg',
    output_file="temp")


# 画像から文字列を抽出する
result_text = ""
temp_img_list = sorted(os.listdir(temp_dir))
for i, temp_img_name in enumerate(temp_img_list):
    print(f"\n--------- {i+1}/{len(temp_img_list)} ----------\n")

    # 画像取得
    temp_img_path = os.path.join(temp_dir, temp_img_name)
    temp_img = Image.open(temp_img_path)

    # OCR
    pdf_txt = tool.image_to_string(
        temp_img,
        lang='jpn+eng',
        builder=pyocr.builders.TextBuilder(tesseract_layout=6)
    )

    # テキスト整形
    format_pdf_txt = \
        pdf_txt.replace('\n', '').replace(' ', '').replace(',', '、').replace('。', '。\n')

    # 結果に結合
    result_text += format_pdf_txt
    result_text += "\n\n"

# テキストファイルに保存
text_file_name = Path(pdf_path).stem + ".txt"
output_path = os.path.join(output_dir, text_file_name)
with open(output_path, 'w') as f:
    f.write(result_text)

