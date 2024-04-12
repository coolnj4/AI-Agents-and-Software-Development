import socket, threading
from crewai import Crew, Process, Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI
from customtkinter import *
import customtkinter
from tkinter import *
import tkinter
from textwrap import *
import time
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

wrapper = TextWrapper(width=100)

row = 0
server_row = 0
context = ""
sender = "TESTER"
receiver = "MANAGER"
file_name = ""

root = CTk()
root.geometry("1650x500")
root.title("Tester")
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

font = CTkFont(family="Verdana",size=14)


chat_frame = CTkScrollableFrame(master=root,width=1400, height=250)
chat_frame.pack(pady=30)

user_frame = CTkFrame(master=root, width=800, height=1)
user_frame.pack()

chat_frame_2 = CTkScrollableFrame(master=root, width=1400, height=250)
chat_frame_2.pack(pady=30)

user_frame_2 = CTkFrame(master=root, width=800, height=1)
user_frame_2.pack()

client_ip = '127.0.0.1'
client_port = 999
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((client_ip,client_port))
client_socket.send("TESTER".encode())

llm = ChatGoogleGenerativeAI(model="gemini-pro",verbose=True,temperature=0.6,google_api_key=api_key)
tester_agent = Agent(role="Software Tester",goal="Test the code for any errors, generate the corrected code and test cases for it",backstory="You are a code tester who hates incorrect code and love an error free code so you always correct the code", llm=llm, verbose=True, allow_delegation=True, max_rpm=20)

description_entry = CTkEntry(master=user_frame, placeholder_text="Send the code for generating test cases", width=800, border_color='white', text_color='white')
description_entry.grid(row=0, column=1, columnspan=3, padx=20, pady=30, sticky=NE)

chat_entry = CTkEntry(master=user_frame_2, placeholder_text="Ask about your problem", width=1000, border_color='white', text_color='white')
chat_entry.grid(row=0, column=1, columnspan=3, padx=20, pady=30, sticky=NE)


def textboxDimensions(text):
    char_length = []
    
    wrapped_text = wrapper.wrap(text)

    for text in wrapped_text:
        char_length.append(font.measure(text))
                
    text_box_width = max(char_length)
                
    if(text_box_width <= 32):
        text_box_width = 35

    text_box_height = font.metrics("linespace") * len(wrapped_text)

    return (text_box_width, text_box_height)


def responseOnReceivingMessage(content):
    global server_row, font

    char_length = []

    try:
        task = Task(description=content, agent=tester_agent)
        crew = Crew(tasks=[task], agents=[tester_agent], verbose=2, max_rpm=20)
        test_cases = crew.kickoff()

        print(test_cases)
        
        width, height = textboxDimensions(test_cases)

        text_message = CTkTextbox(master=chat_frame_2, width=width, height=height, font=font)
        text_message.insert(index=END, text=test_cases)
        text_message.configure(state="disabled")
        text_message.grid(row=server_row, column=10, columnspan=3, padx=20, pady=30, sticky=NE)

        server_row += 5 + height
    
    except Exception as e:
        print("An error occured",e)

def receiveMessages():
    global server_row, file_name, tester_agent

    while(True):
        try:
            message = client_socket.recv(1024).decode()
            received_message = message.split(":")
            print(message)

            if(len(received_message) == 2):
                sender = received_message[0]
                # receiver = received_message[1]
                message = sender + " : " + received_message[1]
                print(message)

                width, height = textboxDimensions(text=message)

                text_message = CTkTextbox(master=chat_frame_2, width=width, height=height, font=font)
                text_message.insert(index=END, text=message)
                text_message.configure(state="disabled")
                text_message.grid(row=server_row, column=5, columnspan=3, padx=20, pady=30, sticky=NE)

                server_row += 10 + height

            elif(len(received_message) == 3):
                sender = received_message[0]
                # receiver = received_message[1]
                file_name = received_message[1]
                content = received_message[2]
                message = sender + " : " + file_name
                print(message)

                while(True):
                    i = 1
                    try:
                        file = open(file_name,"x")
                        file.writelines(content)
                        file.close()
                        break
                    
                    except FileExistsError as exists_error:
                        file_name = str(i) + "_" + file_name
                        i += 1
                
                width, height = textboxDimensions(text=message)

                text_message = CTkTextbox(master=chat_frame_2, width=width, height=height, font=font)
                text_message.insert(index=END, text=message)
                text_message.configure(state="disabled")
                text_message.grid(row=server_row, column=5, columnspan=3, padx=20, pady=30, sticky=NE)

                server_row += 10 + height

                responseOnReceivingMessage(content)            

            elif(len(received_message) == 4):
                sender = received_message[0]
                # receiver = received_message[1]
                file_name = received_message[1]
                content = received_message[2]
                message = sender + " : " + file_name + " : " + received_message[3]
                print(message)
                
                while(True):
                    i = 1
                    try:
                        file = open(file_name,"x")
                        file.writelines(content)
                        file.close()
                        break
                    
                    except FileExistsError as exists_error:
                        file_name = str(i) + "_" + file_name
                        i += 1

                width, height = textboxDimensions(text=message)

                text_message = CTkTextbox(master=chat_frame_2, width=width, height=height, font=font)
                text_message.insert(index=END, text=message)
                text_message.configure(state="disabled")
                text_message.grid(row=server_row, column=5, columnspan=3, padx=20, pady=30, sticky=NE)

                server_row += 10 + height
                
                responseOnReceivingMessage(content)
        
        except ConnectionResetError as c:
            print(c)            

def response(description):
    global row

    task = Task(description=description, agent=tester_agent)
    crew = Crew(tasks=[task], agents=[tester_agent])
    test_cases = crew.kickoff()

    width, height = textboxDimensions(test_cases)

    response_message = CTkTextbox(master=chat_frame, width=width, height=height)
    response_message.insert(index=END, text=test_cases)
    response_message.configure(state="disabled")
    response_message.grid(row=row, column=5, columnspan=3, padx=20, pady=30, sticky=NE)

    row += 10 + height

    print(test_cases)

def getDescription():
    global server_row, context

    if(context == ""):
        description = description_entry.get()
    else:
        description = context + description_entry.get()
        context = ""

    width, height = textboxDimensions(description)

    text_message = CTkTextbox(master=chat_frame_2, width=width, height=height, font=font)
    text_message.insert(index=END, text=description)
    text_message.configure(state="disabled")
    text_message.grid(row=server_row, column=10, columnspan=3, padx=20, pady=30, sticky=NE)

    server_row += 10 + height

    response(description=description)

def uploadFilesToAssistant():
    global server_row, context, file_name
    file_path = filedialog.askopenfilename()

    
    index = file_path.rindex("/")+1
    file_name = file_path[index:]

    try:
        with open(file_path) as file:
            context = file.read()

        text = "You uploaded a file: ",file_path
        text_message = CTkTextbox(master=chat_frame, height=10)
        text_message.insert(index=END, text=text)
        text_message.configure(state="disabled")
        text_message.grid(row=server_row, column=5, columnspan=3, padx=20, pady=30, sticky=NE)

        server_row += 12
        
        print(context)

    except Exception as e:
        print("An error occurred ",e)

def uploadFilesToServer():
    global row, context, file_name
    file_path = filedialog.askopenfilename()

    
    index = file_path.rindex("/")+1
    file_name = file_path[index:]

    try:
        with open(file_path) as file:
            context = file.read()

        text = "You uploaded a file: ",file_path
        text_message = CTkTextbox(master=chat_frame_2, height=10)
        text_message.insert(index=END, text=text)
        text_message.configure(state="disabled")
        text_message.grid(row=row, column=5, columnspan=3, padx=20, pady=30, sticky=NE)

        row += 12
        
        print(context)

    except Exception as e:
        print("An error occurred ",e)

def sendData():
    global file_name, context, sender, receiver, server_row

    if(file_name != "" and context != ""):
        if(chat_entry.get() != ""):
            message = sender + ":" + receiver + ":" + file_name + ":" + context + ":" + chat_entry.get()
            shown_message = sender + ":" + receiver + ":" + file_name + ":" + chat_entry.get()
        else:
            message = sender + ":" + receiver + ":" + file_name + ":" + context
            shown_message = sender + ":" + receiver + ":" + file_name
            
        client_socket.send(message.encode())

        width , height = textboxDimensions(text=shown_message)
        
        text_message = CTkTextbox(master=chat_frame_2, width=width, height=height, font=font)
        text_message.insert(index=END, text=shown_message)
        text_message.configure(state="disabled")
        text_message.grid(row=server_row, column=5, columnspan=3, padx=20, pady=30, sticky=NE)

        server_row += 12 + height
    
    elif(chat_entry.get() != ""):
        message = sender + ":" + receiver + ":" + chat_entry.get()
        client_socket.send(message.encode())

        width , height = textboxDimensions(text=message)
        
        text_message = CTkTextbox(master=chat_frame_2, width=width, height=height, font=font)
        text_message.insert(index=END, text=message)
        text_message.configure(state="disabled")
        text_message.grid(row=server_row, column=5, columnspan=3, padx=20, pady=30, sticky=NE)

        server_row += 12 + height

    else:
        print("Message cannot be empty !")
    
    file_name = ""
    

upload_button = CTkButton(master=user_frame_2, text="+",command=uploadFilesToServer, width=50, hover=True)
upload_button.grid(row=0, column=8, columnspan=5, padx=20, pady=30, sticky=NE)

send_button = CTkButton(master=user_frame, text="Send",command=getDescription, width=50, hover=True)
send_button.grid(row=0, column=15, columnspan=5, padx=20, pady=30, sticky=NE)

send_button_2 = CTkButton(master=user_frame_2, text="Send",command=sendData, width=50, hover=True)
send_button_2.grid(row=0, column=15, columnspan=5, padx=20, pady=30, sticky=NE)

threading.Thread(target=receiveMessages).start()

root.mainloop()