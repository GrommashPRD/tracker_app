from rest_framework import serializers
from tracker_app.models import UserDomainsHistory

class ErrInvalidValueStartOrEnd(Exception):
    """
    Обрабатываем общие случаи \
    при невалидном значении \
    start & end переменных
    """
    pass

class ErrInvalidUrlList(Exception):
    """
    Обработчик ошибок \
    связанных с поступающим \
    списком URL
    """
    pass


class VisitedLinksSerializer(serializers.Serializer):
    urls = serializers.ListField(child=serializers.URLField(), required=True)
    user_id = serializers.SerializerMetaclass

    def validate(self, data):
        if not data['urls']:
            raise ErrInvalidUrlList({"message": "URL's list can't be empty", "code": "empty_url_list"})
        return data


class ViewPeriodSerializer(serializers.Serializer):
    start = serializers.IntegerField()
    end = serializers.IntegerField()

    def validate(self, data):

        if data['start'] > data['end']:
            raise ErrInvalidValueStartOrEnd({"message":"start should be smaller than a end", "code": "small_start_value"})
        if data['start'] < 0:
            raise ErrInvalidValueStartOrEnd({"message":"start should be largest than a 0", "code": "start_less_than_zero"})
        if data['end'] < 0:
            raise ErrInvalidValueStartOrEnd({"message":"end should be largest than a 0", "code": "small_end_value"})

        return data

class DomainSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    class Meta:
        model = UserDomainsHistory
        fields = ('user_id', 'domain', 'created_at')


