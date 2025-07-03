#!/usr/bin/env python3
import os
import json

# Path to users.json
USER_JSON_PATH = os.path.join(
    os.getcwd(),
    'meine_app',
    'backend',
    'registrierung_login',
    'users.json'
)

print(f"Reading from: {USER_JSON_PATH}")

try:
    with open(USER_JSON_PATH, 'r', encoding='utf-8') as f:
        all_users = json.load(f)
except Exception as e:
    print(f"Error reading file: {e}")
    all_users = []

print(f"Total users found: {len(all_users)}")

avatar_map = {u.get('username'): u.get('avatar_url', '') for u in all_users if u.get('username')}

print("\nAvatar map:")
for username, avatar_url in avatar_map.items():
    if avatar_url:
        print(f"  {username}: {avatar_url}")
    else:
        print(f"  {username}: NO AVATAR")

print(f"\nUsers with avatars: {len([url for url in avatar_map.values() if url])}")
print(f"Users without avatars: {len([url for url in avatar_map.values() if not url])}")
