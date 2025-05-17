import sqlite3
import os
from datetime import datetime

def check_chat_database():
    # Get the database path
    db_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
    db_path = os.path.join(db_dir, "chat_support_db.db")
    
    if not os.path.exists(db_path):
        print("Database file not found!")
        return
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all messages
    cursor.execute("SELECT id, prompt, response, timestamp FROM chat_messages ORDER BY timestamp DESC")
    messages = cursor.fetchall()
    
    if not messages:
        print("No messages found in the database.")
    else:
        print("\nChat History:")
        print("-" * 80)
        for msg in messages:
            print(f"ID: {msg[0]}")
            print(f"Timestamp: {msg[3]}")
            print(f"Prompt: {msg[1]}")
            print(f"Response: {msg[2]}")
            print("-" * 80)
    
    conn.close()

if __name__ == "__main__":
    check_chat_database() 