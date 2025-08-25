import os
from fbchat import Client
from fbchat.models import Message

class MessengerLockerBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        # Ignore messages sent by the bot itself
        if author_id == self.uid:
            return

        text = message_object.text
        print(f"Received message from {author_id}: {text}")

        # Simple command handling with prefix "!"
        if text and text.startswith('!'):
            command_parts = text[1:].split(' ', 1)
            cmd = command_parts[0].lower()
            arg = command_parts[1] if len(command_parts) > 1 else None

            if cmd == 'help':
                help_text = (
                    "Commands:\n"
                    "!lockgroup <name> - Lock the group name (admin only)\n"
                    "!locknick <nickname> - Lock your nickname\n"
                    "!help - Show this message"
                )
                self.send(Message(text=help_text), thread_id=thread_id, thread_type=thread_type)

            elif cmd == 'lockgroup' and arg:
                # For demonstration only: store locked group name
                # (No real group name change possible with fbchat)
                global locked_group_name
                locked_group_name = arg
                self.send(Message(text=f"Group name locked as: {arg}"), thread_id=thread_id, thread_type=thread_type)

            elif cmd == 'locknick' and arg:
                # For demonstration only: store locked nickname per user
                locked_nicknames[author_id] = arg
                self.send(Message(text=f"Your nickname locked as: {arg}"), thread_id=thread_id, thread_type=thread_type)

            else:
                self.send(Message(text="Unknown command! Use !help"), thread_id=thread_id, thread_type=thread_type)


# Global variables to store locked names (in-memory only, reset on restart)
locked_group_name = None
locked_nicknames = {}

if __name__ == '__main__':
    email = os.getenv('FB_EMAIL')
    password = os.getenv('FB_PASSWORD')
    appstate_file = 'appstate.json'

    if os.path.exists(appstate_file):
        print("Logging in using appstate.json...")
        client = MessengerLockerBot(session_cookies=appstate_file)
    else:
        print("Logging in using email and password...")
        client = MessengerLockerBot(email, password)
        client.saveSession(appstate_file)  # Save session for future logins

    print("Bot started and listening for messages...")
    client.listen()
