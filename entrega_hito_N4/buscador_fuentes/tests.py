from django.test import TestCase
from django.urls import reverse
from .models import DocumentoPDF
from django.core.files.uploadedfile import SimpleUploadedFile

class DocumentoPDFTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Crear PDF publicado
        pdf_publicado = SimpleUploadedFile("archivo.pdf", b"Contenido PDF", content_type="application/pdf")
        cls.pdf_publicado = DocumentoPDF.objects.create(
            nombre="PDF Publicado",
            archivo=pdf_publicado,
            publicado=True
        )

        # Crear PDF no publicado
        pdf_no_publicado = SimpleUploadedFile("archivo2.pdf", b"Contenido PDF 2", content_type="application/pdf")
        cls.pdf_no_publicado = DocumentoPDF.objects.create(
            nombre="PDF No Publicado",
            archivo=pdf_no_publicado,
            publicado=False
        )

    def test_acceso_pdf_publicado(self):
        url = reverse('detalle_pdf', args=[self.pdf_publicado.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.pdf_publicado.nombre)

    def test_acceso_pdf_no_publicado(self):
        url = reverse('detalle_pdf', args=[self.pdf_no_publicado.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
