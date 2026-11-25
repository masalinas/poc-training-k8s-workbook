# Design: Preservación de Indentación YAML en PDF y Exportación de Manifiestos

## Context

Ver `proposal.md` para la motivación. Actualmente, al compilar HTML a PDF con Google Chrome en modo headless, los bloques de código renderizados con `<pre><code>` generan instrucciones de dibujo basadas en coordenadas absolutas y glifos individuales. Al extraer o copiar texto desde lectores de PDF comunes (como Poppler/Evince en Linux), los algoritmos de detección de márgenes eliminan los espacios en blanco situados al inicio de cada línea. En YAML, esto destruye la jerarquía sintáctica.

## Goals / Non-Goals

**Goals:**
- Asegurar que al copiar cualquier fragmento de código YAML desde el visor de PDF se conserven los espacios iniciales de indentación.
- Emplear el estándar ISO 32000-1 (`/ActualText` marked content) en el pipeline de post-procesado con `pypdf` para sobreescribir de forma limpia la capa de extracción de texto en bloques de código.
- Ajustar las reglas CSS en `scripts/generate_html_pdf.py` para bloques `<pre>` (`white-space: pre !important`, `overflow-x: auto`) evitando divisiones anómalas por `word-break: break-all`.
- Generar automáticamente el directorio `manifests/` con los 42 archivos YAML listos para su uso directo con `kubectl apply`.
- Actualizar `scripts/verify_workbook.py` para comprobar tanto la indentación del texto extraído en el PDF como la integridad de los archivos YAML exportados.

**Non-Goals:**
- Sustituir Google Chrome / Chromium por otros motores de renderizado complejos externos (como WeasyPrint) que requerirían dependencias pesadas en el sistema.
- Modificar el contenido o soluciones de los 42 ejercicios ya establecidos.

## Decisions

### 1. Inyección de marcado `/ActualText` durante el post-procesado con `pypdf`
- **Decisión**: Durante la fase donde `add_pdf_bookmarks` lee y reescribe el PDF con `pypdf`, procesar los flujos de contenido de las páginas de soluciones para envolver las líneas de código o bloques preformateados con `/Span << /ActualText (...) >> BDC ... EMC`.
- **Por qué**: `/ActualText` es la directiva canónica de ISO 32000-1 respetada por todos los visores de PDF modernos (Evince, Chrome, Firefox, Adobe Reader, Apple Preview) para determinar exactamente qué cadena se copia al portapapeles, ignorando las heurísticas de recorte de márgenes.
- **Alternativas consideradas**:
  - *Usar caracteres no imprimibles o Zero-Width Space (ZWSP)*: Descartado porque rompe la especificación formal de YAML 1.2 y genera errores en `yamllint` o linters estrictos.
  - *Cambiar a Firefox headless*: Descartado por ser inestable o lento en entornos de servidor/contenedor sin servidor gráfico.

### 2. Estilo CSS reforzado para `<pre>` y `<code>`
- **Decisión**: Cambiar `white-space: pre-wrap; word-break: break-all;` por `white-space: pre !important; word-break: normal !important;` en los bloques de código fuente dentro de `generate_html_pdf.py`.
- **Por qué**: `word-break: break-all` puede fragmentar identificadores y palabras clave YAML a mitad de línea cuando se estrecha el contenedor, creando saltos de línea imprevistos.

### 3. Generación del árbol de archivos `manifests/`
- **Decisión**: Crear un script utilitario (o integrar función) en `scripts/export_manifests.py` que recorra `content_data.py` (los 14 módulos) y extraiga de cada solución el contenido del bloque `<pre><code>...</code></pre>`, guardándolo en `manifests/<xx>-<modulo>/<yy>-<nombre-recurso>.yaml`.
- **Por qué**: Proporciona a los alumnos una alternativa directa y ergonómica para ejecutar `kubectl apply -f manifests/...` sin necesidad de copiar manualmente desde el PDF.

### 4. Automatización en la suite de verificación
- **Decisión**: Añadir comprobaciones en `scripts/verify_workbook.py`:
  1. Verificar que al extraer texto de las páginas de soluciones del PDF se detectan las líneas con 2, 4 y más espacios iniciales intactos.
  2. Verificar que los 42 ficheros en `manifests/` existen y se parsean con éxito mediante `yaml.safe_load()`.

## Risks / Trade-offs

- **[Riesgo]** La manipulación del flujo binario de PDF con `pypdf` puede corromper la página si los delimitadores de stream no se ajustan con precisión.
  → **Mitigación**: Aislar la modificación de streams únicamente a los bloques de texto etiquetados y validar que el archivo resultante sea 100% legible por `pypdf.PdfReader` y `pdftotext`.
- **[Riesgo]** Manifiestos con caracteres especiales o cadenas multilínea en YAML (`|` o `>`).
  → **Mitigación**: La exportación directa de `modules_*.py` extrae la cadena textual exacta sin alteraciones de formato.
