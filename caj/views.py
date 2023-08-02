# Create your views here.
import traceback
from pathlib import Path

from django.http import JsonResponse, FileResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .caj2pdf.cajparser import CAJParser


@csrf_exempt
def caj2pdf(request):
    if request.method == "GET":
        return render(request, template_name="caj.html")
    elif request.method == "POST":
        try:
            file = request.FILES.get("file")
            if file.size > 1024 * 1024 * 100:
                return JsonResponse({"message": "file too large"})
            caj_abs_path = (caj_path := Path("caj/caj_files") / file.name).absolute()
            if not caj_abs_path.exists():
                with open(caj_abs_path, "wb+") as dst:
                    for chunk in file.chunks():
                        dst.write(chunk)

            if not (
                pdf_path := Path("caj/pdf_files") / f"{Path(file.name).stem}.pdf"
            ).exists():
                caj = CAJParser(caj_abs_path)
                caj.convert(pdf_path)
            # Open the PDF for reading
            with open(pdf_path, "rb") as pdf_file:
                # Read the data in the file
                # Create the response
                return FileResponse(pdf_file,filename=pdf_path.name,content_type="application/pdf")
        except Exception as e:
            traceback.print_exc()
            print(e)
            return JsonResponse({"message": "sth went wrong"})
