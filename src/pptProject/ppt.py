import win32com.client as win32
import time
filePath = "C:\\Users\\tsi_nao\\Desktop\\text.pptx"
ppoint = win32.gencache.EnsureDispatch('Powerpoint.Application')
ppoint.Visible = True
presentation = ppoint.Presentations.Open(filePath)
slideShow = presentation.SlideShowSettings.Run()
time.sleep(0.5)
slideShow.View.Next()
time.sleep(0.5)
slideShow.View.Next()
time.sleep(0.5)
slideShow.View.Next()
time.sleep(0.5)
slideShow.View.Next()
time.sleep(0.5)
slideShow.View.Next()
time.sleep(0.5)
presentation.Close()
ppoint.Quit()