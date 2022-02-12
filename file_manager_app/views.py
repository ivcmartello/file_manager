"""File manager views"""
from abc import ABC
import mimetypes
from django.http import FileResponse
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Structure
from .serializers import StructureSerializer
from .exceptions import NoFile


def save_file(request):
    """Save file in file system"""
    try:
        file_obj = request.FILES["myfile"]
    except Exception as error:
        raise NoFile from error

    file_system_storage = FileSystemStorage()
    filename = file_system_storage.save(file_obj.name, file_obj)
    uploaded_file_path = file_system_storage.url(filename)

    return filename, uploaded_file_path


class StructureBaseView(ABC, APIView):
    """Structure base view"""

    def get(self, request, pk=0):  # pylint: disable=invalid-name
        """Get structure folder/files"""
        structure_list = Structure.objects.filter(parent_id=pk)

        try:
            structure = Structure.objects.get(pk=pk)
            parent_name = structure.name
            last_parent_id = structure.parent_id
        except Exception:  # pylint: disable=broad-except
            parent_name = "root"
            last_parent_id = 0

        return self.handle_get_response(structure_list, pk, parent_name, last_parent_id)

    def handle_get_response(
        self, struct, pk=0, parent_name="root", last_parent_id=0
    ):  # pylint: disable=invalid-name
        """Handle base get response"""
        raise NotImplementedError()

    def post(self, request, pk=0):  # pylint: disable=invalid-name
        """Create folder and upload file"""
        serializer_context = {"parent_id": pk}

        try:
            filename, file_path = save_file(request)
            request.data["name"] = filename
            serializer_context["file_path"] = file_path
        except NoFile:
            ...

        serializer = StructureSerializer(data=request.data, context=serializer_context)

        return self.handle_post_response(serializer, pk)

    def handle_post_response(self, serializer, pk=0):  # pylint: disable=invalid-name
        """Handle base post response"""
        raise NotImplementedError()


class StructureAPIView(StructureBaseView):
    """Structure api view"""

    def handle_get_response(self, struct, pk=0, parent_name="root", last_parent_id=0):
        serializer = StructureSerializer(struct, many=True)
        data = {
            "parent_id": pk,
            "parent_name": parent_name,
            "last_parent_id": last_parent_id,
            "structure": serializer.data,
        }
        return Response(data)

    def handle_post_response(self, serializer, pk=0):
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as error:  # pylint: disable=broad-except
                return Response(str(error), status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StructureTemplateView(StructureBaseView):
    """Structure template view"""

    swagger_schema = None

    renderer_classes = [
        TemplateHTMLRenderer,
    ]

    def handle_get_response(self, struct, pk=0, parent_name="root", last_parent_id=0):
        return Response(
            {
                "serializer": StructureSerializer(),
                "structure": struct,
                "parent_id": pk,
                "parent_name": parent_name,
                "last_parent_id": last_parent_id,
            },
            template_name="index.html",
        )

    def handle_post_response(self, serializer, pk=0):
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception:  # pylint: disable=broad-except
                ...

        return redirect("folders", pk)


class FileDownloadView(APIView):
    """File download view"""

    def get(self, request, pk=0):  # pylint: disable=invalid-name
        """Download a file"""
        structure = Structure.objects.get(pk=pk)

        mimetype, _ = mimetypes.guess_type(structure.file_path)

        file_system_storage = FileSystemStorage()
        file = file_system_storage.open(structure.name, "rb")

        response = FileResponse(file, content_type=mimetype)
        response["Content-Length"] = file.size
        response["Content-Disposition"] = f"attachment; filename={structure.name}"

        return response
