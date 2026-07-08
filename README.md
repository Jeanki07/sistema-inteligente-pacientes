# Sistema Inteligente de Gestión de Pacientes con Predicción Bayesiana

## Descripción general

Este proyecto consiste en el desarrollo de un **Sistema Inteligente de Gestión de Pacientes**, implementado en Python, que permite registrar pacientes, doctores, síntomas, diagnósticos y tratamientos. Además, incorpora un módulo de **predicción bayesiana** para estimar enfermedades probables a partir de los síntomas ingresados por el usuario.

El sistema fue desarrollado como proyecto académico del curso **Programación Orientada a Objetos Avanzada**, aplicando conceptos como encapsulamiento, herencia simple, herencia múltiple, polimorfismo, métodos especiales, propiedades, descriptores, decoradores, metaclases y patrones de diseño.

El proyecto pertenece al dominio de la medicina, ya que trabaja con entidades como pacientes, doctores, enfermedades, síntomas, signos vitales y tratamientos.

> **Nota importante:** este sistema tiene finalidad académica. La predicción generada no reemplaza el diagnóstico de un profesional de salud.

---

## Problemática

En muchos contextos médicos o académicos, el registro de pacientes, síntomas, diagnósticos y tratamientos puede realizarse de forma manual o poco estructurada. Esto puede generar problemas como:

- Dificultad para organizar información de pacientes.
- Pérdida o duplicidad de registros.
- Falta de control sobre diagnósticos y tratamientos.
- Dificultad para consultar síntomas relacionados con enfermedades.
- Ausencia de una herramienta computacional que oriente posibles enfermedades según los síntomas registrados.

Además, cuando un paciente presenta varios síntomas al mismo tiempo, puede ser difícil identificar de manera rápida qué enfermedad podría estar asociada. Por ello, se plantea un sistema que no solo gestione información médica básica, sino que también utilice un modelo probabilístico para apoyar la identificación de enfermedades probables.

---

## Solución propuesta

La solución consiste en desarrollar un sistema en Python que permita:

- Registrar pacientes normales.
- Registrar pacientes críticos.
- Registrar doctores.
- Agregar síntomas a un paciente.
- Buscar síntomas dentro de la base de datos médica.
- Realizar una predicción bayesiana de enfermedades.
- Registrar diagnósticos probables.
- Asignar tratamientos.
- Registrar signos vitales.
- Guardar información en formato JSON.

El sistema utiliza archivos CSV con información médica traducida al español. De esta manera, el usuario puede ingresar síntomas como:

- fatiga
- fiebre alta
- dolor de cabeza
- tos
- náuseas
- dolor abdominal

Luego, el sistema compara esos síntomas con la data médica y calcula las enfermedades más probables.

---

## Metodología aplicada: CRISP-DM

El desarrollo del proyecto se organizó siguiendo la metodología **CRISP-DM**, utilizada en proyectos basados en datos.

### 1. Comprensión del problema

Se identificó la necesidad de construir un sistema que permita gestionar pacientes y utilizar síntomas como evidencia para estimar enfermedades probables.

### 2. Comprensión de los datos

Se analizaron dos archivos CSV:

- `DiseaseAndSymptoms_ES.csv`: contiene enfermedades y síntomas asociados.
- `Disease_precaution_ES.csv`: contiene precauciones recomendadas según la enfermedad.

### 3. Preparación de los datos

La data original fue adaptada al español para mejorar la interacción del usuario con el sistema. También se normalizaron los textos para facilitar la búsqueda y comparación de síntomas.

### 4. Modelado

Se implementó un motor de predicción basado en **Naive Bayes**, donde:

- La enfermedad es la clase a predecir.
- Los síntomas son las evidencias.
- El sistema calcula qué enfermedad es más probable según los síntomas ingresados.

### 5. Evaluación

El sistema se evaluó mediante casos de prueba como registro de pacientes, búsqueda de síntomas, predicción bayesiana, asignación de tratamientos y validación de signos vitales.

### 6. Despliegue

El sistema se ejecuta desde consola mediante un menú interactivo desarrollado en Python.

---

## Funcionamiento del sistema

El flujo general del sistema es el siguiente:

```text
Inicio del programa
        ↓
Carga de data médica en español
        ↓
Registro de paciente o paciente crítico
        ↓
Registro de doctor
        ↓
Ingreso de síntomas
        ↓
Predicción bayesiana
        ↓
Registro del diagnóstico probable
        ↓
Asignación de tratamiento
        ↓
Guardado de información en JSON
```

---

## Menú principal

```text
SISTEMA INTELIGENTE DE GESTIÓN DE PACIENTES

1. Registrar paciente
2. Registrar paciente crítico
3. Registrar doctor
4. Agregar síntomas a paciente
5. Realizar predicción bayesiana
6. Asignar tratamiento
7. Registrar signos vitales de paciente crítico
8. Mostrar pacientes
9. Mostrar doctores
10. Buscar síntomas en la data
11. Guardar información en JSON
12. Cargar caso de prueba
0. Salir
```

---

## Conceptos de Programación Orientada a Objetos aplicados

### Clases y objetos

El sistema está organizado mediante clases que representan entidades del dominio médico.

Principales clases utilizadas:

- `Persona`
- `Paciente`
- `Doctor`
- `PacienteCritico`
- `Monitoreo`
- `ValidarRango`
- `TratamientoBase`
- `TratamientoMedicamento`
- `TratamientoTerapia`
- `TratamientoCirugia`
- `TratamientoFactory`
- `MotorBayes`
- `RegistroMedicoCentral`
- `PersistenciaJSON`

### Encapsulamiento

Se utiliza encapsulamiento para proteger atributos importantes, como el DNI de una persona, controlando su acceso mediante propiedades.

### Herencia simple

La clase `Paciente` y la clase `Doctor` heredan de la clase base `Persona`.

```text
Persona
 ├── Paciente
 └── Doctor
```

Esto evita duplicar atributos comunes como nombre, apellido y DNI.

### Herencia múltiple

La clase `PacienteCritico` hereda de `Paciente` y `Monitoreo`.

```text
PacienteCritico(Paciente, Monitoreo)
```

Esto permite que un paciente crítico tenga datos personales, síntomas, diagnósticos y también signos vitales como temperatura y ritmo cardiaco.

### Polimorfismo

El sistema aplica polimorfismo en los tratamientos. Todas las clases de tratamiento tienen el método `aplicar()`, pero cada una lo ejecuta de forma diferente.

Ejemplos:

- `TratamientoMedicamento`
- `TratamientoTerapia`
- `TratamientoCirugia`

### Métodos dunder

Se utilizan métodos especiales de Python para personalizar el comportamiento de los objetos:

- `__str__()`: muestra información del objeto.
- `__len__()`: devuelve la cantidad de tratamientos o registros.
- `__eq__()`: compara objetos mediante el DNI.

### Descriptores

Se utiliza un descriptor para validar signos vitales, como temperatura y ritmo cardiaco. Esto evita ingresar valores fuera de rango.

### Decoradores

El sistema usa decoradores para registrar acciones importantes como consultas médicas y predicciones bayesianas.

### Metaclases

Se aplica una metaclase para controlar la creación de clases médicas y asegurar que algunas clases cumplan con métodos obligatorios.

### Patrón Factory

El patrón Factory se utiliza para crear tratamientos según la opción seleccionada por el usuario.

### Patrón Singleton

El patrón Singleton se aplica en el registro médico central, garantizando que exista una única instancia encargada de almacenar pacientes y doctores.

---

## Predicción bayesiana

El sistema utiliza una versión simplificada de **Naive Bayes** para estimar enfermedades probables según los síntomas registrados.

La idea general es:

```text
P(Enfermedad | Síntomas)
```

Esto significa calcular la probabilidad de una enfermedad dado que el paciente presenta ciertos síntomas.

El sistema evalúa las enfermedades disponibles en la data y muestra las más probables ordenadas de mayor a menor probabilidad.

---

## Archivos del repositorio

```text
Sistema_Inteligente_Pacientes/
├── sistema_inteligente_pacientes.py
├── DiseaseAndSymptoms_ES.csv
├── Disease_precaution_ES.csv
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Requisitos

El sistema fue desarrollado con Python 3.

No requiere librerías externas, ya que utiliza módulos estándar de Python, como:

- `csv`
- `json`
- `math`
- `pathlib`
- `functools`
- `unicodedata`

---

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/Jeanki07/sistema-inteligente-pacientes.git
```

Entrar a la carpeta:

```bash
cd sistema-inteligente-pacientes
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## Ejecución

Ejecutar el sistema con:

```bash
python sistema_inteligente_pacientes.py
```

O también:

```bash
python3 sistema_inteligente_pacientes.py
```

---

## Ejemplo de uso

1. Registrar un paciente.
2. Registrar un doctor.
3. Agregar síntomas al paciente.
4. Realizar predicción bayesiana.
5. Revisar las enfermedades probables.
6. Asignar un tratamiento.
7. Guardar la información.

Ejemplo de síntomas:

```text
fatiga, fiebre alta, dolor de cabeza
```

---

## Resultados esperados

El sistema debe mostrar una lista de enfermedades probables según los síntomas ingresados. También debe permitir registrar diagnósticos, asignar tratamientos y guardar información en un archivo JSON.

---

## Limitaciones

- La predicción depende de la calidad de la data utilizada.
- El modelo Naive Bayes asume independencia entre síntomas.
- El sistema no reemplaza la evaluación de un profesional de salud.
- El proyecto tiene finalidad académica.

---

## Autor

**Frank Bustamante**  
Universidad Nacional Toribio Rodríguez de Mendoza de Amazonas  
Escuela Profesional de Ingeniería en Ciencia de Datos e Inteligencia Artificial

---

## Estado del proyecto

Proyecto funcional para presentación académica.
