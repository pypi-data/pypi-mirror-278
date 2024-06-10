import argparse
import os
from src.api_client import APIClient
from src.session_manager import SessionManager
from src.code_storage import CodeStorage
from src.config_manager import ConfigManager
from src.logger import Logger
from src.error_handler import ErrorHandler

def main():
    parser = argparse.ArgumentParser(description="CLI-based Coding Co-Pilot")
    parser.add_argument("command", choices=["generate", "save", "load", "configure"], help="Command to execute")
    parser.add_argument("prompt", type=str, nargs="?", help="The prompt to generate code for")
    parser.add_argument("--session-name", type=str, help="Name of the session to save/load")
    parser.add_argument("--f", action="store_true", help="View all the saved sessions.")
    parser.add_argument("--d", action="store_true", help="Name of the session to be deleted.")
    parser.add_argument("--file-name", type=str, help="File name to save generated code")
    args = parser.parse_args()

    logger = Logger()
    config_manager = ConfigManager()
    api_client = APIClient(config_manager.get_api_key(), logger)
    session_manager = SessionManager(logger)
    code_storage = CodeStorage(logger)
    error_handler = ErrorHandler(logger)

    try:
        if args.command == "generate":
            if args.prompt:
                generated_code = api_client.generate_code(args.prompt)
                if generated_code is None:
                    print("\nFailed to generate code. Please try again.")
                    return
                print("\nGenerated Code:\n\n", generated_code)
                if args.file_name:
                    code_storage.save_code(args.file_name, generated_code)
                else:
                    save_it = input("\nDo you want to save this code? (Y/n): ")
                    while save_it.lower() not in ["y", "n", ""]:
                        print("\n> Invalid input.")
                        save_it = input("\nDo you want to save this code? (Y/n): ")
                    if save_it.lower() == "y":
                        file_name = input("\nEnter a file name to save the code: ")
                        code_storage.save_code(file_name, generated_code)
            else:
                print("\nPlease provide a prompt to generate code.")
        
        elif args.command == "save":
            if args.session_name and args.prompt:
                generated_code = api_client.generate_code(args.prompt)
                if generated_code is None:
                    print("\nFailed to generate code. Please try again.")
                    return
                print("\nGenerated Code:\n\n", generated_code)
                session_manager.save_session(args.session_name, args.prompt, generated_code)
            else:
                print("\nPlease provide both session name and prompt.")
        
        elif args.command == "load":
            if args.d:
                if args.session_name:
                    session_manager.delete_session(args.session_name)
                else:
                    print("\nPlease provide the session name to delete.")
            elif args.f:
                session_manager.display_saved_sessions()
            elif args.session_name:
                session = session_manager.load_session(args.session_name)
                print("\nLoaded Session:\n\n", session)
            else:
                print("\nPlease provide a session name to load.")
        
        elif args.command == "configure":
            config_manager.configure()
        
        else:
            parser.print_help()

    except Exception as e:
        error_handler.handle(e)

if __name__ == "__main__":
    main()
