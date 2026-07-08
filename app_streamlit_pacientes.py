# ============================================================
# SISTEMA INTELIGENTE DE GESTIÓN DE PACIENTES - STREAMLIT V3
# Interfaz clara, profesional y con opciones CRUD
# ============================================================

from __future__ import annotations

import json
import math
import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd
import streamlit as st


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="Sistema Inteligente de Gestión de Pacientes",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

RUTA_BASE = Path(__file__).resolve().parent
RUTA_DATASET_SINTOMAS = RUTA_BASE / "DiseaseAndSymptoms_ES.csv"
RUTA_DATASET_PRECAUCIONES = RUTA_BASE / "Disease_precaution_ES.csv"


# ============================================================
# ESTILO VISUAL CLARO Y PROFESIONAL
# ============================================================

st.markdown(
    """
    <style>
        :root {
            --primary: #0F766E;
            --primary-dark: #115E59;
            --secondary: #2563EB;
            --bg: #F8FAFC;
            --card: #FFFFFF;
            --text: #0F172A;
            --muted: #475569;
            --border: #D8E3EA;
            --danger: #DC2626;
            --warning: #D97706;
            --success: #059669;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        .stApp {
            background: linear-gradient(180deg, #F8FAFC 0%, #EEF7F6 100%);
            color: var(--text);
        }

        .block-container {
            padding-top: 1rem;
            padding-bottom: 2.5rem;
            max-width: 1320px;
        }

        /* Sidebar claro */
        [data-testid="stSidebar"] {
            background: #FFFFFF;
            border-right: 1px solid var(--border);
        }

        [data-testid="stSidebar"] * {
            color: var(--text) !important;
        }

        [data-testid="stSidebar"] hr {
            border-color: #E2E8F0;
        }

        /* Titulares */
        h1, h2, h3, h4, h5, h6, p, label, span {
            color: var(--text);
        }

        .hero {
            background: linear-gradient(135deg, #0F766E 0%, #0E7490 45%, #2563EB 100%);
            padding: 2rem 2.3rem;
            border-radius: 24px;
            color: white;
            box-shadow: 0 14px 32px rgba(15, 118, 110, 0.20);
            margin-bottom: 1.2rem;
        }

        .hero h1 {
            color: white !important;
            font-size: 2.35rem;
            margin: 0;
            line-height: 1.08;
            font-weight: 850;
        }

        .hero p {
            color: #E0F2FE !important;
            font-size: 1.05rem;
            margin-top: 0.7rem;
            margin-bottom: 0;
        }

        .hero-badge {
            display: inline-block;
            background: rgba(255,255,255,0.17);
            color: #FFFFFF !important;
            border: 1px solid rgba(255,255,255,0.28);
            padding: 0.35rem 0.75rem;
            border-radius: 999px;
            font-size: 0.88rem;
            font-weight: 700;
            margin-bottom: 0.8rem;
        }

        .academic-cover {
            text-align: center;
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 24px;
            padding: 2rem 2.2rem;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
            margin-bottom: 1.4rem;
        }

        .academic-cover h2 {
            color: var(--text) !important;
            margin-bottom: 0.4rem;
            font-weight: 850;
        }

        .academic-cover h3 {
            color: #334155 !important;
            margin: 0.3rem 0;
            font-weight: 750;
        }

        .academic-cover p {
            color: var(--muted) !important;
            margin: 0.3rem 0;
        }

        .section-title {
            font-size: 1.45rem;
            font-weight: 850;
            color: var(--text);
            margin-top: 1.2rem;
            margin-bottom: 0.7rem;
        }

        .mini-card {
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 1.15rem;
            min-height: 168px;
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.07);
            transition: all 0.2s ease-in-out;
        }

        .mini-card:hover {
            border-color: var(--primary);
            box-shadow: 0 14px 30px rgba(14, 116, 144, 0.16);
            transform: translateY(-2px);
        }

        .mini-card h3 {
            color: var(--text) !important;
            margin: 0 0 0.4rem 0;
            font-size: 1.1rem;
        }

        .mini-card p {
            color: var(--muted) !important;
            font-size: 0.94rem;
            line-height: 1.45;
        }

        .metric-card {
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1rem 1.2rem;
            box-shadow: 0 8px 18px rgba(15, 23, 42, 0.06);
        }

        .metric-card .number {
            font-size: 2rem;
            font-weight: 850;
            color: var(--primary);
            line-height: 1;
        }

        .metric-card .label {
            color: var(--muted);
            font-size: 0.92rem;
            margin-top: 0.35rem;
        }

        .info-box {
            border-left: 5px solid #0E7490;
            background: #ECFEFF;
            color: #164E63 !important;
            border-radius: 12px;
            padding: 1rem 1.1rem;
            margin: 0.6rem 0;
        }

        .warning-box {
            border-left: 5px solid #F59E0B;
            background: #FFFBEB;
            color: #78350F !important;
            border-radius: 12px;
            padding: 1rem 1.1rem;
            margin: 0.6rem 0;
        }

        .success-box {
            border-left: 5px solid #10B981;
            background: #ECFDF5;
            color: #064E3B !important;
            border-radius: 12px;
            padding: 1rem 1.1rem;
            margin: 0.6rem 0;
        }

        .danger-box {
            border-left: 5px solid #DC2626;
            background: #FEF2F2;
            color: #7F1D1D !important;
            border-radius: 12px;
            padding: 1rem 1.1rem;
            margin: 0.6rem 0;
        }

        /* Labels negros y visibles */
        [data-testid="stWidgetLabel"] p {
            color: var(--text) !important;
            font-weight: 750 !important;
            font-size: 0.95rem !important;
        }

        /* Inputs claros */
        input, textarea {
            background-color: #FFFFFF !important;
            color: var(--text) !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 12px !important;
        }

        input:focus, textarea:focus {
            border: 1px solid var(--primary) !important;
            box-shadow: 0 0 0 2px rgba(15, 118, 110, 0.15) !important;
        }

        div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            color: var(--text) !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 12px !important;
        }

        div[data-baseweb="select"] span {
            color: var(--text) !important;
        }

        /* Number input */
        [data-testid="stNumberInput"] input {
            background-color: #FFFFFF !important;
            color: var(--text) !important;
        }

        /* Botones */
        div.stButton > button {
            border-radius: 14px;
            border: 1px solid var(--primary);
            background: #FFFFFF;
            color: var(--primary-dark);
            font-weight: 800;
            padding: 0.68rem 1rem;
            transition: 0.15s ease;
        }

        div.stButton > button:hover {
            background: var(--primary);
            color: #FFFFFF;
            border-color: var(--primary);
            transform: translateY(-1px);
        }

        div.stButton > button[kind="primary"] {
            background: var(--primary) !important;
            color: #FFFFFF !important;
            border-color: var(--primary) !important;
        }

        /* Métricas */
        div[data-testid="stMetric"] {
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1rem;
            box-shadow: 0 8px 18px rgba(15, 23, 42, 0.06);
        }

        div[data-testid="stMetric"] * {
            color: var(--text) !important;
        }

        /* Tabs */
        button[data-baseweb="tab"] {
            color: var(--text) !important;
            font-weight: 750 !important;
        }

        /* Dataframes */
        [data-testid="stDataFrame"] {
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid var(--border);
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def normalizar_texto(texto: str) -> str:
    if texto is None:
        return ""

    texto = str(texto).strip().lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"\s+", " ", texto)
    return texto


def separar_sintomas(texto: str) -> List[str]:
    if not texto:
        return []

    partes = re.split(r"[,;\n]+", texto)
    return [p.strip() for p in partes if p.strip()]


def formatear_porcentaje(valor: float) -> str:
    return f"{valor * 100:.2f}%"


def validar_dni(dni: str) -> bool:
    return str(dni).isdigit() and len(str(dni)) == 8


def extraer_dni_opcion(opcion: str) -> str:
    return opcion.split(" - ")[0].strip()


def limpiar_resultado_prediccion():
    st.session_state.ultimo_resultado = []
    st.session_state.paciente_prediccion_dni = None


# ============================================================
# POO: DESCRIPTOR
# ============================================================

class ValidarRango:
    def __init__(self, minimo: float, maximo: float):
        self.minimo = minimo
        self.maximo = maximo
        self.nombre = ""

    def __set_name__(self, owner, name):
        self.nombre = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.nombre, None)

    def __set__(self, obj, valor):
        try:
            valor = float(valor)
        except ValueError:
            raise ValueError(f"{self.nombre} debe ser numérico.")

        if valor < self.minimo or valor > self.maximo:
            raise ValueError(
                f"{self.nombre} fuera de rango. Debe estar entre {self.minimo} y {self.maximo}."
            )

        obj.__dict__[self.nombre] = valor


# ============================================================
# POO: DECORADORES
# ============================================================

def registrar_consulta(func):
    def wrapper(*args, **kwargs):
        resultado = func(*args, **kwargs)
        if "historial_acciones" in st.session_state:
            st.session_state.historial_acciones.append(
                {
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Acción": "Consulta médica registrada",
                    "Detalle": func.__name__,
                }
            )
        return resultado

    return wrapper


def registrar_prediccion(func):
    def wrapper(*args, **kwargs):
        resultado = func(*args, **kwargs)
        if "historial_acciones" in st.session_state:
            st.session_state.historial_acciones.append(
                {
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Acción": "Predicción bayesiana realizada",
                    "Detalle": func.__name__,
                }
            )
        return resultado

    return wrapper


# ============================================================
# POO: METACLASE
# ============================================================

class MetaClaseMedica(type):
    def __new__(mcls, name, bases, attrs):
        clase = super().__new__(mcls, name, bases, attrs)
        nombres_bases = [base.__name__ for base in bases]

        if "TratamientoBase" in nombres_bases and "aplicar" not in attrs:
            raise TypeError(f"La clase {name} debe implementar el método aplicar().")

        return clase


# ============================================================
# POO: CLASES PRINCIPALES
# ============================================================

@dataclass
class Persona:
    nombre: str
    apellido: str
    _dni: str

    @property
    def dni(self) -> str:
        return self._dni

    @dni.setter
    def dni(self, valor: str):
        if not validar_dni(valor):
            raise ValueError("El DNI debe contener exactamente 8 dígitos.")
        self._dni = valor

    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"

    def __str__(self) -> str:
        return f"{self.nombre_completo()} - DNI: {self.dni}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Persona):
            return False
        return self.dni == other.dni


@dataclass
class Paciente(Persona):
    edad: int
    sintomas: List[str] = field(default_factory=list)
    tratamientos: List[str] = field(default_factory=list)
    diagnosticos: List[str] = field(default_factory=list)

    def agregar_sintoma(self, sintoma: str):
        sintoma = sintoma.strip().lower()
        if sintoma and sintoma not in self.sintomas:
            self.sintomas.append(sintoma)

    def eliminar_sintoma(self, sintoma: str):
        if sintoma in self.sintomas:
            self.sintomas.remove(sintoma)

    def agregar_tratamiento(self, tratamiento: str):
        self.tratamientos.append(tratamiento)

    def eliminar_tratamiento(self, tratamiento: str):
        if tratamiento in self.tratamientos:
            self.tratamientos.remove(tratamiento)

    def agregar_diagnostico(self, diagnostico: str):
        if diagnostico and diagnostico not in self.diagnosticos:
            self.diagnosticos.append(diagnostico)

    def eliminar_diagnostico(self, diagnostico: str):
        if diagnostico in self.diagnosticos:
            self.diagnosticos.remove(diagnostico)

    def mostrar_info(self) -> str:
        return f"{self.nombre_completo()} | DNI: {self.dni} | Edad: {self.edad}"

    def __len__(self) -> int:
        return len(self.tratamientos)


@dataclass
class Doctor(Persona):
    especialidad: str
    colegiatura: str

    @registrar_consulta
    def diagnosticar(self, paciente: Paciente, diagnostico: str):
        paciente.agregar_diagnostico(diagnostico)

    @registrar_consulta
    def asignar_tratamiento(self, paciente: Paciente, tratamiento: str):
        paciente.agregar_tratamiento(tratamiento)

    def mostrar_info(self) -> str:
        return f"{self.nombre_completo()} | DNI: {self.dni} | {self.especialidad} | CMP: {self.colegiatura}"


class Monitoreo:
    temperatura = ValidarRango(30.0, 45.0)
    ritmo_cardiaco = ValidarRango(30.0, 220.0)

    def __init__(self, temperatura: float = 36.5, ritmo_cardiaco: float = 75.0):
        self.temperatura = temperatura
        self.ritmo_cardiaco = ritmo_cardiaco

    def mostrar_signos(self) -> Dict[str, float]:
        return {
            "temperatura": self.temperatura,
            "ritmo_cardiaco": self.ritmo_cardiaco,
        }


@dataclass
class PacienteCritico(Paciente, Monitoreo):
    nivel_riesgo: str = "Medio"

    def __post_init__(self):
        Monitoreo.__init__(self, 36.5, 75.0)

    def generar_alerta(self) -> str:
        if self.temperatura >= 39 or self.ritmo_cardiaco >= 120:
            return "Alerta: paciente crítico requiere evaluación inmediata."
        return "Paciente crítico estable según signos vitales registrados."


# ============================================================
# POO: TRATAMIENTOS Y FACTORY
# ============================================================

class TratamientoBase(metaclass=MetaClaseMedica):
    def aplicar(self) -> str:
        raise NotImplementedError


class TratamientoMedicamento(TratamientoBase):
    def aplicar(self) -> str:
        return "Tratamiento con medicamento asignado."


class TratamientoTerapia(TratamientoBase):
    def aplicar(self) -> str:
        return "Tratamiento con terapia asignado."


class TratamientoCirugia(TratamientoBase):
    def aplicar(self) -> str:
        return "Tratamiento quirúrgico asignado."


class TratamientoFactory:
    @staticmethod
    def crear_tratamiento(tipo: str) -> TratamientoBase:
        tipo = normalizar_texto(tipo)

        if tipo == "medicamento":
            return TratamientoMedicamento()
        if tipo == "terapia":
            return TratamientoTerapia()
        if tipo == "cirugia" or tipo == "cirugía":
            return TratamientoCirugia()

        raise ValueError("Tipo de tratamiento no reconocido.")


# ============================================================
# POO: SINGLETON - REGISTRO CENTRAL
# ============================================================

class RegistroMedicoCentral:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.pacientes = []
            cls._instancia.doctores = []
        return cls._instancia

    def registrar_paciente(self, paciente: Paciente):
        if self.buscar_paciente(paciente.dni):
            raise ValueError("Ya existe un paciente con ese DNI.")
        self.pacientes.append(paciente)

    def buscar_paciente(self, dni: str) -> Optional[Paciente]:
        for paciente in self.pacientes:
            if paciente.dni == dni:
                return paciente
        return None

    def eliminar_paciente(self, dni: str):
        paciente = self.buscar_paciente(dni)
        if paciente:
            self.pacientes.remove(paciente)

    def registrar_doctor(self, doctor: Doctor):
        if self.buscar_doctor(doctor.dni):
            raise ValueError("Ya existe un doctor con ese DNI.")
        self.doctores.append(doctor)

    def buscar_doctor(self, dni: str) -> Optional[Doctor]:
        for doctor in self.doctores:
            if doctor.dni == dni:
                return doctor
        return None

    def eliminar_doctor(self, dni: str):
        doctor = self.buscar_doctor(dni)
        if doctor:
            self.doctores.remove(doctor)

    def obtener_doctor_principal(self) -> Optional[Doctor]:
        if self.doctores:
            return self.doctores[0]
        return None

    def __len__(self) -> int:
        return len(self.pacientes)


# ============================================================
# MOTOR BAYESIANO
# ============================================================

class MotorBayes:
    def __init__(self, df_sintomas: pd.DataFrame, df_precauciones: pd.DataFrame):
        self.df_sintomas = df_sintomas.copy()
        self.df_precauciones = df_precauciones.copy()

        self.col_enfermedad = self._detectar_columna_enfermedad(self.df_sintomas)
        self.columnas_sintomas = self._detectar_columnas_sintomas(self.df_sintomas)

        self.vocabulario = set()
        self.sintoma_canonico: Dict[str, str] = {}
        self.conteo_enfermedad = Counter()
        self.conteo_sintoma_enfermedad = defaultdict(Counter)
        self.total_sintomas_enfermedad = Counter()

        self._precalcular()

    @staticmethod
    def _detectar_columna_enfermedad(df: pd.DataFrame) -> str:
        if "Enfermedad" in df.columns:
            return "Enfermedad"
        if "Disease" in df.columns:
            return "Disease"
        return df.columns[0]

    @staticmethod
    def _detectar_columnas_sintomas(df: pd.DataFrame) -> List[str]:
        columnas = []
        for col in df.columns:
            col_norm = normalizar_texto(col)
            if col_norm.startswith("sintoma") or col_norm.startswith("symptom"):
                columnas.append(col)
        return columnas

    def _precalcular(self):
        for _, fila in self.df_sintomas.iterrows():
            enfermedad = str(fila[self.col_enfermedad]).strip()
            if not enfermedad or enfermedad.lower() == "nan":
                continue

            self.conteo_enfermedad[enfermedad] += 1

            for col in self.columnas_sintomas:
                valor = fila.get(col, "")
                if pd.isna(valor):
                    continue

                sintoma = str(valor).strip().lower()
                if not sintoma or sintoma == "nan":
                    continue

                sintoma_norm = normalizar_texto(sintoma)
                self.vocabulario.add(sintoma_norm)
                self.sintoma_canonico[sintoma_norm] = sintoma
                self.conteo_sintoma_enfermedad[enfermedad][sintoma_norm] += 1
                self.total_sintomas_enfermedad[enfermedad] += 1

    def sintomas_disponibles(self) -> List[str]:
        return sorted(self.sintoma_canonico.values())

    def buscar_sintomas(self, consulta: str) -> List[str]:
        consulta_norm = normalizar_texto(consulta)

        if not consulta_norm:
            return self.sintomas_disponibles()

        encontrados = []
        for sintoma_norm, sintoma_original in self.sintoma_canonico.items():
            if consulta_norm in sintoma_norm:
                encontrados.append(sintoma_original)

        return sorted(set(encontrados))

    def obtener_precauciones(self, enfermedad: str) -> List[str]:
        if self.df_precauciones.empty:
            return []

        col_enfermedad = self._detectar_columna_enfermedad(self.df_precauciones)
        coincidencias = self.df_precauciones[
            self.df_precauciones[col_enfermedad].astype(str).str.lower() == enfermedad.lower()
        ]

        if coincidencias.empty:
            return []

        fila = coincidencias.iloc[0]
        precauciones = []

        for col in self.df_precauciones.columns:
            if col == col_enfermedad:
                continue

            valor = fila.get(col, "")
            if pd.notna(valor) and str(valor).strip():
                precauciones.append(str(valor).strip())

        return precauciones

    @registrar_prediccion
    def predecir(self, sintomas_usuario: List[str], top_n: int = 5) -> List[Dict]:
        sintomas_norm = [normalizar_texto(s) for s in sintomas_usuario if s.strip()]
        sintomas_norm = [s for s in sintomas_norm if s]

        if not sintomas_norm:
            return []

        total_registros = sum(self.conteo_enfermedad.values())
        total_enfermedades = len(self.conteo_enfermedad)
        total_vocabulario = max(len(self.vocabulario), 1)

        resultados = []

        for enfermedad, conteo in self.conteo_enfermedad.items():
            log_prob = math.log((conteo + 1) / (total_registros + total_enfermedades))
            denominador = self.total_sintomas_enfermedad[enfermedad] + total_vocabulario
            sintomas_coincidentes = []

            for sintoma in sintomas_norm:
                conteo_sintoma = self.conteo_sintoma_enfermedad[enfermedad][sintoma]
                prob_sintoma = (conteo_sintoma + 1) / denominador
                log_prob += math.log(prob_sintoma)

                if conteo_sintoma > 0:
                    sintomas_coincidentes.append(self.sintoma_canonico.get(sintoma, sintoma))

            resultados.append(
                {
                    "enfermedad": enfermedad,
                    "log_prob": log_prob,
                    "sintomas_coincidentes": sintomas_coincidentes,
                    "n_coincidencias": len(sintomas_coincidentes),
                    "precauciones": self.obtener_precauciones(enfermedad),
                }
            )

        resultados.sort(key=lambda x: (x["log_prob"], x["n_coincidencias"]), reverse=True)
        top = resultados[:top_n]

        max_log = max(r["log_prob"] for r in top)
        pesos = [math.exp(r["log_prob"] - max_log) for r in top]
        suma_pesos = sum(pesos) if sum(pesos) else 1

        for r, peso in zip(top, pesos):
            r["score_relativo"] = peso / suma_pesos

        return top


# ============================================================
# CARGA DE DATOS
# ============================================================

@st.cache_data
def cargar_datos() -> Tuple[pd.DataFrame, pd.DataFrame]:
    if not RUTA_DATASET_SINTOMAS.exists():
        st.error(f"No se encontró el archivo: {RUTA_DATASET_SINTOMAS.name}")
        st.stop()

    if not RUTA_DATASET_PRECAUCIONES.exists():
        st.error(f"No se encontró el archivo: {RUTA_DATASET_PRECAUCIONES.name}")
        st.stop()

    df_sintomas = pd.read_csv(RUTA_DATASET_SINTOMAS, encoding="utf-8-sig")
    df_precauciones = pd.read_csv(RUTA_DATASET_PRECAUCIONES, encoding="utf-8-sig")

    return df_sintomas, df_precauciones


@st.cache_resource
def crear_motor_bayes(df_sintomas: pd.DataFrame, df_precauciones: pd.DataFrame) -> MotorBayes:
    return MotorBayes(df_sintomas, df_precauciones)


# ============================================================
# ESTADO
# ============================================================

def inicializar_estado():
    if "registro" not in st.session_state:
        st.session_state.registro = RegistroMedicoCentral()

    if "historial_acciones" not in st.session_state:
        st.session_state.historial_acciones = []

    if "ultimo_resultado" not in st.session_state:
        st.session_state.ultimo_resultado = []

    if "paciente_prediccion_dni" not in st.session_state:
        st.session_state.paciente_prediccion_dni = None

    if "pagina" not in st.session_state:
        st.session_state.pagina = "Inicio"


def cambiar_pagina(nombre: str):
    st.session_state.pagina = nombre


def obtener_lista_pacientes() -> List[str]:
    pacientes = st.session_state.registro.pacientes
    return [f"{p.dni} - {p.nombre_completo()}" for p in pacientes]


def obtener_lista_doctores() -> List[str]:
    doctores = st.session_state.registro.doctores
    return [f"{d.dni} - {d.nombre_completo()} ({d.especialidad})" for d in doctores]


def convertir_registro_a_json(registro: RegistroMedicoCentral) -> str:
    data = {
        "fecha_exportacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pacientes": [],
        "doctores": [],
        "historial_acciones": st.session_state.historial_acciones,
    }

    for paciente in registro.pacientes:
        item = {
            "tipo": paciente.__class__.__name__,
            "nombre": paciente.nombre,
            "apellido": paciente.apellido,
            "dni": paciente.dni,
            "edad": paciente.edad,
            "sintomas": paciente.sintomas,
            "diagnosticos": paciente.diagnosticos,
            "tratamientos": paciente.tratamientos,
        }

        if isinstance(paciente, PacienteCritico):
            item["nivel_riesgo"] = paciente.nivel_riesgo
            item["temperatura"] = paciente.temperatura
            item["ritmo_cardiaco"] = paciente.ritmo_cardiaco

        data["pacientes"].append(item)

    for doctor in registro.doctores:
        data["doctores"].append(
            {
                "nombre": doctor.nombre,
                "apellido": doctor.apellido,
                "dni": doctor.dni,
                "especialidad": doctor.especialidad,
                "colegiatura": doctor.colegiatura,
            }
        )

    return json.dumps(data, ensure_ascii=False, indent=4)


# ============================================================
# COMPONENTES VISUALES
# ============================================================

def hero():
    st.markdown(
        """
        <div class="hero">
            <span class="hero-badge">🩺 Proyecto académico · POO Avanzada · CRISP-DM</span>
            <h1>Sistema Inteligente de Gestión de Pacientes</h1>
            <p>Interfaz médica para registrar pacientes, analizar síntomas y estimar enfermedades probables mediante predicción bayesiana.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def tarjeta(icono: str, titulo: str, texto: str):
    st.markdown(
        f"""
        <div class="mini-card">
            <h3>{icono} {titulo}</h3>
            <p>{texto}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(numero: str, etiqueta: str):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="number">{numero}</div>
            <div class="label">{etiqueta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# VISTAS
# ============================================================

def vista_inicio(df_sintomas: pd.DataFrame, df_precauciones: pd.DataFrame, motor: MotorBayes):
    hero()

    st.markdown(
        """
        <div class="academic-cover">
            <h2>UNIVERSIDAD NACIONAL TORIBIO RODRÍGUEZ DE MENDOZA DE AMAZONAS</h2>
            <h3>Facultad de Ingeniería Zootecnista, Biotecnología, Agronegocios y Ciencia de Datos</h3>
            <h3>Escuela Profesional de Ingeniería en Ciencia de Datos e Inteligencia Artificial</h3>
            <br>
            <p><b>Curso:</b> Programación Orientada a Objetos Avanzada</p>
            <p><b>Título:</b> Sistema Inteligente de Gestión de Pacientes con Predicción Bayesiana de Enfermedades</p>
            <p><b>Estudiantes:</b> Bustamante Vela, Jean Frank; Salon Ynga, Dangelo Emanuel; Marreros Cortegana, Miguel Angel</p>
            <p><b>Docente:</b> MSc. Abraham Sopla Maslucán</p>
            <p><b>Chachapoyas, 2026</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-title">Panel principal de navegación</div>', unsafe_allow_html=True)
    st.write("Seleccione una opción para iniciar el flujo de trabajo del sistema.")

    col1, col2, col3 = st.columns(3)

    with col1:
        tarjeta("👤", "Gestión de pacientes", "Registra, modifica y elimina pacientes normales o críticos.")
        if st.button("Abrir pacientes", use_container_width=True):
            cambiar_pagina("Registrar paciente")
            st.rerun()

    with col2:
        tarjeta("👨‍⚕️", "Gestión de doctores", "Registra, modifica y elimina doctores responsables.")
        if st.button("Abrir doctores", use_container_width=True):
            cambiar_pagina("Registrar doctor")
            st.rerun()

    with col3:
        tarjeta("🧬", "Predicción bayesiana", "Agrega síntomas y estima enfermedades probables usando Naive Bayes.")
        if st.button("Abrir predicción", use_container_width=True):
            cambiar_pagina("Síntomas y predicción")
            st.rerun()

    col4, col5, col6 = st.columns(3)

    with col4:
        tarjeta("💊", "Tratamientos y signos", "Asigna tratamientos, elimina registros y controla signos vitales.")
        if st.button("Abrir tratamientos", use_container_width=True):
            cambiar_pagina("Tratamientos y signos vitales")
            st.rerun()

    with col5:
        tarjeta("📚", "Dataset médico", "Consulta la data de enfermedades, síntomas y precauciones.")
        if st.button("Consultar dataset", use_container_width=True):
            cambiar_pagina("Dataset médico")
            st.rerun()

    with col6:
        tarjeta("💾", "Exportar información", "Descarga el registro médico del sistema en formato JSON.")
        if st.button("Exportar registro", use_container_width=True):
            cambiar_pagina("Exportar JSON")
            st.rerun()

    st.markdown('<div class="section-title">Indicadores del sistema</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card(f"{len(st.session_state.registro.pacientes)}", "Pacientes registrados")
    with c2:
        metric_card(f"{len(st.session_state.registro.doctores)}", "Doctores registrados")
    with c3:
        metric_card(f"{len(motor.vocabulario)}", "Síntomas únicos")
    with c4:
        metric_card(f"{df_sintomas[motor.col_enfermedad].nunique()}", "Enfermedades en la data")

    st.markdown('<div class="section-title">Problemática</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="info-box">
        En el registro médico básico pueden existir dificultades para organizar pacientes, síntomas, diagnósticos y tratamientos.
        Además, cuando un paciente presenta varios síntomas, puede ser complicado orientar rápidamente qué enfermedad podría estar relacionada.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-title">Solución propuesta</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="success-box">
        El sistema permite registrar pacientes y doctores, ingresar síntomas, realizar una predicción bayesiana de enfermedades probables,
        asignar tratamientos, validar signos vitales y exportar información en formato JSON.
        </div>
        """,
        unsafe_allow_html=True,
    )


def vista_registro_paciente():
    hero()
    st.markdown("## 👤 Gestión de pacientes")

    tab_registrar, tab_modificar, tab_eliminar, tab_listar = st.tabs(
        ["Registrar", "Modificar", "Eliminar", "Pacientes registrados"]
    )

    with tab_registrar:
        with st.form("form_paciente"):
            col1, col2 = st.columns(2)

            with col1:
                tipo_paciente = st.selectbox("Tipo de paciente", ["Paciente normal", "Paciente crítico"])
                nombre = st.text_input("Nombre del paciente")
                apellido = st.text_input("Apellido del paciente")
                dni = st.text_input("DNI del paciente", max_chars=8)

            with col2:
                edad = st.number_input("Edad", min_value=0, max_value=120, value=20, step=1)
                nivel_riesgo = "Medio"

                if tipo_paciente == "Paciente crítico":
                    nivel_riesgo = st.selectbox("Nivel de riesgo", ["Bajo", "Medio", "Alto", "Muy alto"])

            enviar = st.form_submit_button("Registrar paciente")

        if enviar:
            try:
                if not nombre.strip() or not apellido.strip():
                    st.error("Debe ingresar nombre y apellido.")
                    return

                if not validar_dni(dni):
                    st.error("El DNI debe contener exactamente 8 dígitos.")
                    return

                if tipo_paciente == "Paciente crítico":
                    paciente = PacienteCritico(nombre.strip(), apellido.strip(), dni.strip(), int(edad), nivel_riesgo=nivel_riesgo)
                else:
                    paciente = Paciente(nombre.strip(), apellido.strip(), dni.strip(), int(edad))

                st.session_state.registro.registrar_paciente(paciente)
                st.success("Paciente registrado correctamente.")

            except Exception as e:
                st.error(str(e))

    with tab_modificar:
        opciones = obtener_lista_pacientes()

        if not opciones:
            st.info("No hay pacientes para modificar.")
        else:
            seleccion = st.selectbox("Seleccione el paciente a modificar", opciones, key="editar_paciente_select")
            paciente = st.session_state.registro.buscar_paciente(extraer_dni_opcion(seleccion))

            with st.form("form_editar_paciente"):
                col1, col2 = st.columns(2)

                with col1:
                    nuevo_nombre = st.text_input("Nuevo nombre", value=paciente.nombre)
                    nuevo_apellido = st.text_input("Nuevo apellido", value=paciente.apellido)

                with col2:
                    nueva_edad = st.number_input("Nueva edad", min_value=0, max_value=120, value=int(paciente.edad), step=1)
                    if isinstance(paciente, PacienteCritico):
                        nuevo_riesgo = st.selectbox(
                            "Nuevo nivel de riesgo",
                            ["Bajo", "Medio", "Alto", "Muy alto"],
                            index=["Bajo", "Medio", "Alto", "Muy alto"].index(paciente.nivel_riesgo)
                            if paciente.nivel_riesgo in ["Bajo", "Medio", "Alto", "Muy alto"] else 1,
                        )
                    else:
                        nuevo_riesgo = None

                guardar = st.form_submit_button("Guardar cambios")

            if guardar:
                paciente.nombre = nuevo_nombre.strip()
                paciente.apellido = nuevo_apellido.strip()
                paciente.edad = int(nueva_edad)

                if isinstance(paciente, PacienteCritico):
                    paciente.nivel_riesgo = nuevo_riesgo

                st.success("Paciente modificado correctamente.")

    with tab_eliminar:
        opciones = obtener_lista_pacientes()

        if not opciones:
            st.info("No hay pacientes para eliminar.")
        else:
            seleccion = st.selectbox("Seleccione el paciente a eliminar", opciones, key="eliminar_paciente_select")
            dni = extraer_dni_opcion(seleccion)
            confirmar = st.checkbox("Confirmo que deseo eliminar este paciente.")

            if st.button("Eliminar paciente", use_container_width=True):
                if not confirmar:
                    st.warning("Debe confirmar la eliminación.")
                else:
                    st.session_state.registro.eliminar_paciente(dni)
                    limpiar_resultado_prediccion()
                    st.success("Paciente eliminado correctamente.")
                    st.rerun()

    with tab_listar:
        pacientes = st.session_state.registro.pacientes

        if not pacientes:
            st.info("Aún no hay pacientes registrados.")
        else:
            data = []
            for p in pacientes:
                data.append(
                    {
                        "DNI": p.dni,
                        "Nombre": p.nombre_completo(),
                        "Edad": p.edad,
                        "Tipo": p.__class__.__name__,
                        "Síntomas": len(p.sintomas),
                        "Diagnósticos": len(p.diagnosticos),
                        "Tratamientos": len(p.tratamientos),
                    }
                )
            st.dataframe(pd.DataFrame(data), use_container_width=True)


def vista_registro_doctor():
    hero()
    st.markdown("## 👨‍⚕️ Gestión de doctores")

    tab_registrar, tab_modificar, tab_eliminar, tab_listar = st.tabs(
        ["Registrar", "Modificar", "Eliminar", "Doctores registrados"]
    )

    with tab_registrar:
        with st.form("form_doctor"):
            col1, col2 = st.columns(2)

            with col1:
                nombre = st.text_input("Nombre del doctor")
                apellido = st.text_input("Apellido del doctor")
                dni = st.text_input("DNI del doctor", max_chars=8)

            with col2:
                especialidad = st.text_input("Especialidad", value="Medicina General")
                colegiatura = st.text_input("Número de colegiatura", value="CMP-001")

            enviar = st.form_submit_button("Registrar doctor")

        if enviar:
            try:
                if not nombre.strip() or not apellido.strip():
                    st.error("Debe ingresar nombre y apellido.")
                    return

                if not validar_dni(dni):
                    st.error("El DNI debe contener exactamente 8 dígitos.")
                    return

                doctor = Doctor(nombre.strip(), apellido.strip(), dni.strip(), especialidad.strip(), colegiatura.strip())
                st.session_state.registro.registrar_doctor(doctor)
                st.success("Doctor registrado correctamente.")

            except Exception as e:
                st.error(str(e))

    with tab_modificar:
        opciones = obtener_lista_doctores()

        if not opciones:
            st.info("No hay doctores para modificar.")
        else:
            seleccion = st.selectbox("Seleccione el doctor a modificar", opciones, key="editar_doctor_select")
            doctor = st.session_state.registro.buscar_doctor(extraer_dni_opcion(seleccion))

            with st.form("form_editar_doctor"):
                col1, col2 = st.columns(2)

                with col1:
                    nuevo_nombre = st.text_input("Nuevo nombre", value=doctor.nombre)
                    nuevo_apellido = st.text_input("Nuevo apellido", value=doctor.apellido)

                with col2:
                    nueva_especialidad = st.text_input("Nueva especialidad", value=doctor.especialidad)
                    nueva_colegiatura = st.text_input("Nueva colegiatura", value=doctor.colegiatura)

                guardar = st.form_submit_button("Guardar cambios")

            if guardar:
                doctor.nombre = nuevo_nombre.strip()
                doctor.apellido = nuevo_apellido.strip()
                doctor.especialidad = nueva_especialidad.strip()
                doctor.colegiatura = nueva_colegiatura.strip()
                st.success("Doctor modificado correctamente.")

    with tab_eliminar:
        opciones = obtener_lista_doctores()

        if not opciones:
            st.info("No hay doctores para eliminar.")
        else:
            seleccion = st.selectbox("Seleccione el doctor a eliminar", opciones, key="eliminar_doctor_select")
            dni = extraer_dni_opcion(seleccion)
            confirmar = st.checkbox("Confirmo que deseo eliminar este doctor.")

            if st.button("Eliminar doctor", use_container_width=True):
                if not confirmar:
                    st.warning("Debe confirmar la eliminación.")
                else:
                    st.session_state.registro.eliminar_doctor(dni)
                    st.success("Doctor eliminado correctamente.")
                    st.rerun()

    with tab_listar:
        doctores = st.session_state.registro.doctores

        if not doctores:
            st.info("Aún no hay doctores registrados.")
        else:
            data = [
                {
                    "DNI": d.dni,
                    "Nombre": d.nombre_completo(),
                    "Especialidad": d.especialidad,
                    "Colegiatura": d.colegiatura,
                }
                for d in doctores
            ]
            st.dataframe(pd.DataFrame(data), use_container_width=True)


def vista_prediccion(motor: MotorBayes):
    hero()
    st.markdown("## 🧬 Síntomas y predicción bayesiana")

    pacientes_opciones = obtener_lista_pacientes()

    if not pacientes_opciones:
        st.warning("Primero registre al menos un paciente.")
        return

    paciente_opcion = st.selectbox("Seleccione paciente", pacientes_opciones)
    paciente = st.session_state.registro.buscar_paciente(extraer_dni_opcion(paciente_opcion))

    tab_agregar, tab_modificar, tab_prediccion = st.tabs(
        ["Agregar síntomas", "Modificar síntomas", "Predicción bayesiana"]
    )

    with tab_agregar:
        sintomas_disponibles = motor.sintomas_disponibles()

        sintomas_seleccionados = st.multiselect(
            "Seleccione síntomas desde la data",
            options=sintomas_disponibles,
            placeholder="Buscar y seleccionar síntomas",
        )

        sintomas_texto = st.text_area(
            "También puede escribir síntomas separados por coma",
            placeholder="Ejemplo: fatiga, fiebre alta, dolor de cabeza",
        )

        if st.button("Agregar síntomas al paciente", use_container_width=True):
            sintomas_manuales = separar_sintomas(sintomas_texto)
            todos = list(sintomas_seleccionados) + sintomas_manuales

            if not todos:
                st.warning("Debe seleccionar o escribir al menos un síntoma.")
            else:
                for sintoma in todos:
                    paciente.agregar_sintoma(sintoma)

                limpiar_resultado_prediccion()
                st.success("Síntomas agregados correctamente.")

        if paciente.sintomas:
            st.markdown("### Síntomas registrados")
            st.info(", ".join(paciente.sintomas))
        else:
            st.info("Este paciente todavía no tiene síntomas registrados.")

    with tab_modificar:
        if not paciente.sintomas:
            st.info("El paciente no tiene síntomas para modificar o eliminar.")
        else:
            st.markdown("### Eliminar síntomas específicos")
            sintomas_eliminar = st.multiselect("Seleccione síntomas a eliminar", paciente.sintomas)

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Eliminar síntomas seleccionados", use_container_width=True):
                    if not sintomas_eliminar:
                        st.warning("Seleccione al menos un síntoma.")
                    else:
                        for s in sintomas_eliminar:
                            paciente.eliminar_sintoma(s)
                        limpiar_resultado_prediccion()
                        st.success("Síntomas eliminados correctamente.")
                        st.rerun()

            with col2:
                if st.button("Eliminar todos los síntomas", use_container_width=True):
                    paciente.sintomas.clear()
                    limpiar_resultado_prediccion()
                    st.success("Todos los síntomas fueron eliminados.")
                    st.rerun()

            st.markdown("### Síntomas actuales")
            st.write(paciente.sintomas)

    with tab_prediccion:
        if paciente.sintomas:
            st.markdown("### Síntomas usados para la predicción")
            st.info(", ".join(paciente.sintomas))
        else:
            st.warning("El paciente no tiene síntomas registrados.")

        top_n = st.slider("Cantidad de resultados", min_value=3, max_value=10, value=5)

        if st.button("Realizar predicción bayesiana", type="primary", use_container_width=True):
            if not paciente.sintomas:
                st.warning("El paciente no tiene síntomas registrados.")
                return

            resultados = motor.predecir(paciente.sintomas, top_n=top_n)
            st.session_state.ultimo_resultado = resultados
            st.session_state.paciente_prediccion_dni = paciente.dni

        resultados = st.session_state.ultimo_resultado

        if resultados and st.session_state.paciente_prediccion_dni == paciente.dni:
            st.markdown("## Resultados de predicción")

            tabla = []
            for i, r in enumerate(resultados, start=1):
                tabla.append(
                    {
                        "N°": i,
                        "Enfermedad probable": r["enfermedad"],
                        "Score relativo": formatear_porcentaje(r["score_relativo"]),
                        "Coincidencias": r["n_coincidencias"],
                        "Síntomas coincidentes": ", ".join(r["sintomas_coincidentes"]) if r["sintomas_coincidentes"] else "Sin coincidencias directas",
                    }
                )

            df_resultados = pd.DataFrame(tabla)
            st.dataframe(df_resultados, use_container_width=True)

            st.markdown("### Gráfico de probabilidad relativa")
            grafico = pd.DataFrame(
                {
                    "Enfermedad": [r["enfermedad"] for r in resultados],
                    "Score relativo": [r["score_relativo"] for r in resultados],
                }
            )
            st.bar_chart(grafico.set_index("Enfermedad"))

            principal = resultados[0]

            st.markdown("### Enfermedad más probable")
            st.success(f"{principal['enfermedad']} — score relativo: {formatear_porcentaje(principal['score_relativo'])}")

            if principal["precauciones"]:
                st.markdown("### Precauciones recomendadas")
                for p in principal["precauciones"]:
                    st.write(f"- {p}")

            st.markdown(
                """
                <div class="warning-box">
                La predicción es una orientación académica basada en datos. No reemplaza un diagnóstico médico profesional.
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button("Registrar enfermedad más probable como diagnóstico"):
                doctor = st.session_state.registro.obtener_doctor_principal()

                if doctor is None:
                    paciente.agregar_diagnostico(principal["enfermedad"])
                else:
                    doctor.diagnosticar(paciente, principal["enfermedad"])

                st.success("Diagnóstico registrado en el paciente.")


def vista_tratamientos_y_signos():
    hero()
    st.markdown("## 💊 Tratamientos, diagnósticos y signos vitales")

    pacientes_opciones = obtener_lista_pacientes()
    doctores_opciones = obtener_lista_doctores()

    if not pacientes_opciones:
        st.warning("Primero registre al menos un paciente.")
        return

    paciente_opcion = st.selectbox("Seleccione paciente", pacientes_opciones, key="tratamiento_paciente")
    paciente = st.session_state.registro.buscar_paciente(extraer_dni_opcion(paciente_opcion))

    tab_trat, tab_historial, tab_signos = st.tabs(
        ["Asignar tratamiento", "Modificar historial", "Signos vitales"]
    )

    with tab_trat:
        st.markdown("### Asignar tratamiento")

        col1, col2 = st.columns(2)

        with col1:
            tipo_tratamiento = st.selectbox("Tipo de tratamiento", ["Medicamento", "Terapia", "Cirugía"])

        with col2:
            if doctores_opciones:
                doctor_opcion = st.selectbox("Doctor responsable", doctores_opciones)
                doctor = st.session_state.registro.buscar_doctor(extraer_dni_opcion(doctor_opcion))
            else:
                doctor = None
                st.info("No hay doctores registrados. El tratamiento se asignará directamente al paciente.")

        if st.button("Asignar tratamiento", use_container_width=True):
            try:
                tratamiento = TratamientoFactory.crear_tratamiento(tipo_tratamiento)
                descripcion = tratamiento.aplicar()

                if doctor:
                    doctor.asignar_tratamiento(paciente, descripcion)
                else:
                    paciente.agregar_tratamiento(descripcion)

                st.success(descripcion)

            except Exception as e:
                st.error(str(e))

    with tab_historial:
        st.markdown("### Historial del paciente")

        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Síntomas", len(paciente.sintomas))
        col_b.metric("Diagnósticos", len(paciente.diagnosticos))
        col_c.metric("Tratamientos", len(paciente.tratamientos))

        st.markdown("#### Diagnósticos")
        if paciente.diagnosticos:
            diag_eliminar = st.multiselect("Seleccione diagnósticos a eliminar", paciente.diagnosticos)
            if st.button("Eliminar diagnósticos seleccionados", use_container_width=True):
                if not diag_eliminar:
                    st.warning("Seleccione al menos un diagnóstico.")
                else:
                    for d in diag_eliminar:
                        paciente.eliminar_diagnostico(d)
                    st.success("Diagnósticos eliminados correctamente.")
                    st.rerun()
            st.write(paciente.diagnosticos)
        else:
            st.info("Sin diagnósticos registrados.")

        st.markdown("#### Tratamientos")
        if paciente.tratamientos:
            trat_eliminar = st.multiselect("Seleccione tratamientos a eliminar", paciente.tratamientos)
            if st.button("Eliminar tratamientos seleccionados", use_container_width=True):
                if not trat_eliminar:
                    st.warning("Seleccione al menos un tratamiento.")
                else:
                    for t in trat_eliminar:
                        paciente.eliminar_tratamiento(t)
                    st.success("Tratamientos eliminados correctamente.")
                    st.rerun()
            st.write(paciente.tratamientos)
        else:
            st.info("Sin tratamientos registrados.")

    with tab_signos:
        st.markdown("### Signos vitales para paciente crítico")

        if isinstance(paciente, PacienteCritico):
            col1, col2 = st.columns(2)

            with col1:
                temperatura = st.number_input("Temperatura (°C)", min_value=30.0, max_value=45.0, value=float(paciente.temperatura), step=0.1)

            with col2:
                ritmo = st.number_input("Ritmo cardiaco (lpm)", min_value=30.0, max_value=220.0, value=float(paciente.ritmo_cardiaco), step=1.0)

            if st.button("Actualizar signos vitales"):
                try:
                    paciente.temperatura = temperatura
                    paciente.ritmo_cardiaco = ritmo
                    st.success("Signos vitales actualizados correctamente.")
                    st.info(paciente.generar_alerta())

                except Exception as e:
                    st.error(str(e))
        else:
            st.info("El paciente seleccionado no es paciente crítico.")


def vista_busqueda_dataset(motor: MotorBayes, df_sintomas: pd.DataFrame, df_precauciones: pd.DataFrame):
    hero()
    st.markdown("## 📚 Consulta del dataset médico")

    consulta = st.text_input("Buscar síntoma en la data", placeholder="Ejemplo: fatiga, fiebre, dolor")

    if consulta:
        encontrados = motor.buscar_sintomas(consulta)

        if encontrados:
            st.success(f"Se encontraron {len(encontrados)} síntomas.")
            st.write(encontrados[:50])
        else:
            st.warning("No se encontraron síntomas con esa búsqueda.")

    st.markdown("### Vista previa de enfermedades y síntomas")
    st.dataframe(df_sintomas.head(30), use_container_width=True)

    st.markdown("### Vista previa de precauciones")
    st.dataframe(df_precauciones.head(30), use_container_width=True)


def vista_exportacion():
    hero()
    st.markdown("## 💾 Exportación y registro del sistema")

    registro = st.session_state.registro

    col1, col2, col3 = st.columns(3)
    col1.metric("Pacientes", len(registro.pacientes))
    col2.metric("Doctores", len(registro.doctores))
    col3.metric("Acciones registradas", len(st.session_state.historial_acciones))

    st.markdown("### Descargar información")

    json_data = convertir_registro_a_json(registro)

    st.download_button(
        label="Descargar registro en JSON",
        data=json_data,
        file_name="registro_medico.json",
        mime="application/json",
        use_container_width=True,
    )

    st.markdown("### Historial de acciones")

    if st.session_state.historial_acciones:
        st.dataframe(pd.DataFrame(st.session_state.historial_acciones), use_container_width=True)
    else:
        st.info("Aún no hay acciones registradas.")


# ============================================================
# APLICACIÓN PRINCIPAL
# ============================================================

def main():
    inicializar_estado()

    df_sintomas, df_precauciones = cargar_datos()
    motor = crear_motor_bayes(df_sintomas, df_precauciones)

    opciones = [
        "Inicio",
        "Registrar paciente",
        "Registrar doctor",
        "Síntomas y predicción",
        "Tratamientos y signos vitales",
        "Dataset médico",
        "Exportar JSON",
    ]

    with st.sidebar:
        st.markdown("# 🩺 Sistema Médico")
        st.markdown("Panel de navegación")

        st.session_state.pagina = st.radio(
            "Seleccione una sección",
            opciones,
            index=opciones.index(st.session_state.pagina),
        )

        st.markdown("---")
        st.markdown("### Estado del sistema")
        st.write(f"👤 Pacientes: **{len(st.session_state.registro.pacientes)}**")
        st.write(f"👨‍⚕️ Doctores: **{len(st.session_state.registro.doctores)}**")
        st.write(f"🧬 Síntomas únicos: **{len(motor.vocabulario)}**")
        st.write(f"📚 Enfermedades: **{df_sintomas[motor.col_enfermedad].nunique()}**")

    pagina = st.session_state.pagina

    if pagina == "Inicio":
        vista_inicio(df_sintomas, df_precauciones, motor)
    elif pagina == "Registrar paciente":
        vista_registro_paciente()
    elif pagina == "Registrar doctor":
        vista_registro_doctor()
    elif pagina == "Síntomas y predicción":
        vista_prediccion(motor)
    elif pagina == "Tratamientos y signos vitales":
        vista_tratamientos_y_signos()
    elif pagina == "Dataset médico":
        vista_busqueda_dataset(motor, df_sintomas, df_precauciones)
    elif pagina == "Exportar JSON":
        vista_exportacion()


if __name__ == "__main__":
    main()
