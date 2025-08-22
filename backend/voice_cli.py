import requests
import argparse
import sys

BASE_URL = "http://127.0.0.1:5000"

def check_voice(audio_path):
    """Send voice sample to Flask API for checking."""
    with open(audio_path, "rb") as f:
        files = {"audio": f}
        response = requests.post(f"{BASE_URL}/monitor/start", files=files)
    return response.json()

def add_user(audio_paths, user_id):
    """Add a new user with voice sample."""
    # Convert single path to list if needed
    if isinstance(audio_paths, str):
        audio_paths = [audio_paths]
    
    data = {"user_id": user_id, "audio_paths": audio_paths}

    response = requests.post(f"{BASE_URL}/user/enroll", json=data)

    if response.status_code == 200:
        print(f"User '{user_id}' enrolled successfully.")
    else:
        print(f"Failed to enroll user: {response.text}")
    return response.json()

def main():
    parser = argparse.ArgumentParser(description="Voice Recognition CLI Tool")
    parser.add_argument("audio", help="Path to audio sample file")
    args = parser.parse_args()

    print("\nChecking voice sample against database...\n")
    result = check_voice(args.audio)

    if result.get("status") == "exists":
        print(f"Voice matches with user: {result['user']}")
        print("Access Granted\n")
        sys.exit(0)

    else:
        print("Voice not recognized in database.\n")
        choice = input("Would you like to add this as a new user? (y/n): ").strip().lower()
        
        if choice != "y":
            print("User addition cancelled. Exiting...\n")
            sys.exit(0)

        # Ask for name if user wants to add
        name = input("Enter the name of the user to register: ").strip()

        response = requests.get(f"{BASE_URL}/user/all_users")
        users = response.json()

        # Extract just the user_ids
        user_ids = [u["user_id"] for u in users]

        # Check if name already exists
        if name in user_ids:
            print(f"Username '{name}' already exists in database. Exiting...\n")
            sys.exit(0)

        confirm = input(f"Confirm add user '{name}' with this voice sample? (y/n): ").strip().lower()

        if confirm == "y":
            response = add_user(args.audio, name)
            if response.get("status") == "User enrolled":
                print(f"User '{name}' added successfully with voice sample!")
            else:
                print("Failed to add user. Try again later.")
        else:
            print("User addition cancelled.")

if __name__ == "__main__":
    main()
