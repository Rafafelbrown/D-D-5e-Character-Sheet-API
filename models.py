#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pydantic models for the D&D 5e Character Sheet.
"""

from typing import Optional
from pydantic import BaseModel, Field


class FichaPersonagem(BaseModel):
    """Complete D&D 5e character data."""

    # ── Header ───────────────────────────────────────────────────
    nome_personagem: str = Field(..., description="Character name")
    classe_nivel: Optional[str] = Field(None, description="Class and level (e.g. Fighter 5)")
    antecedente: Optional[str] = Field(None, description="Background (e.g. Soldier)")
    nome_jogador: Optional[str] = Field(None, description="Player name")
    raca: Optional[str] = Field(None, description="Race (e.g. Human)")
    alinhamento: Optional[str] = Field(None, description="Alignment (e.g. Lawful Good)")
    experiencia: Optional[int] = Field(0, ge=0, description="Experience points")

    # ── Ability scores ────────────────────────────────────────────
    forca: int = Field(10, ge=1, le=30, description="Strength")
    destreza: int = Field(10, ge=1, le=30, description="Dexterity")
    constituicao: int = Field(10, ge=1, le=30, description="Constitution")
    inteligencia: int = Field(10, ge=1, le=30, description="Intelligence")
    sabedoria: int = Field(10, ge=1, le=30, description="Wisdom")
    carisma: int = Field(10, ge=1, le=30, description="Charisma")

    # ── Combat stats ──────────────────────────────────────────────
    inspiracao: bool = Field(False, description="Inspiration active")
    bonus_proficiencia: int = Field(2, ge=2, le=6, description="Proficiency bonus (+2 to +6)")
    classe_armadura: int = Field(10, ge=0, description="Armor class (AC)")
    deslocamento: int = Field(9, ge=0, description="Speed in meters")
    dado_vida: Optional[str] = Field(None, description="Hit die (e.g. 1d10)")

    # ── Hit points ────────────────────────────────────────────────
    pv_maximo: int = Field(10, ge=0, description="Maximum hit points")
    pv_atuais: int = Field(10, ge=0, description="Current hit points")
    pv_temporarios: int = Field(0, ge=0, description="Temporary hit points")

    # ── Saving throws — proficiency ───────────────────────────────
    salv_forca_prof: bool = Field(False)
    salv_destreza_prof: bool = Field(False)
    salv_constituicao_prof: bool = Field(False)
    salv_inteligencia_prof: bool = Field(False)
    salv_sabedoria_prof: bool = Field(False)
    salv_carisma_prof: bool = Field(False)

    # ── Skills — proficiency ──────────────────────────────────────
    acrobacia_prof: bool = Field(False)
    arcanismo_prof: bool = Field(False)
    atletismo_prof: bool = Field(False)
    atuacao_prof: bool = Field(False)
    enganacao_prof: bool = Field(False)
    furtividade_prof: bool = Field(False)
    historia_prof: bool = Field(False)
    intimidacao_prof: bool = Field(False)
    intuicao_prof: bool = Field(False)
    investigacao_prof: bool = Field(False)
    lidar_animais_prof: bool = Field(False)
    medicina_prof: bool = Field(False)
    natureza_prof: bool = Field(False)
    percepcao_prof: bool = Field(False)
    persuasao_prof: bool = Field(False)
    prestidigitacao_prof: bool = Field(False)
    religiao_prof: bool = Field(False)
    sobrevivencia_prof: bool = Field(False)

    # ── Attacks ───────────────────────────────────────────────────
    ataque1_nome: Optional[str] = Field(None, description="1st attack name")
    ataque1_bonus: Optional[str] = Field(None, description="1st attack bonus (e.g. +5)")
    ataque1_dano: Optional[str] = Field(None, description="1st attack damage/type (e.g. 1d8+3 slashing)")
    ataque2_nome: Optional[str] = Field(None)
    ataque2_bonus: Optional[str] = Field(None)
    ataque2_dano: Optional[str] = Field(None)
    ataque3_nome: Optional[str] = Field(None)
    ataque3_bonus: Optional[str] = Field(None)
    ataque3_dano: Optional[str] = Field(None)
    ataques_conjuracao_extra: Optional[str] = Field(None, description="Additional attacks & spellcasting notes")

    # ── Personality traits ────────────────────────────────────────
    tracos_personalidade: Optional[str] = Field(None)
    ideais: Optional[str] = Field(None)
    vinculos: Optional[str] = Field(None)
    fraquezas: Optional[str] = Field(None)

    # ── Text areas (page 1) ───────────────────────────────────────
    outras_proficiencias: Optional[str] = Field(None, description="Weapon, armor, tool and language proficiencies")
    equipamento: Optional[str] = Field(None, description="Items, weapons, armor, money…")
    caracteristicas_talentos: Optional[str] = Field(None, description="Class, racial features and feats")

    # ── Physical appearance (page 2) ─────────────────────────────
    idade: Optional[str] = Field(None)
    altura: Optional[str] = Field(None)
    peso: Optional[str] = Field(None)
    cor_olhos: Optional[str] = Field(None)
    cor_pele: Optional[str] = Field(None)
    cor_cabelo: Optional[str] = Field(None)

    # ── Backstory & organization (page 2) ────────────────────────
    aliados_nome: Optional[str] = Field(None)
    aliados_organizacoes: Optional[str] = Field(None)
    caract_talentos_adicionais: Optional[str] = Field(None)
    historia_personagem: Optional[str] = Field(None)
    tesouros: Optional[str] = Field(None)

    # ── Spells (page 3) ──────────────────────────────────────────
    classe_conjuradora: Optional[str] = Field(None)
    atributo_conjuracao: Optional[str] = Field(None)
    cd_magias: Optional[str] = Field(None)
    bonus_ataque_magico: Optional[str] = Field(None)

    model_config = {"json_schema_extra": {
        "example": {
            "nome_personagem": "Aldric Stonefist",
            "classe_nivel": "Fighter 5",
            "antecedente": "Soldier",
            "nome_jogador": "Rafael",
            "raca": "Human",
            "alinhamento": "Lawful Good",
            "experiencia": 6500,
            "forca": 18,
            "destreza": 14,
            "constituicao": 16,
            "inteligencia": 10,
            "sabedoria": 12,
            "carisma": 8,
            "bonus_proficiencia": 3,
            "classe_armadura": 18,
            "deslocamento": 9,
            "dado_vida": "1d10",
            "pv_maximo": 52,
            "pv_atuais": 52,
            "pv_temporarios": 0,
            "salv_forca_prof": True,
            "salv_constituicao_prof": True,
            "atletismo_prof": True,
            "intimidacao_prof": True,
            "ataque1_nome": "Longsword",
            "ataque1_bonus": "+7",
            "ataque1_dano": "1d8+4 slashing",
        }
    }}


class ModificadoresAtributo(BaseModel):
    forca: str
    destreza: str
    constituicao: str
    inteligencia: str
    sabedoria: str
    carisma: str


class ValoresSalvaguarda(BaseModel):
    forca: str
    destreza: str
    constituicao: str
    inteligencia: str
    sabedoria: str
    carisma: str


class ValoresPericia(BaseModel):
    acrobacia: str
    arcanismo: str
    atletismo: str
    atuacao: str
    enganacao: str
    furtividade: str
    historia: str
    intimidacao: str
    intuicao: str
    investigacao: str
    lidar_animais: str
    medicina: str
    natureza: str
    percepcao: str
    persuasao: str
    prestidigitacao: str
    religiao: str
    sobrevivencia: str


class FichaCalculada(BaseModel):
    """Result of the automatic sheet calculations."""
    iniciativa: str = Field(..., description="Initiative modifier (= Dexterity modifier)")
    sabedoria_passiva: int = Field(..., description="Passive Perception (10 + Perception modifier)")
    modificadores: ModificadoresAtributo
    salvaguardas: ValoresSalvaguarda
    pericias: ValoresPericia
