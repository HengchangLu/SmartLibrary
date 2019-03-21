from PIL import Image
from pytesseract import image_to_string


def initTable(threshold=140):  # 降噪，图片二值化
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table


def get_verify_via_ocr(img_path):
    image = Image.open(img_path)
    image = image.convert('L')  # 彩色图转换为灰度图
    binaryImage = image.point(initTable(), '1')  # 将灰度图二值化
    verify = image_to_string(binaryImage)  # 使用image_to_string识别验证码
    verify = verify.strip()
    return verify
