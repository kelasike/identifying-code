"""
open()  #打开图片

new(mode,size,color)   #创建一张空白图片

save("test.gif","GIF")   #保存（新图片路径和名称，保存格式）

size()   #获取图片大小

thumbnail(weight,high)   #缩放图片大小（宽，高）

show()    #显示图片

blend(img1,img2,alpha)   #两张图片相加，alpha表示img1和img2的比例参数。

crop()   #剪切，提取某个矩阵大小的图像。它接收一个四元素的元组作为参数，各元素为（left, upper, right, lower），坐标系统的原点（0, 0）是左上角。

rotate(45)    #逆时针旋转45度

transpose()    #旋转图像
    transpose(Image.FLIP_LEFT_RIGHT)       #左右对换。
    transpose(Image.FLIP_TOP_BOTTOM)       #上下对换。
    transpose(Image.ROTATE_90)             #旋转 90 度角。
    transpose(Image.ROTATE_180)            #旋转 180 度角。
    transpose(Image.ROTATE_270)            #旋转 270 度角。

paste(im,box)#粘贴box大小的im到原先的图片对象中。

convert()    #用来将图像转换为不同色彩模式。

filters()     #滤镜
    BLUR   #虚化
    EMBOSS
resize((128,128))     #resize成128*128像素大小

convert("RGBA")    #图形类型转换

getpixel((4,4))   #获取某个像素位置的值

putpixel((4,4),(255,0,0))    #写入某个像素位置的值
"""

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFilter
import random


class ValidCodeImg:

    def __init__(self,width=150,height=30,code_count=5,font_size=32,point_count=20,line_count=3,img_format="png"):
        '''
        可以生成一个经过降噪后的随机验证码的图片
        :param width: 图片宽度 单位px
        :param height: 图片高度 单位px
        :param code_count: 验证码个数
        :param font_size: 字体大小
        :param point_count: 噪点个数
        :param line_count: 划线个数
        :param img_format: 图片格式
        :return 生成的图片的bytes类型的data
        '''
        self.width = width
        self.height = height
        self.code_count = code_count
        self.font_size = font_size
        self.point_count = point_count
        self.line_count = line_count
        self.img_format = img_format

    def getRandomColor(self):
        '''获取一个随机颜色(r,g,b)格式的'''
        c1 = random.randint(0, 255)
        c2 = random.randint(0, 255)
        c3 = random.randint(0, 255)
        return (c1,c2,c3)

    def getRandomStr(self):
        '''获取一个随机字符串'''
        random_num = int(random.randint(0,9))
        random_low_alpha = chr(random.randint(97,122)).lower()
        random_upper_alpha = chr(random.randint(65,90)).upper()
        random_str = str(random.choice([random_num,random_low_alpha,random_upper_alpha]))
        return random_str

    def getValidCodeImg(self):
        # 获取一个Image对象，参数分别是RGB模式、宽、高，随机颜色
        image = Image.new("RGB",(self.width,self.height),self.getRandomColor())

        # 获取一个画笔对象，将图片对象传过去
        draw = ImageDraw.Draw(image)

        # 获取一个font字体对象参数是ttf的字体文件的目录，以及字体的大小
        font = ImageFont.truetype("arial.ttf",size=self.font_size)

        temp = []
        for i in range(self.code_count):
            # 循环5次，获取5个随机字符串
            random_str = self.getRandomStr()

            # 在图片上一次写入得到的随机字符串,参数是：定位，字符串，颜色，字体
            draw.text((10+i*30,-2), random_str, self.getRandomColor(), font=font)

            # 保存随机字符，以供验证用户输入的验证码是否正确时使用
            temp.append(random_str)

        # 噪点噪线
        for i in range(self.line_count):  # 划线
            x1 = random.randint(0, self.width)
            x2 = random.randint(0, self.width)
            y1 = random.randint(0, self.width)
            y2 = random.randint(0, self.width)
            draw.line((x1, y1, x2, y2), fill=self.getRandomColor())
        for i in range(self.point_count):     # 划点
            draw.point([random.randint(0, self.width), random.randint(0, self.height)], fill=self.getRandomColor())
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            draw.arc((x, y, x + 4, y + 4), 0, 90, fill=self.getRandomColor())

        # 在内存生成图片
        from io import BytesIO
        f = BytesIO()
        image.save(f,self.img_format)
        data = f.getvalue()
        f.close()

        return data

if __name__ == '__main__':
    img = ValidCodeImg()
    data = img.getValidCodeImg()
    with open("test.png","wb") as f:
        f.write(data)
