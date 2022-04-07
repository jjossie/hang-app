from rest_framework import serializers
from .models import Option, Decision, Homie, HangoutSession, VoteDetail


class VoteDetailSerializer(serializers.Serializer):
    vote = serializers.IntegerField()
    time_passed = serializers.FloatField()

    def create(self, validated_data):
        return VoteDetail(**validated_data)


class OptionSerializer(serializers.ModelSerializer):
    decision = serializers.PrimaryKeyRelatedField(many=False,
                                                  queryset=Decision.objects.all())

    class Meta:
        model = Option
        fields = ['optionText', 'decision']


class DecisionSerializer(serializers.ModelSerializer):
    session = serializers.PrimaryKeyRelatedField(many=False, queryset=HangoutSession.objects.all())

    class Meta:
        model = Decision
        fields = ['decisionText', 'session']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homie
        fields = ['username']


class HangoutSerializer(serializers.ModelSerializer):


    class Meta:
        model = HangoutSession
        fields = ['']
