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


class AddOrRemoveTypeFromPokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = ['types']

    def validate_add(self, data):
        pokemon = self.instance
        if pokemon.types.count() >= 2:
            raise serializers.ValidationError({"error": "this pokemon already has 2 types"})

        if len(data['types']) > 2:
            raise serializers.ValidationError({"error": "cannot pass more than 2 types"})
        return data


class AddOrRemoveAbilityFromPokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = ['abilities']

    def validate_add(self, data):
        pokemon = self.instance
        if pokemon.abilities.count() >= 3:
            raise serializers.ValidationError({"error": "this pokemon already has 3 abilities"})

        if len(data['abilities']) > 3:
            raise serializers.ValidationError({"error": "cannot pass more than 3 abilities"})
        return data
