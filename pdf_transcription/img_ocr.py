from PIL import Image
import pyocr
import cv2

# pyocrが使えることを確認する
tools = pyocr.get_available_tools()
# tesseractのみダウンロードしたため0番目を指定
tool = tools[0]

pdf_img_path = "pdf_transcription/output/sc202310_20001-2.jpg"
pdf_img = Image.open(pdf_img_path)

pdf_txt = tool.image_to_string(
    pdf_img,
    lang='jpn+eng',
    builder=pyocr.builders.TextBuilder(tesseract_layout=6)
)

print("\n#####################################\n")
# print(pdf_txt)

format_pdf_txt = \
    pdf_txt.replace('\n', '').replace(' ', '').replace(',', '、').replace('。', '。\n')
print(format_pdf_txt)