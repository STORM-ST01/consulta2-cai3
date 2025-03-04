# Consulta2-CAI3

Este proyecto incluye dos scripts para evaluar y clasificar algoritmos de cifrado basados en datos experimentales.

## Requisitos

Asegúrate de tener instalados los siguientes paquetes en un entorno virtual.

### Crear un entorno virtual

```sh
python -m venv venv
source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
```

### Instalar los paquetes requeridos

```sh
pip install -r requirements.txt
```

## Ejecución de los Scripts

### 1. Script de Evaluación

Este script evalúa el rendimiento de diferentes algoritmos de cifrado en archivos DICOM.

#### Uso

1. Coloca tus archivos DICOM en el mismo directorio que el script.
2. Ejecuta el script:

```sh
python evaluacion.py
```

3. El script procesará los archivos DICOM y generará un archivo CSV llamado `resultados_cifrado.csv` con los resultados de la evaluación.

### 2. Script de Clasificación

Este script clasifica los algoritmos de cifrado basándose en los resultados de la evaluación utilizando el método TOPSIS.

#### Uso

1. Asegúrate de que el archivo `resultados_cifrado.csv` generado por el script `evaluacion.py` esté en el mismo directorio.
2. Ejecuta el script:

```sh
python ranking.py
```

3. El script generará un archivo CSV llamado `ranking_topsis.csv` con los resultados de la clasificación.

## Notas

- Asegúrate de que los archivos DICOM estén correctamente nombrados y colocados en el mismo directorio que los scripts.
- Los scripts asumen que los archivos DICOM no están vacíos y se pueden leer correctamente.