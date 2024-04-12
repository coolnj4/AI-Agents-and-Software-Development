import socket, threading
from crewai import Crew, Process, Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI
import customtkinter
from customtkinter import *
import time 
from textwrap import *
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv("GOOGLE_API_KEY")

root = CTk()
root.geometry("1650x500")
root.title("Manager")
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")
font = CTkFont(family="Verdana",size=14)


context = ""
file_name = ""
sender = "MANAGER"

row = 0
server_row = 0

client_ip = '127.0.0.1'
client_port = 999 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((client_ip,client_port))
client_socket.send("MANAGER".encode())

llm = ChatGoogleGenerativeAI(model="gemini-pro",verbose=True,temperature=0.6,google_api_key=api_key)

chat_frame = CTkScrollableFrame(master=root,width=1400, height=250)
chat_frame.pack(pady=30)
chat_frame.grid_columnconfigure(0, weight=1)

user_frame = CTkFrame(master=root, width=800, height=1)
user_frame.pack()

chat_frame_2 = CTkScrollableFrame(master=root, width=1400, height=250)
chat_frame_2.pack(pady=30)

user_frame_2 = CTkFrame(master=root, width=800, height=1)
user_frame_2.pack()

description_entry = CTkEntry(master=user_frame, placeholder_text="Tell me about the project and let me explain you", width=800, border_color='white', text_color='white')
description_entry.grid(row=0, column=1, columnspan=3, padx=20, pady=30, sticky=NE)

chat_entry = CTkEntry(master=user_frame_2, placeholder_text="Ask about your problem", width=600, border_color='white', text_color='white')
chat_entry.grid(row=0, column=1, columnspan=3, padx=20, pady=30, sticky=NE)

def textboxDimensions(text):
    wrapper = TextWrapper(width = 100)
    char_length = []
    
    wrapped_text = wrapper.wrap(text)

    for text in wrapped_text:
        char_length.append(font.measure(text))
                
    text_box_width = max(char_length) + 50
                
    if(text_box_width <= 32):
        text_box_width = 35
    
    print("text_box_width :",text_box_width)

    text_box_height = font.metrics("linespace") * len(wrapped_text)

    width, height = (text_box_width, text_box_height)

    return width, height

def response(description):
    global row
    # char_length = []

    manager = Agent(role="Manager", max_rpm=20, goal="explain the project create plan for the software projects, suggest ideas on how the project should be executed in the most effecient way and in the minimum time", backstory="You are a manager of a software developer department and you are the best at explaning a project to others managing work and delegating work among your teammates based on their skills", allow_delegation=False, llm=llm)
    manager_task = Task(description=description, agent=manager)

    try:
        crew = Crew(tasks=[manager_task], agents=[manager], max_rpm=20)
        result = crew.kickoff()
                    
        width, height = textboxDimensions(text=result)
                
        response_message = CTkTextbox(master=chat_frame, width=width, height=height, font=font)
        response_message.insert(index=END, text=result)
        response_message.configure(state="disabled")
        response_message.grid(row=row, column=0, columnspan=3, padx=20, pady=30, sticky=NSEW)

        row += 12 + height

        print(result)
    
    except Exception as e:
        print("An error occured",e)

def getDescription():
    global row, context

    if(context == ""):
        description = description_entry.get()
    
    else:
        description = context + description_entry.get()
        context = ""
    
    width, height = textboxDimensions(text=description)
    
    text_message = CTkTextbox(master=chat_frame, width=width, height=+50, font=font)
    text_message.insert(index=END, text=description)
    text_message.configure(state="disabled")
    text_message.grid(row=row, column=0, columnspan=3, padx=20, pady=30, sticky=NSEW)
    

    row += 12 + height
    

    print("Description: \n",description)


    response(description)

def sendDataToTester():
    global file_name, context, sender, server_row

    receiver = "TESTER"

    if(file_name != "" and context != ""):
        if(chat_entry.get() != ""):
            message = sender + ":" + receiver + ":" + file_name + ":" + context + ":" + chat_entry.get()
            shown_message = sender + ":" + receiver + ":" + file_name + ":" + chat_entry.get()
        else:
            message = sender + ":" + receiver + ":" + file_name + ":" + context
            shown_message = sender + ":" + receiver + ":" + file_name
            
        client_socket.send(message.encode())

        width, height = textboxDimensions(text=message)
        
        text_message = CTkTextbox(master=chat_frame_2, width=width, height=+50, font=font)
        text_message.insert(index=END, text=shown_message)
        text_message.configure(state="disabled")
        text_message.grid(row=server_row, column=5, columnspan=3, padx=20, pady=30, sticky=NE)

        server_row += 12 + height
    
    elif(chat_entry.get() != ""):
        message = sender + ":" + receiver + ":" + chat_entry.get()

        client_socket.send(message.encode())

        width, height = textboxDimensions(text=message)
        
        text_message = CTkTextbox(master=chat_frame_2, width=width, height=height, font=font)
        text_message.insert(index=END, text=message)
        text_message.configure(state="disabled")
        text_message.grid(row=server_row, column=5, columnspan=3, padx=20, pady=30, sticky=NE)

        server_row += 12 + height

    else:
        print("Message cannot be empty !")

    context = ""
    file_name = ""

def sendDataToDeveloper():
    print("sending to dev")
    global file_name, context, sender, server_row

    receiver = "DEVELOPER"

    if(file_name != "" and context != ""):
        if(chat_entry.get() != ""):
            message = sender + ":" + receiver + ":" + file_name + ":" + context + ":" + chat_entry.get()
            shown_message = sender + ":" + receiver + ":" + file_name + ":" + chat_entry.get()
        else:
            message = sender + ":" + receiver + ":" + file_name + ":" + context
            shown_message = sender + ":" + receiver + ":" + file_name
            
        client_socket.send(message.encode())

        print("lol")

        width, height = textboxDimensions(message)

        
        text_message = CTkTextbox(master=chat_frame_2, width=width, height=height+50, font=font, activate_scrollbars=False)
        text_message.insert(index=END, text=shown_message)
        text_message.configure(state="disabled")
        text_message.grid(row=server_row, column=5, columnspan=3, padx=20, pady=30, sticky=NE)

        server_row += 12 + height
    
    elif(chat_entry.get() != ""):
        message = sender + ":" + receiver + ":" + chat_entry.get()

        client_socket.send(message.encode())

        width, height = textboxDimensions(text=message)
        
        text_message = CTkTextbox(master=chat_frame_2, width=width, height=height, font=font, activate_scrollbars=False)
        text_message.insert(index=END, text=message)
        text_message.configure(state="disabled")
        text_message.grid(row=server_row, column=5, columnspan=3, padx=20, pady=30, sticky=NE)

        server_row += 12 + height

    else:
        print("Message cannot be empty !")

    context = ""
    file_name = ""

def sendFileToAssistant():
    global row, context
    file_path = filedialog.askopenfilename()

    try:
        with open(file_path) as file:
            context = file.read()

        text = "You uploaded a file: ",file_path
        
        # width, height = textboxDimensions(text=text)

        text_message = CTkTextbox(master=chat_frame, height=10, font=font)
        text_message.insert(index=END, text=text)
        text_message.configure(state="disabled")
        text_message.grid(row=row, column=5, columnspan=3, padx=20, pady=30, sticky=NE)

        row += 12
        
        print(context)

    except Exception as e:
        print("An error occurred ",e)

def sendFileToServer():
    global server_row, context, file_name
    file_path = filedialog.askopenfilename()

    
    index = file_path.rindex("/")+1
    file_name = file_path[index:]
    
    try:
        with open(file_path) as file:
            context = file.read()

        text = "You uploaded a file: " + file_path

        # texbox_dimensions = textboxDimensions(text=text)

        text_message = CTkTextbox(master=chat_frame_2, height=10, font=font)
        text_message.insert(index=END, text=text)
        text_message.configure(state="disabled")
        text_message.grid(row=server_row, column=5, columnspan=3, padx=20, pady=30, sticky=NE)

        # sendFile(file_path, context)

        server_row += 12 
        
        print(context)
        
    except Exception as e:
        print("An error occurred ",e)

def receiveMessages():
    global server_row
    print("Receiving messages")
    while(True):
        try:
            message = client_socket.recv(1024).decode()
            received_message = message.split(":")

            if(len(received_message) == 2):
                sender = received_message[0]
                # receiver = received_message[1]
                message = sender + " : " + received_message[1]
                print(message)

                width, height = textboxDimensions(text=message)

                text_message = CTkTextbox(master=chat_frame_2, width=width,  height=height, font=font)
                text_message.insert(index=END, text=message)
                text_message.configure(state="disabled")
                text_message.grid(row=server_row, column=50, columnspan=3, padx=20, pady=30, sticky=NE)

                server_row += 12 + height

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
                        print("file saved")
                        break
                    
                    except FileExistsError as exists_error:
                        file_name = str(i) + "_" + file_name
                        i += 1
                
                width, height = textboxDimensions(text=message)

                text_message = CTkTextbox(master=chat_frame_2, width=width, height=height, font=font)
                text_message.insert(index=END, text=message)
                text_message.configure(state="disabled")
                text_message.grid(row=server_row, column=50, columnspan=3, padx=20, pady=30, sticky=NE)

                server_row += 12 + height

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
                        print("file saved")
                        break
                    
                    except FileExistsError as exists_error:
                        file_name = str(i) + "_" + file_name
                        i += 1
                
                width, height = textboxDimensions(text=message)

                text_message = CTkTextbox(master=chat_frame_2, width=width, height=height, font=font)
                text_message.insert(index=END, text=message)
                text_message.configure(state="disabled")
                text_message.grid(row=server_row, column=50, columnspan=3, padx=20, pady=30, sticky=NE)

                server_row += 12 + height
        
        except ConnectionResetError as c:
            print(c)

upload_button_up = CTkButton(master=user_frame, text="Send Files",command=sendFileToAssistant, width=50, hover=True)
upload_button_up.grid(row=0, column=8, columnspan=5, padx=20, pady=30, sticky=NE)

send_button = CTkButton(master=user_frame, text="Send",command=getDescription, width=50, hover=True)
send_button.grid(row=0, column=15, columnspan=5, padx=20, pady=30, sticky=NE)

upload_button_down = CTkButton(master=user_frame_2, text="Share Files",command=sendFileToServer, width=50, hover=True)
upload_button_down.grid(row=0, column=8, columnspan=5, padx=20, pady=30, sticky=NE)

send_to_tester_button = CTkButton(master=user_frame_2, text="Send to Tester",command=sendDataToTester, width=50, hover=True)
send_to_tester_button.grid(row=0, column=15, columnspan=5, padx=20, pady=30, sticky=NE)

send_to_developer_button = CTkButton(master=user_frame_2, text="Send to Developer",command=sendDataToDeveloper, width=50, hover=True)
send_to_developer_button.grid(row=0, column=20, columnspan=5, padx=20, pady=30, sticky=NE)

threading.Thread(target=receiveMessages).start()

root.mainloop()