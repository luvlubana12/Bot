from config import ADMIN_ID, LOCKED_GROUP_NAME, LOCKED_NICKNAMES

def handle_lock_group_name(new_name):
    global LOCKED_GROUP_NAME
    LOCKED_GROUP_NAME = new_name
    return f"Group name locked as '{new_name}'."

def handle_lock_all_nicknames(nicknames_dict):
    global LOCKED_NICKNAMES
    LOCKED_NICKNAMES = nicknames_dict.copy()
    return f"Nicknames locked for all members."

def handle_help():
    return (
        "Commands:\n"
        "!lockgroup <name> - Lock the group name\n"
        "!locknick <nickname> - Lock your nickname\n"
        "!lockallnicks - Lock all nicknames (admin only)\n"
        "!help - Show this help message"
    )
