class HelpCommand:
    description = " Display help for a command"
    usage = " help [command]"
    help_text = " If no command is specified, display the list of available commands. Otherwise, display help for the specified command."

    @staticmethod
    def execute(console, arg):
        if not arg:
            print(" Welcome to the CRM console. Use 'help <command>' to get help on a specific command.")
            print(" Available commands:")
            for command, instance in console.commands.items():
                print(f"  {command}: {instance.description}")
                if instance.usage:
                    print(f"    Usage: {instance.usage}")
            return

        if arg in console.commands:
            instance = console.commands[arg]
            print(f"  Help for the '{arg}' command:")
            print(f"   {instance.description}")
            if instance.usage:
                print(f"   Usage: {instance.usage}")
            if instance.help_text:
                print(f"  {instance.help_text}")
        else:
            print(f"  Command not found: {arg}. Use 'help' to see the list of available commands.")
