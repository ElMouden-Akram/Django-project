import django_filters
from django import forms
from .models import *


class VoyageFilter(django_filters.FilterSet):
    titre = django_filters.CharFilter(field_name='titre', label='Titre', widget=forms.TextInput(attrs={"class": "form-control","placeholder":"Destination"}))
    date_depart = django_filters.DateFilter(field_name='date_depart', lookup_expr='gte', widget=forms.TextInput(attrs={"class": "form-control","placeholder":"Date de départ",}))
    date_arrivee = django_filters.DateFilter(field_name='date_depart', lookup_expr='lte', widget=forms.TextInput(attrs={"class": "form-control","placeholder":"Date d'arrivée",}))
    classe_vol = django_filters.ChoiceFilter(choices=Vol.CLASSE_CHOICES, field_name='vol__classe', label='Classe de vol', widget=forms.Select(attrs={"class": "form-control"}),empty_label='Eco/Business')
    nombre_etoiles_hotel = django_filters.ChoiceFilter(choices=Hotel.NBR_ETOILE, field_name='hotel__nbr_etoiles', label='Nombre d\'étoiles d\'hôtel', widget=forms.Select(attrs={"class": "form-control"}),empty_label='Étoiles d\'Hôtel')
    ville_depart = django_filters.CharFilter(field_name='vol__ville_depart', label='Ville de départ', widget=forms.TextInput(attrs={"class": "form-control","placeholder":"Ville de départ"}))
    ville_arrive = django_filters.CharFilter(field_name='vol__ville_arrive', label='Ville d\'arrivée', widget=forms.TextInput(attrs={"class": "form-control","placeholder":"Ville d'arrivée"}))

    class Meta:
        model = Voyage
        fields = ['titre', 'date_depart', 'date_arrivee', 'classe_vol', 'nombre_etoiles_hotel', 'ville_depart', 'ville_arrive']
        exclude = ['image_voyage']


