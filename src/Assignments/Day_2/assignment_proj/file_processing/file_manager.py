import json

def save_users_to_file(users):
    filename = 'users_data.txt'
    try:
        with open(filename, 'w') as file:
            json.dump(users, file, indent=4)
        return "Users saved successfully"
    except PermissionError:
        return "Error: Permission denied"
    except FileNotFoundError:
        return "Error: File not found"
    except Exception as e:
        return f"Error: {str(e)}"

def load_users_from_file():
    filename = 'users_data.txt'
    try:
        with open(filename, 'r') as file:
            users = json.load(file)
        return users
    except FileNotFoundError:
        return "Error: File not found"
    except PermissionError:
        return "Error: Permission denied"
    except Exception as e:
        return f"Error: {str(e)}"


def write_summary(filename, text_analysis):
    try:
        with open(filename, 'w') as file:
            file.write(text_analysis)
        return "Summary written successfully"
    except PermissionError:
        return "Error: Permission denied"
    except FileNotFoundError:
        return "Error: File not found"
    except Exception as e:
        return f"Error: {str(e)}"

