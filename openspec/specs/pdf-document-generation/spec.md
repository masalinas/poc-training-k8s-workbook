# pdf-document-generation Specification

## Purpose

Define el motor de maquetación, estilo visual profesional y compilación automatizada del documento PDF con soporte para doble índice interactivo (TOC interno y marcadores PDF en panel lateral).

## Requirements

### Requirement: Estilo visual editorial y fidelidad gráfica
El documento PDF generado SHALL mantener una estética profesional idéntica a la plantilla de referencia de k8s-installation-steps.pdf, incluyendo formato A4, tipografías Inter y JetBrains Mono, paleta cromática Kubernetes, portada con metadatos, banners temáticos y cajas de advertencia y tips.

#### Scenario: Inspección visual de la maquetación y bloques de código
- **WHEN** se renderiza y visualiza el archivo PDF
- **THEN** el documento presenta paginación continua en cabecera/pie, resaltado oscuro con ajuste de línea en bloques de código y contenedores informativos estilizados.

### Requirement: Índice analítico interactivo interno (TOC)
El documento SHALL incluir un índice general de contenidos tras la portada y el resumen con hipervínculos activos que permitan saltar a cualquier recurso, ejercicio o solución con un solo clic.

#### Scenario: Clic en elemento del índice interno
- **WHEN** el usuario hace clic sobre cualquier entrada del índice de contenidos
- **THEN** el visor navega de forma instantánea a la página exacta que contiene la sección, ejercicio o solución solicitada.

### Requirement: Marcadores jerárquicos integrados en el visor de PDF (Outlines)
El archivo PDF final SHALL contener un árbol jerárquico de marcadores nativos (Document Outlines) visible en el panel lateral del visor, estructurado por secciones principales, recursos y ejercicios/soluciones individuales.

#### Scenario: Navegación desde el panel lateral del visor PDF
- **WHEN** el usuario abre el panel lateral de marcadores o tabla de contenidos de su visor de PDF
- **THEN** se despliega el árbol estructurado completo y al hacer clic sobre cualquier nodo se salta a la página correspondiente.

### Requirement: Pipeline de compilación y postprocesado con Chrome y pypdf
El proceso de generación SHALL implementarse mediante un script en Python que escriba el HTML estructurado, compile el PDF utilizando Google Chrome o Chromium en modo headless sin bordes y aplique pypdf para inyectar los marcadores jerárquicos.

#### Scenario: Ejecución del script de generación
- **WHEN** se ejecuta el script automatizado scripts/generate_html_pdf.py
- **THEN** se compilan sin errores el archivo HTML intermedio y el archivo PDF final k8s-exercises-workbook.pdf con sus marcadores inyectados.

### Requirement: Preservación de indentación y espacios en bloques de código
El pipeline de generación y compilación PDF SHALL asegurar que todos los bloques de código YAML y comandos conserven sus espacios en blanco iniciales (sangría) cuando el usuario selecciona y copia texto desde el documento PDF en cualquier visor estándar (Evince, Chrome, Adobe Acrobat).

#### Scenario: Copia de manifiesto YAML desde visor PDF
- **WHEN** el usuario selecciona y copia las líneas de un manifiesto YAML en el archivo PDF y las pega en un editor o fichero local
- **THEN** las líneas indentadas conservan sus espacios precedentes respetando la sintaxis estricta de Kubernetes.

### Requirement: Sintaxis correcta de continuación de línea en comandos de terminal
Los comandos de consola y scripts divididos en varias líneas dentro de bloques `<pre><code>` SHALL emplear una única barra invertida (`\`) al final de la línea como carácter de continuación de shell (bash/sh), evitando dobles barras invertidas (`\\`) que impidan su ejecución directa al copiar y pegar.

#### Scenario: Copia y ejecución de comandos multilínea
- **WHEN** el usuario copia y ejecuta comandos multilínea desde cualquier caja de código del cuaderno o PDF
- **THEN** las líneas continuadas terminan con exactamente una barra invertida `\` y salto de línea, permitiendo la ejecución fluida en terminal sin errores sintácticos de escape.
