# Proposal: Preservación de Indentación YAML en PDF y Exportación de Manifiestos

## Why

Al copiar fragmentos de código o manifiestos YAML desde el documento PDF `k8s-exercises-workbook.pdf` hacia ficheros locales (ej. `pod.yaml`), los visores de PDF recortan los espacios a la izquierda de cada línea por el algoritmo de extracción y coalescencia de líneas de texto, haciendo que el YAML resultante sea sintácticamente inválido e inutilizable para `kubectl`.
Para solucionar este problema de raíz y mejorar la experiencia de laboratorio de los alumnos, es necesario asegurar que la selección y copia de texto en el PDF preserve el 100% de la indentación original, y simultáneamente proporcionar un directorio estructurado con los 42 manifiestos YAML listos para ser aplicados directamente en el clúster.

## What Changes

- **Preservación de indentación en PDF con `/ActualText`**: Actualización del pipeline de generación y compilación en `scripts/generate_html_pdf.py` para interceptar bloques de código y utilizar marcado semántico ISO 32000-1 (`/ActualText`) y reglas CSS de espaciado estricto, garantizando que al seleccionar y copiar texto desde cualquier visor (Evince, Chrome, Acrobat, etc.) se preserven todos los espacios iniciales de sangría.
- **Exportación de manifiestos declarativos (`manifests/`)**: Generación automatizada del directorio `manifests/` conteniendo los 42 ficheros YAML comentados y organizados por carpetas modulares (`manifests/01-pods/`, `manifests/02-replicasets/`, ..., `manifests/14-kustomize/`).
- **Comprobación y validación**: Extensión de `scripts/verify_workbook.py` para validar que el texto extraído de los bloques de código en el PDF mantiene la indentación correcta y verificar la existencia e integridad de los 42 ficheros YAML exportados.
- **Actualización de documentación**: Actualización de `README.md` reflejando la nueva carpeta de manifiestos y las instrucciones de uso rápido con `kubectl apply -f manifests/...`.

## Capabilities

### New Capabilities
- `k8s-manifests-export`: Generación y estructura del árbol de ficheros de manifiestos YAML independientes organizados por módulo para ejecución directa en el clúster.

### Modified Capabilities
- `pdf-document-generation`: Incorpora el requisito de preservación estricta de espacios en blanco e indentación en bloques de código copiables a través de marcado `/ActualText` en el pipeline de compilación.

## Impact

- **Generador PDF**: `scripts/generate_html_pdf.py` añade la rutina de inyección `/ActualText` en el flujo de post-procesado con `pypdf` y refina estilos de `<pre>`/`<code>`.
- **Estructura del Repositorio**: Se introduce el directorio `manifests/` con 14 subdirectorios y 42 archivos YAML.
- **Validación**: `scripts/verify_workbook.py` incorpora aserciones sobre la indentación en la extracción de texto y sobre la paridad de los manifiestos en disco.
