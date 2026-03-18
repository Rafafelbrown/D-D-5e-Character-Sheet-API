#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF filling service for the D&D 5e Character Sheet.
All business logic extracted from the original Streamlit app.
"""

import io
from pdfrw import PdfReader, PdfWriter, PdfDict, PdfObject

# ─────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────

CHECKED   = "/Yes"
UNCHECKED = "/Off"

# Mapping: internal key → real field ID in the PDF
MAPA_CAMPOS = {

    # ── Page 1 · Header ─────────────────────────────────────────
    "nome_personagem":     "Campo de Texto0",
    "classe_nivel":        "Campo de Texto8",
    "antecedente":         "Campo de Texto9",
    "nome_jogador":        "Campo de Texto10",
    "raca":                "Campo de Texto13",
    "alinhamento":         "Campo de Texto12",
    "experiencia":         "Campo de Texto11",

    # ── Page 1 · Ability scores (raw value) ─────────────────────
    "forca":               "Campo de Texto27",
    "destreza":            "Campo de Texto30",
    "constituicao":        "Campo de Texto32",
    "inteligencia":        "Campo de Texto35",
    "sabedoria":           "Campo de Texto36",
    "carisma":             "Campo de Texto38",

    # ── Page 1 · Ability modifiers (calculated) ─────────────────
    "forca_mod":           "Campo de Texto29",
    "destreza_mod":        "Campo de Texto33",
    "constituicao_mod":    "Campo de Texto31",
    "inteligencia_mod":    "Campo de Texto34",
    "sabedoria_mod":       "Campo de Texto39",
    "carisma_mod":         "Campo de Texto37",

    # ── Page 1 · Combat stats ────────────────────────────────────
    "inspiracao":          "Campo de Texto26",
    "bonus_proficiencia":  "Campo de Texto25",
    "classe_armadura":     "Campo de Texto23",
    "iniciativa":          "Campo de Texto24",
    "deslocamento":        "Campo de Texto28",

    # ── Page 1 · Hit points ──────────────────────────────────────
    "pv_maximo":           "Campo de Texto42",
    "pv_atuais":           "Campo de Texto40",
    "pv_temporarios":      "Campo de Texto41",
    "dado_vida":           "Campo de Texto44",

    # ── Page 1 · Saving throws — proficiency (checkbox) ─────────
    "salv_forca_prof":         "Caixa de Seleção0",
    "salv_destreza_prof":      "Caixa de Seleção1",
    "salv_constituicao_prof":  "Caixa de Seleção2",
    "salv_inteligencia_prof":  "Caixa de Seleção3",
    "salv_sabedoria_prof":     "Caixa de Seleção4",
    "salv_carisma_prof":       "Caixa de Seleção5",

    # ── Page 1 · Saving throws — numeric value ───────────────────
    "salv_forca_val":          "Campo de Texto60",
    "salv_destreza_val":       "Campo de Texto61",
    "salv_constituicao_val":   "Campo de Texto62",
    "salv_inteligencia_val":   "Campo de Texto63",
    "salv_sabedoria_val":      "Campo de Texto64",
    "salv_carisma_val":        "Campo de Texto65",

    # ── Page 1 · Skills — proficiency (checkbox) ─────────────────
    "acrobacia_prof":          "Caixa de Seleção6",
    "arcanismo_prof":          "Caixa de Seleção7",
    "atletismo_prof":          "Caixa de Seleção8",
    "atuacao_prof":            "Caixa de Seleção9",
    "enganacao_prof":          "Caixa de Seleção10",
    "furtividade_prof":        "Caixa de Seleção11",
    "historia_prof":           "Caixa de Seleção12",
    "intimidacao_prof":        "Caixa de Seleção13",
    "intuicao_prof":           "Caixa de Seleção14",
    "investigacao_prof":       "Caixa de Seleção15",
    "lidar_animais_prof":      "Caixa de Seleção16",
    "medicina_prof":           "Caixa de Seleção17",
    "natureza_prof":           "Caixa de Seleção18",
    "percepcao_prof":          "Caixa de Seleção19",
    "persuasao_prof":          "Caixa de Seleção20",
    "prestidigitacao_prof":    "Caixa de Seleção21",
    "religiao_prof":           "Caixa de Seleção22",
    "sobrevivencia_prof":      "Caixa de Seleção23",

    # ── Page 1 · Skills — calculated value ───────────────────────
    "acrobacia_val":           "Campo de Texto66",
    "arcanismo_val":           "Campo de Texto67",
    "atletismo_val":           "Campo de Texto68",
    "atuacao_val":             "Campo de Texto69",
    "enganacao_val":           "Campo de Texto70",
    "furtividade_val":         "Campo de Texto71",
    "historia_val":            "Campo de Texto72",
    "intimidacao_val":         "Campo de Texto73",
    "intuicao_val":            "Campo de Texto74",
    "investigacao_val":        "Campo de Texto75",
    "lidar_animais_val":       "Campo de Texto76",
    "medicina_val":            "Campo de Texto77",
    "natureza_val":            "Campo de Texto78",
    "percepcao_val":           "Campo de Texto79",
    "persuasao_val":           "Campo de Texto80",
    "prestidigitacao_val":     "Campo de Texto81",
    "religiao_val":            "Campo de Texto82",
    "sobrevivencia_val":       "Campo de Texto83",

    # ── Page 1 · Attacks & Spellcasting (3 rows) ─────────────────
    "ataque1_nome":    "Campo de Texto45",
    "ataque1_bonus":   "Campo de Texto48",
    "ataque1_dano":    "Campo de Texto51",
    "ataque2_nome":    "Campo de Texto46",
    "ataque2_bonus":   "Campo de Texto49",
    "ataque2_dano":    "Campo de Texto52",
    "ataque3_nome":    "Campo de Texto47",
    "ataque3_bonus":   "Campo de Texto50",
    "ataque3_dano":    "Campo de Texto53",

    # ── Page 1 · Personality traits ──────────────────────────────
    "tracos_personalidade":  "Campo de Texto1",
    "ideais":                "Campo de Texto2",
    "vinculos":              "Campo de Texto3",
    "fraquezas":             "Campo de Texto4",

    # ── Page 1 · Large text areas ────────────────────────────────
    "ataques_conjuracao_extra": "Campo de Texto5",
    "sabedoria_passiva":        "Campo de Texto54",
    "outras_proficiencias":     "Campo de Texto7",
    "equipamento":              "Campo de Texto6",
    "caracteristicas_talentos": "Campo de Texto14",

    # ── Page 2 · Appearance ──────────────────────────────────────
    "nome_personagem_p2": "Campo de Texto84",
    "idade":              "Campo de Texto85",
    "altura":             "Campo de Texto86",
    "peso":               "Campo de Texto87",
    "cor_olhos":          "Campo de Texto90",
    "cor_pele":           "Campo de Texto89",
    "cor_cabelo":         "Campo de Texto88",

    # ── Page 2 · Backstory & Organization ────────────────────────
    "aliados_nome":                   "Campo de Texto18",
    "aliados_organizacoes":           "Campo de Texto209",
    "caract_talentos_adicionais":     "Campo de Texto15",
    "historia_personagem":            "Campo de Texto17",
    "tesouros":                       "Campo de Texto16",

    # ── Page 3 · Spells — Header ─────────────────────────────────
    "classe_conjuradora": "Campo de Texto19",
    "atributo_conjuracao": "Campo de Texto20",
    "cd_magias":           "Campo de Texto21",
    "bonus_ataque_magico": "Campo de Texto22",
}

PERICIAS = [
    ("Acrobatics (Dex)",       "acrobacia",      "destreza"),
    ("Arcana (Int)",           "arcanismo",      "inteligencia"),
    ("Athletics (Str)",        "atletismo",      "forca"),
    ("Performance (Cha)",      "atuacao",        "carisma"),
    ("Deception (Cha)",        "enganacao",      "carisma"),
    ("Stealth (Dex)",          "furtividade",    "destreza"),
    ("History (Int)",          "historia",       "inteligencia"),
    ("Intimidation (Cha)",     "intimidacao",    "carisma"),
    ("Insight (Wis)",          "intuicao",       "sabedoria"),
    ("Investigation (Int)",    "investigacao",   "inteligencia"),
    ("Animal Handling (Wis)",  "lidar_animais",  "sabedoria"),
    ("Medicine (Wis)",         "medicina",       "sabedoria"),
    ("Nature (Int)",           "natureza",       "inteligencia"),
    ("Perception (Wis)",       "percepcao",      "sabedoria"),
    ("Persuasion (Cha)",       "persuasao",      "carisma"),
    ("Sleight of Hand (Dex)",  "prestidigitacao","destreza"),
    ("Religion (Int)",         "religiao",       "inteligencia"),
    ("Survival (Wis)",         "sobrevivencia",  "sabedoria"),
]

SALVAGUARDAS = [
    ("Strength",      "forca"),
    ("Dexterity",     "destreza"),
    ("Constitution",  "constituicao"),
    ("Intelligence",  "inteligencia"),
    ("Wisdom",        "sabedoria"),
    ("Charisma",      "carisma"),
]

# ─────────────────────────────────────────────────────────────────
# Utility functions
# ─────────────────────────────────────────────────────────────────

def calcular_modificador(score: int) -> int:
    """Returns the D&D 5e ability modifier: (score - 10) // 2."""
    return (score - 10) // 2


def formatar_modificador(mod: int) -> str:
    """Formats with sign: '+2' or '-1'."""
    return f"+{mod}" if mod >= 0 else str(mod)


def calcular_pericia(mod_atributo: int, proficiente: bool, bonus_prof: int) -> int:
    """Calculates the total skill value."""
    return mod_atributo + (bonus_prof if proficiente else 0)


# ─────────────────────────────────────────────────────────────────
# Main business logic
# ─────────────────────────────────────────────────────────────────

def calcular_ficha(ficha: dict) -> dict:
    """
    Calculates all derived values (modifiers, saving throws, skills)
    and returns a structured dictionary compatible with FichaCalculada.
    """
    atrs = ("forca", "destreza", "constituicao", "inteligencia", "sabedoria", "carisma")
    mods = {a: calcular_modificador(ficha.get(a, 10)) for a in atrs}
    bp   = ficha.get("bonus_proficiencia", 2)

    salvaguardas = {}
    for _label, chave in SALVAGUARDAS:
        prof  = ficha.get(f"salv_{chave}_prof", False)
        total = mods[chave] + (bp if prof else 0)
        salvaguardas[chave] = formatar_modificador(total)

    pericias = {}
    for _label, chave, attr in PERICIAS:
        prof  = ficha.get(f"{chave}_prof", False)
        total = calcular_pericia(mods[attr], prof, bp)
        pericias[chave] = formatar_modificador(total)

    mod_percepcao = calcular_pericia(
        mods["sabedoria"],
        ficha.get("percepcao_prof", False),
        bp,
    )

    return {
        "iniciativa":        formatar_modificador(mods["destreza"]),
        "sabedoria_passiva": 10 + mod_percepcao,
        "modificadores":     {a: formatar_modificador(mods[a]) for a in atrs},
        "salvaguardas":      salvaguardas,
        "pericias":          pericias,
    }


def construir_dados_pdf(ficha: dict) -> dict:
    """
    Translates character sheet values into the PDF field dictionary.

    Args:
        ficha: Dictionary with all character information.

    Returns:
        Dictionary {pdf_field: value}.
    """
    dados = {}
    atrs = ("forca", "destreza", "constituicao", "inteligencia", "sabedoria", "carisma")
    mods = {a: calcular_modificador(ficha.get(a, 10)) for a in atrs}
    bp   = ficha.get("bonus_proficiencia", 2)

    # Simple fields: text and numbers
    campos_simples = [
        "nome_personagem", "classe_nivel", "antecedente", "nome_jogador",
        "raca", "alinhamento", "experiencia",
        "bonus_proficiencia", "classe_armadura", "deslocamento",
        "pv_maximo", "pv_atuais", "pv_temporarios", "dado_vida",
        "tracos_personalidade", "ideais", "vinculos", "fraquezas",
        "ataques_conjuracao_extra", "outras_proficiencias", "equipamento",
        "caracteristicas_talentos",
        "ataque1_nome", "ataque1_bonus", "ataque1_dano",
        "ataque2_nome", "ataque2_bonus", "ataque2_dano",
        "ataque3_nome", "ataque3_bonus", "ataque3_dano",
        "sabedoria_passiva",
        "nome_personagem_p2", "idade", "altura", "peso",
        "cor_olhos", "cor_pele", "cor_cabelo",
        "aliados_nome", "aliados_organizacoes",
        "caract_talentos_adicionais", "historia_personagem", "tesouros",
        "classe_conjuradora", "atributo_conjuracao", "cd_magias", "bonus_ataque_magico",
    ]
    for c in campos_simples:
        if c in MAPA_CAMPOS and ficha.get(c) is not None:
            dados[MAPA_CAMPOS[c]] = ficha[c]

    # Duplicate character name to page 2 of the PDF
    dados[MAPA_CAMPOS["nome_personagem_p2"]] = ficha.get("nome_personagem", "")

    # Inspiration
    dados[MAPA_CAMPOS["inspiracao"]] = "X" if ficha.get("inspiracao") else ""

    # Ability scores and their modifiers
    for a in atrs:
        dados[MAPA_CAMPOS[a]]          = str(ficha.get(a, 10))
        dados[MAPA_CAMPOS[f"{a}_mod"]] = formatar_modificador(mods[a])

    # Initiative = Dexterity modifier
    dados[MAPA_CAMPOS["iniciativa"]] = formatar_modificador(mods["destreza"])

    # Saving throws
    for _label, chave in SALVAGUARDAS:
        prof_key = f"salv_{chave}_prof"
        val_key  = f"salv_{chave}_val"
        prof     = ficha.get(prof_key, False)
        total    = mods[chave] + (bp if prof else 0)
        dados[MAPA_CAMPOS[prof_key]] = CHECKED if prof else UNCHECKED
        dados[MAPA_CAMPOS[val_key]]  = formatar_modificador(total)

    # Skills
    for _label, chave, attr in PERICIAS:
        prof_key = f"{chave}_prof"
        val_key  = f"{chave}_val"
        prof     = ficha.get(prof_key, False)
        total    = calcular_pericia(mods[attr], prof, bp)
        dados[MAPA_CAMPOS[prof_key]] = CHECKED if prof else UNCHECKED
        dados[MAPA_CAMPOS[val_key]]  = formatar_modificador(total)

    # Passive Perception = 10 + Perception modifier
    mod_percepcao = calcular_pericia(
        mods["sabedoria"],
        ficha.get("percepcao_prof", False),
        bp,
    )
    dados[MAPA_CAMPOS["sabedoria_passiva"]] = str(10 + mod_percepcao)

    return dados


def preencher_pdf(dados: dict, template_bytes: bytes) -> bytes:
    """
    Fills the fields of a PDF using pdfrw.

    Args:
        dados:          Dictionary {field_id: value}.
        template_bytes: Binary content of the PDF template.

    Returns:
        Binary content of the filled PDF.
    """
    reader = PdfReader(fdata=template_bytes)
    if reader.Root.AcroForm:
        reader.Root.AcroForm.update(PdfDict(NeedAppearances=PdfObject("true")))

    for page in reader.pages:
        if "/Annots" not in page:
            continue
        for annot in page["/Annots"]:
            if annot["/Subtype"] != "/Widget" or not annot["/T"]:
                continue
            campo_id = annot["/T"][1:-1]  # Remove PDF string delimiters
            if campo_id not in dados:
                continue
            valor = dados[campo_id]
            if valor is None or valor == "":
                continue
            annot.update(PdfDict(V=str(valor)))

    buf = io.BytesIO()
    PdfWriter().write(buf, reader)
    return buf.getvalue()
