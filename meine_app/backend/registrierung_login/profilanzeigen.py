#from django.shortcuts import render, get_object_or_404
#from django.contrib.auth.decorators import login_required
#from .models import CustomUser  # Importiere dein Custom User Model
#from .models import MediaItem  # Importiere dein Medien-Modell (angenommener Name)


#@login_required
def profile_view(request, username):
    """
    Zeigt das Profil eines Benutzers an
    Args:
        request: Django Request-Objekt
        username: Benutzername aus der URL
    Returns:
        Gerendertes Profil-Template mit Kontextdaten
    """
    
    user = get_object_or_404(CustomUser, username=username)

    
    user_media = MediaItem.objects.filter(user=user)

    
    context = {
        'profile_user': user, 
        'beschreibung': user.beschreibung,  
        'profilbild': user.profilbild,  
        'media_items': user_media,  
    }

    return render(request, 'profileseite.html', context)



#urly.py
# path('profilseite/<str:username>/', views.profile_view, name='profileseite'),


#settings.py
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')