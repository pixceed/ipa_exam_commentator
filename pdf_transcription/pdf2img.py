from pathlib import Path
from pdf2image import convert_from_path

# PDFファイルのパス
pdf_path = Path("pdf_transcription/input/2023r05a_sc_pm_qs_1.pdf")
#outputのファイルパス
img_path=Path("pdf_transcription/output")

#この1文で変換されたjpegファイルが、imageホルダー内に作られます。
convert_from_path(pdf_path, output_folder=img_path,fmt='jpeg',output_file=pdf_path.stem)

