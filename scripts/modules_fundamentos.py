# =============================================================================
# scripts/modules_fundamentos.py
# Módulos 1 a 4: Pods, ReplicaSets, Deployments, Services
# =============================================================================

MODULE_PODS = {
    "id": "pods",
    "num": "1",
    "name": "Pods: Contenedores y Ciclo de Vida",
    "ns": "lab-pods",
    "description": "El Pod es la unidad mínima ejecutable en Kubernetes. En este bloque se profundiza en patrones multi-contenedor (Sidecar), inicialización secuencial con InitContainers y mecanismos avanzados de detección de fallos y preparación (Probes).",
    "exercises": [
        {
            "id": "ex-1-1",
            "sol_id": "sol-1-1",
            "num": "Ejercicio 1.1:",
            "title": "Pod Multi-contenedor con Volumen Compartido (Patrón Sidecar)",
            "difficulty_label": "Intermedio",
            "difficulty_class": "intermedio",
            "scenario": "El equipo de desarrollo ha diseñado un servicio web ligero que genera logs continuos en un archivo local. Para cumplir las políticas de monitorización corporativas, se necesita un contenedor auxiliar (sidecar) que lea esos registros en tiempo real y los procese, sin modificar la imagen base de la aplicación.",
            "requirements": [
                "Crear el namespace <code>lab-pods</code> si no existe previamente.",
                "Crear un Pod con nombre <code>pod-sidecar-logger</code> en el namespace <code>lab-pods</code>.",
                "El Pod debe montar un volumen en memoria compartida de tipo <code>emptyDir: {}</code> en la ruta <code>/var/log/app</code> en ambos contenedores.",
                "Contenedor primario (<code>app</code>): Imagen <code>busybox:1.36</code>. Debe ejecutar un bucle en segundo plano escribiendo la fecha actual y un mensaje cada 5 segundos en <code>/var/log/app/events.log</code>.",
                "Contenedor secundario (<code>sidecar</code>): Imagen <code>busybox:1.36</code>. Debe monitorear continuamente el archivo con <code>tail -f /var/log/app/events.log</code>."
            ],
            "verification": "<p>Ejecutar <code>kubectl logs -n lab-pods pod-sidecar-logger -c sidecar</code> y comprobar que aparecen las líneas de log generadas por el contenedor principal en intervalos de 5 segundos.</p>"
        },
        {
            "id": "ex-1-2",
            "sol_id": "sol-1-2",
            "num": "Ejercicio 1.2:",
            "title": "Inicialización con InitContainer para Validación de Dependencias",
            "difficulty_label": "Intermedio",
            "difficulty_class": "intermedio",
            "scenario": "Una API de negocio no debe arrancar hasta que su base de datos o servicio dependiente responda por red. De lo contrario, la aplicación colapsará con errores de conexión.",
            "requirements": [
                "Crear un Pod llamado <code>pod-backend-init</code> en el namespace <code>lab-pods</code>.",
                "Incluir un <code>initContainer</code> llamado <code>wait-db</code> con imagen <code>busybox:1.36</code> que use <code>nc -z -w 2 db-service 3306</code> en un bucle con retardo de 3 segundos hasta que el host y puerto respondan.",
                "El contenedor principal (<code>backend-api</code>) debe usar la imagen <code>nginx:1.25-alpine</code> y escuchar en el puerto 80.",
                "Probar el estado del Pod antes y después de simular el servicio dependiente con un Pod/Service temporal."
            ],
            "verification": "<p>Al crear el Pod, debe permanecer en estado <code>Init:0/1</code>. Tras crear el servicio y pod temporal <code>db-service</code> en el puerto 3306, el Pod debe transicionar automáticamente a <code>PodInitializing</code> y luego a <code>Running (1/1)</code>.</p>"
        },
        {
            "id": "ex-1-3",
            "sol_id": "sol-1-3",
            "num": "Ejercicio 1.3:",
            "title": "Resiliencia Avanzada con Startup, Liveness y Readiness Probes",
            "difficulty_label": "Nivel CKA",
            "difficulty_class": "cka",
            "scenario": "En entornos de producción, una aplicación con carga pesada tarda 20 segundos en cargar sus cachés en memoria. Si se usan únicamente sondas Liveness agresivas, Kubelet matará el contenedor antes de terminar de arrancar, entrando en CrashLoopBackOff. Se debe diseñar una estrategia completa de tres sondas.",
            "requirements": [
                "Crear un Pod con nombre <code>pod-health-hardened</code> en el namespace <code>lab-pods</code>.",
                "Contenedor: imagen <code>nginx:1.25-alpine</code>, puerto de contenedor 80.",
                "Configurar <code>startupProbe</code> HTTP en <code>path: /</code>, <code>port: 80</code>, con <code>failureThreshold: 10</code> y <code>periodSeconds: 5</code> (hasta 50 segundos de ventana de arranque).",
                "Configurar <code>livenessProbe</code> HTTP en <code>path: /</code>, <code>port: 80</code>, con <code>periodSeconds: 10</code>, <code>failureThreshold: 3</code>.",
                "Configurar <code>readinessProbe</code> HTTP en <code>path: /</code>, <code>port: 80</code>, con <code>periodSeconds: 5</code>, <code>successThreshold: 1</code>, <code>failureThreshold: 2</code>."
            ],
            "verification": "<p>Ejecutar <code>kubectl describe pod -n lab-pods pod-health-hardened</code> y verificar que las 3 sondas aparecen registradas y que no hay reinicios (Restarts: 0). Simular un fallo renombrando index.html y observar cómo el Pod deja de estar Ready y luego se reinicia.</p>"
        }
    ],
    "solutions": [
        {
            "id": "sol-1-1",
            "ex_id": "ex-1-1",
            "num": "Solución 1.1:",
            "title": "Pod Multi-contenedor con Volumen Compartido (Patrón Sidecar)",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Los contenedores dentro de un mismo Pod comparten el espacio de red (misma IP y localhost) y pueden compartir almacenamiento montando el mismo volumen. Un volumen <code>emptyDir</code> se crea vacío al instanciarse el Pod en el nodo y permanece vivo mientras el Pod exista.</p>

<p><strong>Manifiesto Declarativo YAML:</strong></p>
<pre><code>apiVersion: v1
kind: Namespace
metadata:
  name: lab-pods
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-sidecar-logger
  namespace: lab-pods
  labels:
    app: multi-container-demo
spec:
  volumes:
    - name: shared-logs
      emptyDir: {}
  containers:
    - name: app
      image: busybox:1.36
      command: ["/bin/sh", "-c"]
      args:
        - |
          while true; do
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Evento procesado en app" >> /var/log/app/events.log;
            sleep 5;
          done
      volumeMounts:
        - name: shared-logs
          mountPath: /var/log/app
    - name: sidecar
      image: busybox:1.36
      command: ["/bin/sh", "-c"]
      args:
        - |
          touch /var/log/app/events.log
          tail -n +1 -f /var/log/app/events.log
      volumeMounts:
        - name: shared-logs
          mountPath: /var/log/app</code></pre>

<p><strong>Procedimiento de Validación:</strong></p>
<pre><code># 1. Aplicar el manifiesto
kubectl apply -f pod-sidecar.yaml

# 2. Verificar que ambos contenedores estén listos (2/2)
kubectl get pods -n lab-pods pod-sidecar-logger

# 3. Comprobar que el sidecar lee los eventos emitidos por el app
kubectl logs -n lab-pods pod-sidecar-logger -c sidecar --tail=10</code></pre>

<div class="callout callout-tip">
  <div class="callout-title">Tip de Examen CKA</div>
  Cuando se consultan logs de un Pod multi-contenedor, el flag <code>-c &lt;nombre-contenedor&gt;</code> es estrictamente obligatorio; de lo contrario, <code>kubectl logs</code> devolverá error pidiendo especificar el contenedor.
</div>
"""
        },
        {
            "id": "sol-1-2",
            "ex_id": "ex-1-2",
            "num": "Solución 1.2:",
            "title": "Inicialización con InitContainer para Validación de Dependencias",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Los <code>initContainers</code> se ejecutan en orden secuencial antes de que los contenedores de la aplicación se inicien. Si un InitContainer no finaliza con código de salida 0, el Pod se reinicia según su <code>restartPolicy</code> y los contenedores principales nunca se ejecutan.</p>

<p><strong>Manifiesto Declarativo YAML:</strong></p>
<pre><code>apiVersion: v1
kind: Pod
metadata:
  name: pod-backend-init
  namespace: lab-pods
  labels:
    tier: backend
spec:
  initContainers:
    - name: wait-db
      image: busybox:1.36
      command: ['sh', '-c']
      args:
        - |
          echo "Verificando disponibilidad de db-service:3306...";
          until nc -z -w 2 db-service 3306; do
            echo "Base de datos no alcanzable aún. Esperando 3s...";
            sleep 3;
          done;
          echo "¡Conexión establecida exitosamente!";
  containers:
    - name: backend-api
      image: nginx:1.25-alpine
      ports:
        - containerPort: 80</code></pre>

<p><strong>Validación y Simulación del Servicio Dependiente:</strong></p>
<pre><code># 1. Crear el pod con el initContainer
kubectl apply -f pod-backend-init.yaml

# 2. Comprobar estado: Debe quedar en Init:0/1
kubectl get pod -n lab-pods pod-backend-init
kubectl logs -n lab-pods pod-backend-init -c wait-db

# 3. Simular la base de datos creando un pod y servicio temporal
kubectl run db-service --image=busybox:1.36 -n lab-pods --port=3306 -- nc -lk -p 3306
kubectl expose pod db-service -n lab-pods --port=3306

# 4. Verificar que pod-backend-init transiciona a Running (1/1)
kubectl get pod -n lab-pods pod-backend-init -w</code></pre>

<div class="callout callout-warning">
  <div class="callout-title">Trampa Frecuente</div>
  Si el servicio <code>db-service</code> se crea en otro namespace, la resolución DNS requerirá el FQDN completo: <code>db-service.&lt;otro-namespace&gt;.svc.cluster.local</code>. En este ejercicio, ambos conviven en <code>lab-pods</code>.
</div>
"""
        },
        {
            "id": "sol-1-3",
            "ex_id": "ex-1-3",
            "num": "Solución 1.3:",
            "title": "Resiliencia Avanzada con Startup, Liveness y Readiness Probes",
            "content_html": """
<p><strong>Explicación Técnica:</strong> La combinación correcta de las 3 sondas evita bucles de muerte (CrashLoop) en arranques lentos (startupProbe deshabilita liveness y readiness hasta tener éxito), asegura que el tráfico solo llegue a Pods operativos (readinessProbe) y reinicia instancias congeladas (livenessProbe).</p>

<p><strong>Manifiesto Declarativo YAML:</strong></p>
<pre><code>apiVersion: v1
kind: Pod
metadata:
  name: pod-health-hardened
  namespace: lab-pods
  labels:
    app: hardened-web
spec:
  containers:
    - name: web
      image: nginx:1.25-alpine
      ports:
        - containerPort: 80
      # 1. Startup Probe: da hasta 10 * 5s = 50s para arrancar
      startupProbe:
        httpGet:
          path: /
          port: 80
        initialDelaySeconds: 2
        periodSeconds: 5
        failureThreshold: 10
      # 2. Liveness Probe: reinicia si el servicio muere tras el startup
      livenessProbe:
        httpGet:
          path: /
          port: 80
        periodSeconds: 10
        timeoutSeconds: 2
        failureThreshold: 3
      # 3. Readiness Probe: extrae el Pod de los endpoints si no está listo
      readinessProbe:
        httpGet:
          path: /
          port: 80
        periodSeconds: 5
        successThreshold: 1
        failureThreshold: 2</code></pre>

<p><strong>Validación Operativa:</strong></p>
<pre><code># 1. Aplicar y verificar registro de sondas
kubectl apply -f pod-probes.yaml
kubectl describe pod -n lab-pods pod-health-hardened | grep -E "Startup|Liveness|Readiness"

# 2. Simular fallo de readiness
kubectl exec -n lab-pods pod-health-hardened -c web -- mv /usr/share/nginx/html/index.html /tmp/
# Observar que el Pod pasa a READY 0/1 sin reiniciarse inmediatamente
kubectl get pod -n lab-pods pod-health-hardened

# 3. Tras fallar la livenessProbe (3 fallos * 10s = 30s), Kubelet reinicia el contenedor
kubectl get pod -n lab-pods pod-health-hardened</code></pre>
"""
        }
    ]
}

MODULE_REPLICASETS = {
    "id": "replicasets",
    "num": "2",
    "name": "ReplicaSets: Controladores de Réplicas y Auto-sanación",
    "ns": "lab-replicasets",
    "description": "El ReplicaSet garantiza que un número específico de réplicas de Pods idénticos se encuentren en ejecución en cualquier momento. Se evalúa el funcionamiento de sus selectores basados en conjuntos, la auto-sanación y la gestión de Pods huérfanos.",
    "exercises": [
        {
            "id": "ex-2-1",
            "sol_id": "sol-2-1",
            "num": "Ejercicio 2.1:",
            "title": "Selectores Basados en Conjuntos (matchExpressions) y Adopción de Pods",
            "difficulty_label": "Intermedio",
            "difficulty_class": "intermedio",
            "scenario": "Un equipo ha desplegado manualmente dos Pods etiquetados para pre-producción. Se debe crear un ReplicaSet con selectores avanzados que adopte automáticamente dichos Pods y complete las réplicas restantes.",
            "requirements": [
                "Crear el namespace <code>lab-replicasets</code>.",
                "Crear manualmente un Pod llamado <code>legacy-pod-1</code> con etiquetas <code>app: payment, tier: backend, env: staging</code>.",
                "Crear un ReplicaSet llamado <code>rs-payment-processor</code> con <code>replicas: 3</code>.",
                "El selector del ReplicaSet debe usar <code>matchExpressions</code>: <code>app In [payment]</code> y <code>env In [staging, production]</code>.",
                "La plantilla de Pods (template) debe generar Pods con imagen <code>nginx:1.25-alpine</code> y las etiquetas correspondientes."
            ],
            "verification": "<p>Ejecutar <code>kubectl get pods -n lab-replicasets --show-labels</code> y verificar que el ReplicaSet sólo creó 2 Pods nuevos porque adoptó a <code>legacy-pod-1</code>, sumando 3 réplicas en total.</p>"
        },
        {
            "id": "ex-2-2",
            "sol_id": "sol-2-2",
            "num": "Ejercicio 2.2:",
            "title": "Escalado Elástico y Prueba de Auto-recuperación",
            "difficulty_label": "Intermedio",
            "difficulty_class": "intermedio",
            "scenario": "Es necesario verificar el comportamiento del bucle de reconciliación de Kubernetes cuando se producen picos de carga y caídas intencionadas de procesos.",
            "requirements": [
                "Crear un ReplicaSet <code>rs-elastic-worker</code> en <code>lab-replicasets</code> con 2 réplicas usando <code>redis:7.2-alpine</code>.",
                "Escalar imperativamente el ReplicaSet a 5 réplicas mediante <code>kubectl scale</code>.",
                "Eliminar forzosamente dos de los Pods existentes y comprobar la reacción del controlador.",
                "Verificar los eventos del ReplicaSet con <code>kubectl describe</code>."
            ],
            "verification": "<p>Al eliminar 2 Pods, el ReplicaSet debe instanciar de forma inmediata 2 Pods sustitutos con nuevos IDs de Pod, manteniendo permanentemente 5 réplicas en estado Running.</p>"
        },
        {
            "id": "ex-2-3",
            "sol_id": "sol-2-3",
            "num": "Ejercicio 2.3:",
            "title": "Aislamiento y Depuración de un Pod en Caliente (Quarantine)",
            "difficulty_label": "Nivel CKA",
            "difficulty_class": "cka",
            "scenario": "Uno de los Pods gestionados por un ReplicaSet presenta un consumo anómalo o comportamiento errático. Para depurarlo sin afectar a los clientes y sin que el cluster pierda su número deseado de réplicas, se debe 'aislar' el Pod de su controlador cambiando sus etiquetas.",
            "requirements": [
                "Partir de un ReplicaSet <code>rs-monitored</code> con <code>replicas: 3</code> y selector <code>app: web-worker</code>.",
                "Seleccionar uno de los 3 Pods en ejecución y modificar su etiqueta para que sea <code>app: debug-quarantine</code>.",
                "Observar cómo el ReplicaSet detecta la falta de un Pod con <code>app: web-worker</code> y crea un cuarto Pod en el clúster.",
                "Verificar que el Pod aislado continúa en ejecución de forma independiente para tareas de diagnóstico forense."
            ],
            "verification": "<p>Ejecutar <code>kubectl get pods -n lab-replicasets</code>. Deben existir 4 Pods en total: 3 vinculados al ReplicaSet y 1 huérfano con la etiqueta de cuarentena.</p>"
        }
    ],
    "solutions": [
        {
            "id": "sol-2-1",
            "ex_id": "ex-2-1",
            "num": "Solución 2.1:",
            "title": "Selectores Basados en Conjuntos (matchExpressions) y Adopción de Pods",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Los ReplicaSets no crean réplicas si ya existen Pods cuyas etiquetas satisfacen sus selectores. El selector con <code>matchExpressions</code> permite reglas lógicas avanzadas con operadores <code>In</code>, <code>NotIn</code>, <code>Exists</code> y <code>DoesNotExist</code>.</p>

<p><strong>Comandos y Manifiesto YAML:</strong></p>
<pre><code># 1. Crear namespace y Pod preexistente
kubectl create namespace lab-replicasets
kubectl run legacy-pod-1 --namespace=lab-replicasets --image=nginx:1.25-alpine \\
  --labels="app=payment,tier=backend,env=staging"</code></pre>

<p><strong>Manifiesto del ReplicaSet:</strong></p>
<pre><code>apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: rs-payment-processor
  namespace: lab-replicasets
spec:
  replicas: 3
  selector:
    matchExpressions:
      - {key: app, operator: In, values: [payment]}
      - {key: env, operator: In, values: [staging, production]}
  template:
    metadata:
      labels:
        app: payment
        tier: backend
        env: staging
    spec:
      containers:
        - name: processor
          image: nginx:1.25-alpine
          ports:
            - containerPort: 80</code></pre>

<p><strong>Validación:</strong></p>
<pre><code>kubectl apply -f rs-payment.yaml
# Comprobar que legacy-pod-1 tiene como Controller al ReplicaSet
kubectl get pods -n lab-replicasets -l app=payment --show-labels</code></pre>
"""
        },
        {
            "id": "sol-2-2",
            "ex_id": "ex-2-2",
            "num": "Solución 2.2:",
            "title": "Escalado Elástico y Prueba de Auto-recuperación",
            "content_html": """
<p><strong>Explicación Técnica:</strong> El controlador del ReplicaSet ejecuta un bucle continuo de control (Reconciliation Loop) comparando el estado actual con el estado deseado declarado en <code>spec.replicas</code>.</p>

<p><strong>Manifiesto YAML Base:</strong></p>
<pre><code>apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: rs-elastic-worker
  namespace: lab-replicasets
spec:
  replicas: 2
  selector:
    matchLabels:
      app: elastic-worker
  template:
    metadata:
      labels:
        app: elastic-worker
    spec:
      containers:
        - name: redis
          image: redis:7.2-alpine</code></pre>

<p><strong>Comandos Imperativos de Escalado y Prueba de Resiliencia:</strong></p>
<pre><code># 1. Desplegar
kubectl apply -f rs-elastic.yaml

# 2. Escalar a 5 réplicas
kubectl scale rs rs-elastic-worker -n lab-replicasets --replicas=5
kubectl get pods -n lab-replicasets -l app=elastic-worker

# 3. Matar dos pods de forma simultánea
PODS_TO_DELETE=$(kubectl get pods -n lab-replicasets -l app=elastic-worker -o jsonpath='{.items[0..1].metadata.name}')
kubectl delete pods -n lab-replicasets $PODS_TO_DELETE

# 4. Comprobar que el número total se mantiene inmediatamente en 5
kubectl get rs -n lab-replicasets rs-elastic-worker</code></pre>
"""
        },
        {
            "id": "sol-2-3",
            "ex_id": "ex-2-3",
            "num": "Solución 2.3:",
            "title": "Aislamiento y Depuración de un Pod en Caliente (Quarantine)",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Los ReplicaSets gestionan Pods basándose exclusivamente en etiquetas. Si alteramos la etiqueta de un Pod en ejecución con <code>--overwrite</code>, el ReplicaSet ya no lo reconocerá como suyo, lo desasociará y generará un reemplazo para volver a cumplir la cuota deseada.</p>

<p><strong>Procedimiento Paso a Paso:</strong></p>
<pre><code># 1. Desplegar el ReplicaSet inicial
cat &lt;&lt;EOF | kubectl apply -f -
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: rs-monitored
  namespace: lab-replicasets
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-worker
  template:
    metadata:
      labels:
        app: web-worker
    spec:
      containers:
        - name: nginx
          image: nginx:1.25-alpine
EOF

# 2. Identificar el nombre de uno de los pods
TARGET_POD=$(kubectl get pods -n lab-replicasets -l app=web-worker -o jsonpath='{.items[0].metadata.name}')
echo "Aislando pod: $TARGET_POD"

# 3. Sobreescribir la etiqueta selectora para sacarlo del control del ReplicaSet
kubectl label pod $TARGET_POD -n lab-replicasets app=debug-quarantine --overwrite

# 4. Verificar que existen 4 pods: 3 del RS y 1 aislado
kubectl get pods -n lab-replicasets -L app</code></pre>

<div class="callout callout-tip">
  <div class="callout-title">Patrón Clave en Producción</div>
  Esta técnica es la recomendada en incidentes reales (Troubleshooting) para conectarse mediante <code>kubectl exec</code> a un Pod defectuoso sin que el tráfico de los usuarios continúe impactando en él.
</div>
"""
        }
    ]
}

MODULE_DEPLOYMENTS = {
    "id": "deployments",
    "num": "3",
    "name": "Deployments: Actualizaciones Continuas y Estrategias Rollout",
    "ns": "lab-deployments",
    "description": "Los Deployments gestionan ReplicaSets de forma declarativa y permiten actualizaciones sin caída de servicio (RollingUpdate), pausas, revisiones históricas y rollback instantáneo.",
    "exercises": [
        {
            "id": "ex-3-1",
            "sol_id": "sol-3-1",
            "num": "Ejercicio 3.1:",
            "title": "Despliegue Declarativo con Requests y Limits de Recursos",
            "difficulty_label": "Intermedio",
            "difficulty_class": "intermedio",
            "scenario": "Para garantizar la estabilidad del clúster y evitar el efecto 'vecino ruidoso' (noisy neighbor), todos los Pods de la aplicación web deben declarar explícitamente sus peticiones mínimas y techos de memoria y CPU.",
            "requirements": [
                "Crear el namespace <code>lab-deployments</code>.",
                "Crear un Deployment llamado <code>deploy-web-secured</code> con 3 réplicas e imagen <code>nginx:1.25-alpine</code>.",
                "Etiqueta del Deployment y del Pod: <code>app: web-secured, tier: frontend</code>.",
                "Configurar <code>resources.requests</code>: 64Mi de memoria y 50m de CPU.",
                "Configurar <code>resources.limits</code>: 128Mi de memoria y 100m de CPU.",
                "El contenedor debe exponer el puerto 80 con nombre <code>http</code>."
            ],
            "verification": "<p>Ejecutar <code>kubectl get deployment -n lab-deployments deploy-web-secured -o jsonpath='{.spec.template.spec.containers[0].resources}'</code> y comprobar que los límites y peticiones coinciden exactamente.</p>"
        },
        {
            "id": "ex-3-2",
            "sol_id": "sol-3-2",
            "num": "Ejercicio 3.2:",
            "title": "RollingUpdate Controlado con maxSurge y maxUnavailable",
            "difficulty_label": "Nivel CKA",
            "difficulty_class": "cka",
            "scenario": "En un entorno de alta disponibilidad se actualiza un microservicio de 4 réplicas. La política de la empresa exige que durante la actualización nunca haya menos del 100% de la capacidad disponible y que no se incremente el consumo de recursos en más de 1 Pod adicional a la vez.",
            "requirements": [
                "Crear un Deployment <code>deploy-rolling-tuned</code> en <code>lab-deployments</code> con <code>replicas: 4</code> e imagen <code>httpd:2.4-alpine</code>.",
                "Configurar la estrategia <code>RollingUpdate</code> con <code>maxUnavailable: 0</code> y <code>maxSurge: 1</code>.",
                "Actualizar la imagen a <code>httpd:2.4.58-alpine</code>.",
                "Monitorear el estado del despliegue en tiempo real con <code>kubectl rollout status</code>."
            ],
            "verification": "<p>Durante el proceso de actualización, comprobar que en ningún momento el número de réplicas en estado Ready desciende de 4 y que el total temporal de réplicas no excede de 5.</p>"
        },
        {
            "id": "ex-3-3",
            "sol_id": "sol-3-3",
            "num": "Ejercicio 3.3:",
            "title": "Simulación de Release Fallida y Rollback a Revisión Específica",
            "difficulty_label": "Nivel CKA",
            "difficulty_class": "cka",
            "scenario": "Durante una guardia se despliega por error una versión con una imagen inexistente, provocando que los nuevos Pods queden en ImagePullBackOff. Se debe diagnosticar el problema y revertir el despliegue a la versión previa saludable usando el historial de rollout.",
            "requirements": [
                "Desplegar <code>deploy-ecommerce</code> en <code>lab-deployments</code> con <code>nginx:1.24-alpine</code> y <code>--record</code> o anotación de cambio.",
                "Actualizar intencionadamente la imagen a una etiqueta inválida: <code>nginx:v999.invalid</code>.",
                "Comprobar cómo los pods nuevos quedan en <code>ErrImagePull</code> o <code>ImagePullBackOff</code> mientras los pods viejos continúan dando servicio.",
                "Examinar el historial de revisiones con <code>kubectl rollout history</code>.",
                "Ejecutar un rollback a la revisión estable previa (revisión 1) y confirmar el restablecimiento del estado <code>Running</code>."
            ],
            "verification": "<p>Ejecutar <code>kubectl rollout status deployment/deploy-ecommerce -n lab-deployments</code> y verificar que finaliza con éxito mostrando la imagen <code>nginx:1.24-alpine</code> en todos los Pods.</p>"
        }
    ],
    "solutions": [
        {
            "id": "sol-3-1",
            "ex_id": "ex-3-1",
            "num": "Solución 3.1:",
            "title": "Despliegue Declarativo con Requests y Limits de Recursos",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Los <code>requests</code> determinan qué nodo puede alojar el Pod (scheduling), mientras que los <code>limits</code> son aplicados por cgroups en el kernel de Linux. Superar el límite de memoria provoca terminación inmediata por OOMKilled.</p>

<p><strong>Manifiesto Declarativo YAML:</strong></p>
<pre><code>apiVersion: v1
kind: Namespace
metadata:
  name: lab-deployments
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deploy-web-secured
  namespace: lab-deployments
  labels:
    app: web-secured
    tier: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-secured
  template:
    metadata:
      labels:
        app: web-secured
        tier: frontend
    spec:
      containers:
        - name: nginx
          image: nginx:1.25-alpine
          ports:
            - name: http
              containerPort: 80
          resources:
            requests:
              memory: "64Mi"
              cpu: "50m"
            limits:
              memory: "128Mi"
              cpu: "100m"</code></pre>

<p><strong>Comando Imperativo Rápido (Truco CKA):</strong></p>
<pre><code>kubectl create deployment deploy-web-secured -n lab-deployments --image=nginx:1.25-alpine \\
  --replicas=3 --dry-run=client -o yaml &gt; deploy.yaml
# Añadir la sección resources en el fichero generado y aplicar:
kubectl apply -f deploy.yaml</code></pre>
"""
        },
        {
            "id": "sol-3-2",
            "ex_id": "ex-3-2",
            "num": "Solución 3.2:",
            "title": "RollingUpdate Controlado con maxSurge y maxUnavailable",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Con <code>maxUnavailable: 0</code>, Kubernetes no apagará ningún Pod existente hasta que un nuevo Pod esté completamente en estado Ready. Con <code>maxSurge: 1</code>, creará los nuevos Pods de uno en uno.</p>

<p><strong>Manifiesto Declarativo YAML:</strong></p>
<pre><code>apiVersion: apps/v1
kind: Deployment
metadata:
  name: deploy-rolling-tuned
  namespace: lab-deployments
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: rolling-tuned
  template:
    metadata:
      labels:
        app: rolling-tuned
    spec:
      containers:
        - name: httpd
          image: httpd:2.4-alpine
          ports:
            - containerPort: 80</code></pre>

<p><strong>Actualización y Seguimiento:</strong></p>
<pre><code># 1. Aplicar el deployment base
kubectl apply -f deploy-rolling.yaml

# 2. Actualizar la imagen imperativamente
kubectl set image deployment/deploy-rolling-tuned httpd=httpd:2.4.58-alpine -n lab-deployments

# 3. Seguir el progreso del despliegue paso a paso
kubectl rollout status deployment/deploy-rolling-tuned -n lab-deployments</code></pre>
"""
        },
        {
            "id": "sol-3-3",
            "ex_id": "ex-3-3",
            "num": "Solución 3.3:",
            "title": "Simulación de Release Fallida y Rollback a Revisión Específica",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Kubernetes almacena el historial de revisiones creando un ReplicaSet nuevo para cada cambio en el template de Pods. Si una nueva versión falla, la versión anterior permanece en ejecución hasta que la nueva alcance el estado Ready, protegiendo a los usuarios finales.</p>

<p><strong>Procedimiento Completo de Fallo y Rollback:</strong></p>
<pre><code># 1. Crear despliegue inicial estable
kubectl create deployment deploy-ecommerce -n lab-deployments --image=nginx:1.24-alpine --replicas=3
kubectl annotate deployment/deploy-ecommerce -n lab-deployments kubernetes.io/change-cause="Version 1.0 estable"

# 2. Provocar el fallo con imagen errónea
kubectl set image deployment/deploy-ecommerce nginx=nginx:v999.invalid -n lab-deployments
kubectl annotate deployment/deploy-ecommerce -n lab-deployments kubernetes.io/change-cause="Update fallido v999"

# 3. Comprobar que los nuevos pods quedan bloqueados
kubectl get pods -n lab-deployments -l app=deploy-ecommerce

# 4. Inspeccionar el historial
kubectl rollout history deployment/deploy-ecommerce -n lab-deployments

# 5. Ejecutar Rollback a la revision 1
kubectl rollout undo deployment/deploy-ecommerce -n lab-deployments --to-revision=1

# 6. Comprobar resolucion exitosa
kubectl rollout status deployment/deploy-ecommerce -n lab-deployments
kubectl get deployment -n lab-deployments deploy-ecommerce -o wide</code></pre>
"""
        }
    ]
}

MODULE_SERVICES = {
    "id": "services",
    "num": "4",
    "name": "Services: Abstracción de Red y Descubrimiento",
    "ns": "lab-services",
    "description": "Los Servicios proporcionan una dirección IP virtual estable y un nombre DNS interno para balancear el tráfico entre Pods dinámicos. Se exploran ClusterIP, NodePort y Headless Services.",
    "exercises": [
        {
            "id": "ex-4-1",
            "sol_id": "sol-4-1",
            "num": "Ejercicio 4.1:",
            "title": "Servicio ClusterIP con Desacoplamiento de Puertos y Endpoints",
            "difficulty_label": "Intermedio",
            "difficulty_class": "intermedio",
            "scenario": "Un backend escrito en NodeJS escucha internamente en el puerto 3000. La arquitectura de microservicios exige que otros servicios del clúster se conecten a él a través del puerto HTTP estándar 80 mediante un servicio ClusterIP.",
            "requirements": [
                "Crear el namespace <code>lab-services</code>.",
                "Crear un Deployment con 2 réplicas llamado <code>deploy-api-node</code> con imagen <code>hashicorp/http-echo:latest</code> y argumentos <code>-text='Respuesta de API'</code> y <code>-listen=:3000</code>.",
                "Crear un Service tipo <code>ClusterIP</code> llamado <code>svc-api-node</code> en <code>lab-services</code>.",
                "Configurar <code>port: 80</code> y <code>targetPort: 3000</code> con selector hacia los Pods de la API.",
                "Verificar los Endpoints asociados al servicio."
            ],
            "verification": "<p>Ejecutar <code>kubectl get endpoints -n lab-services svc-api-node</code> y comprobar que aparecen listadas las IPs de los dos Pods en el puerto 3000. Probar un <code>curl</code> desde un Pod busybox temporal a <code>http://svc-api-node:80</code>.</p>"
        },
        {
            "id": "ex-4-2",
            "sol_id": "sol-4-2",
            "num": "Ejercicio 4.2:",
            "title": "Exposición Externa mediante Servicio NodePort en Puerto Fijo",
            "difficulty_label": "Intermedio",
            "difficulty_class": "intermedio",
            "scenario": "Un panel de administración interno necesita ser accesible desde las máquinas anfitrionas del laboratorio sin usar balanceadores externos en la nube, fijando un puerto específico en todos los nodos del clúster.",
            "requirements": [
                "Desplegar una aplicación web llamada <code>web-admin</code> en <code>lab-services</code> con imagen <code>nginx:1.25-alpine</code>.",
                "Crear un Service tipo <code>NodePort</code> llamado <code>svc-admin-nodeport</code>.",
                "El servicio debe exponer el puerto 80 del servicio, apuntar al puerto 80 del contenedor y reservar exactamente el <code>nodePort: 30088</code>.",
                "Comprobar el acceso a través de la IP de cualquier nodo del clúster en el puerto 30088."
            ],
            "verification": "<p>Ejecutar <code>curl http://&lt;IP-NODO&gt;:30088</code> desde el terminal del host y verificar que devuelve la página de bienvenida de Nginx con código 200 OK.</p>"
        },
        {
            "id": "ex-4-3",
            "sol_id": "sol-4-3",
            "num": "Ejercicio 4.3:",
            "title": "Headless Service (clusterIP: None) y Resolución DNS Directa",
            "difficulty_label": "Nivel CKA",
            "difficulty_class": "cka",
            "scenario": "Bases de datos distribuidas y clústeres como Cassandra, Kafka o Elasticsearch requieren comunicarse directamente Pod a Pod sin pasar por la IP virtual proxy del balanceador. Se debe configurar un Headless Service y validar sus registros DNS A y SRV.",
            "requirements": [
                "Crear un Deployment <code>deploy-cluster-members</code> en <code>lab-services</code> con 3 réplicas.",
                "Crear un Service con nombre <code>svc-headless</code> con <code>clusterIP: None</code> apuntando al puerto 80 de los Pods.",
                "Desplegar un Pod temporal con herramientas DNS (<code>dnsutils</code>) para inspeccionar la respuesta de CoreDNS.",
                "Ejecutar <code>nslookup svc-headless.lab-services.svc.cluster.local</code> y analizar la salida."
            ],
            "verification": "<p>A diferencia de un ClusterIP normal que devuelve una única IP virtual, el comando <code>nslookup</code> sobre el servicio Headless debe devolver directamente las 3 IPs individuales de los Pods activos.</p>"
        }
    ],
    "solutions": [
        {
            "id": "sol-4-1",
            "ex_id": "ex-4-1",
            "num": "Solución 4.1:",
            "title": "Servicio ClusterIP con Desacoplamiento de Puertos y Endpoints",
            "content_html": """
<p><strong>Explicación Técnica:</strong> El objeto <code>Service</code> abstrae los Pods mediante etiquetas. El campo <code>port</code> es el puerto expuesto en el clúster por el Service, mientras que <code>targetPort</code> es el puerto real en el que escucha el contenedor dentro del Pod.</p>

<p><strong>Manifiesto YAML:</strong></p>
<pre><code>apiVersion: v1
kind: Namespace
metadata:
  name: lab-services
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deploy-api-node
  namespace: lab-services
spec:
  replicas: 2
  selector:
    matchLabels:
      app: api-node
  template:
    metadata:
      labels:
        app: api-node
    spec:
      containers:
        - name: echo
          image: hashicorp/http-echo:latest
          args:
            - "-text=Respuesta de API"
            - "-listen=:3000"
          ports:
            - containerPort: 3000
---
apiVersion: v1
kind: Service
metadata:
  name: svc-api-node
  namespace: lab-services
spec:
  type: ClusterIP
  selector:
    app: api-node
  ports:
    - name: http
      port: 80
      targetPort: 3000</code></pre>

<p><strong>Comprobación de Endpoints y Tráfico:</strong></p>
<pre><code># 1. Aplicar manifiestos
kubectl apply -f svc-clusterip.yaml

# 2. Inspeccionar los endpoints vinculados
kubectl get endpoints -n lab-services svc-api-node

# 3. Validar conectividad interna desde un pod temporal
kubectl run test-curl --rm -it -n lab-services --image=curlimages/curl:8.6.0 -- \\
  curl -s http://svc-api-node:80</code></pre>
"""
        },
        {
            "id": "sol-4-2",
            "ex_id": "ex-4-2",
            "num": "Solución 4.2:",
            "title": "Exposición Externa mediante Servicio NodePort en Puerto Fijo",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Un servicio NodePort asigna un puerto en el rango 30000-32767 en todas las interfaces de red de cada nodo del clúster (Worker y Control Plane). Kube-proxy enruta los paquetes entrantes al NodePort hacia los Pods correspondientes.</p>

<p><strong>Manifiesto YAML:</strong></p>
<pre><code>apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-admin
  namespace: lab-services
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web-admin
  template:
    metadata:
      labels:
        app: web-admin
    spec:
      containers:
        - name: nginx
          image: nginx:1.25-alpine
          ports:
            - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: svc-admin-nodeport
  namespace: lab-services
spec:
  type: NodePort
  selector:
    app: web-admin
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30088</code></pre>

<p><strong>Verificación:</strong></p>
<pre><code># 1. Aplicar manifiesto
kubectl apply -f svc-nodeport.yaml

# 2. Obtener la IP de un nodo
NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}')
echo "Probando en: http://$NODE_IP:30088"

# 3. Realizar petición HTTP
curl -I http://$NODE_IP:30088</code></pre>
"""
        },
        {
            "id": "sol-4-3",
            "ex_id": "ex-4-3",
            "num": "Solución 4.3:",
            "title": "Headless Service (clusterIP: None) y Resolución DNS Directa",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Al declarar <code>clusterIP: None</code>, Kubernetes no reserva ninguna IP virtual en el rango de servicios ni crea reglas de proxy en iptables/IPVS. CoreDNS responde a las peticiones del nombre del servicio devolviendo directamente la lista de IPs de los Pods asociados.</p>

<p><strong>Manifiesto YAML:</strong></p>
<pre><code>apiVersion: apps/v1
kind: Deployment
metadata:
  name: deploy-cluster-members
  namespace: lab-services
spec:
  replicas: 3
  selector:
    matchLabels:
      role: member
  template:
    metadata:
      labels:
        role: member
    spec:
      containers:
        - name: web
          image: nginx:1.25-alpine
          ports:
            - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: svc-headless
  namespace: lab-services
spec:
  clusterIP: None
  selector:
    role: member
  ports:
    - port: 80
      targetPort: 80</code></pre>

<p><strong>Inspección DNS con nslookup:</strong></p>
<pre><code># 1. Aplicar
kubectl apply -f svc-headless.yaml

# 2. Consultar DNS desde un pod temporal con dnsutils
kubectl run dns-test --rm -it -n lab-services --image=registry.k8s.io/e2e-test-images/jessie-dnsutils:1.3 -- \\
  nslookup svc-headless.lab-services.svc.cluster.local

# Observar que la respuesta contiene las 3 IPs de los pods (Address 1, Address 2, Address 3)</code></pre>

<div class="callout callout-tip">
  <div class="callout-title">Uso en StatefulSets</div>
  Los Headless Services son un requisito indispensable para los StatefulSets, ya que permiten resolver a cada Pod individual por su nombre canónico (ej: <code>web-0.svc-headless</code>, <code>web-1.svc-headless</code>).
</div>
"""
        }
    ]
}

MODULES_FUNDAMENTOS = [MODULE_PODS, MODULE_REPLICASETS, MODULE_DEPLOYMENTS, MODULE_SERVICES]
