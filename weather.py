import smtplib
import tkinter as tk
import tkinter.messagebox

import requests
from bs4 import BeautifulSoup
from tkinter import *
from PIL import ImageTk, Image
from tkinter.simpledialog import askstring


def makeSoup():
    url = "https://www.google.com/search?client=firefox-b-d&q=wetter"

    userAgent = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0"}
    try:
     page = requests.get(url, headers=userAgent)

     soup = BeautifulSoup(page.content, "html.parser")

     return soup
    except:
     tkinter.messagebox.showinfo("Error", "No connection with the internet.")




def getTempList():
    soup = makeSoup()

    currenttemp = "Current: " + soup.find(id="wob_tm").get_text()

    tempList = [currenttemp + " °C"]

    daysList = []

    soupList = soup.find(id="wob_dp")
    tempSoup = soupList.find_all(class_="wob_t")

    daysSoup = soup.find_all("div", class_="vk_lgy")
    for e in daysSoup:
        if (containsNumber(e.get_text()) == False):
            daysList.append(e.get_text()[0:2])

    firstDayTemp = daysList[0] + ": " + tempSoup[0].get_text()
    tempList.append(firstDayTemp + " °C")

    for i in [4, 8, 12, 16, 20, 24, 28]:
        tempForOneDay = daysList[int(i / 4)] + ": " + tempSoup[i].get_text()
        tempList.append(tempForOneDay + " °C")

    return tempList


def buildStartGUI():
    window = tk.Tk()
    window.title("Weather App")
    window.geometry("600x400")
    window.resizable(False, False)
    window.eval('tk::PlaceWindow . center')
    window.configure(background="black")

    canvas = tk.Canvas(window, width="600", height="400")
    weatherimage = ImageTk.PhotoImage(file="C:\\Users\\timos\\Desktop\\PythonWeather\\picture.gif")
    canvas.create_image(0, 0, anchor=NW, image=weatherimage)
    canvas.pack()

    weatherdata = tk.Text(window, height="9", width="20", bg="gray15", fg="white")

    for e in getTempList():
        weatherdata.insert(tk.INSERT, e + "\n")

    weatherdata.config(state="disabled", font=("Courier", 15, "bold"))
    weatherdata.pack()

    canvas.create_window(170, 10, anchor=NW, window=weatherdata)

    sendEmailButton = tk.Button(
        window, text="Send email", command=lambda: buildSendEmailGUI(window), bg="orange", font=("Courier", 15, "bold"))
    sendEmailButton.pack()

    canvas.create_window(220, 240, anchor=NW, window=sendEmailButton)

    window.mainloop()


def buildSendEmailGUI(oldWindow):
    oldWindow.destroy()
    window = tk.Tk()
    window.resizable(False, False)
    window.title("Weather App")
    window.geometry("600x400")
    window.eval('tk::PlaceWindow . center')

    canvas = tk.Canvas(window, width="600", height="400")
    weatherimage = ImageTk.PhotoImage(file="C:\\Users\\timos\\Desktop\\PythonWeather\\picture.gif")
    canvas.create_image(0, 0, anchor=NW, image=weatherimage)
    canvas.pack()

    enterEmailLabel = tk.Label(window, text="Please enter your email:",
                               width="40", bg="gray15", fg="white", font=("Courier", 15, "bold"))
    enterEmailLabel.pack()

    canvas.create_window(79, 62, anchor=NW, window=enterEmailLabel)

    textField = tk.Entry(window, width="40", font=("Courier", 15, "bold"), bg="gray15", fg="white"
                         , insertbackground="white")
    textField.pack()

    canvas.create_window(80, 90, anchor=NW, window=textField)

    sendEmailButton = tk.Button(window, text="Send email",
                                command=lambda: sendEmailWithWeather(textField.get(), window), bg="orange",
                                font=("Courier", 15, "bold"))
    sendEmailButton.pack()

    canvas.create_window(240, 130, anchor=NW, window=sendEmailButton)

    goBackButton = tk.Button(window, text="Go back", command=lambda: goBack(window), bg="orange",
                             font=("Courier", 15, "bold"))
    goBackButton.pack()

    canvas.create_window(260, 180, anchor=NW, window=goBackButton)

    window.mainloop()


def goBack(oldWindow):
    oldWindow.destroy()
    buildStartGUI()


def sendEmailWithWeather(userEmail, oldWindow):
    flag = True

    password = askstring("Message", "Enter the server password:")
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("timo.schessl@gmail.com", password)
    except:
        tkinter.messagebox.showinfo("Error", "Login not successful!")
        server.quit()
        flag = False

    if (flag):
        templist = getTempList()
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
                "Python Weather App",
                userEmail,
                message.encode("utf8"))
            tkinter.messagebox.showinfo("Message", "Email was sent successfully!")
        except:
            tkinter.messagebox.showinfo("Error", "This is not a valid email!")
        server.quit()


def containsNumber(string):
    for i in range(len(string)):
        if string[i].isdigit():
            return True
    return False


buildStartGUI()
