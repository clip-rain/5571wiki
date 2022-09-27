import imageio
from PIL import Image



filenames = ["/Users/raineslei/Documents/family/rourou/WechatIMG27.jpeg",
 "/Users/raineslei/Documents/family/rourou/WechatIMG28.jpeg",
 "/Users/raineslei/Documents/family/rourou/WechatIMG29.jpeg"]
images = []

for filename in filenames:
    img = imageio.imread(filename)
    img = Image.fromarray(img).resize((180, 320))
    images.append(img)

imageio.mimsave('move.gif', images, 'GIF', duration=1)