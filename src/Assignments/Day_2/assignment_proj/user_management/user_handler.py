def add_user(users, username, age):
    """Add a user to the list of users
    Args:
        users (list): List of users
        username (str): Username of the user
        age (int): Age of the user
    Returns:
        str: Message indicating the success or failure of the operation
    """
    try:
        if any(user['username'] == username for user in users):
            raise Exception(f"User with username {username} already exists")
        elif age <= 0:
            raise Exception("Age cannot be negative")
        else:
            users.append({'username': username, 'age': age})
            return f"User with username : {username} is added successfully"
    except TypeError:
        return "Error in input data type"
 
def remove_user(users, username):
    """Remove a user from the list of users
    Args:
        users (list): List of users
        username (str): Username of the user to be removed
    Returns:
        str: Message indicating the success or failure of the operation
    """
    try:
        for user in users:
            if user['username'] == username:
                users.remove(user)
                return f"User with username : {username} is removed successfully"
        raise Exception(f"User with username : {username} does not exist")
    except TypeError:
        return "Error in input data type"
 
def get_user_info(users, username):
    """Get the age of a user from the list of users
    Args:
        users (list): List of users
        username (str): Username of the user
    Returns:
        str: Message indicating the success or failure of the operation
    """
    try:
        for user in users:
            if user['username'] == username:
                return f"User with username : {username} is {user['age']} years old"
        raise Exception(f"User with username : {username} does not exist")
    except ValueError:
        return "Error in input"
 
def update_user_age(users, username, new_age):
    """Update the age of a user in the list of users
    Args:
        users (list): List of users
        username (str): Username of the user
        new_age (int): New age of the user
    Returns:
        str: Message indicating the success or failure of the operation
    """
    try:
        for user in users:
            if user['username'] == username:
                user['age'] = new_age
                return f"User with username : {username} is updated successfully"
        raise Exception(f"User with username : {username} does not exist")
    except TypeError:
        return "Error in input datatype"
 
def update_username(users, username, new_name):
    """Update the username of a user in the list of users
    Args:
        users (list): List of users
        username (str): Username of the user
        new_name (str): New username of the user
    Returns:
        str: Message indicating the success or failure of the operation
    """
    try:
        if any(user['username'] == new_name for user in users):
            raise Exception(f"User with username {new_name} already exists")
        for user in users:
            if user['username'] == username:
                user['username'] = new_name
                return f"User with username : {username} is updated successfully"
        raise Exception(f"User with username : {username} does not exist")
    except TypeError:
        return "Error in input datatype"
    except ValueError:
        return "Error in input"