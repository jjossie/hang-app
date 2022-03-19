from rest_framework import serializers

from .models import Option, Decision, User, Session


class VoteDetailSerializer(serializers.Serializer):
    vote = serializers.IntegerField()
    time_passed = serializers.FloatField()


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
        model = User
        fields = ['username']


class SessionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Session
        fields = ['']
