import random
from PIL import Image, ImageDraw, ImageFont

def image_code():
    # 通过数字获取ascii表中的对应字母
    def get_char():
        return chr(random.randint(65, 90))

    # 获取随机颜色
    def get_color(*args):
        if args == ():
            return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        while True:
            text_color = get_color()
            aberration = 3 * (text_color[0] - args[0][0]) ** 2 + 4 * (text_color[0] - args[0][1]) ** 2 + 2 * (text_color[0] - args[0][2]) ** 2
            rgb2 = 100000
            if aberration > rgb2:
                return text_color

    # 创建图片对象
    img_back = get_color()
    img = Image.new(mode='RGB', size=(120, 50), color=img_back)

    # 创建画笔对象
    draw = ImageDraw.Draw(img, mode='RGB')

    # 在图片中添加随机的噪声点
    for i in range(100):
        x1 = random.randint(0, 120)
        y1 = random.randint(0, 50)
        draw.point((x1, y1), fill=get_color())

    # 在图片中添加随机的直线
    for i in range(10):
        x21 = random.randint(0, 120)
        y21 = random.randint(0, 50)
        x22 = random.randint(0, 120)
        y22 = random.randint(0, 50)
        draw.line((x21, y21, x22, y22), fill=get_color())

    # 在图片中添加随机的弧线
    for i in range(10):
        x31 = random.randint(0, 120)
        y31 = random.randint(0, 50)
        x32 = x31 + 4
        y32 = y31 + 4
        draw.arc((x31, y31, x32, y32), 0, 90, fill=get_color())

    font = ImageFont.truetype("consola.ttf", 40, encoding="unic")

    # 随机获取验证码字符
    char_list = []
    for i in range(4):
        char = get_char()
        char_list.append(char)
        height = random.randint(10, 15)
        # 在图片中添加验证码字符
        draw.text([18 * (i + 1), height], char, get_color(img_back), font=font)

    # 连接验证码字符生成验证码
    char_code = ''.join(char_list)

    return img, char_code