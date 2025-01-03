import json
import os
from functools import reduce

DATA_FILE = "data.txt"

FEATURE_FLAGS = {
    "feature_1": True,
    "feature_2": True,
    "feature_3": True,
    "feature_4": True,
    "feature_5": True,
    "feature_6": True,
    "feature_7": True,
}


def feature_toggle(feature_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if FEATURE_FLAGS.get(feature_name, False):
                return func(*args, **kwargs)
            else:
                print(f"The feature '{feature_name}' is currently disabled.")
                return None
        return wrapper
    return decorator

# Functional Programming Utilities
def save_to_file(data, file_path):
    with open(file_path, "w") as f:
        json.dump(data, f)

def load_from_file(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("Warning: Data file is empty or corrupt. Starting fresh.")
            return None

def create_user(users, name):
    if name in users:
        return users, f"User {name} already exists."
    return {**users, name: {"sheets": {}}}, f"Create a user named \"{name}\"."

def create_sheet(users, username, sheet_name, rows, cols): 
    if username not in users:
        return users, f"User {username} does not exist."
    if sheet_name in users[username]["sheets"]:
        return users, f"Sheet {sheet_name} already exists."

    sheet = {
        "name": sheet_name,
        "data": [[0 for _ in range(cols)] for _ in range(rows)],
        "access_rights": {username: "Editable"}
    }
    
    updated_user = {
        **users[username],
        "sheets": {**users[username]["sheets"], sheet_name: sheet}
    }
    return {**users, username: updated_user}, f"Create a sheet named \"{sheet_name}\" with size {rows}x{cols} for \"{username}\"."

def find_sheet(users, username, sheet_name):
    if username not in users:
        return None, "User not found."

    user_sheets = users[username]["sheets"]
    if sheet_name in user_sheets:
        return user_sheets[sheet_name], username, None

    for owner, data in users.items():
        if sheet_name in data["sheets"] and username in data["sheets"][sheet_name]["access_rights"]:
            return data["sheets"][sheet_name], owner, None

    return None, None, "Sheet not found."

def update_sheet_value(sheet, row, col, expression):
    try:
        value = eval(expression)
        updated_data = sheet["data"][:]
        updated_data[row][col] = value
        return {**sheet, "data": updated_data}, "Value updated."
    except Exception:
        return sheet, "Invalid input."

def update_value(users, username, sheet_name, row, col, expression):
    sheet, owner, error = find_sheet(users, username, sheet_name)
    if error:
        return users, error

    if sheet["access_rights"].get(username, "ReadOnly") != "Editable":
        return users, "This sheet is not editable."

    updated_sheet, message = update_sheet_value(sheet, row, col, expression)
    updated_owner = {
        **users[owner],
        "sheets": {**users[owner]["sheets"], sheet_name: updated_sheet}
    }

    return {**users, owner: updated_owner}, message

def change_access(users, username, sheet_name, access_right):
    if username not in users:
        return users, "User not found."
    if sheet_name not in users[username]["sheets"]:
        return users, "Sheet not found."

    sheet = users[username]["sheets"][sheet_name]
    sheet["access_rights"][username] = access_right

    updated_user = {
        **users[username],
        "sheets": {**users[username]["sheets"], sheet_name: sheet}
    }

    return {**users, username: updated_user}, f"Access right updated to {access_right}."



def collaborate(users, username, sheet_name, collaborator, access_right="ReadOnly"):
    # 檢查擁有者是否存在
    if username not in users:
        return users, "Owner not found."
    # 檢查工作表是否存在
    if sheet_name not in users[username]["sheets"]:
        return users, "Sheet not found."
    # 檢查協作者是否存在
    if collaborator not in users:
        return users, f"Collaborator \"{collaborator}\" does not exist. Please create the user first."

    # 共享工作表權限
    sheet = users[username]["sheets"][sheet_name]
    updated_rights = {**sheet["access_rights"], collaborator: access_right}
    updated_sheet = {**sheet, "access_rights": updated_rights}

    updated_user = {
        **users[username],
        "sheets": {**users[username]["sheets"], sheet_name: updated_sheet}
    }

    return {**users, username: updated_user}, f"Access right updated for {collaborator}."

@feature_toggle("feature_1")
def option_1(users):
    username = input("Enter username: ")
    users, message = create_user(users, username)
    print(message)
    return users


@feature_toggle("feature_2")
def option_2(users):
    username, sheet_name = input("Enter username and sheet name: ").split()
    rows, cols = map(int, input("Enter number of rows and columns: ").split())
    users, message = create_sheet(users, username, sheet_name, rows, cols)
    print(message)
    return users


@feature_toggle("feature_3")
def option_3(users):
    username, sheet_name = input("Enter username and sheet name: ").split()

    # 呼叫 check_sheet 來檢查工作表
    result = check_sheet(users, username, sheet_name)
    if "not found" in result.lower():  # 如果返回的結果包含 "not found"
        print(f"Error: {result}")
    else:
        print(f"Sheet content:\n{result}")
    
    return users



@feature_toggle("feature_4")
def option_4(users):
    username, sheet_name = input("Enter username and sheet name: ").split()
    sheet, owner, error = find_sheet(users, username, sheet_name)
    if error:
        print(error)
        return users

    # 打印工作表內容
    print(f"Sheet content (owner: {owner}):")
    print(check_sheet(users, owner, sheet_name))

    row, col, expression = input("Enter row, col, and expression: ").split()
    users, message = update_value(users, username, sheet_name, int(row), int(col), expression)
    print(f"{message}\n{check_sheet(users, owner, sheet_name)}")
    return users


@feature_toggle("feature_5")
def option_5(users):
    username, sheet_name, access_right = input("Enter username, sheet name, and access right: ").split()

    # 呼叫 change_sheet_access 並接收返回值
    result = change_sheet_access(users, username, sheet_name, access_right)

    # 根據返回值的類型來決定輸出的內容
    if isinstance(result, str):  # 如果返回的是錯誤訊息
        print(result)
        return users

    # 否則，返回更新後的用戶數據並打印成功訊息
    users = result
    print(f"Access rights for {sheet_name} updated.")
    return users


@feature_toggle("feature_6")
def option_6(users):
    owner, sheet_name, collaborator, access_right = input("Enter owner, sheet name, collaborator, and access right: ").split()
    if collaborator not in users:
        print(f"Collaborator \"{collaborator}\" does not exist. Please create the user first.")
        return users

    users, message = collaborate(users, owner, sheet_name, collaborator, access_right)
    print(message)
    return users


@feature_toggle("feature_7")
def option_7(users):
    owner, sheet_name, collaborator, new_access = input("Enter owner, sheet name, collaborator, and new access right: ").split()
    users, message = modify_shared_access(users, owner, sheet_name, collaborator, new_access)
    print(message)
    return users


# def change_sheet_access(users, username, sheet_name, access_right): 
#     users, message = change_access(users, username, sheet_name, access_right)
#     print(message)
#     return users
def change_sheet_access(users, username, sheet_name, access_right):
    # 檢查擁有者是否存在
    if username not in users:
        return "User not found."

    # 檢查工作表是否存在於擁有者名下
    if sheet_name not in users[username]["sheets"]:
        return "Sheet not found."

    # 更新工作表的訪問權限
    sheet = users[username]["sheets"][sheet_name]
    sheet["access_rights"][username] = access_right

    updated_user = {
        **users[username],
        "sheets": {**users[username]["sheets"], sheet_name: sheet}
    }

    # 返回更新後的用戶數據
    return {**users, username: updated_user}



def collaborate_with_user(users, owner, sheet_name, collaborator, access_right):
    users, message = collaborate(users, owner, sheet_name, collaborator, access_right)
    print("6:", message)
    return users

def modify_shared_access(users, owner, sheet_name, collaborator, new_access): 
    if owner not in users:
        return users, "Owner not found."
    if sheet_name not in users[owner]["sheets"]:
        return users, "Sheet not found."

    sheet = users[owner]["sheets"][sheet_name]
    if collaborator not in sheet["access_rights"]:
        return users, f"Collaborator \"{collaborator}\" does not have access to \"{sheet_name}\"."

    updated_rights = {**sheet["access_rights"], collaborator: new_access}
    updated_sheet = {**sheet, "access_rights": updated_rights}

    updated_owner = {
        **users[owner],
        "sheets": {**users[owner]["sheets"], sheet_name: updated_sheet}
    }
    return {**users, owner: updated_owner}, f"Updated \"{collaborator}\"'s access to \"{new_access}\" for \"{sheet_name}\"."

def check_sheet(users, username, sheet_name):
    sheet, owner, error = find_sheet(users, username, sheet_name)
    if error:
        return error  # 返回錯誤訊息

    if sheet is None:  # 如果工作表為 None，返回明確錯誤
        return "Error: Sheet not found."

    # 確保 sheet["data"] 存在並可以被處理
    if "data" not in sheet or not isinstance(sheet["data"], list):
        return "Error: Invalid sheet data."

    # 生成工作表的內容字符串
    return "\n".join(", ".join(map(str, row)) for row in sheet["data"])


# Main program logic
def main():
    users = {}
    loaded_data = load_from_file(DATA_FILE)
    if loaded_data:
        users = loaded_data.get("users", {})

    while True:
        print("---------------Menu---------------")
        print("1. Create a user")
        print("2. Create a sheet")
        print("3. Check a sheet")
        print("4. Change a value in a sheet")
        if FEATURE_FLAGS["feature_5"]:
            print("5. Change a sheet's access right.")
        if FEATURE_FLAGS["feature_6"]:
            print("6. Collaborate with another user")
        if FEATURE_FLAGS["feature_7"]:
            print("7. Modify shared user's access right")
        print("----------------------------------")
        choice = input("> ")

        
        if choice == "1":
            users = option_1(users)

        elif choice == "2":
            users = option_2(users)

        elif choice == "3":
            users = option_3(users)

        elif choice == "4":
            users = option_4(users)

        elif choice == "5":
            users = option_5(users)

        elif choice == "6":
            users = option_6(users)

        elif choice == "7":
            users = option_7(users)

        else:
            print("Invalid choice. Please try again.")

        save_to_file({"users": users}, DATA_FILE)

if __name__ == "__main__":
    main()
