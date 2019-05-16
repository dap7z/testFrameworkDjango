from django.shortcuts import render


# Create your views here.


def index(request):
    apps = [
        {'link': "/orders", 'desc': "Intégration et visualisation des commandes"},
        {'link': "/admin", 'desc': "Module d'administration de django"},
        {'link': "/api/orders/?format=json", 'desc': "API orders via django rest framework"},
        {'link': "/api/docs", 'desc': "Documentation de l'API via swagger"}
    ]
    return render(request, 'home/index.html', {
        'title': 'Applications',
        'apps': apps,
    })
