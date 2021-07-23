import qi, time

import PIL
from PIL import Image

# ip = "192.168.252.226"
ip = "192.168.252.247"
# ip = "192.168.253.155"

session = qi.Session()
session.connect("tcp://" + ip + ":" + "9559")

audio = session.service("ALAudioDevice")

audio.enableEnergyComputation()

print ("start")
# for i in range(20):
#     print "{} test".format(i)
#     print audio.getFrontMicEnergy()
#     print audio.getRearMicEnergy()
#     print audio.getLeftMicEnergy()
#     print audio.getRightMicEnergy()

# audio.startMicrophonesRecording("/home/nao/audio/audio.wav")
# time.sleep(10)
# audio.stopMicrophonesRecording()
# print ("stop")

# from pydub import AudioSegment

# songPath = os.path.join(self.behaviorAbsolutePath(), "audio_file.wav")
# self.song = AudioSegment.from_wav(songPath)
# try:
#     # here is important to note that the second parameter is contigus memory audio data!
#     self.ad.sendLocalBufferToOutput(int(self.song.frame_count()), id(self.song._data))
# except Exception as e:
#     self.log("error for buffer: " + str(e) + str(id(self.song.data)))
# self.onUnload()
# pass


# soundex.



# tts = session.service("ALTextToSpeech")
# tts.say ("HelpME")


video = session.service( "ALVideoDevice" )
videoClient = video.subscribeCamera("myCam",0,2,11,10)
naoImage = video.getImageRemote(videoClient)
video.releaseImage(videoClient)
# naoImage = video.getDirectRawImageRemote(videoClient)
# video.releaseDirectRawImage(videoClient)
video.unsubscribe(videoClient)

imageWidth = naoImage[0]
imageHeight = naoImage[1]
array = naoImage[6]

# array = array[:200][200:]
image_string = str(bytearray(array))

im = Image.frombytes("RGB", (imageWidth, imageHeight), image_string)
im.save("camImage.png", "PNG")
# im.show()