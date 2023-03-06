from .models import Pokemon
from rest_framework import serializers
from type.serializers import TypeSerializer
from ability.serializers import AbilitySerializer


class PokemonSerializer(serializers.ModelSerializer):
    types = TypeSerializer(many=True, read_only=True)
    abilities = AbilitySerializer(many=True, read_only=True)

    class Meta:
        model = Pokemon
        fields = '__all__'
