from rest_framework import serializers
from .models import PrivateFile

class PrivateFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = PrivateFile
        fields = ['id', 'name', 'file', 'file_url', 'category', 'uploaded_at', 'size']

    def get_file_url(self, obj):
        url = obj.file.url
        
        # If it is already a Cloudinary link (http...), return it.
        if url.startswith('http'):
            return url
            
        # If it is a local link (/media...), prepend the server domain
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(url)
            
        return url