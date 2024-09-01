import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List

DIR_ROOT = str(Path(__file__).parent.parent.parent)
sys.path.append(DIR_ROOT)


@dataclass
class Pilar:
    nome_etl: str
    nome_front: str
    cor_background: str


@dataclass
class ScorePilarMap:
    pilar_list: List[Pilar]


@dataclass
class Tema:
    nome_front: str
    nome_etl: str
    cor_background: str


@dataclass
class ScoreTemaMap:
    tema_list: List[Tema]


@dataclass
class Farol:
    nome_etl: str
    nome_front: str
    cor_icone: str
    icones: str


@dataclass
class ScoreFarolMap:
    farol_list: List[Farol]
