from rest_framework import serializers
from imagera.models import accessKey, imagera

class keySerializer(serializers.HyperlinkedModelSerializer):
    """ Serializer to map accessKey model into JSON format """
    class Meta:
        """ Meta class to map serializer fields with model labels """
        model = accessKey
        fields = ("key",)
    
class imageraSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializer to map imagera model into JSON format """
    class Meta:
        """ Meta class to map serializer fields with model labels """
        model = imagera
        fields = ('key', 'image_name')