import database
import json
import random
import getpass
from os import system, name
from time import sleep

user = []
connection = database.connect()
database.create_user_table(connection)

def play():
    clear()
    print("\n==========QUIZ START==========\n\n")
    score = 0
    user_name = input("\nEnter your USER NAME: ")
    with open("data_file/questions.json", 'r+') as file:
        dic_questions = json.load(file)
        for i in range(10):
            no_of_questions = len(dic_questions)
            choice = random.randint(0, no_of_questions-1)
            print('Q' + str(i+1) + ' :' +
                dic_questions[choice]["question"] + '\n')

            for option in dic_questions[choice]["options"]:
                print(option)
            answer = input("\nEnter your answer: ")
            if dic_questions[choice]["answer"][0] == answer[0].upper():
                print("\nYou are correct")
                score += 1
                sleep(1)
                clear()
            else:
                print("\nYou are incorrect")
                sleep(1)
                clear()
            del dic_questions[choice]
        print('\nFINAL SCORE:  ' + str(score) + '/10\n')
        print('\nSuccess Rate: ' + str((score/10)*100) + '%')
        database.insert_user(connection, user_name, score)


def viewScore():
    clear()
    name = input("\nEnter your user name to get your score\n\n")
    user = database.get_user_by_name(connection, name)
    for i in user:
        print(f"Your current score is {i[2]}")
    print("\n\n--------- SCORE BOARD ------------\n")
    scoreboard = database.get_all_user(connection)
    for i in scoreboard:
        print(f"| {i[0]}     |  {i[1].ljust(10)} |     {i[2]} |")



def quizQuestions():
    clear()
    if len(user) == 0:
        print("You must first login before adding questions.")
    elif len(user) == 2:
        if user[1] == "ADMIN":
            print('\n==========ADD QUESTIONS==========\n')
            question = input("Enter the question that you want to add:\n")
            options = []
            print("Enter the 4 options with character initials (A, B, C, D)")
            for _ in range(4):
                options.append(input())
            answer = input("Enter the answer:\n")
            with open("data_file/questions.json", 'r+') as file:
                dic_questions = json.load(file)
                dic = {"question": question,
                       "options": options, "answer": answer}
                dic_questions.append(dic)
                file.seek(0)
                json.dump(dic_questions, file)
                file.truncate()
                print("Question successfully added.")
        else:
            print(
                "Only admins are allowed to add questions.")


def createAccount():
    clear()
    print("\n==========CREATE ACCOUNT==========")
    username = input("Enter your USERNAME: ")
    password = getpass.getpass(prompt='Enter your PASSWORD: ')
    with open('data_file/user_accounts.json', 'r+') as user_accounts:
        users = json.load(user_accounts)
        if username in users.keys():
            print(
                "Username already already exists!\nTry loggin in or use a different username.")
        else:
            users[username] = [password, "CANDIDATE"]
            user_accounts.seek(0)
            json.dump(users, user_accounts)
            user_accounts.truncate()
            print("Account created successfully!")


def loginAccount():
    clear()
    print('\n==========LOGIN PANEL==========')
    username = input("USERNAME: ")
    password = getpass.getpass(prompt='PASSWORD: ')
    with open('data_file/user_accounts.json', 'r') as user_accounts:
        users = json.load(user_accounts)
    if username not in users.keys():
        print("Account doesn't exist.\nPlease create an account first.")
    elif username in users.keys():
        if users[username][0] != password:
            print(
                "Incorrect Password.\nPlease enter the correct password and try again.")
        elif users[username][0] == password:
            print("Login Successful.\n")
            user.append(username)
            user.append(users[username][1])


def logout():
    clear()
    global user
    if len(user) == 0:
        print("Already logged out.")
    else:
        user = []
        print("You have been logged out successfully.")


def rules():
    clear()
    print('''\n==========RULES==========

        1. Each round consists of 10 random questions. To answer, you must press A/B/C/D (case-insensitive).
           Your final score will be given at the end.

        2. Each question consists of 1 point. There's no negative point for wrong answers.

        3. You can create an account from ACCOUNT CREATION panel.

        4. You can login using the LOGIN PANEL to add more questions if you are an admin.
	    ''')


def about():
    clear()
    print('''\n==========ABOUT US==========
        This project has been created by:
        TUSHAR SANGLE
        GULAM TAHA YASEEN
        ISHAN RAJ''')


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


if __name__ == "__main__":
    choice = 1
    clear()
    while True:
        print("\n\nPress ENTER to continue...")
        input()
        sleep(1)
        clear()
        MENU_PROMPT = """----------WELCOME TO QUIZ MASTER------------'
        
        Please chose one of the options :
        1. LOGIN PANEL
        2. CREATE AN ACCOUNT
        3. SEE INSTRUCTIONS ON HOW TO PLAY THE GAME
        4. PLAY QUIZ
        5. ADD QUIZ QUESTIONS
        6. VIEW SCOREBOARD
        7. LOGOUT PANEL
        8. ABOUT US
        9. EXIT
        
        ENTER YOUR CHOICE: """
        
        choice = int(input(MENU_PROMPT))

        if choice == 1:
            loginAccount()
        elif choice == 2:
            createAccount()
        elif choice == 3:
            rules()
        elif choice == 4:
            play()
        elif choice == 5:
            quizQuestions()
        elif choice == 6:
            viewScore()
        elif choice == 7:
            logout()
        elif choice == 8:
            about()
        elif choice == 9:
            break
        else:
            print('WRONG INPUT: Enter the choice again')

        if choice == 9:
            break
