# Tasks: Cuaderno de Ejercicios y Solucionario de Kubernetes (PDF)

## 1. Infraestructura de Maquetación y Pipeline de Generación

- [x] 1.1 Crear el script `scripts/generate_html_pdf.py` adaptando la arquitectura de estilos y renderizado de `poc-kubeadm-ubuntu`, verificando su ejecución con `python3 -m py_compile scripts/generate_html_pdf.py`.
- [x] 1.2 Implementar en el script la función de postprocesado con `pypdf` para inyectar los marcadores jerárquicos (Document Outlines) del panel lateral y verificar que `pypdf.PdfWriter.add_outline_item` se ejecuta sin errores.
- [x] 1.3 Diseñar la portada editorial, el resumen ejecutivo, la tabla de metadatos y el índice general de contenidos interactivo (TOC) con navegación clicable hacia los recursos y secciones.

## 2. Redacción de Ejercicios y Solucionario - Bloque Fundamentos (Pods, ReplicaSets, Deployments, Services)

- [x] 2.1 Redactar enunciados y soluciones completas (YAML, comandos imperativos, salidas esperadas y trampas CKA) para los ejercicios de Pods (1.1, 1.2, 1.3) en el namespace `lab-pods`.
- [x] 2.2 Redactar enunciados y soluciones completas para los ejercicios de ReplicaSets (2.1, 2.2, 2.3) en el namespace `lab-replicasets`.
- [x] 2.3 Redactar enunciados y soluciones completas para los ejercicios de Deployments (3.1, 3.2, 3.3) en el namespace `lab-deployments`.
- [x] 2.4 Redactar enunciados y soluciones completas para los ejercicios de Services (4.1, 4.2, 4.3) en el namespace `lab-services`.

## 3. Redacción de Ejercicios y Solucionario - Bloque Configuración y Almacenamiento (ConfigMaps, Secrets, PV/PVC)

- [x] 3.1 Redactar enunciados y soluciones completas para los ejercicios de ConfigMaps (5.1, 5.2, 5.3) en el namespace `lab-configmaps`.
- [x] 3.2 Redactar enunciados y soluciones completas para los ejercicios de Secrets (6.1, 6.2, 6.3) en el namespace `lab-secrets`.
- [x] 3.3 Redactar enunciados y soluciones completas para los ejercicios de PersistentVolumes y PVCs (7.1, 7.2, 7.3) en el namespace `lab-storage`.

## 4. Redacción de Ejercicios y Solucionario - Bloque Cargas de Trabajo Avanzadas (Jobs, DaemonSets, StatefulSets)

- [x] 4.1 Redactar enunciados y soluciones completas para los ejercicios de Jobs y CronJobs (8.1, 8.2, 8.3) en el namespace `lab-jobs`.
- [x] 4.2 Redactar enunciados y soluciones completas para los ejercicios de DaemonSets (9.1, 9.2, 9.3) en el namespace `lab-daemonsets`.
- [x] 4.3 Redactar enunciados y soluciones completas para los ejercicios de StatefulSets (10.1, 10.2, 10.3) en el namespace `lab-statefulsets`.

## 5. Redacción de Ejercicios y Solucionario - Bloque Redes y Seguridad (Ingress, RBAC)

- [x] 5.1 Redactar enunciados y soluciones completas para los ejercicios de Ingress (11.1, 11.2, 11.3) en el namespace `lab-ingress`.
- [x] 5.2 Redactar enunciados y soluciones completas para los ejercicios de RBAC (12.1, 12.2, 12.3) en el namespace `lab-rbac`.

## 6. Redacción de Ejercicios y Solucionario - Bloque Empaquetado y Personalización (Helm, Kustomize)

- [x] 6.1 Redactar enunciados y soluciones completas para los ejercicios de Helm (13.1 Chart básico y anatomía, 13.2 Valores y sobreescritura, 13.3 Actualización de release y rollback) en el namespace `lab-helm`.
- [x] 6.2 Redactar enunciados y soluciones completas para los ejercicios de Kustomize (14.1 Base con mutación de nombres y etiquetas, 14.2 Generadores de ConfigMap/Secret con hash, 14.3 Overlays multi-entorno con parches estratégicos) en el namespace `lab-kustomize`.

## 7. Compilación, Enlace Cruzado y Verificación Integral del PDF

- [x] 7.1 Compilar el documento HTML en `docs/k8s-exercises-workbook.html` y generar el archivo PDF `k8s-exercises-workbook.pdf` ejecutando `python3 scripts/generate_html_pdf.py`, verificando que el archivo PDF se genera con tamaño superior a 500 KB.
- [x] 7.2 Validar la integridad de los 84 enlaces bidireccionales mediante script de verificación HTML comprobando que cada ancla `ex-X-Y` tiene su destino `sol-X-Y` y viceversa para los 42 ejercicios.
- [x] 7.3 Inspeccionar programáticamente con `pypdf` el árbol de marcadores del archivo PDF final para verificar que los 14 módulos y sus 42 ejercicios aparecen indexados en el panel lateral.
