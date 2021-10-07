from rest_framework import serializers

from .models import *


# объявляем сериалайзер изображения, для подключения их в рукописях
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


# сериалайзер получения рукописи (с изображениями)
class ManuscriptGetSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, required=False)

    class Meta:
        model = Manuscript
        fields = '__all__'


# сериалайзер создания/обновления рукописи (без изображений)
class ManuscriptSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manuscript
        fields = '__all__'


class ImageInfoSerializer(serializers.ModelSerializer):
    cipher = serializers.StringRelatedField(source='manuscript.cipher')
    storage = serializers.StringRelatedField(source='manuscript.storage')
    type = serializers.StringRelatedField(source='manuscript.type')
    lec_type = serializers.StringRelatedField(source='manuscript.lec_type')

    class Meta:
        model = Image
        fields = '__all__'
