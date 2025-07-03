import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

def registrieren(request, USER_JSON_PATH):
    if request.method == 'GET':
        name = request.GET.get('name')
        username = request.GET.get('username')
        email = request.GET.get('email')
        password = request.GET.get('password')
        confirm_password = request.GET.get('confirm-password')

        if password != confirm_password:
            messages.error(request, "Passwörter stimmen nicht überein.")
            return render(request, 'meine_app/registrierung.html')

        try:
            with open(USER_JSON_PATH, 'r',encoding='utf-8') as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            users = []

        if any(u['username'] == username for u in users):
            messages.error(request, "Benutzername ist bereits vergeben.")
            return render(request, 'meine_app/registrierung.html')

        users.append({
            'name': name,
            'username': username,
            'email': email,
            'password': make_password(password),
        })

        with open(USER_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2)

        messages.success(request, "Registrierung erfolgreich.")
        return redirect('login')
    return render(request, 'meine_app/registrierung.html')
