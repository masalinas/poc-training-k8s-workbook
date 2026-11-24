# Proposal: Cuaderno de Ejercicios Prácticos y Solucionario de Kubernetes (PDF)

## Why

Los alumnos de cursos de Kubernetes y profesionales que preparan certificaciones oficiales como CKA/CKAD requieren material práctico estructurado, progresivo y riguroso para afianzar el dominio de los recursos fundamentales y avanzados del orquestador, así como de las herramientas estándar de la industria para empaquetado y personalización de manifiestos (Helm y Kustomize). Actualmente no se dispone en el repositorio de una guía didáctica en formato PDF profesional que ofrezca ejercicios con escenarios realistas organizados por namespaces específicos, niveles de dificultad explícitos, y un solucionario técnico exhaustivo con doble índice de navegación (interactivo interno y panel lateral).

## What Changes

- Creación de un cuaderno de formación completo con **42 ejercicios prácticos** distribuidos uniformemente entre 14 recursos y herramientas esenciales del ecosistema Kubernetes (3 ejercicios por bloque):
  - Recursos core: Pods, ReplicaSets, Deployments, Services, ConfigMaps, Secrets, PersistentVolumes/PVC, Jobs/CronJobs, DaemonSets, StatefulSets, Ingress, RBAC.
  - Empaquetado y personalización: Helm y Kustomize.
- Incorporación de metadatos de dificultad para cada ejercicio: `[Intermedio]`, `[Avanzado]` y `[Nivel CKA]`.
- Organización estricta de los ejercicios en **namespaces temáticos independientes** (`lab-pods`, `lab-deployments`, `lab-services`, `lab-storage`, `lab-helm`, `lab-kustomize`, etc.) para garantizar aislamiento y evitar colisiones de recursos.
- Separación estructural en dos grandes bloques:
  - **Sección I (Ejercicios)**: Escenario, requerimientos técnicos (nombres, selectores, puertos, restricciones, plantillas de valores y overlays) y criterios de auto-evaluación.
  - **Sección II (Solucionario)**: Manifiestos YAML oficiales y comentados, charts de Helm, capas Kustomize, comandos imperativos de resolución rápida con `kubectl`, procedimientos de validación paso a paso y análisis de errores comunes ("Gotchas" / trampas de examen).
- Integración de **doble índice interactivo**:
  - Índice analítico interno en el documento con enlaces clicables bidireccionales entre enunciados y soluciones.
  - Árbol de marcadores jerárquicos (*Document Outlines*) integrado nativamente en el visor de PDF para navegación fluida desde el panel lateral.
- Automatización del pipeline de renderizado y compilación PDF basado en HTML5/CSS (A4, tipografías Inter y JetBrains Mono, paleta oficial Kubernetes) mediante Google Chrome headless y el inyector de marcadores con `pypdf`, replicando la estética del documento de referencia `poc-kubeadm-ubuntu/k8s-installation-steps.pdf`.

## Capabilities

### New Capabilities
- `k8s-exercises-content`: Estructura, redacción y especificación técnica de los 42 ejercicios prácticos y sus respectivas soluciones detalladas para los 14 recursos y herramientas de Kubernetes con niveles de dificultad y aislamiento por namespaces.
- `pdf-document-generation`: Generación y compilación del documento PDF profesional con estilo editorial corporativo, doble índice interactivo (TOC interno y marcadores de panel lateral de visor de PDF).

### Modified Capabilities
*(Ninguna; repositorio de nueva creación)*

## Impact
- **Documentación y recursos del curso**: Generación del archivo fuente `docs/k8s-exercises-workbook.html` y del PDF compilado final `k8s-exercises-workbook.pdf`.
- **Automatización**: Script Python en `scripts/generate_html_pdf.py` para compilar y post-procesar el PDF inyectando la estructura de marcadores.
- **Dependencias**: Uso de Python 3, `google-chrome-stable` (o Chromium), paquete `pypdf`, y comandos cliente `kubectl`, `helm` y soporte nativo `kustomize` (`kubectl -k`).
