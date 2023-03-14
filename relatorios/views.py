from django.shortcuts import render

from django.views.generic import TemplateView

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

from clientes.models import Clientes


# Create your views here.


class ReportPageView(TemplateView):
    template_name = "report.html"


def pdf_report(request):
    # Retrieve data from your database
    items = Clientes.objects.all()

    # Create a new PDF document
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="report.pdf"'
    p = canvas.Canvas(response, pagesize=A4)

    # Define the header and footer
    def header(canvasc):
        # Load the logo image
        logo = ImageReader("/path/to/logo.png")

        # Add the logo to the header
        canvas.drawImage(
            logo, inch, A4[1] - 1.25 * inch, width=2 * inch, height=1 * inch
        )

        # Add the title to the header
        canvas.setFont("Helvetica-Bold", 16)
        canvas.drawString(inch + 2 * inch, A4[1] - 0.75 * inch, "My Report")

    def footer(canvas):
        canvas.saveState()
        canvas.setFont("Helvetica", 10)
        canvas.drawString(inch, 0.75 * inch, "Page %d" % 1)
        canvas.restoreState()

    # Add the header and footer to the document
    p.setTitle("My Report")
    p.setPageCompression(1)
    header(canvas)
    footer(canvas)

    # Add a list of items to the report
    p.setFont("Helvetica", 12)
    y = 700
    for item in items:
        p.drawString(100, y, str(item))
        y -= 20

    # Save the PDF document and return it as a response
    p.showPage()
    p.save()
    return response
