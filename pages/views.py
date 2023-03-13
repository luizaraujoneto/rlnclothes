from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader

from clientes.models import Clientes

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import PageTemplate
from reportlab.platypus.frames import Frame
from reportlab.lib import pagesizes
from reportlab.platypus.paragraph import Paragraph
from functools import partial


class HomePageView(TemplateView):
    template_name = "home.html"


class AboutPageView(TemplateView):
    template_name = "about.html"


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
    def header(canvas, doc):
        # Load the logo image
        logo = ImageReader("/path/to/logo.png")

        # Add the logo to the header
        canvas.drawImage(logo, mm, A4[1] - 1.25 * mm, width=2 * mm, height=1 * mm)

        # Add the title to the header
        canvas.setFont("Helvetica-Bold", 16)
        canvas.drawString(mm + 2 * mm, A4[1] - 0.75 * mm, "My Report")

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 10)
        canvas.drawString(mm, 0.75 * mm, "Page %d" % doc.page)
        canvas.restoreState()

    # Add the header and footer to the document
    p.setTitle("My Report")
    p.setPageCompression(1)
    # p.setHeader(header)
    # p.setFooter(footer)

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


def pdf_report2(request):
    def header(canvas, doc, content):
        canvas.saveState()
        w, h = content.wrap(doc.width, doc.topMargin)
        content.drawOn(
            canvas, doc.leftMargin, doc.height + doc.bottomMargin + doc.topMargin - h
        )
        canvas.restoreState()

    def footer(canvas, doc, content):
        canvas.saveState()
        w, h = content.wrap(doc.width, doc.bottomMargin)
        content.drawOn(canvas, doc.leftMargin, h)
        canvas.restoreState()

    def header_and_footer(canvas, doc, header_content, footer_content):
        header(canvas, doc, header_content)
        footer(canvas, doc, footer_content)

    # Create a new PDF document
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="report.pdf"'

    styles = getSampleStyleSheet()

    filename = "out.pdf"

    PAGESIZE = pagesizes.portrait(pagesizes.A4)

    #    pdf3 = SimpleDocTemplate(
    #        filename,
    #        pagesize=PAGESIZE,
    #        leftMargin=2.2 * cm,
    #        rightMargin=2.2 * cm,
    #        topMargin=1.5 * cm,
    #        bottomMargin=2.5 * cm,
    #    )

    pdf = canvas.Canvas(response, pagesize=A4)

    #    frame = Frame(pdf.leftMargin, pdf.bottomMargin, pdf.width, pdf.height, id="normal")
    frame = Frame(1, 1, 21, 29, id="normal")

    header_content = Paragraph(
        "This is a header. testing testing testing  ", styles["Normal"]
    )
    footer_content = Paragraph(
        "This is a footer. It goes on every page.  ", styles["Normal"]
    )

    template = PageTemplate(
        id="test",
        frames=frame,
        onPage=partial(
            header_and_footer,
            header_content=header_content,
            footer_content=footer_content,
        ),
    )

    pdf.addPageTemplates([template])

    pdf.build([Paragraph("This is content")])

    pdf.showPage()
    pdf.save()

    return response
