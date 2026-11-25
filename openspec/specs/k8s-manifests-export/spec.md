# k8s-manifests-export Specification

## Purpose
Define la estructura de exportación y generación automatizada de los 42 manifiestos YAML de solución en un directorio organizado para su aplicación directa en el clúster con kubectl.

## Requirements

### Requirement: Jerarquía modular de manifiestos exportados
El sistema SHALL exportar los 42 manifiestos declarativos de solución en un árbol de directorios bajo `manifests/` distribuido en 14 subdirectorios ordenados por módulo temático.

#### Scenario: Generación y existencia de los archivos YAML
- **WHEN** se ejecuta el script de exportación o verificación
- **THEN** existen 14 subcarpetas temáticas en `manifests/` conteniendo exactamente los 42 archivos `.yaml` de laboratorio numerados y etiquetados.

### Requirement: Validez sintáctica y autosuficiencia
Cada manifiesto YAML generado SHALL ser sintácticamente válido, incluir comentarios aclaratorios en cabecera y pertenecer al namespace asignado a su módulo temático.

#### Scenario: Validación de sintaxis YAML
- **WHEN** se analiza cada archivo bajo `manifests/` con un parser YAML estándar
- **THEN** todos los manifiestos se interpretan sin errores y definen los metadatos y especificaciones de recurso correctos.
