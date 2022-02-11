"""File manager tests"""
import shutil
import tempfile
import uuid
from django.conf import settings

from django.test import TestCase, RequestFactory, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Structure
from .exceptions import ItemStructureAlredyExists

# Create your tests here.
MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class TestViewBase(TestCase):
    """Test view base"""

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()


class TestStructureModel(TestCase):
    """Test structure model"""

    def test_item_already_exists(self):
        """Test item already exists"""
        folder_name = "Folder"
        Structure.objects.create(name=folder_name)
        with self.assertRaises(ItemStructureAlredyExists):
            Structure.objects.create(name=folder_name)


class TestStructureAPIView(TestViewBase):
    """Test StructureAPIView"""

    def setUp(self):
        self.factory = RequestFactory()
        self.folder = Structure.objects.create(name="Folder")
        self.subfolder = Structure.objects.create(
            name="SubFolder", parent_id=self.folder.pk
        )
        self.url = reverse("api")

    def test_get_root_structure_api_view(self):
        """Test API get folder method"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_get_subfolder_structure_api_view(self):
        """Test API get subfolder method"""
        response = self.client.get(reverse("api", kwargs={"pk": self.subfolder.pk}))

        self.assertEqual(response.status_code, 200)

    def test_post_folder_structure_api_view(self):
        """Test API post folder method"""
        name = "test"
        response = self.client.post(
            self.url,
            {"name": name},
            HTTP_REFERER=self.url,
        )

        self.assertEqual(response.status_code, 201)

        structure = Structure.objects.filter(name=name).first()
        self.assertIsNotNone(structure)
        self.assertEqual(structure.name, name)

    def test_post_subfolder_structure_api_view(self):
        """Test API post subfolder method"""
        name = "test"
        response = self.client.post(
            reverse("api", kwargs={"pk": self.folder.pk}),
            {"name": name},
            HTTP_REFERER=self.url,
        )

        self.assertEqual(response.status_code, 201)

        structure = Structure.objects.filter(name=name).first()
        self.assertIsNotNone(structure)
        self.assertEqual(structure.name, name)
        self.assertEqual(structure.parent_id, self.folder.pk)

    def test_post_file_structure_api_view(self):
        """Test API post file method"""
        file_name = uuid.uuid4().hex.upper()[0:6] + ".mp4"

        video = SimpleUploadedFile(file_name, b"file_content", content_type="video/mp4")
        response = self.client.post(
            reverse("api"), {"myfile": video}, HTTP_REFERER=self.url
        )

        self.assertEqual(response.status_code, 201)


class TestStructureTemplateView(TestViewBase):
    """Test StructureTemplateView"""

    def setUp(self):
        self.factory = RequestFactory()
        self.folder = Structure.objects.create(name="Folder")
        self.subfolder = Structure.objects.create(
            name="SubFolder", parent_id=self.folder.pk
        )
        self.url = reverse("folders")

    def test_get_root_structure_template_view(self):
        """Test Template get folder method"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_get_subfolder_structure_template_view(self):
        """Test Template get subfolder method"""
        response = self.client.get(reverse("folders", kwargs={"pk": self.subfolder.pk}))

        self.assertEqual(response.status_code, 200)

    def test_post_folder_structure_template_view(self):
        """Test Template post folder method"""
        name = "test"
        response = self.client.post(
            self.url,
            {"name": name},
            HTTP_REFERER=self.url,
        )

        self.assertEqual(response.status_code, 302)

        structure = Structure.objects.filter(name=name).first()
        self.assertIsNotNone(structure)
        self.assertEqual(structure.name, name)

    def test_post_subfolder_structure_template_view(self):
        """Test Template post subfolder method"""
        name = "test"
        response = self.client.post(
            reverse("folders", kwargs={"pk": self.folder.pk}),
            {"name": name},
            HTTP_REFERER=self.url,
        )

        self.assertEqual(response.status_code, 302)

        structure = Structure.objects.filter(name=name).first()
        self.assertIsNotNone(structure)
        self.assertEqual(structure.name, name)
        self.assertEqual(structure.parent_id, self.folder.pk)

    def test_post_file_structure_template_view(self):
        """Test Template post file method"""
        file_name = uuid.uuid4().hex.upper()[0:6] + ".mp4"
        video = SimpleUploadedFile(file_name, b"file_content", content_type="video/mp4")
        response = self.client.post(self.url, {"myfile": video}, HTTP_REFERER=self.url)

        self.assertEqual(response.status_code, 302)


class TestFileDownloadView(TestViewBase):
    """Test FileDownloadView"""

    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse("folders")

    def test_file_download_view(self):
        """Test file download method"""
        file_name = uuid.uuid4().hex.upper()[0:6] + ".mp4"
        video = SimpleUploadedFile(file_name, b"file_content", content_type="video/mp4")
        response = self.client.post(self.url, {"myfile": video}, HTTP_REFERER=self.url)

        self.assertEqual(response.status_code, 302)

        structure = Structure.objects.first()

        response = self.client.get(reverse("files", kwargs={"pk": structure.pk}))
        self.assertEqual(
            response.get("Content-Disposition"), f"attachment; filename={file_name}"
        )
