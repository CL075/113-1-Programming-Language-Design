class User:
    def __init__(self, name):
        self.name = name
        self.sheets = {}

class Sheet:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.data = [[0 for _ in range(3)] for _ in range(3)]
        self.access_rights = {owner: "Editable"}

    def set_value(self, row, col, expression):
        try:
            value = eval(expression)
            self.data[row][col] = value
        except Exception:
            return "Invalid input."

    def get_value(self, row, col):
        return self.data[row][col]

    def is_editable(self, user):
        return self.access_rights.get(user, "ReadOnly") == "Editable"

    def change_access(self, user, right):
        self.access_rights[user] = right

    def share(self, collaborator):
        self.access_rights[collaborator] = "ReadOnly"

class SheetManager:
    def __init__(self):
        self.users = {}

    def create_user(self, name):
        if name in self.users:
            return f"User {name} already exists."
        self.users[name] = User(name)
        return f"Create a user named \"{name}\"."

    def create_sheet(self, username, sheet_name):
        if username not in self.users:
            return f"User {username} does not exist."
        user = self.users[username]
        if sheet_name in user.sheets:
            return f"Sheet {sheet_name} already exists."
        sheet = Sheet(sheet_name, username)
        user.sheets[sheet_name] = sheet
        return f"Create a sheet named \"{sheet_name}\" for \"{username}\"."

    def check_sheet(self, username, sheet_name):
        if username not in self.users:
            return "User not found."
        user = self.users[username]
        if sheet_name not in user.sheets:
            return "Sheet not found."
        sheet = user.sheets[sheet_name]
        return "\n".join(", ".join(map(str, row)) for row in sheet.data)

    def change_value(self, username, sheet_name, row, col, expression):
        if username not in self.users:
            return "User not found."
        user = self.users[username]
        if sheet_name not in user.sheets:
            return "Sheet not found."
        sheet = user.sheets[sheet_name]
        if not sheet.is_editable(username):
            return "This sheet is not accessible."
        return sheet.set_value(row, col, expression) or "Value updated."

    def change_access(self, username, sheet_name, right):
        if username not in self.users:
            return "User not found."
        user = self.users[username]
        if sheet_name not in user.sheets:
            return "Sheet not found."
        sheet = user.sheets[sheet_name]
        sheet.change_access(username, right)
        return f"Access right updated to {right}."

    def collaborate(self, owner, sheet_name, collaborator):
        if owner not in self.users or collaborator not in self.users:
            return "User not found."
        user = self.users[owner]
        if sheet_name not in user.sheets:
            return "Sheet not found."
        sheet = user.sheets[sheet_name]
        sheet.share(collaborator)
        return f"Share \"{owner}\"'s \"{sheet_name}\" with \"{collaborator}\"."

manager = SheetManager()

def display_menu():
    print("---------------Menu---------------")
    print("1. Create a user")
    print("2. Create a sheet")
    print("3. Check a sheet")
    print("4. Change a value in a sheet")
    print("5. Change a sheet's access right.")
    print("6. Collaborate with another user")
    print("----------------------------------")

while True:
    display_menu()
    choice = input("> ")

    if choice == "1":
        username = input("Enter username: ")
        print(manager.create_user(username))

    elif choice == "2":
        username, sheet_name = input("Enter username and sheet name: ").split()
        print(manager.create_sheet(username, sheet_name))

    elif choice == "3":
        username, sheet_name = input("Enter username and sheet name: ").split()
        print(manager.check_sheet(username, sheet_name))

    elif choice == "4":
        username, sheet_name = input("Enter username and sheet name: ").split()
        print(manager.check_sheet(username, sheet_name))
        row, col, expression = input("Enter row, col, and expression: ").split()
        print(manager.change_value(username, sheet_name, int(row), int(col), expression))

    elif choice == "5":
        username, sheet_name, right = input("Enter username, sheet name, and access right: ").split()
        print(manager.change_access(username, sheet_name, right))

    elif choice == "6":
        owner, sheet_name, collaborator = input("Enter owner, sheet name, and collaborator: ").split()
        print(manager.collaborate(owner, sheet_name, collaborator))

    else:
        print("Invalid choice. Please try again.")
