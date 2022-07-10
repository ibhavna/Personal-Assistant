import speech_recognition as sr
import pyttsx3 #converts speech to text 
import pywhatkit
import datetime
import wikipedia
import pyjokes
import time 
import webbrowser                  #To open websites
import os                          #To open files                       
import subprocess                  #To open files
from tkinter import *              #For the graphics                    
from playsound import playsound    #To play sounds
import keyboard 
import winshell
from urllib.request import urlopen
import requests
import json
import PyPDF2
#from ecapture import ecapture as ec


#name_assistant = "Joonie" #The name of the assistant
name_file = open('C:/Users/DELL/OneDrive/Desktop/PYTHON/Virtual Assistant/Assistant_name.txt', "r")
name_assistant = name_file.read() 


listener = sr.Recognizer() #object creation of speech_recognition
listener.energy_threshold = 4000 #Values below this threshold are considered silence, and values above this threshold are considered speech. Can be changed.
engine = pyttsx3.init() #object creation
#voices = engine.getProperty('voices')
#engine.setProperty('voice',voices[1].id)
rate = engine.getProperty('rate')
engine.setProperty('rate', 120) 

def talk(text):
    engine.say(text)
    print(name_assistant + " : "  +  text)
    engine.runAndWait()

#taking command from user and returning it
def take_command():
    try:
        with sr.Microphone() as source: #creating a microphone to record
            print('listening...')
            playsound('C:/Users/DELL/OneDrive/Desktop/PYTHON/Virtual Assistant/assistant_on.wav')
            voice = listener.listen(source,phrase_time_limit = 10)
            playsound('C:/Users/DELL/OneDrive/Desktop/PYTHON/Virtual Assistant/assistant_off.wav')
            print("Stop...")
            command = listener.recognize_google(voice)
            print('You: ' + ': '+ command)
            if name_assistant in command:
                command = command.replace(name_assistant,"") #to remove the name of engine from our command
                #print(command)
    except Exception as e:
        print(e)
        #talk("Say that again sir")
        #return "None"
    return command


def wishMe():
    hour=datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
       talk("Hello,Good Morning I am you personal Assistant "+name_assistant)
    elif hour >= 12 and hour < 18:
       talk("Hello,Good Afternoon I am you personal Assistant "+name_assistant)
    else:
       talk("Hello,Good Evening I am you personal Assistant "+name_assistant)


def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])


wishMe()
#executing the command
def run_alexa():
 run=1
 while run==1:
    command = take_command().lower()
    run+=1

    if "hello" or "hi" in command():
        wishMe()

    elif "goodbye" in command or "okbye" in command or "stop" in command:
            talk('Your personal assistant ' + name_assistant +' is shutting down, Good bye')
            screen.destroy()
            break

    elif 'date' in command:
        now = datetime.datetime.now()
        my_date = datetime.datetime.today()

        month_name = now.month
        day_name = now.day
        month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        ordinalnames = [ '1st', '2nd', '3rd', ' 4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd','24rd', '25th', '26th', '27th', '28th', '29th', '30th', '31st'] 
    

        talk("Today is "+ month_names[month_name-1] +" " + ordinalnames[day_name-1] + '.')
           
    elif 'play' in command:
        song = command.replace('play',"")
        talk('playing'+song)
        pywhatkit.playonyt(song) #plays song on youtube
        time.sleep(5)

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p') #getting the current time in stringformat(strftime)
        talk('Current time is ' + time)
    
    elif 'search' in command:
        try:
           person = command.replace("search","")
           info = wikipedia.summary(person,2) #fetching only 2 lines of info
           talk(info) #making the assistant to read
           #wikipedia_screen(info)
        except:
            talk("Error.. Couldn't find!")
        
    elif 'joke' in command:
        talk(pyjokes.get_joke())

    elif 'cricket' in command:
        news1 = webbrowser.open_new_tab("cricbuzz.com")
        talk('This is live news from cricbuzz')
        time.sleep(6)

    elif 'news' in command:
        news2 = webbrowser.open_new_tab("https://timesofindia.indiatimes.com")
        talk('Here are some headlines from the Times of India, Happy reading')
        time.sleep(6)
    
    elif 'note this' or 'make a note' in command:    
        command = command.replace("note this", "")
        note(command)

    elif 'open google' in command:
        webbrowser.open_new_tab("https://www.google.com")
        talk("Google chrome is open now")
        time.sleep(5)

    elif 'empty recycle bin' in command:
        winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
        talk("Recycle Bin Recycled")

    elif "weather" in command:  
        # Google Open weather website
        # to get API of Open weather
        talk(" City name ")
        print("City name : ")
        with sr.Microphone() as source: #creating a microphone to record
            new= sr.Recognizer()
            voice1 = new.listen(source,phrase_time_limit = 5)
            city_name = new.recognize_google(voice1)
        #city_name = take_command()
        api = "https://api.openweathermap.org/data/2.5/weather?q="+city_name+"&appid=98c178f21b28af823ffb9282fb68eca9"
        json_data = requests.get(api).json()
             
        if json_data["cod"] != "404":
            condition = json_data['weather'][0]['main'] #getting the weather json data
            temp = int(json_data['main']['temp'] - 273.15) 
            min_temp = int(json_data['main']['temp_min'] - 273.15) 
            max_temp = int(json_data['main']['temp_max'] - 273.15) 
            pressure = json_data['main']['pressure']
            humidity = json_data['main']['humidity']
            wind = json_data['wind']['speed']
    
            final_info = condition+" "+ str(temp) +" "+ "Degree celsius"
            print(final_info)
            talk("The weather updates are")
            talk(final_info)
            final_data = {"Maximum Temperature": max_temp, "Minimum Temperature":min_temp, "Pressure":+ pressure,"Humidity" : humidity, "Wind Speed":wind}
            print(final_data) 
            for i in final_data:
                talk(i)
                talk(str(final_data[i]))
             
        else:
            talk(" City Not Found ")
            talk("Repeat the command")

    
    elif "read the book" in command:
        pdfFileObject = open('C:/Users/DELL/OneDrive/Desktop/PYTHON/Virtual Assistant/my_book.pdf', 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
        text=''
        for i in range(13,pdfReader.numPages):
            # creating a page object
            pageObj = pdfReader.getPage(i)
            # extracting text from page
            text=text+pageObj.extractText()
            print(text)
            talk(text)


    elif 'open gmail' in command:
        webbrowser.open_new_tab("mail.google.com")
        talk("Google Mail open now")
        time.sleep(5) 

    elif 'who are you' in command or 'what can you do' in command:
        talk('I am '+name_assistant+' your personal assistant. I am programmed to minor tasks like opening youtube, google chrome, and search wikipedia etcetra') 


    elif "who made you" in command or "who created you" in command or "who discovered you" in command:
        talk("I was built by my master Bhavna")

    else:
        talk('please say the command again!')

#while True:
#run_alexa()
   #time.sleep(10)

def change_name():
  name_info = name.get()
  file=open("Assistant_name", "w")
  file.write(name_info)
  file.close()
  settings_screen.destroy()
  #screen.destroy()


def change_name_window():
    global settings_screen
    global name


    settings_screen = Toplevel(screen)
    settings_screen.title("Settings")
    settings_screen.geometry("300x300")
    settings_screen.iconbitmap('C:/Users/DELL/OneDrive/Desktop/PYTHON/Virtual Assistant/app_icon.ico')

      
    name = StringVar()

    current_label = Label(settings_screen, text = "Current name: "+ name_assistant)
    current_label.pack()

    enter_label = Label(settings_screen, text = "Please enter your Virtual Assistant's name below") 
    enter_label.pack(pady=10)   
      

    Name_label = Label(settings_screen, text = "Name")
    Name_label.pack(pady=10)
     
    name_entry = Entry(settings_screen, textvariable = name)
    name_entry.pack()


    change_name_button = Button(settings_screen, text = "Ok", width = 10, height = 1, command = change_name)
    change_name_button.pack(pady=10)


def info():
  info_screen = Toplevel(screen)
  info_screen.title("Info")
  info_screen.iconbitmap('C:/Users/DELL/OneDrive/Desktop/PYTHON/Virtual Assistant/app_icon.ico')

  creator_label = Label(info_screen,text = "Created by Bhavna")
  creator_label.pack()

  Age_label = Label(info_screen, text= "She lives in Bhopal")
  Age_label.pack()

  for_label = Label(info_screen, text = "She likes AI!")
  for_label.pack()

keyboard.add_hotkey("enter", run_alexa)

def wikipedia_screen(text):
  wikipedia_screen = Toplevel(screen)
  wikipedia_screen.title(text)
  wikipedia_screen.iconbitmap('C:/Users/DELL/OneDrive/Desktop/PYTHON/Virtual Assistant/app_icon.ico')

  message = Message(wikipedia_screen, text= text)
  message.pack()

def main_screen():
      global screen
      screen = Tk()
      screen.title(name_assistant)
      screen.geometry("300x400")
      screen.iconbitmap('C:/Users/DELL/OneDrive/Desktop/PYTHON/Virtual Assistant/app_icon.ico')


      name_label = Label(text = name_assistant,width = 300, bg = "black", fg="white", font = ("Calibri", 13))
      name_label.pack()

      microphone_photo = PhotoImage(file = 'C:/Users/DELL/OneDrive/Desktop/PYTHON/Virtual Assistant/assistant_logo.png')
      microphone_button = Button(image=microphone_photo, command = run_alexa)
      microphone_button.pack(pady=10)

      settings_photo = PhotoImage(file = 'C:/Users/DELL/OneDrive/Desktop/PYTHON/Virtual Assistant/settings.png')
      settings_button = Button(image=settings_photo, command = change_name_window)
      settings_button.pack(pady=10)
       
      info_button = Button(text ="Info", command = info)
      info_button.pack(pady=10)

      screen.mainloop()
main_screen()




