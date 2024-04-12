# **AI Assisted Software Development using AI Agents**
**This project is just a Proof of Concept not for production use**

## **Overview**
This project is developed to assist software developers in developing the softwares especially the coding part where several AI Agents are employed as the assitant for the user to perform the task as per the instructions sent by their user. These AI Agents are able to understand the task, breakdown the task into subtasks & asign the subtasks to the the AI Agents which are employed under the primary AI Agent.

### **Advantages of Our Approach**
Major problem with LLM is that they hallucinate a lot on a large complex task. So our approach solves this by making multiple instances of an LLM in the form of AI Agents which have their own memory & their own tools & which are specialised for their own specific tasks. These agents will work together to solve the large complex problem same as we work in a real office environment by considering the positive & negative points for each approach/solution & making an informed decision to solve the specific problem.

**This helps in providing the capability of reasoning to the LLMs**

## **Modules**

The project has 3 primary AI Agents in 3 different modules
1. Manager - The one who tends to understand the task & make a plan out of it
2. Developer - The one who has the ability to develop the code as per the instructions given by the user
3. Tester - The one who can generate test cases corresponding to the code sent by the user

Server - A server is also created to allow the user of these 3 agents to communicate with another agent's user for now only manager can communicate with both tester & developer & developer can communicate with manager so that manager always know what is happening in the development.





## **Installation**
1. Clone this git repository `git clone <url of the repository>`
2. Create a virtual environment in the directory where the repository is cloned by using this command
    ```
    python -m venv my_env
    ```
3. Activate the envrionemt by moving into the **my_env** forlder then go into **Scripts** then double click on **activate**
4. Now in the command prompt run command
    ```
    pip install -r requirements.txt
    ```
5. Create a file in the same directory with name **.env**
    ```
    GOOGLE_API_KEY = "your api key" //google's gemini api key
    ```
6. Run the **server.py**
7. Now run the other files & ask the questions related to goal of the AI Agent




