from PIL import Image
import pytesseract
path ="example_page-0001.jpg"
img = Image.open(path)
text = pytesseract.image_to_string(img, lang='eng', config='-c preserve_interword_spaces=1 --psm 6')
print text