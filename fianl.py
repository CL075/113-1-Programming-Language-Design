import json
import os

DATA_FILE = "data.txt"

class User:
    def __init__(self, name):
        self.name = name
        self.sheets = {}

class Sheet:
    def __init__(self, name, owner, rows=3, cols=3):
        self.name = name
        self.owner = owner
        self.data = [[0 for _ in range(cols)] for _ in range(rows)]
        self.access_rights = {owner: "Editable"}

    def set_value(self, row, col, expression):
        try:
            value = eval(expression)
            self.data[row][col] = value
        except Exception:
            return "Invalid input."

    def is_editable(self, user):
        return self.access_rights.get(user, "ReadOnly") == "Editable"

    def share(self, collaborator, access_right):
        self.access_rights[collaborator] = access_right

    def modify_access(self, collaborator, access_right):
        if collaborator in self.access_rights:
            self.access_rights[collaborator] = access_right
            return True
        return False


class SheetManager:
    def __init__(self):
        self.users = {}
        self.load_data()

    def save_data(self):
        data = {
            "users": list(self.users.keys()),
            "sheets": {
                user: {
                    name: {
                        "data": sheet.data,
                        "access_rights": sheet.access_rights
                    }
                    for name, sheet in user_obj.sheets.items()
                }
                for user, user_obj in self.users.items()
            },
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f)

    def load_data(self):
        if not os.path.exists(DATA_FILE):  # 文件不存在时直接返回
            return
        with open(DATA_FILE, "r") as f:
            try:
                data = json.load(f)  # 尝试加载文件
            except json.JSONDecodeError:
                print("Warning: Data file is empty or corrupt. Starting fresh.")
                return
        # 加载用户和表格数据
        for user in data["users"]:
            self.users[user] = User(user)
        for user, sheets in data["sheets"].items():
            for sheet_name, sheet_data in sheets.items():
                sheet = Sheet(sheet_name, user)
                sheet.data = sheet_data["data"]
                sheet.access_rights = sheet_data["access_rights"]
                self.users[user].sheets[sheet_name] = sheet


    def create_user(self, name):
        if name in self.users:
            return f"User {name} already exists."
        self.users[name] = User(name)
        self.save_data()
        return f"Create a user named \"{name}\"."

    def create_sheet(self, username, sheet_name, rows, cols):
        if username not in self.users:
            return f"User {username} does not exist."
        user = self.users[username]
        if sheet_name in user.sheets:
            return f"Sheet {sheet_name} already exists."
        sheet = Sheet(sheet_name, username, rows, cols)
        user.sheets[sheet_name] = sheet
        self.save_data()
        return f"Create a sheet named \"{sheet_name}\" with size {rows}x{cols} for \"{username}\"."

    def check_sheet(self, username, sheet_name):
        sheet, error = self.find_sheet(username, sheet_name)
        if error:
            return error
        return "\n".join(", ".join(map(str, row)) for row in sheet.data)


    def find_sheet(self, username, sheet_name):
        # 检查用户是否存在
        if username not in self.users:
            return None, "User not found."
        
        # 检查用户自己的表格
        user = self.users[username]
        if sheet_name in user.sheets:
            return user.sheets[sheet_name], None
        
        # 检查是否有其他用户共享给该用户的表格
        for owner, owner_obj in self.users.items():
            if sheet_name in owner_obj.sheets:
                sheet = owner_obj.sheets[sheet_name]
                if username in sheet.access_rights:
                    return sheet, None
        
        return None, "Sheet not found."


    def change_value(self, username, sheet_name, row, col, expression):
        sheet, error = self.find_sheet(username, sheet_name)
        if error:
            return error
        if not sheet.is_editable(username):
            current_sheet = "\n".join(", ".join(map(str, row)) for row in sheet.data)
            return f"This sheet is not accessible.\n{current_sheet}"
        update_result = sheet.set_value(row, col, expression) or "Value updated."
        self.save_data()
        current_sheet = "\n".join(", ".join(map(str, row)) for row in sheet.data)
        return f"{update_result}\n{current_sheet}"

    def change_access(self, username, sheet_name, right):
        if username not in self.users:
            return "User not found."
        user = self.users[username]
        if sheet_name not in user.sheets:
            return "Sheet not found."
        sheet = user.sheets[sheet_name]
        sheet.access_rights[username] = right
        self.save_data()
        return f"Access right updated to {right}."

    def collaborate(self, owner, sheet_name, collaborator, access_right="ReadOnly"):
        if owner not in self.users or collaborator not in self.users:
            return "User not found."
        user = self.users[owner]
        if sheet_name not in user.sheets:
            return "Sheet not found."
        sheet = user.sheets[sheet_name]
        sheet.share(collaborator, access_right)
        self.save_data()
        return f"Share \"{owner}\"'s \"{sheet_name}\" with \"{collaborator}\"."

    def modify_shared_access(self, owner, sheet_name, collaborator, new_access):
        if owner not in self.users:
            return "Owner not found."
        user = self.users[owner]
        if sheet_name not in user.sheets:
            return "Sheet not found."
        sheet = user.sheets[sheet_name]
        if sheet.modify_access(collaborator, new_access):
            self.save_data()
            return f"Updated \"{collaborator}\"'s access to \"{new_access}\" for \"{sheet_name}\"."
        return f"Collaborator \"{collaborator}\" does not have access to \"{sheet_name}\"."



manager = SheetManager()

def display_menu():
    print("---------------Menu---------------")
    print("1. Create a user")
    print("2. Create a sheet")
    print("3. Check a sheet")
    print("4. Change a value in a sheet")
    print("5. Change a sheet's access right.")
    print("6. Collaborate with another user")
    print("7. Modify shared user's access right")
    print("----------------------------------")

while True:
    display_menu()
    choice = input("> ")

    if choice == "1":
        username = input("Enter username: ")
        print(manager.create_user(username))

    elif choice == "2":
        username, sheet_name = input("Enter username and sheet name: ").split()
        rows, cols = map(int, input("Enter number of rows and columns: ").split())
        print(manager.create_sheet(username, sheet_name, rows, cols))

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
        owner, sheet_name, collaborator, access_right = input("Enter owner, sheet name, collaborator, and access right: ").split()
        print(manager.collaborate(owner, sheet_name, collaborator, access_right))

    elif choice == "7":
        owner, sheet_name, collaborator, new_access = input("Enter owner, sheet name, collaborator, and new access right: ").split()
        print(manager.modify_shared_access(owner, sheet_name, collaborator, new_access))

    else:
        print("Invalid choice. Please try again.")
