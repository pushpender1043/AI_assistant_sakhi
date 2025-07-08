from Frontend.GUI import (
    GraphicalUserInterface,
    SetAsssistantStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    SetMicrophoneStatus,
    AnswerModifier,
    QueryModifier,
    GetMicrophoneStatus,
    GetAssistantStatus,
)
from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("Assistantname", "Assistant")

DefaultMessage = f""" {Username}: Hello {Assistantname}, How are you?
{Assistantname}: Welcome {Username}. I am doing well. How may I help you? """

functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]
subprocess_list = []


def ShowDefaultChatIfNoChats():
    try:
        with open(r'Data\ChatLog.json', "r", encoding='utf-8') as file:
            if len(file.read()) < 5:
                with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as temp_file:
                    temp_file.write("")
                with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as response_file:
                    response_file.write(DefaultMessage)
    except FileNotFoundError:
        print("ChatLog.json file not found. Creating default response.")
        os.makedirs("Data", exist_ok=True)
        with open(r'Data\ChatLog.json', "w", encoding='utf-8') as file:
            file.write("[]")
        with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as response_file:
            response_file.write(DefaultMessage)


def ReadChatLogJson():
    try:
        with open(r'Data\ChatLog.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print("ChatLog.json not found.")
        return []


def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"{Username}: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"{Assistantname}: {entry['content']}\n"

    os.makedirs(TempDirectoryPath(''), exist_ok=True)

    with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))


def ShowChatOnGUI():
    try:
        with open(TempDirectoryPath('Database.data'), 'r', encoding='utf-8') as file:
            data = file.read()
        if data:
            with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as response_file:
                response_file.write(data)
    except FileNotFoundError:
        print("Database.data file not found.")


def InitialExecution():
    SetMicrophoneStatus("True")
    SetAsssistantStatus("Available...")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatOnGUI()


def MainExecution():
    try:
        TaskExecution = False
        ImageExecution = False
        ImageGenerationQuery = ""

        SetAsssistantStatus("Listening...")

        try:
            Query = SpeechRecognition()
        except Exception as sr_error:
            print(f"[SpeechRecognition ERROR]: {sr_error}")
            ShowTextToScreen(f"{Assistantname}: I'm having trouble hearing you.")
            TextToSpeech("I'm having trouble hearing you.")
            return

        if not Query or Query.strip() == "":
            ShowTextToScreen(f"{Assistantname}: Sorry, I didn't catch that.")
            TextToSpeech("Sorry, I didn't catch that.")
            return

        ShowTextToScreen(f"{Username}: {Query}")
        SetAsssistantStatus("Thinking...")

        try:
            Decision = FirstLayerDMM(Query)
            if not isinstance(Decision, list):
                raise ValueError("Decision should be a list")
        except Exception as dmm_error:
            print(f"[FirstLayerDMM ERROR]: {dmm_error}")
            ShowTextToScreen(f"{Assistantname}: Sorry, I couldn’t understand that.")
            TextToSpeech("Sorry, I couldn’t understand that.")
            return

        print(f"\nDecision: {Decision}\n")

        G = any(i.startswith("general") for i in Decision)
        R = any(i.startswith("realtime") for i in Decision)

        Merged_query = " and ".join(
            [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
        )

        for queries in Decision:
            if "generate" in queries:
                ImageGenerationQuery = str(queries)
                ImageExecution = True

        for queries in Decision:
            if not TaskExecution and any(queries.startswith(func) for func in functions):
                try:
                    run(Automation(list(Decision)))
                    TaskExecution = True
                except Exception as auto_error:
                    print(f"[Automation ERROR]: {auto_error}")

        if ImageExecution:
            try:
                with open(r'Frontend\Files\ImageGeneration.data', "w") as file:
                    file.write(f"{ImageGenerationQuery},True")
                p1 = subprocess.Popen(
                    ['python', r"Backend\ImageGeneration.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    shell=False,
                )
                subprocess_list.append(p1)
            except Exception as e:
                print(f"[ImageGeneration ERROR]: {e}")

        try:
            if G and R or R:
                SetAsssistantStatus("Searching...")
                Answer = RealtimeSearchEngine(QueryModifier(Merged_query))
            elif G:
                SetAsssistantStatus("Thinking...")
                Answer = ChatBot(QueryModifier(Merged_query))
            else:
                Answer = ChatBot("I'm sorry, I don't understand that.")
        except Exception as reply_error:
            print(f"[ChatBot/RealtimeSearchEngine ERROR]: {reply_error}")
            Answer = "Sorry, I faced a problem while finding the answer."

        ShowTextToScreen(f"{Assistantname}: {Answer}")
        SetAsssistantStatus("Answering...")

        try:
            TextToSpeech(Answer)
        except Exception as tts_error:
            print(f"[TextToSpeech ERROR]: {tts_error}")
            ShowTextToScreen(f"{Assistantname}: (Speaking failed)")

        if any("exit" in i for i in Decision):
            os._exit(1)

    except Exception as e:
        print(f"[MainExecution Global ERROR]: {e}")
        ShowTextToScreen(f"{Assistantname}: Sorry, something went wrong.")
        TextToSpeech("Sorry, something went wrong.")


def FirstThread():
    while True:
        try:
            CurrentStatus = GetMicrophoneStatus()
            print(f"Current Microphone Status: {CurrentStatus}")

            if CurrentStatus.lower() == "true":
                print("Executing MainExecution")
                MainExecution()
            else:
                print("Mic is OFF. Turning ON.")
                SetMicrophoneStatus("True")
                SetAsssistantStatus("Available...")
        except Exception as e:
            print(f"Error in FirstThread: {e}")
            sleep(1)


def SecondThread():
    try:
        GraphicalUserInterface()
    except Exception as e:
        print(f"Error in SecondThread: {e}")


if __name__ == "__main__":
    InitialExecution()
    thread1 = threading.Thread(target=FirstThread, daemon=True)
    thread1.start()
    SecondThread()
