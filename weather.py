import smtplib
import tkinter as tk
import tkinter.messagebox

import requests
from bs4 import BeautifulSoup
from tkinter import *
from PIL import ImageTk,Image


def makeSoup():
    url = "https://www.google.com/search?client=firefox-b-d&q=wetter"

    userAgent = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0"}

    page = requests.get(url, headers=userAgent)

    soup = BeautifulSoup(page.content, "html.parser")

    return soup


def getTempList():
    soup = makeSoup()

    currenttemp = "Aktuell: " + soup.find(id="wob_tm").get_text()

    tempList = [currenttemp]

    daysList = []

    soupList = soup.find(id="wob_dp")
    tempSoup = soupList.find_all(class_="wob_t")

    daysSoup = soup.find_all("div", class_="vk_lgy")
    for e in daysSoup:
        if (containsNumber(e.get_text()) == False):
            daysList.append(e.get_text()[0:2])

    firstDayTemp = daysList[0] + ": " + tempSoup[0].get_text()
    tempList.append(firstDayTemp)

    for i in [4, 8, 12, 16, 20, 24, 28]:
        tempForOneDay = daysList[int(i / 4)] + ": " + tempSoup[i].get_text()
        tempList.append(tempForOneDay)

    return tempList


def buildStartGUI():
    window = tk.Tk()
    window.title("Weather App")
    window.geometry("400x300")
    window.resizable(False, False)
    window.eval('tk::PlaceWindow . center')
    window.configure(background="black")

    canvas = tk.Canvas(window,width="400",height="300")
    weatherimage = ImageTk.PhotoImage(file="C:\\Users\\timos\\Desktop\\PythonWeather\\picture.gif")
    canvas.create_image(0, 0, anchor=NW, image =weatherimage)
    canvas.pack()

    weatherdata = tk.Text(window, height="10", width="30")

    for e in getTempList():
        weatherdata.insert(tk.INSERT, e + "\n")

    weatherdata.config(state="disabled")
    weatherdata.pack()

    canvas.create_window(70, 10, anchor=NW, window=weatherdata)

    doYouWantEmailLabel = tk.Label(
        window, text="Do you want an email with the weather?")
    doYouWantEmailLabel.pack()

    canvas.create_window(70, 200, anchor=NW, window=doYouWantEmailLabel)

    sendEmailButton = tk.Button(
        window, text="Yes", command=lambda: buildSendEmailGUI(window))
    sendEmailButton.pack()

    canvas.create_window(170, 240, anchor=NW, window=sendEmailButton)

    window.mainloop()


def buildSendEmailGUI(oldWindow):
    oldWindow.destroy()
    window = tk.Tk()
    window.resizable(False, False)
    window.title("Weather App")
    window.geometry("400x300")
    window.eval('tk::PlaceWindow . center')

    canvas = tk.Canvas(window, width="400", height="300")
    weatherimage = ImageTk.PhotoImage(file="C:\\Users\\timos\\Desktop\\PythonWeather\\picture.gif")
    canvas.create_image(0, 0, anchor=NW, image=weatherimage)
    canvas.pack()

    enterEmailLabel = tk.Label(window, text="Please enter your email:")
    enterEmailLabel.pack()

    canvas.create_window(130, 60, anchor=NW, window=enterEmailLabel)

    textField = tk.Entry(window, width="40")
    textField.pack()

    canvas.create_window(80, 90, anchor=NW, window=textField)

    sendEmailButton = tk.Button(window, text="Send email",
                                command=lambda: sendEmailWithWeather(textField.get(), window))
    sendEmailButton.pack()

    canvas.create_window(160, 120, anchor=NW, window=sendEmailButton)

    goBackButton = tk.Button(window, text="Go back", command=lambda: goBack(window))
    goBackButton.pack()

    canvas.create_window(165, 150, anchor=NW, window=goBackButton)

    window.mainloop()


def goBack(oldWindow):
    oldWindow.destroy()
    buildStartGUI()


def sendEmailWithWeather(userEmail, oldWindow):
    templist = getTempList()
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    # This uses an app password for my computer!
    server.login("timo.schessl@gmail.com", "fmlwlptlhldmblai")

    subject = "Python Mail Weather"

    body = ""

    for element in templist:
        body = body + "\n" + element

    body = body.replace('ö', 'oe')
    body = body.replace('ü', 'ue')
    body = body.replace('ä', 'ae')

    message = f"Subject: {subject}\n\n{body}"

    try:
        server.sendmail(
            "Timo",
            userEmail,
            message.encode("utf8"))
        tkinter.messagebox.showinfo("Message", "Email was sent successfully!")
        oldWindow.destroy()
        buildStartGUI()
    except:
        tkinter.messagebox.showinfo("Error", "This is not a valid email!")
    server.quit()


def containsNumber(string):
    for i in range(len(string)):
        if string[i].isdigit():
            return True
    return False


buildStartGUI()
