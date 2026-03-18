# D&D 5e — Character Sheet API

A REST API built with **FastAPI** for generating D&D 5e character sheets. Receives character data as JSON and returns the official sheet as a filled PDF.

---

## Project structure

```
dnd_api/
├── main.py           # FastAPI app — routes and configuration
├── models.py         # Pydantic models (request/response)
├── pdf_service.py    # Business logic: calculations and PDF filling
├── requirements.txt
└── Ficha-Oficial-D-D-5E-Editavel.pdf   ← place the template here
```

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Running the server

```bash
uvicorn main:app --reload
```

Interactive documentation will be available at:

- Swagger UI → http://localhost:8000/docs
- ReDoc → http://localhost:8000/redoc

---

## Endpoints

### `GET /html`
Serves the HTML character sheet interface directly in the browser.

### `POST /ficha/gerar-pdf`
Receives character data as JSON and returns the filled PDF for download. The PDF template must be present in the project folder as `Ficha-Oficial-D-D-5E-Editavel.pdf`, or it can be sent in the `template` field as `multipart/form-data`.

**Example with curl:**
```bash
curl -X POST http://localhost:8000/ficha/gerar-pdf \
  -H "Content-Type: application/json" \
  -d '{
    "nome_personagem": "Aldric Stonefist",
    "classe_nivel": "Fighter 5",
    "raca": "Human",
    "forca": 18,
    "destreza": 14,
    "constituicao": 16,
    "inteligencia": 10,
    "sabedoria": 12,
    "carisma": 8,
    "bonus_proficiencia": 3,
    "classe_armadura": 18,
    "pv_maximo": 52,
    "pv_atuais": 52,
    "salv_forca_prof": true,
    "salv_constituicao_prof": true,
    "atletismo_prof": true,
    "ataque1_nome": "Longsword",
    "ataque1_bonus": "+7",
    "ataque1_dano": "1d8+4 slashing"
  }' \
  --output ficha_aldric.pdf
```

### `POST /ficha/gerar-pdf-upload`
Multipart alternative: send the PDF template and a JSON file with character data as separate uploads. Useful for clients that prefer not to serialize JSON in form fields.

### `POST /ficha/calcular`
Calculates and returns modifiers, saving throws and skills without generating a PDF. Useful for front-ends that need to display computed values in real time.

### `GET /ficha/campos`
Returns the full JSON schema of the character model, including a description of every available field.

---

## Differences from the original Streamlit app

| Streamlit (`dnd_ficha_v4.py`) | FastAPI (`dnd_api/`) |
|-------------------------------|----------------------|
| Graphical interface in the browser | Pure REST API |
| Template uploaded via the sidebar | Template on disk or sent via `multipart/form-data` |
| Calculations only at generation time | Dedicated `/ficha/calcular` endpoint for isolated calculations |
| Single file | Split into `main`, `models`, `pdf_service` |
| `streamlit`, `pdfrw` | `fastapi`, `uvicorn`, `pdfrw`, `python-multipart` |
