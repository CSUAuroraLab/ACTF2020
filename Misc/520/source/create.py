# import cv2
# import numpy as np
# import binascii
#
# def create(flag, k):
#     img = range(1, 255)
#     if(flag == "black"):
#         img = np.zeros((365, 500, 3), np.uint8)
#         img[:, :, 2] = np.ones((365, 500))*255
#         img[:, :, 1] = np.ones((365, 500)) * 182
#         img[:, :, 0] = np.ones((365, 500)) * 193
#     else:
#         img = np.zeros((365, 500, 3), np.uint8)
#         img[:, :, 2] = np.ones((365, 500)) * 220
#         img[:, :, 1] = np.ones((365, 500)) * 20
#         img[:, :, 0] = np.ones((365, 500)) * 60
#
#     # cv2.imshow("Image", img)
#     path = str(k) + ".png"
#     print(path)
#     cv2.imwrite(path, img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#
# text = "oh!fIne"
# res = ""
# for i in text:
#     num = bin(ord(i)).replace("0b", "")
#     res += str(num)
#
# print(len(res))
#
# k = 0
# for i in res:
#     if i == '1':
#         create("black", k)
#     else:
#         create("white", k)
#     k = k + 1


import numpy as np
from PIL import Image, ImageDraw


def heart(size):
    width, height = size
    img = Image.new('L', size, 0)
    draw = ImageDraw.Draw(img)
    polygon = [
        (width / 10, height / 3),
        (width / 10, 81 * height / 120),
        (width / 2, height),
        (width - width / 10, 81 * height / 120),
        (width - width / 10, height / 3),
    ]
    draw.polygon(polygon, fill=255)
    draw.ellipse((0, 0, width / 2, 3 * height / 4), fill=255)
    draw.ellipse((width / 2, 0, width, 3 * height / 4), fill=255)
    return img

for i in range(48):
    path = str(i) + ".png"
    img = Image.open(path).convert("RGB")
    npImage = np.array(img)
    img_heart = heart(img.size)
    npAlpha = np.array(img_heart)
    npImage = np.dstack((npImage, npAlpha))
    Image.fromarray(npImage).save("img/" + path)
