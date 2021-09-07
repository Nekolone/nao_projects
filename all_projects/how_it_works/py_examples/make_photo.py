import qi
from PIL import Image

ip = "192.168.252.247"

session = qi.Session()
session.connect("tcp://" + ip + ":" + "9559")

video = session.service("ALVideoDevice")
videoClient = video.subscribeCamera("myCam", 0, 2, 11, 10)
naoImage = video.getImageRemote(videoClient)
video.releaseImage(videoClient)
video.unsubscribe(videoClient)

imageWidth = naoImage[0]
imageHeight = naoImage[1]
array = naoImage[6]

image_string = str(bytearray(array))

im = Image.frombytes("RGB", (imageWidth, imageHeight), image_string)
im.save("camImage.png", "PNG")
