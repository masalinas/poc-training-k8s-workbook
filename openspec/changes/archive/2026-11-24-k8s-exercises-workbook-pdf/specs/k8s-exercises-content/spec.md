# Spec Delta

## Purpose

Define la estructura pedagógica, enunciados técnicos, niveles de dificultad, namespaces y solucionario de los 42 ejercicios prácticos de Kubernetes divididos en 14 módulos temáticos (12 recursos core más Helm y Kustomize).

## ADDED Requirements

### Requirement: Cobertura exhaustiva de recursos core y herramientas de empaquetado
El sistema SHALL incluir al menos 3 ejercicios prácticos con solución para cada uno de los siguientes 14 módulos: Pods, ReplicaSets, Deployments, Services, ConfigMaps, Secrets, PersistentVolumes/PVC, Jobs/CronJobs, DaemonSets, StatefulSets, Ingress, RBAC, Helm y Kustomize.

#### Scenario: Presencia de todos los recursos y ejercicios requeridos
- **WHEN** se examina el índice de contenidos del cuaderno
- **THEN** se constata la presencia de exactamente 14 bloques temáticos y un total de 42 ejercicios numerados secuencialmente.

### Requirement: Etiquetado de nivel de dificultad explícito
Cada ejercicio SHALL especificar de forma visual y textual su nivel de dificultad entre tres categorías posibles: Intermedio, Avanzado y Nivel CKA.

#### Scenario: Visualización del nivel de dificultad
- **WHEN** el alumno lee la cabecera de cualquier ejercicio en la Sección I
- **THEN** encuentra una etiqueta visible que indica claramente el nivel de complejidad del ejercicio ([Intermedio], [Avanzado] o [Nivel CKA]).

### Requirement: Aislamiento por namespaces temáticos dedicados
Cada grupo temático de ejercicios SHALL desarrollarse en un namespace propio e independiente para prevenir conflictos entre recursos y facilitar la limpieza del clúster del estudiante.

#### Scenario: Creación y uso de namespace por recurso
- **WHEN** el alumno ejecuta las instrucciones de un bloque temático
- **THEN** todas las operaciones y manifiestos se ejecutan dentro del namespace correspondiente (ej. lab-pods, lab-deployments, lab-helm, lab-kustomize).

### Requirement: Estructura estandarizada de enunciados en Sección I
Cada ejercicio en la Sección I SHALL contener obligatoriamente: escenario real, objetivos y requerimientos técnicos específicos, criterios de verificación y un enlace interactivo hacia su solución en la Sección II.

#### Scenario: Navegación de enunciado a solución
- **WHEN** el alumno finaliza la lectura o resolución del ejercicio y pulsa sobre el enlace de solución
- **THEN** el visor salta inmediatamente a la solución técnica correspondiente en la Sección II.

### Requirement: Solucionario exhaustivo y didáctico en Sección II
Cada solución en la Sección II SHALL incluir el manifiesto YAML completo o configuración comentada, comandos imperativos alternativos con kubectl o helm cuando aplique, comandos de validación con salidas esperadas, análisis de errores comunes (Gotchas) y un enlace de retorno al enunciado.

#### Scenario: Navegación de retorno desde la solución al enunciado
- **WHEN** el alumno consulta la solución en la Sección II y pulsa sobre el enlace de retorno
- **THEN** el visor salta inmediatamente al enunciado original del ejercicio en la Sección I.
