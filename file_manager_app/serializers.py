"""Serializer classes"""
from rest_framework import serializers
from .models import Structure


class StructureSerializer(serializers.ModelSerializer):
    """Structure serializer."""

    name = serializers.CharField(
        label="",
        max_length=50,
        style={"placeholder": "New folder name", "autofocus": True},
    )
    mtype = serializers.SerializerMethodField()

    class Meta:
        model = Structure
        fields = ["pk", "name", "mtype"]

    def get_mtype(self, obj):
        """Return object type"""
        return obj.mtype()

    def create(self, validated_data):
        parent_id = self.context.get("parent_id", None)
        file_path = self.context.get("file_path", None)
        return Structure.objects.create(
            parent_id=parent_id, file_path=file_path, **validated_data
        )
