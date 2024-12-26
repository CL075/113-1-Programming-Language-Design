class Sheet:
    def __init__(self, name, rows=3, cols=3):
        self.name = name
        self.data = [[0] * cols for _ in range(rows)]
        self.access_rights = {}  # key: username, value: access rights ("Editable" or "ReadOnly")

    def is_editable(self, username):
        return self.access_rights.get(username) == "Editable"

    def set_value(self, row, col, expression):
        try:
            self.data[row][col] = eval(expression)
            return True
        except Exception as e:
            return f"Invalid expression: {e}"

    def share(self, username, access_right):
        self.access_rights[username] = access_right


class User:
    def __init__(self, name):
        self.name = name


class SheetManager:
    def __init__(self):
        self.users = {}  # key: username, value: User object
        self.sheet_registry = {}  # key: username, value: {sheet_name: Sheet object}

    def create_user(self, username):
        if username in self.users:
            return f"User '{username}' already exists."
        self.users[username] = User(username)
        self.sheet_registry[username] = {}
        return f"Create a user named '{username}'."

    def create_sheet(self, username, sheet_name):
        if username not in self.users:
            return "User not found."
        if sheet_name in self.sheet_registry[username]:
            return f"Sheet '{sheet_name}' already exists for '{username}'."
        self.sheet_registry[username][sheet_name] = Sheet(sheet_name)
        self.sheet_registry[username][sheet_name].access_rights[username] = "Editable"
        return f"Create a sheet named '{sheet_name}' for '{username}'."

    def change_value(self, username, sheet_name, row, col, expression):
        if username not in self.users:
            return "User not found."
        sheet = self.find_sheet(sheet_name, username)
        if not sheet:
            return "Sheet not found."
        if not sheet.is_editable(username):
            current_sheet = "\n".join(", ".join(map(str, row)) for row in sheet.data)
            return f"This sheet is not accessible.\n{current_sheet}"
        update_result = sheet.set_value(row, col, expression) or "Value updated."
        current_sheet = "\n".join(", ".join(map(str, row)) for row in sheet.data)
        return f"{update_result}\n{current_sheet}"

    def find_sheet(self, sheet_name, username):
        # Check if the sheet is owned by the user
        if sheet_name in self.sheet_registry.get(username, {}):
            return self.sheet_registry[username][sheet_name]
        # Check if the sheet is shared with the user
        for owner, sheets in self.sheet_registry.items():
            if sheet_name in sheets and username in sheets[sheet_name].access_rights:
                return sheets[sheet_name]
        return None

    def share_sheet(self, owner, sheet_name, collaborator, access_right="ReadOnly"):
        if owner not in self.users or collaborator not in self.users:
            return "User not found."
        if sheet_name not in self.sheet_registry[owner]:
            return "Sheet not found."
        sheet = self.sheet_registry[owner][sheet_name]
        sheet.share(collaborator, access_right)
        return f"Share '{owner}'s '{sheet_name}' with '{collaborator}'."

    def check_sheet(self, username, sheet_name):
        if username not in self.users:
            return "User not found."
        sheet = self.find_sheet(sheet_name, username)
        if not sheet:
            return "Sheet not found."
        current_sheet = "\n".join(", ".join(map(str, row)) for row in sheet.data)
        return current_sheet
