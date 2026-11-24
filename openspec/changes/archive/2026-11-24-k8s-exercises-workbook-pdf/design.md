# Design: Cuaderno de Ejercicios y Solucionario de Kubernetes (PDF)

## Context

Para la formación técnica avanzada y la preparación de certificaciones como CKA/CKAD, se requiere un documento consolidado y altamente estructurado. El documento debe contener tanto los enunciados de los problemas como sus soluciones técnicas completas, cubriendo tanto los recursos nativos de Kubernetes como las herramientas de empaquetado y personalización dominantes (Helm y Kustomize), garantizando una experiencia de navegación interactiva bidireccional y una presentación visual de nivel editorial que replique fielmente el estándar visual de `poc-kubeadm-ubuntu/k8s-installation-steps.pdf`.

Véase `proposal.md` y las especificaciones en `specs/` para la justificación y requisitos normativos.

## Goals / Non-Goals

**Goals:**
- Diseñar la arquitectura técnica de contenidos para 42 ejercicios prácticos y 42 soluciones detalladas distribuidas en 14 módulos (12 recursos core más Helm y Kustomize).
- Integrar metadatos pedagógicos: etiquetas de dificultad (`[Intermedio]`, `[Avanzado]`, `[Nivel CKA]`), namespaces temáticos dedicados (`lab-pods`, `lab-deployments`, `lab-helm`, `lab-kustomize`, etc.) y escenarios del mundo real.
- Implementar una navegación fluida con doble índice:
  1. Índice interno con enlaces hipertexto clicables entre cada ejercicio y su solución respectiva (`ex-X-Y` <-> `sol-X-Y`).
  2. Marcadores nativos de PDF (*Document Outlines*) visibles en el panel lateral del visor, generados mediante `pypdf`.
- Proveer un pipeline automatizado de compilación (`scripts/generate_html_pdf.py`) que renderice el documento HTML con Google Chrome headless sin márgenes adicionales y ensamble el PDF final.

**Non-Goals:**
- Desplegar una aplicación web o plataforma interactiva online; el artefacto final es un documento PDF autónomo de distribución local.
- Provisionar automáticamente clústeres de Kubernetes en la nube; el alumno asume un clúster funcional (local como Minikube/Kind/Vagrant o remoto).

## Decisions

### 1. Motor de Renderizado: HTML5 + CSS Paged Media compilado con Chrome Headless
- **Decisión**: Utilizar HTML5 estructurado con CSS moderno (`@page`, fuentes web Inter/JetBrains Mono, paleta de colores `#326ce5`/`#0f172a`) y compilar mediante `google-chrome-stable --headless --print-to-pdf`.
- **Razón**: Máxima fidelidad y control tipográfico respecto al documento de referencia `k8s-installation-steps.pdf`, evitando las limitaciones de sintaxis o empaquetado de motores como LaTeX o Pandoc estándar.
- **Alternativas consideradas**:
  - *Pandoc + pdflatex*: Mayor complejidad de configuración y soporte deficiente para cajas visuales con esquinas redondeadas y gradientes modernos sin macros complejas.
  - *Weasyprint*: Requiere dependencias pesadas de Pango/Cairo en el sistema, mientras que Chrome ya está disponible en `/usr/bin/google-chrome-stable`.

### 2. Inyección de Marcadores PDF (Outlines) con `pypdf`
- **Decisión**: Utilizar la biblioteca Python `pypdf` para parsear los IDs del documento generado e inyectar un árbol jerárquico de `OutlineItem` en el panel lateral del PDF.
- **Razón**: Chrome headless no siempre genera marcadores jerárquicos profundos de forma automática a partir de etiquetas HTML arbitrarias. La inyección programática con `pypdf` garantiza que tanto la Sección I (Ejercicios por recurso) como la Sección II (Soluciones por recurso) aparezcan desplegadas con precisión en el panel lateral de cualquier visor PDF.
- **Alternativas consideradas**:
  - Confiar solo en los encabezados nativos `<h1>`/`<h2>`: Chrome los aplana o los omite según la versión.

### 3. Esquema de Identificadores y Enlaces Bidireccionales
- **Decisión**: Establecer una convención estricta de anclas HTML:
  - Enunciado del Ejercicio $X.Y$: `id="ex-X-Y"` con botón/enlace hacia `#sol-X-Y`.
  - Solución del Ejercicio $X.Y$: `id="sol-X-Y"` con botón/enlace de retorno hacia `#ex-X-Y`.
- **Razón**: Permite al alumno saltar a comprobar la respuesta y volver inmediatamente al flujo de ejercicios sin tener que desplazarse manualmente por decenas de páginas.

### 4. Enfoque Didáctico del Solucionario: YAML Declarativo + Atajos Imperativos
- **Decisión**: Para cada ejercicio, presentar el manifiesto YAML completo y enriquecerlo con:
  - Comandos imperativos de generación rápida (`kubectl create/run --dry-run=client -o yaml`).
  - Procedimientos de verificación con salidas esperadas (`kubectl get/describe/logs`).
  - Notas de examen ("Gotchas" / Trampas CKA) para los ejercicios avanzados.
- **Razón**: Prepara al alumno no solo para escribir manifiestos en producción, sino para resolver incidentes con agilidad en entornos bajo presión temporal como las pruebas CKA/CKAD.

### 5. Didáctica Práctica para Helm y Kustomize
- **Decisión**: Estructurar los ejercicios de Helm y Kustomize mostrando tanto la estructura de archivos en árbol (`tree`) como los comandos de renderizado e instalación:
  - *Helm*: `Chart.yaml`, `values.yaml`, templates con Go templating, y comandos `helm install/upgrade/rollback`.
  - *Kustomize*: `base/kustomization.yaml`, `overlays/dev`, `overlays/prod`, generadores con hash y comandos de validación `kubectl kustomize` y despliegue `kubectl apply -k`.
- **Razón**: Permite al alumno comprender cómo se gestionan y parametrizan aplicaciones complejas en entornos reales multi-entorno sin duplicar código.

## Risks / Trade-offs

- **[Desbordamiento horizontal en bloques de código]** → *Mitigación*: Reglas CSS estrictas en etiquetas `pre` y `code` con `font-size: 8pt`, `line-height: 1.45`, `white-space: pre-wrap` y `word-break: break-all`.
- **[Salto de página inoportuno en enunciados o soluciones]** → *Mitigación*: Uso extensivo de `page-break-inside: avoid` en las tarjetas de ejercicios y soluciones para asegurar que cada ejercicio se mantenga como una unidad visual compacta.
- **[Tamaño del documento]** → *Mitigación*: Al ser 42 ejercicios con soluciones completas, el documento rondará las 50-60 páginas; la estructura en dos secciones y el doble índice son indispensables para que no resulte abrumador.
