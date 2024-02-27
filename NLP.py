import threading
import time
from tkinter import *
import random
import pyttsx3 
import speech_recognition as sr
r = sr.Recognizer()
list_of_punctuations = {'kama': ',','comma': ',', 'fullstop': '.', 'full stop': '.', 'new line': '\n', 'newline': '\n', 'colon': ':', "exclamation mark": '!', "semicolon": ';', 'question mark': '?', 'hyphen': '-', 'underscore': '_', 'hash': '#'}

fnt1 = ('Arial',12,'bold')
fnt2 = ('Arial',20,'bold')
#Global Variables
btnAnim = 0
rec = 0
def speakText(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def stt():
    global btnAnim, rec, L2
    if (rec ==1):
        L2.delete(0.0,END)
        L2.insert(0.0," "*25+"Please Stay Silent for few Seconds")
        print('Calibrating Microphone')
        speakText('Please Stay silent for few seconds.')
        time.sleep(1)
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source,duration=4)
            L2.delete(0.0,END)
            L2.insert(0.0, " "*25+"Speak Now")
            time.sleep(1)
        with sr.Microphone() as source: 
            speakText("Speak Now!")
            try:
	             audio = r.listen(source,timeout = 10)
            except Exception as e:
                print("MIC ERROR : ",e)      

        # recognize speech using Google Speech Recognition
        try:
            b = r.recognize_google(audio)
            print('\n\n\n'+ b)
            for x in list_of_punctuations.keys():
                if x in b:
                    b = b.replace(x, list_of_punctuations[x])           
            print('\n\n\n'+ b)
            L2.delete(0.0,END)
            L2.insert(0.0,b)
            speakText(b)
            temp = str(random.randint(100,1000))
            f = open(r"C:\Users\Dell\Desktop\New folder\SpeechtoText\storedText"+temp+".txt",'w') #change this path for your convenient to store the converted text
            f.write(b)
            f.close()
            print("Output Saved in storedText"+temp+".txt")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            L2.delete(0.0,END)
            L2.insert(0.0," Speech Recognition could not understand audio. Please Speak Clearly")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            L2.delete(0.0,END)
            L2.insert(0.0,"Could not request results from Google Speech Recognition service. Please Check for Internet Connection ")

        time.sleep(2)
        print('\n\n')
        btnAnim, rec = 0,0

root = Tk()
root.title("Advance Speech to Text")
root.geometry("500x500+400+10")
N = 6 
 #change N value to exact number of frames your gif contains for full  play
frames = [PhotoImage(file=r'C:\Users\Dell\Desktop\New folder\micrec.gif',format = 'gif -index  %i' %(i)) for i in range(N)]

def update(ind):
    global btnAnim
    if(btnAnim==1):
            ind = ind%N
            frame = frames[ind]
            ind += 1
            B1.config(image=frame)
    root.after(100, update, ind)

def multiThreading():
    while True:
        stt()
     
t1 = threading.Thread(target = multiThreading)
t1.start()
def start1():
    global btnAnim, rec
    btnAnim = 1
    rec = 1
win = Frame(root, bg ='powderblue')
L1 = Label(win,text="ADVANCE SPEECH TO TEXT")
L1.config(font = fnt2,bg ='powderblue')
L1.place(x=25,y=10,height = 30,width = 450)
L2 = Text(win)
L2.config(font = fnt1)
L2.place(x=25,y=50,height = 200,width = 450)
B1 = Button(win)
photo = PhotoImage(file=r"C:\Users\Dell\Desktop\New folder\micrec.gif")
B1.config(image=photo,relief = RAISED, command = start1)
B1.config(bg='red')
B1.place(x = 150, y = 280, height = 200, width = 200)
win.place(x=0,y=0,height = 500,width = 500)
root.after(0, update, 0)
mainloop()
