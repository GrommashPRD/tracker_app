from rest_framework import serializers

from tracker_app.models import UserDomainsHistory


class VisitedLinksSerializer(serializers.Serializer):
    urls = serializers.ListField(child=serializers.URLField(), required=True)
    user_id = serializers.SerializerMetaclass


class ViewPeriodSerializer(serializers.Serializer):
    start = serializers.IntegerField()
    end = serializers.IntegerField()

    def validate(self, data):

        if data['start'] > data['end']:
            raise serializers.ValidationError('Начало должен быть больше конца')
        if data['start'] < 0:
            raise serializers.ValidationError('Начало должно быть больше 0')
        if data['end'] < 0:
            raise serializers.ValidationError('Конец должен быть больше 0')

        return data

class DomainSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    class Meta:
        model = UserDomainsHistory
        fields = ('user_id', 'domain', 'created_at')


