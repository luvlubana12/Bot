from config import ADMIN_ID, BOT_PREFIX, LOCKED_GROUP_NAME, LOCKED_NICKNAMES
from commands import handle_lock_group_name, handle_lock_all_nicknames, handle_help

class FakeMessengerBot:
    def __init__(self):
        self.group_name = None
        self.nicknames = {}  # user_id: nickname

    def on_message(self, user_id, message):
        if not message.startswith(BOT_PREFIX):
            return
        
        command_parts = message[len(BOT_PREFIX):].split(' ', 1)
        cmd = command_parts[0].lower()
        arg = command_parts[1] if len(command_parts) > 1 else None
        
        if user_id != ADMIN_ID and cmd in ['lockgroup', 'lockallnicks']:
            self.send_message("Only admin can perform this command.")
            return
        
        if cmd == 'lockgroup' and arg:
            response = handle_lock_group_name(arg)
            self.group_name = arg
            self.send_message(response)
        
        elif cmd == 'locknick' and arg:
            LOCKED_NICKNAMES[user_id] = arg
            self.nicknames[user_id] = arg
            self.send_message(f"Nickname locked as '{arg}'.")
        
        elif cmd == 'lockallnicks':
            # Simulate locking all nicknames to current nicknames
            response = handle_lock_all_nicknames(self.nicknames)
            self.send_message(response)
        
        elif cmd == 'help':
            self.send_message(handle_help())
    
    def on_name_change(self, user_id, new_name):
        # If user tries to change name, revert to locked nickname if exists
        if user_id in LOCKED_NICKNAMES:
            original = LOCKED_NICKNAMES[user_id]
            if new_name != original:
                self.nicknames[user_id] = original
                self.send_message(f"Name change not allowed. Reverting to '{original}'.")
        else:
            self.nicknames[user_id] = new_name
    
    def on_group_name_change(self, new_name):
        # Revert group name if locked
        if LOCKED_GROUP_NAME and new_name != LOCKED_GROUP_NAME:
            self.group_name = LOCKED_GROUP_NAME
            self.send_message(f"Group name change not allowed. Reverting to '{LOCKED_GROUP_NAME}'.")
    
    def send_message(self, text):
        print(f"Bot: {text}")

# Example usage
if __name__ == '__main__':
    bot = FakeMessengerBot()
    bot.on_message('1234567890', '!lockgroup My Locked Group')  # Admin locks group name
    bot.on_message('1111111111', '!locknick JohnDoe')  # User locks own nickname
    bot.on_name_change('1111111111', 'ChangedName')  # User tries to change nickname, bot reverts
    bot.on_group_name_change('New Group Name')  # Attempt to change group name, bot reverts
