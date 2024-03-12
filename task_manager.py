# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

# Function to register a new user
def reg_user():
    '''Add a new user to the user.txt file'''
    # - Request input of a new username
    new_username = input("New Username: ")
    # Check if the username already exists
    if new_username in username_password:
        print("Username already exists. Please choose a different username.")
        return
    # - Request input of a new password
    new_password = input("New Password: ")
    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))
    # - Otherwise you present a relevant message.
    else:
        print("Passwords do not match")

# Function to add a new task
def add_task():
    '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.'''
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

# Function to view all tasks
def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
        '''
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

# Function to view tasks assigned to the current user
def view_mine(curr_user):
    '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
        '''
    print("Your Tasks:")
    # Display tasks with corresponding numbers
    for i, t in enumerate(task_list, 1):
        if t['username'] == curr_user:
            disp_str = f"Task {i}:\n"
            disp_str += f"Title: {t['title']}\n"
            disp_str += f"Assigned to: {t['username']}\n"
            disp_str += f"Date Assigned: {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: {t['description']}\n"
            disp_str += f"Completed: {'Yes' if t['completed'] else 'No'}\n"
            print(disp_str)

    # Allow the user to select a task based on the displayed numbers
    selected_task = input("Enter the number of the task you want to interact with (or enter -1 to go back): ")

    if selected_task.isdigit():
        selected_task_index = int(selected_task) - 1

        if 0 <= selected_task_index < len(task_list) and task_list[selected_task_index]['username'] == curr_user:
            selected_task_info = task_list[selected_task_index]

            # Provide options to the user
            print("\nSelected Task:")
            print(f"Title: {selected_task_info['title']}")
            print(f"Assigned to: {selected_task_info['username']}")
            print(f"Date Assigned: {selected_task_info['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
            print(f"Due Date: {selected_task_info['due_date'].strftime(DATETIME_STRING_FORMAT)}")
            print(f"Task Description: {selected_task_info['description']}")
            print(f"Completed: {'Yes' if selected_task_info['completed'] else 'No'}")

            interaction_choice = input("Choose an action:\n1 - Mark as Complete\n2 - Edit Task\n: ")

            if interaction_choice == '1':
                # Mark the task as complete
                if not selected_task_info['completed']:
                    selected_task_info['completed'] = True
                    print("Task marked as complete.")
                else:
                    print("Task is already marked as complete.")
            elif interaction_choice == '2':
                # Edit the task (if not completed)
                if not selected_task_info['completed']:
                    new_username = input("Enter the new username (or press Enter to keep it unchanged): ")
                    new_due_date = input("Enter the new due date (YYYY-MM-DD) (or press Enter to keep it unchanged): ")

                    # Update task information
                    if new_username:
                        selected_task_info['username'] = new_username
                    if new_due_date:
                        try:
                            selected_task_info['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                        except ValueError:
                            print("Invalid datetime format. Task due date remains unchanged.")
                    print("Task edited successfully.")

                    # Update tasks.txt file
                    with open("tasks.txt", "w") as task_file:
                        task_list_to_write = []
                        for t in task_list:
                            str_attrs = [
                                t['username'],
                                t['title'],
                                t['description'],
                                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                "Yes" if t['completed'] else "No"
                            ]
                            task_list_to_write.append(";".join(str_attrs))
                        task_file.write("\n".join(task_list_to_write))

                else:
                    print("Completed tasks cannot be edited.")
            else:
                print("Invalid choice.")
        else:
            print("Invalid task number or task not assigned to you.")
    elif selected_task == '-1':
        return  # User entered -1 to go back
    else:
        print("Invalid input. Please enter a valid task number or -1 to go back.")

# Function to generate reports
def generate_reports():
    # Task Overview Report
    total_tasks = len(task_list)
    completed_tasks = sum(task['completed'] for task in task_list)
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'].date() < date.today())

    # Calculate percentages
    incomplete_percentage = (uncompleted_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    overdue_percentage = (overdue_tasks / uncompleted_tasks) * 100 if uncompleted_tasks > 0 else 0

    # Write to task_overview.txt
    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write("Task Overview Report\n")
        task_overview_file.write(f"Total tasks: {total_tasks}\n")
        task_overview_file.write(f"Completed tasks: {completed_tasks}\n")
        task_overview_file.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
        task_overview_file.write(f"Overdue tasks: {overdue_tasks}\n")
        task_overview_file.write(f"Percentage of incomplete tasks: {incomplete_percentage:.2f}%\n")
        task_overview_file.write(f"Percentage of overdue tasks: {overdue_percentage:.2f}%\n")

    # User Overview Report
    total_users = len(username_password)
    tasks_assigned_to_users = {user: 0 for user in username_password}

    for task in task_list:
        tasks_assigned_to_users[task['username']] += 1

    # Write to user_overview.txt
    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write("User Overview Report\n")
        user_overview_file.write(f"Total users: {total_users}\n")
        user_overview_file.write(f"Total tasks: {total_tasks}\n")

        for user in tasks_assigned_to_users:
            user_tasks = tasks_assigned_to_users[user]
            user_completed_tasks = sum(1 for task in task_list if task['username'] == user and task['completed'])
            user_uncompleted_tasks = user_tasks - user_completed_tasks
            user_overdue_tasks = sum(1 for task in task_list if task['username'] == user
                                     and not task['completed'] and task['due_date'].date() < date.today())

            # Calculate percentages
            user_percentage = (user_tasks / total_tasks) * 100 if total_tasks > 0 else 0
            user_completed_percentage = (user_completed_tasks / user_tasks) * 100 if user_tasks > 0 else 0
            user_uncompleted_percentage = (user_uncompleted_tasks / user_tasks) * 100 if user_tasks > 0 else 0
            user_overdue_percentage = (user_overdue_tasks / user_tasks) * 100 if user_tasks > 0 else 0

            user_overview_file.write(f"\nUser: {user}\n")
            user_overview_file.write(f"Total tasks assigned: {user_tasks}\n")
            user_overview_file.write(f"Percentage of total tasks: {user_percentage:.2f}%\n")
            user_overview_file.write(f"Percentage of completed tasks: {user_completed_percentage:.2f}%\n")
            user_overview_file.write(f"Percentage of uncompleted tasks: {user_uncompleted_percentage:.2f}%\n")
            user_overview_file.write(f"Percentage of overdue tasks: {user_overdue_percentage:.2f}%\n")

# Function to display statistics
def display_statistics():
    # Check if text files exist; if not, generate reports
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        generate_reports()

    # Display task statistics
    with open("task_overview.txt", "r") as task_stats_file:
        task_stats = task_stats_file.read()
        print("Task Overview Statistics:")
        print(task_stats)

    # Display user statistics
    with open("user_overview.txt", "r") as user_stats_file:
        user_stats = user_stats_file.read()
        print("\nUser Overview Statistics:")
        print(user_stats)

while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()
    
    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine(curr_user)
    
    elif menu == 'gr' and curr_user == 'admin':
        # Generate reports
        generate_reports()
        print("Reports generated successfully.")

    elif menu == 'ds' and curr_user == 'admin':
        # Display statistics
        display_statistics()

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")