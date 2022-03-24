from rest_framework import serializers
from .models import Option, Decision, Homie, HangoutSession, VoteDetail


class VoteDetailSerializer(serializers.Serializer):
    vote = serializers.IntegerField()
    time_passed = serializers.FloatField()

    def create(self, validated_data):
        return VoteDetail(**validated_data)


class OptionSerializer(serializers.HyperlinkedModelSerializer):
    decision = serializers.HyperlinkedRelatedField(read_only=True, view_name='decision-detail')

    class Meta:
        model = Option
        fields = ['optionText', 'decision']


class DecisionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Decision
        fields = ['decisionText']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Homie
        fields = ['username']


class SessionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HangoutSession
        fields = ['']
