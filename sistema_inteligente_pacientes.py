# ============================================================
# SISTEMA INTELIGENTE DE GESTIÓN DE PACIENTES
# Predicción bayesiana de enfermedades usando:
# - DiseaseAndSymptoms_ES.csv
# - Disease precaution_ES.csv
# ============================================================

import csv
import json
import math
import unicodedata
from pathlib import Path
from functools import wraps


# ============================================================
# RUTAS DE ARCHIVOS
# ============================================================

RUTA_BASE = Path(__file__).resolve().parent
# Se priorizan las datas en español.
# Si no existen, el sistema puede usar las datas originales en inglés.
RUTA_DATASET_SINTOMAS_ES = RUTA_BASE / "DiseaseAndSymptoms_ES_COMPAT.csv"
RUTA_DATASET_PRECAUCIONES_ES = RUTA_BASE / "Disease_precaution_ES_COMPAT.csv"
RUTA_DATASET_SINTOMAS_ING = RUTA_BASE / "DiseaseAndSymptoms.csv"
RUTA_DATASET_PRECAUCIONES_ING = RUTA_BASE / "Disease precaution.csv"

RUTA_DATASET_SINTOMAS = RUTA_DATASET_SINTOMAS_ES if RUTA_DATASET_SINTOMAS_ES.exists() else RUTA_DATASET_SINTOMAS_ING
RUTA_DATASET_PRECAUCIONES = RUTA_DATASET_PRECAUCIONES_ES if RUTA_DATASET_PRECAUCIONES_ES.exists() else RUTA_DATASET_PRECAUCIONES_ING
RUTA_REGISTRO = RUTA_BASE / "registro_pacientes.json"


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def normalizar(texto):
    """
    Normaliza textos para comparar síntomas y enfermedades.
    Convierte a minúsculas, quita tildes, reemplaza guiones bajos
    y elimina espacios repetidos.
    """
    if texto is None:
        return ""

    texto = str(texto).strip().lower()
    texto = texto.replace("_", " ")
    texto = " ".join(texto.split())

    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))

    return texto


def titulo_limpio(texto):
    """Devuelve texto normalizado con formato legible."""
    return normalizar(texto).title()


# ============================================================
# DECORADORES PERSONALIZADOS
# Esto es DECORADOR porque agrega una acción extra
# sin modificar directamente el método original.
# ============================================================

def registrar_consulta(funcion):
    @wraps(funcion)
    def envoltura(*args, **kwargs):
        print("\n[REGISTRO] Consulta médica registrada.")
        return funcion(*args, **kwargs)
    return envoltura


def registrar_prediccion(funcion):
    @wraps(funcion)
    def envoltura(*args, **kwargs):
        print("\n[REGISTRO] Predicción bayesiana ejecutada.")
        return funcion(*args, **kwargs)
    return envoltura


# ============================================================
# DESCRIPTOR
# Esto es DESCRIPTOR porque controla lectura y escritura
# usando __get__, __set__ y __set_name__.
# Sirve para validar signos vitales y edad.
# ============================================================

class ValidarRango:
    def __init__(self, minimo, maximo, nombre_campo="Valor"):
        self.minimo = minimo
        self.maximo = maximo
        self.nombre_campo = nombre_campo
        self.nombre_interno = ""

    def __set_name__(self, owner, name):
        self.nombre_interno = "_" + name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.nombre_interno, None)

    def __set__(self, obj, valor):
        try:
            numero = float(valor)
        except (TypeError, ValueError):
            raise ValueError(f"{self.nombre_campo} debe ser numérico.")

        if numero < self.minimo or numero > self.maximo:
            raise ValueError(
                f"{self.nombre_campo} debe estar entre {self.minimo} y {self.maximo}."
            )

        setattr(obj, self.nombre_interno, numero)


# ============================================================
# METACLASE
# Esto es METACLASE porque controla la creación de clases.
# En este caso, valida que los tratamientos tengan aplicar().
# ============================================================

class MetaClaseMedica(type):
    def __new__(cls, name, bases, attrs):
        nueva_clase = super().__new__(cls, name, bases, attrs)

        if name.startswith("Tratamiento") and name != "TratamientoBase":
            if "aplicar" not in attrs:
                raise TypeError(f"La clase {name} debe implementar aplicar().")

        return nueva_clase


# ============================================================
# CLASE BASE: PERSONA
# Esto es CLASE PADRE.
# Aquí se aplica encapsulamiento y property.
# ============================================================

class Persona:
    def __init__(self, nombre, apellido, dni):
        self.nombre = titulo_limpio(nombre)
        self.apellido = titulo_limpio(apellido)
        self.__dni = ""
        self.dni = dni

    # Esto es @property: permite leer un atributo privado.
    @property
    def dni(self):
        return self.__dni

    # Esto es setter: valida antes de asignar.
    @dni.setter
    def dni(self, nuevo_dni):
        nuevo_dni = str(nuevo_dni).strip()
        if len(nuevo_dni) != 8 or not nuevo_dni.isdigit():
            raise ValueError("El DNI debe tener 8 dígitos numéricos.")
        self.__dni = nuevo_dni

    # Esto es DUNDER __str__: se ejecuta con print(objeto).
    def __str__(self):
        return f"{self.nombre} {self.apellido} - DNI: {self.dni}"

    # Esto es DUNDER __eq__: compara objetos con ==.
    def __eq__(self, otro):
        return isinstance(otro, Persona) and self.dni == otro.dni


# ============================================================
# HERENCIA SIMPLE
# Paciente hereda de Persona.
# ============================================================

class Paciente(Persona):
    edad = ValidarRango(0, 120, "Edad")

    def __init__(self, nombre, apellido, dni, edad):
        super().__init__(nombre, apellido, dni)
        self.edad = edad
        self._sintomas = []
        self._tratamientos = []
        self._diagnosticos = []

    # Esto es property: devuelve copia para proteger la lista interna.
    @property
    def sintomas(self):
        return list(self._sintomas)

    @property
    def tratamientos(self):
        return list(self._tratamientos)

    @property
    def diagnosticos(self):
        return list(self._diagnosticos)

    def agregar_sintoma(self, sintoma):
        sintoma = normalizar(sintoma)
        if sintoma and sintoma not in self._sintomas:
            self._sintomas.append(sintoma)

    def agregar_tratamiento(self, tratamiento):
        self._tratamientos.append(tratamiento)

    def agregar_diagnostico(self, diagnostico):
        diagnostico = titulo_limpio(diagnostico)
        if diagnostico:
            self._diagnosticos.append(diagnostico)

    # Esto es DUNDER __len__: se ejecuta con len(paciente).
    def __len__(self):
        return len(self._tratamientos)

    def mostrar_info(self):
        sintomas = ", ".join(self._sintomas) if self._sintomas else "Sin síntomas"
        diagnosticos = ", ".join(self._diagnosticos) if self._diagnosticos else "Sin diagnósticos"
        return (
            f"{self} | Edad: {self.edad:.0f} | "
            f"Síntomas: {sintomas} | Diagnósticos: {diagnosticos}"
        )


# ============================================================
# HERENCIA SIMPLE
# Doctor hereda de Persona.
# ============================================================

class Doctor(Persona):
    def __init__(self, nombre, apellido, dni, especialidad, colegiatura):
        super().__init__(nombre, apellido, dni)
        self.especialidad = titulo_limpio(especialidad)
        self.colegiatura = str(colegiatura).strip()

    @registrar_consulta
    def diagnosticar(self, paciente, diagnostico):
        paciente.agregar_diagnostico(diagnostico)

    @registrar_consulta
    def asignar_tratamiento(self, paciente, tratamiento):
        paciente.agregar_tratamiento(tratamiento)

    def mostrar_info(self):
        return f"{self} | Especialidad: {self.especialidad} | Colegiatura: {self.colegiatura}"


# ============================================================
# CLASE PARA HERENCIA MÚLTIPLE
# Monitoreo aporta signos vitales.
# Usa descriptor ValidarRango.
# ============================================================

class Monitoreo:
    temperatura = ValidarRango(30, 45, "Temperatura")
    ritmo_cardiaco = ValidarRango(40, 180, "Ritmo cardiaco")

    def mostrar_signos(self):
        return (
            f"Temperatura: {self.temperatura} °C | "
            f"Ritmo cardiaco: {self.ritmo_cardiaco} lpm"
        )


# ============================================================
# HERENCIA MÚLTIPLE
# PacienteCritico hereda de Paciente y Monitoreo.
# ============================================================

class PacienteCritico(Paciente, Monitoreo):
    def __init__(self, nombre, apellido, dni, edad, nivel_riesgo):
        super().__init__(nombre, apellido, dni, edad)
        self.nivel_riesgo = titulo_limpio(nivel_riesgo)

    def generar_alerta(self):
        if self.temperatura is not None and self.temperatura >= 39:
            return "ALERTA: fiebre alta en paciente crítico."
        if self.ritmo_cardiaco is not None and self.ritmo_cardiaco > 120:
            return "ALERTA: ritmo cardiaco elevado."
        return "Paciente crítico estable."

    def mostrar_info(self):
        return f"{super().mostrar_info()} | Riesgo: {self.nivel_riesgo}"


# ============================================================
# POLIMORFISMO
# Todas las clases de tratamiento tienen aplicar(),
# pero cada una lo implementa diferente.
# ============================================================

class TratamientoBase(metaclass=MetaClaseMedica):
    def aplicar(self):
        raise NotImplementedError("Debe implementar aplicar().")


class TratamientoMedicamento(TratamientoBase):
    def aplicar(self):
        return "Aplicando tratamiento con medicamento."


class TratamientoTerapia(TratamientoBase):
    def aplicar(self):
        return "Aplicando tratamiento con terapia."


class TratamientoCirugia(TratamientoBase):
    def aplicar(self):
        return "Aplicando tratamiento quirúrgico."


# ============================================================
# PATRÓN FACTORY
# Esto es Factory porque crea objetos según un tipo.
# ============================================================

class TratamientoFactory:
    @staticmethod
    def crear_tratamiento(tipo):
        tipo = normalizar(tipo)

        if tipo in ("medicamento", "1"):
            return TratamientoMedicamento()
        if tipo in ("terapia", "2"):
            return TratamientoTerapia()
        if tipo in ("cirugia", "cirugía", "3"):
            return TratamientoCirugia()

        raise ValueError("Tipo de tratamiento no válido.")


# ============================================================
# BASE DE CONOCIMIENTO DATASET
# Esto es Singleton porque carga la data una sola vez.
# ============================================================

class BaseConocimientoDataset:
    _instancia = None

    def __new__(cls, ruta_sintomas=RUTA_DATASET_SINTOMAS, ruta_precauciones=RUTA_DATASET_PRECAUCIONES):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializado = False
        return cls._instancia

    def __init__(self, ruta_sintomas=RUTA_DATASET_SINTOMAS, ruta_precauciones=RUTA_DATASET_PRECAUCIONES):
        if self._inicializado:
            return

        self.ruta_sintomas = Path(ruta_sintomas)
        self.ruta_precauciones = Path(ruta_precauciones)

        self.total_casos = 0
        self.conteo_enfermedad = {}
        self.conteo_sintoma_por_enfermedad = {}
        self.sintomas_disponibles = set()
        self.nombre_visible_enfermedad = {}
        self.precauciones = {}

        self._cargar_precauciones()
        self._cargar_sintomas_y_precalcular()

        self._inicializado = True

    def _cargar_precauciones(self):
        if not self.ruta_precauciones.exists():
            return

        with open(self.ruta_precauciones, "r", encoding="utf-8-sig", newline="") as archivo:
            lector = csv.DictReader(archivo)

            for fila in lector:
                enfermedad_original = fila.get("Disease", "") or fila.get("Enfermedad", "")
                enfermedad = normalizar(enfermedad_original)

                lista_precauciones = []
                for i in range(1, 5):
                    valor = fila.get(f"Precaution_{i}", "") or fila.get(f"Precaucion_{i}", "")
                    valor = normalizar(valor)
                    if valor:
                        lista_precauciones.append(valor)

                if enfermedad:
                    self.precauciones[enfermedad] = lista_precauciones

    def _cargar_sintomas_y_precalcular(self):
        if not self.ruta_sintomas.exists():
            print("\n[AVISO] No se encontró la data de síntomas. Se usará dataset demo.")
            self._cargar_dataset_demo()
            return

        with open(self.ruta_sintomas, "r", encoding="utf-8-sig", newline="") as archivo:
            lector = csv.DictReader(archivo)

            for fila in lector:
                enfermedad_original = fila.get("Disease", "") or fila.get("Enfermedad", "")
                enfermedad = normalizar(enfermedad_original)

                if not enfermedad:
                    continue

                self.total_casos += 1
                self.conteo_enfermedad[enfermedad] = self.conteo_enfermedad.get(enfermedad, 0) + 1
                self.nombre_visible_enfermedad[enfermedad] = enfermedad_original.strip()

                if enfermedad not in self.conteo_sintoma_por_enfermedad:
                    self.conteo_sintoma_por_enfermedad[enfermedad] = {}

                sintomas_fila = set()

                for i in range(1, 18):
                    sintoma = normalizar(fila.get(f"Symptom_{i}", "") or fila.get(f"Sintoma_{i}", ""))
                    if sintoma:
                        sintomas_fila.add(sintoma)
                        self.sintomas_disponibles.add(sintoma)

                for sintoma in sintomas_fila:
                    actual = self.conteo_sintoma_por_enfermedad[enfermedad].get(sintoma, 0)
                    self.conteo_sintoma_por_enfermedad[enfermedad][sintoma] = actual + 1

    def _cargar_dataset_demo(self):
        datos = [
            ("Gripe", ["fiebre", "tos", "dolor de cabeza", "cansancio"]),
            ("Resfriado comun", ["tos", "estornudos", "congestion nasal"]),
            ("Dengue", ["fiebre", "dolor muscular", "dolor articular"]),
            ("Gastritis", ["dolor abdominal", "nauseas", "vomitos"]),
            ("Covid 19", ["fiebre", "tos", "perdida del olfato", "cansancio"]),
        ]

        for enfermedad_original, sintomas in datos:
            enfermedad = normalizar(enfermedad_original)
            self.total_casos += 1
            self.conteo_enfermedad[enfermedad] = 1
            self.nombre_visible_enfermedad[enfermedad] = enfermedad_original
            self.conteo_sintoma_por_enfermedad[enfermedad] = {}

            for sintoma in sintomas:
                sintoma = normalizar(sintoma)
                self.sintomas_disponibles.add(sintoma)
                self.conteo_sintoma_por_enfermedad[enfermedad][sintoma] = 1

    def resumen(self):
        return {
            "total_casos": self.total_casos,
            "total_enfermedades": len(self.conteo_enfermedad),
            "total_sintomas": len(self.sintomas_disponibles),
        }

    def buscar_sintomas(self, texto):
        texto = normalizar(texto)
        encontrados = []

        for sintoma in sorted(self.sintomas_disponibles):
            if texto in sintoma:
                encontrados.append(sintoma)

        return encontrados[:30]

    def obtener_precauciones(self, enfermedad):
        return self.precauciones.get(normalizar(enfermedad), [])


# ============================================================
# MOTOR BAYESIANO
# Calcula P(enfermedad | síntomas).
# Usa logaritmos para evitar valores extremadamente pequeños.
# Está optimizado porque usa conteos precalculados.
# ============================================================

class MotorBayes:
    def __init__(self, base_conocimiento):
        self.base = base_conocimiento

    @registrar_prediccion
    def predecir(self, sintomas_paciente, limite=5):
        sintomas_paciente = [normalizar(s) for s in sintomas_paciente if normalizar(s)]

        if not sintomas_paciente:
            return []

        resultados_log = {}

        for enfermedad, total_enfermedad in self.base.conteo_enfermedad.items():
            # Probabilidad previa P(enfermedad)
            prob_previa = total_enfermedad / self.base.total_casos
            log_prob = math.log(prob_previa)

            conteos_sintomas = self.base.conteo_sintoma_por_enfermedad.get(enfermedad, {})

            # Naive Bayes: multiplicación de P(síntoma | enfermedad)
            for sintoma in sintomas_paciente:
                casos_sintoma = conteos_sintomas.get(sintoma, 0)

                # Suavizado de Laplace para evitar probabilidad cero.
                prob_sintoma = (casos_sintoma + 1) / (total_enfermedad + 2)
                log_prob += math.log(prob_sintoma)

            resultados_log[enfermedad] = log_prob

        # Normalización tipo softmax para mostrar porcentajes.
        max_log = max(resultados_log.values())
        exp_resultados = {
            enf: math.exp(valor - max_log)
            for enf, valor in resultados_log.items()
        }
        suma_exp = sum(exp_resultados.values())

        resultados = []

        for enfermedad, valor_exp in exp_resultados.items():
            probabilidad = valor_exp / suma_exp
            coincidencias = self._contar_coincidencias(enfermedad, sintomas_paciente)

            resultados.append({
                "enfermedad": self.base.nombre_visible_enfermedad.get(enfermedad, enfermedad),
                "probabilidad": probabilidad,
                "porcentaje": probabilidad * 100,
                "coincidencias": coincidencias,
                "precauciones": self.base.obtener_precauciones(enfermedad),
            })

        resultados.sort(key=lambda x: x["probabilidad"], reverse=True)
        return resultados[:limite]

    def _contar_coincidencias(self, enfermedad, sintomas_paciente):
        conteos = self.base.conteo_sintoma_por_enfermedad.get(enfermedad, {})
        return sum(1 for sintoma in sintomas_paciente if sintoma in conteos)


# ============================================================
# REGISTRO MÉDICO CENTRAL
# Esto es Singleton y también funciona como GESTOR.
# Administra pacientes: agregar, buscar y listar.
# ============================================================

class RegistroMedicoCentral:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.pacientes = []
            cls._instancia.doctores = []
        return cls._instancia

    def registrar_paciente(self, paciente):
        existente = self.buscar_paciente(paciente.dni)

        if existente is not None:
            print("Ya existe un paciente con ese DNI.")
            return

        self.pacientes.append(paciente)
        print("Paciente registrado correctamente.")

    def buscar_paciente(self, dni):
        dni = str(dni).strip()

        for paciente in self.pacientes:
            if paciente.dni == dni:
                return paciente

        return None

    def listar_pacientes(self):
        if len(self.pacientes) == 0:
            print("No hay pacientes registrados.")
            return

        print("\n--- LISTA DE PACIENTES ---")
        for paciente in self.pacientes:
            print("- " + paciente.mostrar_info())

    def registrar_doctor(self, doctor):
        existente = self.buscar_doctor(doctor.dni)

        if existente is not None:
            print("Ya existe un doctor con ese DNI.")
            return

        self.doctores.append(doctor)
        print("Doctor registrado correctamente.")

    def buscar_doctor(self, dni):
        dni = str(dni).strip()

        for doctor in self.doctores:
            if doctor.dni == dni:
                return doctor

        return None

    def listar_doctores(self):
        if len(self.doctores) == 0:
            print("No hay doctores registrados.")
            return

        print("\n--- LISTA DE DOCTORES ---")
        for doctor in self.doctores:
            print("- " + doctor.mostrar_info())

    def obtener_doctor_principal(self):
        if len(self.doctores) > 0:
            return self.doctores[0]

        return None

    def __len__(self):
        return len(self.pacientes)


# ============================================================
# PERSISTENCIA SIMPLE EN JSON
# Guarda pacientes y resultados.
# ============================================================

class PersistenciaJSON:
    def __init__(self, archivo=RUTA_REGISTRO):
        self.archivo = Path(archivo)

    def guardar(self, registro):
        datos = []

        for p in registro.pacientes:
            datos.append({
                "nombre": p.nombre,
                "apellido": p.apellido,
                "dni": p.dni,
                "edad": p.edad,
                "tipo": p.__class__.__name__,
                "sintomas": p.sintomas,
                "diagnosticos": p.diagnosticos,
                "cantidad_tratamientos": len(p),
            })

        with open(self.archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

        print(f"Datos guardados en: {self.archivo.name}")


# ============================================================
# SISTEMA CLI
# Interfaz por consola.
# ============================================================

class SistemaInteligente:
    def __init__(self):
        print("Cargando datasets...")
        self.base = BaseConocimientoDataset()
        self.motor_bayes = MotorBayes(self.base)
        self.registro = RegistroMedicoCentral()
        self.persistencia = PersistenciaJSON()

        self.doctor_demo = Doctor(
            "Carlos",
            "Rojas",
            "87654321",
            "Medicina General",
            "CMP-001"
        )
        #Doctor por defecto registrado en el sistema
        self.registro.registrar_doctor(self.doctor_demo)

        resumen = self.base.resumen()
        print("Dataset cargado correctamente.")
        print(f"Casos: {resumen['total_casos']}")
        print(f"Enfermedades: {resumen['total_enfermedades']}")
        print(f"Síntomas disponibles: {resumen['total_sintomas']}")

    def menu(self):
        while True:
            print("\n" + "=" * 60)
            print("SISTEMA INTELIGENTE DE GESTIÓN DE PACIENTES")
            print("=" * 60)
            print("1. Registrar paciente")
            print("2. Registrar paciente crítico")
            print("3. Registrar doctor")
            print("4. Agregar síntomas a paciente")
            print("5. Realizar predicción bayesiana")
            print("6. Asignar tratamiento")
            print("7. Registrar signos vitales de paciente crítico")
            print("8. Mostrar pacientes")
            print("9. Mostrar doctores")
            print("10. Buscar síntomas en la data")
            print("11. Guardar información en JSON")
            print("12. Cargar caso de prueba")
            print("0. Salir")

            opcion = input("Seleccione una opción: ").strip()

            try:
                if opcion == "1":
                    self.registrar_paciente()
                elif opcion == "2":
                    self.registrar_paciente_critico()
                elif opcion == "3":
                    self.registrar_doctor()
                elif opcion == "4":
                    self.agregar_sintomas()
                elif opcion == "5":
                    self.realizar_prediccion()
                elif opcion == "6":
                    self.asignar_tratamiento()
                elif opcion == "7":
                    self.registrar_signos()
                elif opcion == "8":
                    self.registro.listar_pacientes()
                elif opcion == "9":
                    self.registro.listar_doctores()
                elif opcion == "10":
                    self.buscar_sintomas()
                elif opcion == "11":
                    self.persistencia.guardar(self.registro)
                elif opcion == "12":
                    self.cargar_caso_prueba()
                elif opcion == "0":
                    print("Saliendo del sistema.")
                    break
                else:
                    print("Opción no válida.")
            except Exception as error:
                print(f"Error: {error}")

    def registrar_doctor(self):
        print("\n--- REGISTRAR DOCTOR ---")
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        dni = input("DNI: ")
        especialidad = input("Especialidad: ")
        colegiatura = input("Número de colegiatura: ")

        doctor = Doctor(nombre, apellido, dni, especialidad, colegiatura)
        self.registro.registrar_doctor(doctor)

    def registrar_paciente(self):
        print("\n--- REGISTRAR PACIENTE ---")
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        dni = input("DNI: ")
        edad = input("Edad: ")

        paciente = Paciente(nombre, apellido, dni, edad)
        self.registro.registrar_paciente(paciente)

    def registrar_paciente_critico(self):
        print("\n--- REGISTRAR PACIENTE CRÍTICO ---")
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        dni = input("DNI: ")
        edad = input("Edad: ")
        riesgo = input("Nivel de riesgo: ")

        paciente = PacienteCritico(nombre, apellido, dni, edad, riesgo)
        self.registro.registrar_paciente(paciente)

    def _pedir_paciente(self):
        dni = input("DNI del paciente: ")
        paciente = self.registro.buscar_paciente(dni)

        if paciente is None:
            print("Paciente no encontrado.")
            return None

        return paciente

    def agregar_sintomas(self):
        print("\n--- AGREGAR SÍNTOMAS ---")
        paciente = self._pedir_paciente()

        if paciente is None:
            return

        print("Ingrese síntomas separados por coma.")
        print("Ejemplo: itching, skin rash, nodal skin eruptions")
        entrada = input("Síntomas: ")

        sintomas = entrada.split(",")

        for sintoma in sintomas:
            paciente.agregar_sintoma(sintoma)

        print("Síntomas registrados:")
        print(", ".join(paciente.sintomas))

    def realizar_prediccion(self):
        print("\n--- PREDICCIÓN BAYESIANA ---")
        paciente = self._pedir_paciente()

        if paciente is None:
            return

        if len(paciente.sintomas) == 0:
            print("El paciente no tiene síntomas registrados.")
            return

        resultados = self.motor_bayes.predecir(paciente.sintomas, limite=5)

        print("\nResultados más probables:")
        for i, r in enumerate(resultados, start=1):
            print(f"\n{i}. {r['enfermedad']}")
            print(f"   Probabilidad: {r['porcentaje']:.2f}%")
            print(f"   Coincidencias: {r['coincidencias']}")

            if r["precauciones"]:
                print("   Precauciones:")
                for precaucion in r["precauciones"]:
                    print(f"   - {precaucion}")

            if resultados:
                enfermedad_principal = resultados[0]["enfermedad"]
                doctor = self.registro.obtener_doctor_principal()
                if doctor is None:
                    doctor = self.doctor_demo
                doctor.diagnosticar(paciente, enfermedad_principal)

    def asignar_tratamiento(self):
        print("\n--- ASIGNAR TRATAMIENTO ---")
        paciente = self._pedir_paciente()

        if paciente is None:
            return

        print("1. Medicamento")
        print("2. Terapia")
        print("3. Cirugía")

        tipo = input("Tipo de tratamiento: ")
        tratamiento = TratamientoFactory.crear_tratamiento(tipo)

        doctor = self.registro.obtener_doctor_principal()

        if doctor is None:
            doctor = self.doctor_demo

        doctor.asignar_tratamiento(paciente, tratamiento)

        print("Tratamiento asignado:")
        print(tratamiento.aplicar())

    def registrar_signos(self):
        print("\n--- REGISTRAR SIGNOS VITALES ---")
        paciente = self._pedir_paciente()

        if paciente is None:
            return

        if not isinstance(paciente, PacienteCritico):
            print("Solo los pacientes críticos tienen monitoreo.")
            return

        paciente.temperatura = input("Temperatura: ")
        paciente.ritmo_cardiaco = input("Ritmo cardiaco: ")

        print(paciente.mostrar_signos())
        print(paciente.generar_alerta())

    def buscar_sintomas(self):
        print("\n--- BUSCAR SÍNTOMAS EN LA DATA ---")
        texto = input("Buscar síntoma: ")
        encontrados = self.base.buscar_sintomas(texto)

        if not encontrados:
            print("No se encontraron síntomas.")
            print("Verifica que estés usando DiseaseAndSymptoms_ES_COMPAT.csv o DiseaseAndSymptoms_ES.csv en la misma carpeta del programa.")
            return

        print("Síntomas encontrados:")
        for sintoma in encontrados:
            print("- " + sintoma)

    def cargar_caso_prueba(self):
        print("\n--- CARGANDO CASO DE PRUEBA ---")

        paciente = PacienteCritico(
            "Luis",
            "Pérez",
            "12345678",
            25,
            "Alto"
        )

        # Síntomas presentes en la data subida.
        paciente.agregar_sintoma("picazón")
        paciente.agregar_sintoma("erupción en la piel")
        paciente.agregar_sintoma("erupciones nodulares en la piel")

        paciente.temperatura = 38
        paciente.ritmo_cardiaco = 90

        self.registro.registrar_paciente(paciente)

        print("Caso de prueba cargado.")
        print(paciente.mostrar_info())
        print(paciente.mostrar_signos())


# ============================================================
# PUNTO DE ENTRADA
# ============================================================

if __name__ == "__main__":
    sistema = SistemaInteligente()
    sistema.menu()
