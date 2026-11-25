# Spec Delta: pdf-document-generation

## ADDED Requirements

### Requirement: Preservación de indentación y espacios en bloques de código
El pipeline de generación y compilación PDF SHALL asegurar que todos los bloques de código YAML y comandos conserven sus espacios en blanco iniciales (sangría) cuando el usuario selecciona y copia texto desde el documento PDF en cualquier visor estándar (Evince, Chrome, Adobe Acrobat).

#### Scenario: Copia de manifiesto YAML desde visor PDF
- **WHEN** el usuario selecciona y copia las líneas de un manifiesto YAML en el archivo PDF y las pega en un editor o fichero local
- **THEN** las líneas indentadas conservan sus espacios precedentes respetando la sintaxis estricta de Kubernetes.
