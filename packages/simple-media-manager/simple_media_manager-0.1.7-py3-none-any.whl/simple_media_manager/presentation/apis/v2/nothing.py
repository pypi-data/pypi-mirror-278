from drf_spectacular.utils import extend_schema
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from simple_media_manager.infrastructure.models import Image


class NothingApi(APIView):
    class NothingSerializer(serializers.Serializer):
        images = serializers.ListField(
            child=serializers.ImageField(required=True, use_url=False))

    @extend_schema(request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "images": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "format": "binary",
                    }
                }
            }
        }
    }, )
    def post(self, request):
        try:
            print(request.data)
            serializer = self.NothingSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            new_images = []
            for image in serializer.validated_data.get('images'):
                new_image = Image(original=image, name=image.name)
                new_image.post_initialize()
                new_images.append(new_image)
            Image.objects.bulk_create(new_images)
            return Response(f"Successfully deleted", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Database Error {e}", status=status.HTTP_400_BAD_REQUEST)
