# Spec Delta: pdf-document-generation

## ADDED Requirements

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
