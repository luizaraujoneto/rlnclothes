from django.shortcuts import render

from django.views.generic import TemplateView

from datetime import datetime

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize

from io import BytesIO

import os
from django.http import FileResponse

from clientes.models import Clientes


PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]
styles = getSampleStyleSheet()

# Create your views here.


class ReportPageView(TemplateView):
    template_name = "report.html"


"""
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
        logo = ImageReader("http://localhost:8000/static/images/logo-beige.png")

        # Add the logo to the header
        canvasc.drawImage(logo, 2 * cm, A4[1] - 1.25 * cm, width=2 * cm, height=2 * cm)

        # Add the title to the header
        canvasc.setFont("Helvetica-Bold", 16)
        canvasc.drawString(inch + 2 * inch, A4[1] - 0.75 * inch, "My Report")

    def footer(canvasc):
        canvasc.saveState()
        canvasc.setFont("Helvetica", 10)
        canvasc.drawString(inch, 0.75 * inch, "Page %d" % 1)
        canvasc.restoreState()

    # Add the header and footer to the document
    p.setTitle("My Report")
    p.setPageCompression(1)
    header(p)
    footer(p)

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
"""


def pdf_report2(request):
    Title = "Listagem de Clientes"
    pageinfo = datetime.now().strftime("%d/%m/%Y")

    # Retrieve data from your database
    items = Clientes.objects.all().order_by("nomecliente")

    def myModelPage(canvas, doc):
        canvas.saveState()

        # Load the logo image
        logo = ImageReader("http://localhost:8000/static/images/logo-beige.png")

        # Add the logo to the header
        canvas.drawImage(logo, 2 * cm, A4[1] - 2.5 * cm, width=2 * cm, height=2 * cm)
        canvas.line(
            x1=2 * cm, y1=A4[1] - 2.52 * cm, x2=A4[0] - 2 * cm, y2=A4[1] - 2.52 * cm
        )

        # Add the title to the header
        canvas.setFont("Helvetica-Bold", 16)
        canvas.drawString(4.5 * cm, A4[1] - 1.5 * cm, Title)

        # Draw the footer
        canvas.line(x1=2 * cm, y1=2 * cm, x2=A4[0] - 2 * cm, y2=2 * cm)
        canvas.setFont("Helvetica", 10)
        canvas.drawString(
            A4[0] - 5.5 * cm, 1.4 * cm, "Page %d %s" % (doc.page, pageinfo)
        )

        canvas.restoreState()

    # def go():
    doc = SimpleDocTemplate("report.pdf")
    Story = [Spacer(1, 0.5 * cm)]
    style = styles["Normal"]

    for item in items:
        p = Paragraph(
            str(item.codcliente)
            + " - "
            + item.nomecliente
            + " - "
            + str(item.telefone)
            + " - "
            + str(item.observacao),
            style,
        )
        Story.append(p)
        # Story.append(Spacer(1, 0.2 * inch))
    doc.build(Story, onFirstPage=myModelPage, onLaterPages=myModelPage)

    # Get the path to the PDF file
    pdf_file_path = doc.filename

    # Open the PDF file and create a FileResponse object
    pdf_file = open(pdf_file_path, "rb")
    response = FileResponse(pdf_file, content_type="application/pdf")

    # Set the Content-Disposition header to force the file to be downloaded
    filename = os.path.basename(pdf_file_path)
    response["Content-Disposition"] = 'attachment; filename="{}"'.format(filename)

    return response


def html_report(request):
    dataimpressao = datetime.now().strftime("%d/%m/%Y")
    horaimpressao = datetime.now().strftime("%H:%M:%S")

    clientes = Clientes.objects.all().order_by("nomecliente")

    context = {
        "clientes": clientes,
        "dataimpressao": dataimpressao,
        "horaimpressao": horaimpressao,
    }

    return render(request, "relatorios/relatorio_clientes.html", context=context)
