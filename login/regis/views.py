import distutils
import langid
from googletrans import Translator
from django.contrib import messages
import speech_recognition as sr
from django.shortcuts import render,redirect
from django.http import HttpResponse
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import io,os
import pyttsx3
import pygame
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    return render(request,"login/home.html")

# def log(request):
#     # Your logic to retrieve or authenticate the user
#     user = request.user  # Assuming user is authenticated or retrieved
#     return render(request,"login/login.html", {'user': user})
# # views.py

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def log(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page
                return redirect("login/home")
    else:
        form = AuthenticationForm()
    return render(request, 'login/login.html', {'form': form})



# def signup(request):
    # user = request.user  # Assuming user is authenticated or retrieved
    # return render(request,"login/reg.html")
class UserRegistrtionForm(UserCreationForm):
    class meta:
        model = User
        fields = ['username','email','password1','password2']
def signup(request):
    if request.method == 'POST':
        form = UserRegistrtionForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Account Created For {username} !! ")
            return redirect("login/login")
            
    else:
        form=UserRegistrtionForm()
    context={
        'form':form
        }
    return render(request,"login/reg.html",context)


def speech_reco(request):
    # Your logic to retrieve or authenticate the user
    user = request.user  # Assuming user is authenticated or retrieved
    return render(request,"login/login.html", {'user': user})
    # if request.method == 'POST':
    #     r = sr.Recognizer()
    #     with sr.Microphone() as source:
    #         r.adjust_for_ambient_noise(source)
    #         print("Please Say Something.....")
    #         audio = r.listen(source)
    #         try:
    #             recognized_text = r.recognize_google(audio)
    #             return render(request, 'login/result.html', {'recognized_text': recognized_text})
    #         except Exception as e:
    #             print("Error: " + str(e))
    #             return HttpResponse("Error occurred during speech recognition.")

    # return render(request, 'login/speech_form.html')



def tra(request):
    language_names = {
        'af': 'Afrikaans',
        'ar': 'Arabic',
        'bg': 'Bulgarian',
        'bn': 'Bengali',
        'ca': 'Catalan',
        'cs': 'Czech',
        'cy': 'Welsh',
        'da': 'Danish',
        'de': 'German',
        'el': 'Greek',
        'en': 'English',
        'es': 'Spanish',
        'et': 'Estonian',
        'fa': 'Persian',
        'fi': 'Finnish',
        'fr': 'French',
        'gu': 'Gujarati',
        'he': 'Hebrew',
        'hi': 'Hindi',
        'hr': 'Croatian',
        'hu': 'Hungarian',
        'id': 'Indonesian',
        'it': 'Italian',
        'ja': 'Japanese',
        'kn': 'Kannada',
        'ko': 'Korean',
        'lt': 'Lithuanian',
        'lv': 'Latvian',
        'mk': 'Macedonian',
        'ml': 'Malayalam',
        'mr': 'Marathi',
        'ne': 'Nepali',
        'nl': 'Dutch',
        'no': 'Norwegian',
        'pa': 'Punjabi',
        'pl': 'Polish',
        'pt': 'Portuguese',
        'ro': 'Romanian',
        'ru': 'Russian',
        'sk': 'Slovak',
        'sl': 'Slovenian',
        'so': 'Somali',
        'sq': 'Albanian',
        'sv': 'Swedish',
        'sw': 'Swahili',
        'ta': 'Tamil',
        'te': 'Telugu',
        'th': 'Thai',
        'tl': 'Tagalog',
        'tr': 'Turkish',
        'uk': 'Ukrainian',
        'ur': 'Urdu',
        'vi': 'Vietnamese',
        'zh-cn': 'Chinese (Simplified)',
        'zh-tw': 'Chinese (Traditional)'
    }
    if request.method == 'POST' :
        r = sr.Recognizer()
        
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Please Say Something.....")

            audio = r.listen(source)

            try:
                recognized_text = r.recognize_google(audio)
                # recognized_text="હાય મારું નામ અને હું  છું."
                # recognized_text = request.POST.get('input-text', '')
                lang=request.POST.get('target-language','en')
                lang_tak=request.POST.get('source-language','en')
                lang_code,_ = langid.classify(recognized_text)
                lang_translation = translator.translate(recognized_text, src=lang_code, dest=lang_tak).text
                recognized_text_new=lang_translation                
                # return HttpResponse(f"Selected language: {lang}")
                # Detect the language of the recognized text
                # Map the language code to the language name in English
                language_name = language_names.get(lang_code,'unknown')
                translator = Translator()
                english_translation = translator.translate(recognized_text_new, src=lang_code, dest=lang).text
                tts = gTTS(text=english_translation, lang=lang, slow=False)
                audio_bytes = io.BytesIO()
                tts.write_to_fp(audio_bytes)

                # Reset the file pointer to the beginning
                audio_bytes.seek(0)

                # Initialize Pygame mixer
                pygame.mixer.init()
                pygame.mixer.music.load(audio_bytes)
                pygame.mixer.music.play()

                # Wait for the audio to finish playing
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                return render(request, 'login/home.html', {'recognized_text': lang_tak, 'language_name': language_name,'english_translation':english_translation})
            except Exception as e:
                print("Error: " + str(e))
                return HttpResponse("Error occurred during speech recognition.")

    return render(request, 'login/home.html')


