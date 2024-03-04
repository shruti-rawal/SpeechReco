# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import distutils
import speech_recognition as sr


def main():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Please Say Something.....")

        audio = r.listen(source)

        try:
            print("You have Said : \n " + r.recognize_google(audio))

        except Exception as e:
            print ("Errpr :" + str(e))


main()

