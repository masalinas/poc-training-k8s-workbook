# =============================================================================
# scripts/modules_packaging.py
# Módulos 13 y 14: Helm & Kustomize
# =============================================================================

MODULE_HELM = {
    "id": "helm",
    "num": "13",
    "name": "Helm: Gestor de Paquetes y Templating para Kubernetes",
    "ns": "lab-helm",
    "description": "Helm es el gestor de paquetes estándar de facto en Kubernetes. Permite empaquetar, parametrizar, versionar y desplegar aplicaciones complejas mediante plantillas (Go templates) y archivos de valores (values.yaml).",
    "exercises": [
        {
            "id": "ex-13-1",
            "sol_id": "sol-13-1",
            "num": "Ejercicio 13.1:",
            "title": "Anatomía de un Chart, Creación y Depuración con helm template / lint",
            "difficulty_label": "Intermedio",
            "difficulty_class": "intermedio",
            "scenario": "Un equipo de desarrollo necesita empaquetar un microservicio de frontend como un Helm Chart estandarizado, limpiando los artefactos innecesarios generados por defecto y validando la sintaxis del template antes del despliegue.",
            "requirements": [
                "Crear el namespace <code>lab-helm</code>.",
                "Crear la estructura inicial de un Chart con <code>helm create my-webapp</code>.",
                "Editar <code>Chart.yaml</code> fijando <code>name: my-webapp</code>, <code>version: 1.0.0</code> y <code>appVersion: \"1.25.0\"</code>.",
                "Configurar en <code>values.yaml</code> la imagen <code>nginx:1.25-alpine</code>, <code>replicaCount: 2</code> y servicio de tipo <code>ClusterIP</code> en puerto 80.",
                "Validar la sintaxis con <code>helm lint my-webapp</code> y renderizar localmente los manifiestos YAML sin tocar el clúster con <code>helm template</code>."
            ],
            "verification": "<p>Ejecutar <code>helm lint my-webapp</code> y comprobar que responde <code>1 chart(s) linted, 0 chart(s) failed</code>. Ejecutar <code>helm template my-webapp</code> y verificar que los YAMLs resultantes tienen 2 réplicas.</p>"
        },
        {
            "id": "ex-13-2",
            "sol_id": "sol-13-2",
            "num": "Ejercicio 13.2:",
            "title": "Instalación Parametrizada y Sobreescritura de Valores (--set y -f)",
            "difficulty_label": "Intermedio",
            "difficulty_class": "intermedio",
            "scenario": "Desplegar el Chart en el clúster asignando una release llamada `webapp-prod` en el namespace `lab-helm`, aplicando límites de recursos y sobreescribiendo el número de réplicas a 3 mediante un archivo de valores específico de producción.",
            "requirements": [
                "Crear un archivo <code>values-production.yaml</code> que configure <code>replicaCount: 3</code> y límites de memoria de <code>128Mi</code>.",
                "Instalar el Chart con nombre de release <code>webapp-prod</code> en <code>lab-helm</code> aplicando el archivo con <code>-f values-production.yaml</code>.",
                "Sobreescribir adicionalmente una variable puntual en línea de comandos usando <code>--set service.type=NodePort</code>.",
                "Verificar la lista de releases desplegadas con <code>helm list -n lab-helm</code>."
            ],
            "verification": "<p>Ejecutar <code>kubectl get pods -n lab-helm -l app.kubernetes.io/instance=webapp-prod</code> y comprobar que existen 3 Pods en estado Running.</p>"
        },
        {
            "id": "ex-13-3",
            "sol_id": "sol-13-3",
            "num": "Ejercicio 13.3:",
            "title": "Gestión del Ciclo de Vida: helm upgrade, helm history y helm rollback",
            "difficulty_label": "Nivel CKA",
            "difficulty_class": "cka",
            "scenario": "Simular una actualización de versión de la aplicación que provoca un fallo de servicio, inspeccionar las revisiones históricas almacenadas en Secrets del clúster y revertir la release al estado saludable anterior en un solo comando.",
            "requirements": [
                "Actualizar la release <code>webapp-prod</code> a la versión de imagen errónea <code>nginx:v_error_99</code> con <code>helm upgrade --set image.tag=v_error_99</code>.",
                "Comprobar cómo los Pods quedan en <code>ImagePullBackOff</code>.",
                "Consultar el historial de versiones con <code>helm history webapp-prod -n lab-helm</code>.",
                "Ejecutar un rollback a la revisión 1 con <code>helm rollback webapp-prod 1 -n lab-helm</code>.",
                "Verificar la recuperación completa del servicio."
            ],
            "verification": "<p>Ejecutar <code>helm status webapp-prod -n lab-helm</code> y verificar que el estado es <code>deployed</code> y los Pods vuelven a estar <code>Running (1/1)</code>.</p>"
        }
    ],
    "solutions": [
        {
            "id": "sol-13-1",
            "ex_id": "ex-13-1",
            "num": "Solución 13.1:",
            "title": "Anatomía de un Chart, Creación y Depuración con helm template / lint",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Un Helm Chart contiene metadatos (<code>Chart.yaml</code>), valores por defecto (<code>values.yaml</code>) y plantillas en <code>templates/</code> que combinan sintaxis YAML con Go templating. <code>helm lint</code> valida buenas prácticas y <code>helm template</code> renderiza los YAML sin interactuar con la API de Kubernetes.</p>

<p><strong>Comandos de Preparación y Validación:</strong></p>
<pre><code># 1. Crear namespace
kubectl create namespace lab-helm

# 2. Generar esqueleto de chart
helm create my-webapp

# 3. Limpiar plantillas complejas opcionales para dejar lo esencial
rm -f my-webapp/templates/hpa.yaml \\\\
  my-webapp/templates/ingress.yaml \\\\
  my-webapp/templates/serviceaccount.yaml

# 4. Validar sintaxis estricta
helm lint my-webapp

# 5. Renderizar manifiestos para previsualización
helm template test-render my-webapp --set replicaCount=2</code></pre>
"""
        },
        {
            "id": "sol-13-2",
            "ex_id": "ex-13-2",
            "num": "Solución 13.2:",
            "title": "Instalación Parametrizada y Sobreescritura de Valores (--set y -f)",
            "content_html": """
<p><strong>Explicación Técnica:</strong> La jerarquía de valores en Helm sigue el principio de especificidad: los valores en <code>values.yaml</code> tienen la menor precedencia, sobreescritos por <code>-f custom-values.yaml</code>, y finalmente sobreescritos por flags individuales <code>--set</code>.</p>

<p><strong>Archivo values-production.yaml:</strong></p>
<pre><code>replicaCount: 3
image:
  repository: nginx
  tag: "1.25-alpine"
resources:
  limits:
    memory: 128Mi
  requests:
    memory: 64Mi</code></pre>

<p><strong>Comando de Despliegue:</strong></p>
<pre><code># Desplegar combinando archivo de valores y --set
helm install webapp-prod ./my-webapp \\
  --namespace lab-helm \\
  -f values-production.yaml \\
  --set service.type=NodePort

# Comprobar la release en el clúster
helm list -n lab-helm
kubectl get pods -n lab-helm -l app.kubernetes.io/instance=webapp-prod</code></pre>
"""
        },
        {
            "id": "sol-13-3",
            "ex_id": "ex-13-3",
            "num": "Solución 13.3:",
            "title": "Gestión del Ciclo de Vida: helm upgrade, helm history y helm rollback",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Helm guarda el estado de cada release en Secrets cifrados en el clúster (con el tipo <code>helm.sh/release.v1</code>). Esto permite que <code>helm history</code> conozca el historial completo de despliegues y pueda revertir cualquier cambio al instante con <code>helm rollback</code>.</p>

<p><strong>Simulación de Fallo y Rollback:</strong></p>
<pre><code># 1. Ejecutar upgrade con imagen inexistente
helm upgrade webapp-prod ./my-webapp -n lab-helm --set image.tag=v_error_99

# 2. Comprobar que los Pods fallan
kubectl get pods -n lab-helm

# 3. Consultar el historial de revisiones
helm history webapp-prod -n lab-helm
# Observar que la revisión 1 fue exitosa y la revisión 2 es la actual fallida

# 4. Revertir a la revisión 1
helm rollback webapp-prod 1 -n lab-helm

# 5. Confirmar que los Pods vuelven a estar operativos
kubectl get pods -n lab-helm
helm history webapp-prod -n lab-helm</code></pre>
"""
        }
    ]
}

MODULE_KUSTOMIZE = {
    "id": "kustomize",
    "num": "14",
    "name": "Kustomize: Personalización Declarativa sin Plantillas",
    "ns": "lab-kustomize",
    "description": "Kustomize es la herramienta nativa de personalización de manifiestos integrada en kubectl (-k). A través de un enfoque basado en capas ('base' y 'overlays') permite transformar recursos sin motores de plantillas ni variables.",
    "exercises": [
        {
            "id": "ex-14-1",
            "sol_id": "sol-14-1",
            "num": "Ejercicio 14.1:",
            "title": "Capa Base con Mutación Automática de Metadatos (Labels y Prefijos)",
            "difficulty_label": "Intermedio",
            "difficulty_class": "intermedio",
            "scenario": "Construir una base reutilizable con un Deployment y un Service para una API de usuarios. Usar Kustomize para inyectar automáticamente un prefijo de nombre y etiquetas comunes a todos los recursos sin editar los manifiestos individuales.",
            "requirements": [
                "Crear el namespace <code>lab-kustomize</code>.",
                "Crear el directorio <code>base/</code> con un Deployment <code>api-users</code> y un Service <code>api-users-svc</code>.",
                "Crear <code>base/kustomization.yaml</code> añadiendo <code>namePrefix: dev-</code>, <code>commonLabels: { project: auth-system, managed-by: kustomize }</code> y <code>namespace: lab-kustomize</code>.",
                "Compilar y previsualizar los manifiestos con <code>kubectl kustomize base/</code>."
            ],
            "verification": "<p>Ejecutar <code>kubectl kustomize base/</code> y comprobar que los recursos ahora se llaman <code>dev-api-users</code> y que todos tienen las etiquetas comunes añadidas en metadata y selectores.</p>"
        },
        {
            "id": "ex-14-2",
            "sol_id": "sol-14-2",
            "num": "Ejercicio 14.2:",
            "title": "Generación Declarativa de ConfigMaps y Secrets con Hash de Contenido",
            "difficulty_label": "Intermedio",
            "difficulty_class": "intermedio",
            "scenario": "Cuando se actualiza un archivo de configuración, los Pods no se enteran a menos que cambie su especificación. El `configMapGenerator` de Kustomize añade un sufijo hash único basado en el contenido del archivo, forzando un rollout automático en cada cambio.",
            "requirements": [
                "Crear un archivo local <code>app.properties</code> con el contenido <code>max_threads=16</code>.",
                "En <code>kustomization.yaml</code>, usar <code>configMapGenerator</code> para crear un ConfigMap a partir de dicho archivo.",
                "Vincular el ConfigMap generado dentro del Deployment.",
                "Comprobar cómo Kustomize añade un hash al nombre del ConfigMap (ej: <code>app-config-g2f5d94m88</code>) y actualiza automáticamente la referencia en el Deployment."
            ],
            "verification": "<p>Modificar el archivo <code>app.properties</code> y comprobar que <code>kubectl kustomize</code> genera un nuevo hash diferente.</p>"
        },
        {
            "id": "ex-14-3",
            "sol_id": "sol-14-3",
            "num": "Ejercicio 14.3:",
            "title": "Gestión Multi-Entorno con Overlays y Parches Estratégicos (patches)",
            "difficulty_label": "Nivel CKA",
            "difficulty_class": "cka",
            "scenario": "A partir de la misma capa `base`, se deben crear dos entornos: `overlays/development` (con 1 réplica y sin límites) y `overlays/production` (con 4 réplicas, límites estrictos de CPU/Memoria y prefijo `prod-`).",
            "requirements": [
                "Crear la carpeta <code>overlays/prod/</code> referenciando <code>../../base</code>.",
                "Crear un parche Strategic Merge Patch en <code>overlays/prod/patch-replicas-resources.yaml</code> fijando <code>replicas: 4</code> y recursos.",
                "En <code>overlays/prod/kustomization.yaml</code>, registrar el parche en la sección <code>patches</code>.",
                "Aplicar directamente el entorno de producción con <code>kubectl apply -k overlays/prod/</code>."
            ],
            "verification": "<p>Ejecutar <code>kubectl get deployment -n lab-kustomize -l project=auth-system</code> y comprobar que se ha desplegado con 4 réplicas en producción.</p>"
        }
    ],
    "solutions": [
        {
            "id": "sol-14-1",
            "ex_id": "ex-14-1",
            "num": "Solución 14.1:",
            "title": "Capa Base con Mutación Automática de Metadatos (Labels y Prefijos)",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Kustomize no necesita motor de plantillas: lee archivos YAML estándar de Kubernetes y aplica mutaciones sintácticas estructuradas a través de su archivo descriptor <code>kustomization.yaml</code>.</p>

<p><strong>Estructura de Directorios:</strong></p>
<pre><code>base/
├── deployment.yaml
├── service.yaml
└── kustomization.yaml</code></pre>

<p><strong>Archivo base/kustomization.yaml:</strong></p>
<pre><code>apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: lab-kustomize

namePrefix: dev-

commonLabels:
  project: auth-system
  managed-by: kustomize

resources:
  - deployment.yaml
  - service.yaml</code></pre>

<p><strong>Comandos de Validación:</strong></p>
<pre><code># 1. Crear namespace
kubectl create namespace lab-kustomize

# 2. Renderizar y previsualizar sin aplicar
kubectl kustomize base/

# 3. Aplicar directamente en el clúster
kubectl apply -k base/
kubectl get all -n lab-kustomize -l project=auth-system</code></pre>
"""
        },
        {
            "id": "sol-14-2",
            "ex_id": "ex-14-2",
            "num": "Solución 14.2:",
            "title": "Generación Declarativa de ConfigMaps y Secrets con Hash de Contenido",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Al generar un ConfigMap con hash en el nombre (ej. <code>cm-app-props-k8h5f8mt4d</code>), cualquier cambio en el archivo de origen produce un nuevo hash. Kustomize actualiza simultáneamente la referencia en el Deployment, provocando un RollingUpdate automático de los Pods.</p>

<p><strong>Configuración en kustomization.yaml:</strong></p>
<pre><code>apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml

configMapGenerator:
  - name: cm-app-props
    files:
      - app.properties</code></pre>

<p><strong>Deployment que lo consume (referenciando el nombre base):</strong></p>
<pre><code># En deployment.yaml sólo referenciamos el nombre base:
# Kustomize se encarga de reemplazarlo por el nombre con hash
volumes:
  - name: config-vol
    configMap:
      name: cm-app-props</code></pre>

<p><strong>Validación:</strong></p>
<pre><code>kubectl kustomize . | grep -A 5 "kind: ConfigMap"</code></pre>
"""
        },
        {
            "id": "sol-14-3",
            "ex_id": "ex-14-3",
            "num": "Solución 14.3:",
            "title": "Gestión Multi-Entorno con Overlays y Parches Estratégicos (patches)",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Los <code>overlays</code> reutilizan la capa <code>base</code> y sólo declaran las diferencias (parches) correspondientes a cada entorno específico (desarrollo, staging o producción), eliminando la duplicación de código.</p>

<p><strong>Estructura de Overlays:</strong></p>
<pre><code>k8s-app/
├── base/
│   ├── deployment.yaml
│   └── kustomization.yaml
└── overlays/
    ├── dev/
    │   └── kustomization.yaml
    └── prod/
        ├── kustomization.yaml
        └── patch-prod.yaml</code></pre>

<p><strong>Archivo overlays/prod/patch-prod.yaml:</strong></p>
<pre><code>apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-users
spec:
  replicas: 4
  template:
    spec:
      containers:
        - name: api
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "250m"</code></pre>

<p><strong>Archivo overlays/prod/kustomization.yaml:</strong></p>
<pre><code>apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../../base

namePrefix: prod-

patches:
  - path: patch-prod.yaml</code></pre>

<p><strong>Despliegue y Validación:</strong></p>
<pre><code># 1. Aplicar overlay de producción
kubectl apply -k overlays/prod/

# 2. Comprobar que existen 4 réplicas con el prefijo prod-
kubectl get deployment -n lab-kustomize prod-api-users</code></pre>
"""
        }
    ]
}

MODULES_PACKAGING = [MODULE_HELM, MODULE_KUSTOMIZE]
