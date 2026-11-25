# Tasks

## 1. Ajuste de Estilos CSS y Marcado de Bloques de Código en HTML

- [x] 1.1 Reforzar en `scripts/generate_html_pdf.py` las reglas de estilo de `<pre>` (`white-space: pre !important; word-break: normal !important; overflow-wrap: normal !important;`) para evitar fragmentaciones anómalas de indentación y comprobar el HTML generado con `python3 scripts/generate_html_pdf.py`.
- [x] 1.2 Enriquecer los bloques de código en la generación HTML para facilitar la identificación de líneas de código y delimitadores de manifiestos.
- [x] 1.3 Normalizar las continuaciones de comando multilínea en los módulos a una única barra invertida (`\`), eliminando las dobles barras de escape (`\\`).

## 2. Inyección de Marcado `/ActualText` en el Pipeline PDF

- [x] 2.1 Implementar la rutina de post-procesado con `pypdf` en `scripts/generate_html_pdf.py` para inyectar marcadores `/ActualText` (ISO 32000-1) preservando espacios en blanco exactos por línea en los bloques de manifiestos YAML.
- [x] 2.2 Recompilar el cuaderno con `python3 scripts/generate_html_pdf.py` y verificar con `pdftotext` que al extraer texto de las soluciones se conservan las sangrías de 2, 4 y más espacios.

## 3. Generación y Exportación del Directorio `manifests/`

- [x] 3.1 Crear el módulo de exportación `scripts/export_manifests.py` que recorra los 14 módulos de `content_data.py` y vuelque los 42 manifiestos YAML a `manifests/<xx>-<modulo>/<yy>-<nombre>.yaml` con comentarios de cabecera y namespace asignado.
- [x] 3.2 Ejecutar la exportación y comprobar que los 42 archivos existen y son parseables mediante un validador sintáctico YAML.

## 4. Pruebas de Integración y Actualización Documental

- [x] 4.1 Extender `scripts/verify_workbook.py` para incluir pruebas automatizadas de indentación del PDF (`pdftotext` sin `-layout`) y validación de los 42 manifiestos exportados en `manifests/`.
- [x] 4.2 Actualizar `README.md` documentando la nueva carpeta `manifests/` y la preservación de sangría al copiar desde el PDF.
- [x] 4.3 Ejecutar `python3 scripts/verify_workbook.py` asegurando que todas las verificaciones pasan al 100%.
