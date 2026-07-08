# Sistema Inteligente de Gestión de Pacientes

Proyecto académico desarrollado en Python para la gestión de pacientes, doctores, síntomas, diagnósticos y tratamientos. El sistema utiliza una predicción bayesiana para estimar enfermedades probables a partir de síntomas ingresados por el usuario.

## Descripción del proyecto

El sistema permite registrar pacientes normales y pacientes críticos, registrar doctores, agregar síntomas, realizar una predicción aproximada de enfermedad, asignar tratamientos y guardar información mediante persistencia en archivos JSON.

La predicción se realiza usando una data médica en español, donde cada enfermedad se relaciona con un conjunto de síntomas. El sistema aplica una lógica basada en Naive Bayes para calcular las enfermedades más probables según los síntomas ingresados.

Este sistema es de uso académico y no reemplaza un diagnóstico médico profesional.

## Archivos del proyecto

```text
Sistema_Inteligente_Pacientes/
├── sistema_inteligente_es_corregido.py
├── DiseaseAndSymptoms_ES.csv
├── Disease_precaution_ES.csv
├── README.md
├── .gitignore
└── requirements.txt
cat > requirements.txt <<'EOF'
# No se requieren librerías externas.
# El sistema usa únicamente módulos estándar de Python.
