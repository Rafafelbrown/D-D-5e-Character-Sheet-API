#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
D&D 5e Character Sheet — FastAPI
==================================
Converts the business logic from the original Streamlit app into a REST API.

Main endpoints:
  GET  /html              → Serves the HTML character sheet interface.
  POST /ficha/gerar-pdf   → Receives character data as JSON, returns a filled PDF.
  GET  /ficha/campos      → Lists all available fields with descriptions.
  POST /ficha/calcular    → Calculates modifiers, saving throws and skills from attributes.

Run:
    uvicorn main:app --reload

Dependencies:
    pip install fastapi uvicorn pdfrw python-multipart
"""

import io
import os

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.responses import RedirectResponse

from models import FichaPersonagem, FichaCalculada
from pdf_service import construir_dados_pdf, preencher_pdf, calcular_ficha

PDF_TEMPLATE_DEFAULT = "Ficha-Oficial-D-D-5E-Editavel.pdf"
HTML_FILE_DEFAULT    = "ficha.html"

app = FastAPI(
    title="D&D 5e — Character Sheet API",
    description=(
        "API for generating D&D 5e character sheets. "
        "Receives character data as JSON and returns the official filled PDF."
    ),
    version="4.0.0",
)


def _carregar_template() -> bytes:
    """Tries to load the PDF template from disk. Raises HTTPException if not found."""
    if not os.path.exists(PDF_TEMPLATE_DEFAULT):
        raise HTTPException(
            status_code=503,
            detail=(
                f"Template '{PDF_TEMPLATE_DEFAULT}' not found on the server. "
                "Use the /ficha/gerar-pdf endpoint with a template upload, or "
                "place the PDF in the same folder as main.py."
            ),
        )
    with open(PDF_TEMPLATE_DEFAULT, "rb") as f:
        return f.read()


# ─────────────────────────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────────────────────────

@app.get("/", tags=["Status"], include_in_schema=False)
def raiz():
    return RedirectResponse(url="/html")


@app.get(
    "/html",
    tags=["Interface"],
    summary="Opens the HTML character sheet interface",
    response_class=HTMLResponse,
)
def servir_html():
    """
    Serves the `ficha.html` file directly in the browser.
    Simply visit http://localhost:8000/html to open the interface.
    """
    if not os.path.exists(HTML_FILE_DEFAULT):
        raise HTTPException(
            status_code=404,
            detail=(
                f"File '{HTML_FILE_DEFAULT}' not found. "
                "Place ficha.html in the same folder as main.py."
            ),
        )
    with open(HTML_FILE_DEFAULT, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.post(
    "/ficha/gerar-pdf",
    tags=["Ficha"],
    summary="Generates the PDF filled with character data",
    response_description="Filled PDF file for download",
)
def gerar_pdf(
    ficha: FichaPersonagem,
    template: UploadFile = File(default=None, description="PDF template (optional if already on the server)"),
):
    """
    Receives character data as JSON and returns the official D&D 5e PDF filled in.

    The template can be sent as `multipart/form-data` in the `template` field.
    If omitted, the server looks for `Ficha-Oficial-D-D-5E-Editavel.pdf`
    in the working directory.

    **Note:** to send JSON and a file simultaneously, use `multipart/form-data`
    and pass the character data as a JSON string in the `ficha` field.
    """
    if not ficha.nome_personagem or not ficha.nome_personagem.strip():
        raise HTTPException(status_code=422, detail="The field 'nome_personagem' is required.")

    # Load the template
    if template is not None:
        template_bytes = template.file.read()
    else:
        template_bytes = _carregar_template()

    dados_pdf = construir_dados_pdf(ficha.model_dump())
    pdf_bytes = preencher_pdf(dados_pdf, template_bytes)

    nome_arquivo = ficha.nome_personagem.strip().replace(" ", "_").lower()

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="ficha_{nome_arquivo}.pdf"',
        },
    )


@app.post(
    "/ficha/gerar-pdf-upload",
    tags=["Ficha"],
    summary="Generates the PDF by sending template and data separately via multipart",
)
async def gerar_pdf_com_upload(
    template: UploadFile = File(..., description="Official D&D 5e PDF template"),
    ficha_json: UploadFile = File(..., description="JSON file with character data"),
):
    """
    Multipart alternative: send the PDF template and a JSON file with character data.
    Useful for clients that prefer not to serialize JSON in form fields.
    """
    import json

    template_bytes = await template.read()
    ficha_raw = await ficha_json.read()

    try:
        ficha_dict = json.loads(ficha_raw)
        ficha = FichaPersonagem(**ficha_dict)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Invalid JSON: {exc}")

    if not ficha.nome_personagem or not ficha.nome_personagem.strip():
        raise HTTPException(status_code=422, detail="The field 'nome_personagem' is required.")

    dados_pdf = construir_dados_pdf(ficha.model_dump())
    pdf_bytes = preencher_pdf(dados_pdf, template_bytes)
    nome_arquivo = ficha.nome_personagem.strip().replace(" ", "_").lower()

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="ficha_{nome_arquivo}.pdf"'},
    )


@app.post(
    "/ficha/calcular",
    tags=["Ficha"],
    summary="Calculates modifiers, saving throws and skills",
    response_model=FichaCalculada,
)
def calcular(ficha: FichaPersonagem):
    """
    Returns all calculated values (attribute modifiers, saving throws and skills)
    without generating a PDF. Useful for front-ends that need to display totals in real time.
    """
    return calcular_ficha(ficha.model_dump())


@app.get(
    "/ficha/campos",
    tags=["Ficha"],
    summary="Lists all available fields in the model",
)
def listar_campos():
    """Returns the JSON schema of the FichaPersonagem model with a description of each field."""
    return FichaPersonagem.model_json_schema()
