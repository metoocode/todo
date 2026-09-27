# ============================================================
# ULTRA JARVIS AI AGENT
# Self Learning Desktop AI Assistant
# ============================================================

# FEATURES
# ------------------------------------------------------------
# ✅ Gemini AI Brain
# ✅ Voice Assistant
# ✅ Self Learning Memory
# ✅ Workflow Recording
# ✅ Workflow Replay
# ✅ Hand Gesture Mouse
# ✅ WhatsApp Automation
# ✅ AI Reply Suggestions
# ✅ File Search
# ✅ Smart Screen Reading
# ✅ OCR
# ✅ Screenshot Analysis
# ✅ AI Desktop Control
# ✅ Action Memory
# ✅ Task Automation
# ============================================================

import os
import cv2
import json
import time
import math
import queue
import psutil
import threading
import webbrowser
import pyautogui
import numpy as np
import mediapipe as mp
import speech_recognition as sr
import pyttsx3
import pytesseract
import pywhatkit
import google.generativeai as genai

from pynput import mouse, keyboard

# ============================================================
# GEMINI SETUP
# ============================================================

API_KEY = "AIzaSyCWtODJPgH0oGpygC0K80r9Z0ZnLcYzMSQ"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

chat = model.start_chat(history=[])
# ============================================================
# TEXT TO SPEECH
# ============================================================

engine = pyttsx3.init()

engine.setProperty("rate", 180)

def speak(text):

    print(f"\nJARVIS: {text}\n")

    engine.say(text)

    engine.runAndWait()

# ============================================================
# SPEECH RECOGNITION
# ============================================================

recognizer = sr.Recognizer()

def listen():

    with sr.Microphone() as source:

        print("Listening...")

        recognizer.adjust_for_ambient_noise(source)

        audio = recognizer.listen(source)

        try:

            query = recognizer.recognize_google(audio)

            print(f"You: {query}")

            return query.lower()

        except:#123434

            return ""

# ============================================================
# GEMINI AI
# ============================================================

def ask_ai(prompt):

    try:

        response = chat.send_message(prompt)

        return response.text

    except Exception as e:

        return str(e)

# ============================================================
# MEMORY SYSTEM
# ============================================================

MEMORY_FILE = "jarvis_memory.json"

if not os.path.exists(MEMORY_FILE):

    with open(MEMORY_FILE, "w") as f:

        json.dump([], f)

def save_memory(task, steps):

    with open(MEMORY_FILE, "r") as f:

        data = json.load(f)

    data.append({
        "task": task,
        "steps": steps
    })

    with open(MEMORY_FILE, "w") as f:

        json.dump(data, f, indent=4)

def load_memory():

    with open(MEMORY_FILE, "r") as f:

        return json.load(f)

# ============================================================
# WORKFLOW RECORDING
# ============================================================

recording = False

actions = []

def on_click(x, y, button, pressed):

    global actions

    if recording and pressed:

        actions.append({
            "type": "click",
            "x": x,
            "y": y
        })

def on_press(key):

    global actions

    if recording:

        try:

            actions.append({
                "type": "key",
                "key": key.char
            })

        except:

            pass

mouse_listener = mouse.Listener(on_click=on_click)

keyboard_listener = keyboard.Listener(on_press=on_press)

mouse_listener.start()

keyboard_listener.start()

# ============================================================
# RECORD TASK
# ============================================================

def record_task():

    global recording, actions

    actions = []

    speak("Tell task name")

    task_name = listen()

    speak("Recording started")

    recording = True

    time.sleep(15)

    recording = False

    save_memory(task_name, actions)

    speak("Task learned successfully")

# ============================================================
# REPLAY TASK
# ============================================================

def replay_task(task_name):

    memories = load_memory()

    for memory in memories:

        if task_name in memory["task"]:

            speak("Executing learned workflow")

            for step in memory["steps"]:

                if step["type"] == "click":

                    pyautogui.click(step["x"], step["y"])

                    time.sleep(0.5)

                elif step["type"] == "key":

                    pyautogui.write(step["key"])

                    time.sleep(0.1)

            return

    speak("Task not found")

# ============================================================
# OPEN APPS
# ============================================================

def open_app(app):

    apps = {

        "chrome": "start chrome",
        "vscode": "code",
        "notepad": "notepad",
        "calculator": "calc",
        "paint": "mspaint",
    }

    if app in apps:

        os.system(apps[app])

        speak(f"Opening {app}")

# ============================================================
# WHATSAPP
# ============================================================

def open_whatsapp():

    webbrowser.open("https://web.whatsapp.com")

    speak("Opening WhatsApp")

def send_message():

    speak("Tell number with country code")

    number = listen()

    speak("Tell message")

    message = listen()

    pywhatkit.sendwhatmsg_instantly(
        number,
        message,
        wait_time=10,
        tab_close=True
    )

    speak("Message sent")

# ============================================================
# AI REPLY
# ============================================================

def suggest_reply():

    speak("Speak received message")

    msg = listen()

    prompt = f"""
    Suggest short smart WhatsApp replies:
    {msg}
    """

    response = ask_ai(prompt)

    print(response)

    speak(response[:500])

# ============================================================
# OCR SCREEN READER
# ============================================================

def read_screen():

    screenshot = pyautogui.screenshot()

    screenshot.save("screen.png")

    img = cv2.imread("screen.png")

    text = pytesseract.image_to_string(img)

    print(text)

    speak(text[:500])

# ============================================================
# AI SCREEN ANALYSIS
# ============================================================

def analyze_screen():

    screenshot = pyautogui.screenshot()

    screenshot.save("analysis.png")

    img = cv2.imread("analysis.png")

    text = pytesseract.image_to_string(img)

    response = ask_ai(
        f"Analyze this screen:\n{text}"
    )

    print(response)

    speak(response[:500])

# ============================================================
# FILE SEARCH
# ============================================================

def search_file(filename):

    for root, dirs, files in os.walk("C:/"):

        for file in files:

            if filename.lower() in file.lower():

                path = os.path.join(root, file)

                os.startfile(path)

                speak("File found")

                return

    speak("File not found")

# ============================================================
# SYSTEM STATUS
# ============================================================

def system_status():

    cpu = psutil.cpu_percent()

    ram = psutil.virtual_memory().percent

    status = f"""
    CPU usage {cpu} percent.
    RAM usage {ram} percent.
    """

    print(status)

    speak(status)

# ============================================================
# HAND TRACKING
# ============================================================

mp_hands = mp.solutions.hands

mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.85,
    min_tracking_confidence=0.85
)

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

screen_width, screen_height = pyautogui.size()

prev_x, prev_y = 0, 0

SMOOTHENING = 5

FRAME_MARGIN = 120

# ============================================================
# LANDMARKS
# ============================================================

INDEX_TIP = mp_hands.HandLandmark.INDEX_FINGER_TIP

THUMB_TIP = mp_hands.HandLandmark.THUMB_TIP

# ============================================================
# MAIN SYSTEM
# ============================================================

speak("Ultra Jarvis AI Agent Activated")

# ============================================================
# MAIN LOOP
# ============================================================

while True:

    # ========================================================
    # CAMERA
    # ========================================================

    success, frame = cap.read()

    frame = cv2.flip(frame, 1)

    h, w, c = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            lm = hand_landmarks.landmark

            index_x = int(lm[INDEX_TIP].x * w)

            index_y = int(lm[INDEX_TIP].y * h)

            thumb_x = int(lm[THUMB_TIP].x * w)

            thumb_y = int(lm[THUMB_TIP].y * h)

            # =================================================
            # SMOOTH CURSOR
            # =================================================

            mapped_x = np.interp(
                index_x,
                (FRAME_MARGIN, w - FRAME_MARGIN),
                (0, screen_width)
            )

            mapped_y = np.interp(
                index_y,
                (FRAME_MARGIN, h - FRAME_MARGIN),
                (0, screen_height)
            )

            alpha = 0.2

            curr_x = alpha * mapped_x + (
                1 - alpha
            ) * prev_x

            curr_y = alpha * mapped_y + (
                1 - alpha
            ) * prev_y

            pyautogui.moveTo(curr_x, curr_y)

            prev_x, prev_y = curr_x, curr_y

            # =================================================
            # CLICK
            # =================================================

            dist = math.hypot(
                thumb_x - index_x,
                thumb_y - index_y
            )

            if dist < 25:

                pyautogui.click()

                cv2.circle(
                    frame,
                    (index_x, index_y),
                    15,
                    (0, 255, 0),
                    -1
                )

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    # ========================================================
    # UI
    # ========================================================

    cv2.putText(
        frame,
        "ULTRA JARVIS AI AGENT",
        (120, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    cv2.imshow("JARVIS AI", frame)

    # ========================================================
    # VOICE COMMANDS
    # ========================================================

    query = listen()

    # ========================================================
    # EXIT
    # ========================================================

    if "exit" in query:

        speak("Shutting down")

        break

    # ========================================================
    # LEARN TASK
    # ========================================================

    elif "learn task" in query:

        record_task()

    # ========================================================
    # RUN TASK
    # ========================================================

    elif "run task" in query:

        speak("Tell task name")

        task = listen()

        replay_task(task)

    # ========================================================
    # APPS
    # ========================================================

    elif "open chrome" in query:

        open_app("chrome")

    elif "open vscode" in query:

        open_app("vscode")

    elif "open calculator" in query:

        open_app("calculator")

    # ========================================================
    # WHATSAPP
    # ========================================================

    elif "open whatsapp" in query:

        open_whatsapp()

    elif "send message" in query:

        send_message()

    elif "suggest reply" in query:

        suggest_reply()

    # ========================================================
    # SCREEN AI
    # ========================================================

    elif "read screen" in query:

        read_screen()

    elif "analyze screen" in query:

        analyze_screen()

    # ========================================================
    # FILE SEARCH
    # ========================================================

    elif "find file" in query:

        speak("Tell filename")

        filename = listen()

        search_file(filename)

    # ========================================================
    # SYSTEM
    # ========================================================

    elif "system status" in query:

        system_status()

    # ========================================================
    # AI CHAT
    # ========================================================

    else:

        response = ask_ai(query)

        print(response)

        speak(response[:500])

    if cv2.waitKey(1) & 0xFF == ord('q'):

        break

# ============================================================
# CLEANUP
# ============================================================

cap.release()

cv2.destroyAllWindows()
"""
import json
import os
import google.generativeai as genai

# Configuration
DATA_FILE = "chatbot_memory.json"
GEMINI_API_KEY = "AIzaSyCDuvACNj6_YRe-Y4Z1i4jeicy7rX4I1Sse"  # Replace with your Gemini API key

# Initialize Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')  # Use the Gemini Pro model

# Load previous memory
if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r") as file:
            memory = json.load(file)
    except json.JSONDecodeError:
        memory = {}
else:
    memory = {}

def chatbot_response(user_input):
    
    user_input = user_input.lower()

    if user_input in memory:
        return memory[user_input]  # Return stored answer
    
    return None  # Return None if the chatbot doesn't know the answer

def learn_from_chat(user_input, response):
    
    user_input = user_input.lower()
    memory[user_input] = response  # Store Gemini's response

    try:
        with open(DATA_FILE, "w") as file:
            json.dump(memory, file, indent=4)  # Save memory
    except IOError as e:
        print(f"Error saving memory: {e}")

def fetch_from_gemini(user_input):
    
    try:
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        return f"Error fetching response from Gemini: {e}"

def clear_memory():
    
    global memory
    memory = {}
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(memory, file, indent=4)
        print("Memory cleared successfully.")
    except IOError as e:
        print(f"Error clearing memory: {e}")

print("Chatbot is ready! Type 'exit' to stop or 'clear memory' to reset the chatbot's memory.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    elif user_input.lower() == "clear memory":
        clear_memory()
        continue

    # Check if chatbot knows the answer
    response = chatbot_response(user_input)
    if response:
        print("Bot:", response)
    else:
        # If chatbot doesn't know, ask Gemini for an answer
        print("Bot: I don't know that yet. Let me ask Gemini...")
        gemini_response = fetch_from_gemini(user_input)
        learn_from_chat(user_input, gemini_response)
        print("Bot (from Gemini):", gemini_response)"""