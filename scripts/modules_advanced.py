# =============================================================================
# scripts/modules_advanced.py
# Módulos 8 a 10: Jobs/CronJobs, DaemonSets, StatefulSets
# =============================================================================

MODULE_JOBS = {
    "id": "jobs",
    "num": "8",
    "name": "Jobs y CronJobs: Cargas de Trabajo por Lotes",
    "ns": "lab-jobs",
    "description": "Los Jobs gestionan tareas batch que se ejecutan hasta finalizar con éxito (código de salida 0). Los CronJobs añaden planificación periódica temporal basada en expresiones cron estándar.",
    "exercises": [
        {
            "id": "ex-8-1",
            "sol_id": "sol-8-1",
            "num": "Ejercicio 8.1:",
            "title": "Job Batch de Una Sola Ejecución con Control de Reintentos",
            "difficulty_label": "Intermedio",
            "difficulty_class": "intermedio",
            "scenario": "Se necesita ejecutar una tarea de migración de esquema en la base de datos. La tarea debe reintentar hasta 3 veces si falla, pero si trascurren más de 120 segundos en total debe ser cancelada por timeout.",
            "requirements": [
                "Crear el namespace <code>lab-jobs</code>.",
                "Crear un Job llamado <code>job-schema-migration</code> en <code>lab-jobs</code>.",
                "Configurar <code>backoffLimit: 3</code> y <code>activeDeadlineSeconds: 120</code>.",
                "Contenedor: imagen <code>busybox:1.36</code> con comando que simule una tarea de 10 segundos y termine con éxito: <code>echo 'Iniciando migracion...' && sleep 10 && echo 'Migracion completada exitosamente'</code>.",
                "Configurar <code>restartPolicy: OnFailure</code> en la plantilla del Pod."
            ],
            "verification": "<p>Ejecutar <code>kubectl get job -n lab-jobs job-schema-migration</code> y verificar que el campo <code>COMPLETIONS</code> marca <code>1/1</code> y que el tiempo transcurrido es de unos 10-15s.</p>"
        },
        {
            "id": "ex-8-2",
            "sol_id": "sol-8-2",
            "num": "Ejercicio 8.2:",
            "title": "Job Paralelo con Cola de Completados (completions y parallelism)",
            "difficulty_label": "Nivel CKA",
            "difficulty_class": "cka",
            "scenario": "Para procesar un lote de 6 imágenes de forma acelerada, se requiere un Job que procese un total de 6 tareas con una concurrencia fija de 2 Pods trabajando en paralelo simultáneamente.",
            "requirements": [
                "Crear un Job <code>job-parallel-processor</code> en <code>lab-jobs</code>.",
                "Configurar <code>completions: 6</code> y <code>parallelism: 2</code>.",
                "Contenedor: imagen <code>busybox:1.36</code>, simulando 5 segundos de cómputo por Pod.",
                "Monitorear la ejecución simultánea de los Pods y el incremento del contador de completados."
            ],
            "verification": "<p>Ejecutar <code>kubectl get pods -n lab-jobs -l job-name=job-parallel-processor -w</code> y observar cómo se ejecutan 2 pods a la vez hasta sumar los 6 completados.</p>"
        },
        {
            "id": "ex-8-3",
            "sol_id": "sol-8-3",
            "num": "Ejercicio 8.3:",
            "title": "CronJob Programado con concurrencyPolicy: Forbid e Historial",
            "difficulty_label": "Nivel CKA",
            "difficulty_class": "cka",
            "scenario": "Una tarea de backup debe ejecutarse cada 2 minutos. Si por lentitud del almacenamiento la tarea anterior no ha finalizado cuando toca la siguiente ejecución, el sistema DEBE prohibir la ejecución concurrente para evitar corrupción de datos.",
            "requirements": [
                "Crear un CronJob <code>cron-db-backup</code> en <code>lab-jobs</code> con programación <code>*/2 * * * *</code> (cada 2 minutos).",
                "Configurar <code>concurrencyPolicy: Forbid</code>.",
                "Retener un historial máximo de <code>successfulJobsHistoryLimit: 3</code> y <code>failedJobsHistoryLimit: 1</code>.",
                "El Pod debe ejecutar <code>echo 'Generando backup...' && sleep 30</code> con <code>restartPolicy: OnFailure</code>.",
                "Comprobar las ejecuciones y los Pods generados."
            ],
            "verification": "<p>Ejecutar <code>kubectl get cronjob -n lab-jobs cron-db-backup</code> y verificar los campos <code>SCHEDULE</code> y <code>LAST SCHEDULE</code>.</p>"
        }
    ],
    "solutions": [
        {
            "id": "sol-8-1",
            "ex_id": "ex-8-1",
            "num": "Solución 8.1:",
            "title": "Job Batch de Una Sola Ejecución con Control de Reintentos",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Los Pods creados por un Job deben tener <code>restartPolicy: OnFailure</code> o <code>Never</code> (nunca <code>Always</code>, ya que Always es para servicios continuos como Deployments). El parámetro <code>backoffLimit</code> define los reintentos antes de marcar el Job como fallido.</p>

<p><strong>Manifiesto YAML:</strong></p>
<pre><code>apiVersion: v1
kind: Namespace
metadata:
  name: lab-jobs
---
apiVersion: batch/v1
kind: Job
metadata:
  name: job-schema-migration
  namespace: lab-jobs
spec:
  backoffLimit: 3
  activeDeadlineSeconds: 120
  template:
    spec:
      restartPolicy: OnFailure
      containers:
        - name: migration-worker
          image: busybox:1.36
          command: ["/bin/sh", "-c"]
          args:
            - "echo 'Iniciando migracion...'; sleep 10; echo 'Migracion completada exitosamente'"</code></pre>

<p><strong>Validación:</strong></p>
<pre><code>kubectl apply -f job-single.yaml
kubectl get job -n lab-jobs job-schema-migration -w
kubectl logs -n lab-jobs -l job-name=job-schema-migration</code></pre>
"""
        },
        {
            "id": "sol-8-2",
            "ex_id": "ex-8-2",
            "num": "Solución 8.2:",
            "title": "Job Paralelo con Cola de Completados (completions y parallelism)",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Con <code>parallelism: 2</code>, Kubernetes mantendrá siempre 2 Pods ejecutándose en paralelo hasta que la suma de ejecuciones exitosas alcance <code>completions: 6</code>.</p>

<p><strong>Manifiesto YAML:</strong></p>
<pre><code>apiVersion: batch/v1
kind: Job
metadata:
  name: job-parallel-processor
  namespace: lab-jobs
spec:
  completions: 6
  parallelism: 2
  template:
    metadata:
      labels:
        job: parallel-demo
    spec:
      restartPolicy: OnFailure
      containers:
        - name: worker
          image: busybox:1.36
          command: ["/bin/sh", "-c"]
          args:
            - "echo 'Procesando chunk en pod: $HOSTNAME'; sleep 5; echo 'Finalizado'"</code></pre>

<p><strong>Validación:</strong></p>
<pre><code>kubectl apply -f job-parallel.yaml
kubectl get pods -n lab-jobs -l job=parallel-demo -w</code></pre>
"""
        },
        {
            "id": "sol-8-3",
            "ex_id": "ex-8-3",
            "num": "Solución 8.3:",
            "title": "CronJob Programado con concurrencyPolicy: Forbid e Historial",
            "content_html": """
<p><strong>Explicación Técnica:</strong> La directiva <code>concurrencyPolicy</code> acepta 3 valores: <code>Allow</code> (permite solapamiento), <code>Forbid</code> (si el anterior sigue activo, omite la nueva ejecución) y <code>Replace</code> (mata el anterior e inicia el nuevo).</p>

<p><strong>Manifiesto YAML:</strong></p>
<pre><code>apiVersion: batch/v1
kind: CronJob
metadata:
  name: cron-db-backup
  namespace: lab-jobs
spec:
  schedule: "*/2 * * * *"
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
            - name: backup
              image: busybox:1.36
              command: ["/bin/sh", "-c"]
              args:
                - "echo '[$(date)] Generando backup de base de datos...'; sleep 30; echo 'Backup guardado.'"</code></pre>

<p><strong>Validación y Disparo Manual (Truco CKA):</strong></p>
<pre><code># 1. Aplicar CronJob
kubectl apply -f cronjob.yaml

# 2. Para no esperar 2 minutos en examen, disparar Job manual del CronJob:
kubectl create job --from=cronjob/cron-db-backup test-manual-run -n lab-jobs
kubectl get job -n lab-jobs test-manual-run</code></pre>
"""
        }
    ]
}

MODULE_DAEMONSETS = {
    "id": "daemonsets",
    "num": "9",
    "name": "DaemonSets: Agentes de Nodo y Tolerancias",
    "ns": "lab-daemonsets",
    "description": "Los DaemonSets aseguran que una copia de un Pod se ejecute en todos (o en un subconjunto específico) de los nodos del clúster. Es el recurso idóneo para recolectores de logs, agentes de métricas y proxies de red.",
    "exercises": [
        {
            "id": "ex-9-1",
            "sol_id": "sol-9-1",
            "num": "Ejercicio 9.1:",
            "title": "Agente de Recolección de Logs de Nodo montando /var/log",
            "difficulty_label": "Intermedio",
            "difficulty_class": "intermedio",
            "scenario": "El equipo de observabilidad necesita desplegar un agente FluentBit/Fluentd en cada nodo trabajador para leer los registros generados por el sistema operativo y el runtime de contenedores en `/var/log`.",
            "requirements": [
                "Crear el namespace <code>lab-daemonsets</code>.",
                "Crear un DaemonSet llamado <code>ds-node-log-collector</code> en <code>lab-daemonsets</code>.",
                "Montar el directorio del host <code>/var/log</code> en modo solo lectura (<code>readOnly: true</code>) dentro del contenedor en <code>/host/var/log</code>.",
                "Contenedor: imagen <code>busybox:1.36</code> con comando para monitorizar archivos del nodo.",
                "Verificar que se crea exactamente un Pod por cada nodo activo del clúster."
            ],
            "verification": "<p>Ejecutar <code>kubectl get daemonset -n lab-daemonsets ds-node-log-collector</code> y comprobar que el número en <code>DESIRED</code> coincide con el número en <code>CURRENT</code> y <code>READY</code>.</p>"
        },
        {
            "id": "ex-9-2",
            "sol_id": "sol-9-2",
            "num": "Ejercicio 9.2:",
            "title": "Tolerancias para Forzar Ejecución en Nodos del Control Plane",
            "difficulty_label": "Nivel CKA",
            "difficulty_class": "cka",
            "scenario": "Por defecto, los nodos del Control Plane (Master) tienen un taint (`node-role.kubernetes.io/control-plane:NoSchedule`) que impide que los Pods de usuario se ejecuten en ellos. Un agente crítico de seguridad debe ejecutarse obligatoriamente en TODOS los nodos sin excepción, incluyendo los masters.",
            "requirements": [
                "Crear un DaemonSet <code>ds-security-agent</code> en <code>lab-daemonsets</code>.",
                "Añadir tolerancias (<code>tolerations</code>) para el taint de control-plane / master con operador <code>Exists</code> y efecto <code>NoSchedule</code>.",
                "Verificar que los Pods del DaemonSet se programan exitosamente tanto en nodos Workers como en el nodo Control-Plane."
            ],
            "verification": "<p>Ejecutar <code>kubectl get pods -n lab-daemonsets -l app=security-agent -o wide</code> y comprobar que al menos un Pod se ejecuta en el nodo master / control-plane.</p>"
        },
        {
            "id": "ex-9-3",
            "sol_id": "sol-9-3",
            "num": "Ejercicio 9.3:",
            "title": "Actualización Controlada de DaemonSet (RollingUpdate vs OnDelete)",
            "difficulty_label": "Intermedio",
            "difficulty_class": "intermedio",
            "scenario": "Se requiere actualizar la versión del agente en el DaemonSet asegurando que los Pods en los nodos se renueven de forma progresiva sin dejar nodos desatendidos.",
            "requirements": [
                "Comprobar que la estrategia de actualización en <code>spec.updateStrategy.type</code> está fijada en <code>RollingUpdate</code>.",
                "Configurar <code>maxUnavailable: 1</code>.",
                "Actualizar la imagen del DaemonSet de <code>busybox:1.35</code> a <code>busybox:1.36</code>.",
                "Comprobar el despliegue mediante <code>kubectl rollout status ds/ds-node-log-collector</code>."
            ],
            "verification": "<p>Ejecutar <code>kubectl rollout status ds/ds-node-log-collector -n lab-daemonsets</code> y verificar que la actualización concluye con éxito en todos los nodos.</p>"
        }
    ],
    "solutions": [
        {
            "id": "sol-9-1",
            "ex_id": "ex-9-1",
            "num": "Solución 9.1:",
            "title": "Agente de Recolección de Logs de Nodo montando /var/log",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Los DaemonSets utilizan un volumen <code>hostPath</code> para acceder a archivos del sistema de archivos local del nodo físico subyacente.</p>

<p><strong>Manifiesto YAML:</strong></p>
<pre><code>apiVersion: v1
kind: Namespace
metadata:
  name: lab-daemonsets
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: ds-node-log-collector
  namespace: lab-daemonsets
  labels:
    app: node-logger
spec:
  selector:
    matchLabels:
      app: node-logger
  template:
    metadata:
      labels:
        app: node-logger
    spec:
      volumes:
        - name: host-logs
          hostPath:
            path: /var/log
            type: Directory
      containers:
        - name: log-collector
          image: busybox:1.36
          command:
            - /bin/sh
            - -c
            - "tail -n +1 -f /host/var/log/syslog || sleep 3600"
          volumeMounts:
            - name: host-logs
              mountPath: /host/var/log
              readOnly: true</code></pre>

<p><strong>Validación:</strong></p>
<pre><code>kubectl apply -f ds-log-collector.yaml
kubectl get ds -n lab-daemonsets ds-node-log-collector
kubectl get pods -n lab-daemonsets -o wide</code></pre>
"""
        },
        {
            "id": "sol-9-2",
            "ex_id": "ex-9-2",
            "num": "Solución 9.2:",
            "title": "Tolerancias para Forzar Ejecución en Nodos del Control Plane",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Para tolerar cualquier taint de tipo NoSchedule en el nodo master, se define una tolerancia con <code>operator: Exists</code> que empareje con las claves <code>node-role.kubernetes.io/control-plane</code> y la clave histórica <code>node-role.kubernetes.io/master</code>.</p>

<p><strong>Manifiesto YAML con Tolerations:</strong></p>
<pre><code>apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: ds-security-agent
  namespace: lab-daemonsets
  labels:
    app: security-agent
spec:
  selector:
    matchLabels:
      app: security-agent
  template:
    metadata:
      labels:
        app: security-agent
    spec:
      tolerations:
        - key: node-role.kubernetes.io/control-plane
          operator: Exists
          effect: NoSchedule
        - key: node-role.kubernetes.io/master
          operator: Exists
          effect: NoSchedule
      containers:
        - name: agent
          image: alpine:3.19
          command: ["/bin/sh", "-c", "echo 'Seguridad activa en nodo'; sleep 3600"]</code></pre>

<p><strong>Validación:</strong></p>
<pre><code>kubectl apply -f ds-tolerations.yaml
# Comprobar que existe un Pod en cada nodo incluyendo el master
kubectl get pods -n lab-daemonsets -l app=security-agent -o wide</code></pre>
"""
        },
        {
            "id": "sol-9-3",
            "ex_id": "ex-9-3",
            "num": "Solución 9.3:",
            "title": "Actualización Controlada de DaemonSet (RollingUpdate vs OnDelete)",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Si se usa <code>updateStrategy: OnDelete</code>, los Pods de los nodos no se actualizan hasta que el administrador los elimina manualmente. Con <code>RollingUpdate</code> (el valor por defecto moderno), Kubernetes destruye y recrea Pods nodo a nodo según <code>maxUnavailable</code>.</p>

<p><strong>Comandos de Actualización:</strong></p>
<pre><code># 1. Actualizar la imagen del DaemonSet
kubectl set image ds/ds-node-log-collector \\\\
  log-collector=busybox:1.36.1 -n lab-daemonsets

# 2. Monitorear el progreso en tiempo real
kubectl rollout status ds/ds-node-log-collector -n lab-daemonsets

# 3. Comprobar que todos los Pods ejecutan la nueva versión
kubectl get pods -n lab-daemonsets -l app=node-logger -o jsonpath='{.items[*].spec.containers[*].image}'</code></pre>
"""
        }
    ]
}

MODULE_STATEFULSETS = {
    "id": "statefulsets",
    "num": "10",
    "name": "StatefulSets: Identidad Estable y Almacenamiento Persistente Ordenado",
    "ns": "lab-statefulsets",
    "description": "Los StatefulSets están diseñados para aplicaciones con estado (bases de datos, colas) que requieren nombres de red estables y predecibles (pod-0, pod-1) y almacenamiento persistente dedicado no intercambiable.",
    "exercises": [
        {
            "id": "ex-10-1",
            "sol_id": "sol-10-1",
            "num": "Ejercicio 10.1:",
            "title": "Identidad de Red Estable y Despliegue Secuencial (web-0, web-1)",
            "difficulty_label": "Intermedio",
            "difficulty_class": "intermedio",
            "scenario": "Se necesita desplegar un clúster de 3 réplicas donde cada miembro tenga un nombre de host DNS determinista y secuencial vinculado a un Headless Service.",
            "requirements": [
                "Crear el namespace <code>lab-statefulsets</code>.",
                "Crear un Headless Service (<code>clusterIP: None</code>) llamado <code>svc-stateful-web</code> en <code>lab-statefulsets</code>.",
                "Crear un StatefulSet llamado <code>sts-web</code> con 3 réplicas e imagen <code>nginx:1.25-alpine</code> vinculado al servicio mediante <code>serviceName: svc-stateful-web</code>.",
                "Verificar que los Pods se crean de uno en uno en orden estricto (<code>sts-web-0</code>, luego <code>sts-web-1</code> y finalmente <code>sts-web-2</code>)."
            ],
            "verification": "<p>Ejecutar <code>kubectl get pods -n lab-statefulsets</code> y comprobar que los nombres son exactamente <code>sts-web-0</code>, <code>sts-web-1</code> y <code>sts-web-2</code>.</p>"
        },
        {
            "id": "ex-10-2",
            "sol_id": "sol-10-2",
            "num": "Ejercicio 10.2:",
            "title": "Aprovisionamiento Dinámico de Almacenamiento con volumeClaimTemplates",
            "difficulty_label": "Nivel CKA",
            "difficulty_class": "cka",
            "scenario": "A diferencia de un Deployment donde todos los Pods comparten el mismo PVC, en un StatefulSet cada Pod debe tener su propio disco independiente para que cada réplica guarde sus propios datos de base de datos.",
            "requirements": [
                "Definir en el StatefulSet la sección <code>volumeClaimTemplates</code> solicitando 1Gi por réplica.",
                "Montar el volumen en <code>/usr/share/nginx/html</code>.",
                "Escribir en cada réplica un archivo <code>index.html</code> que contenga el hostname del Pod específico.",
                "Comprobar que Kubernetes generó automáticamente los PVCs correspondientes con nomenclatura determinista."
            ],
            "verification": "<p>Ejecutar <code>kubectl get pvc -n lab-statefulsets</code> y comprobar que existen 3 PVCs llamados <code>data-sts-web-0</code>, <code>data-sts-web-1</code> y <code>data-sts-web-2</code>.</p>"
        },
        {
            "id": "ex-10-3",
            "sol_id": "sol-10-3",
            "num": "Ejercicio 10.3:",
            "title": "Escalado Ordenado Inverso y Política de Preservación de PVCs",
            "difficulty_label": "Avanzado",
            "difficulty_class": "avanzado",
            "scenario": "Al escalar hacia abajo un StatefulSet de 3 a 1 réplica, Kubernetes debe apagar los Pods en orden estrictamente inverso (primero el 2, luego el 1). Por seguridad, los PVCs asociados NUNCA deben eliminarse automáticamente para evitar pérdida accidental de datos.",
            "requirements": [
                "Escalar <code>sts-web</code> a 1 réplica con <code>kubectl scale</code>.",
                "Monitorear el orden de terminación de los Pods.",
                "Verificar que los PVCs <code>data-sts-web-1</code> y <code>data-sts-web-2</code> continúan existiendo en el clúster a pesar de que sus Pods ya no existan.",
                "Volver a escalar a 3 réplicas y comprobar que los nuevos Pods se re-enlazan a sus discos originales."
            ],
            "verification": "<p>Comprobar con <code>curl</code> que al recrearse <code>sts-web-2</code>, este conserva intacto el archivo que escribió en el ejercicio anterior.</p>"
        }
    ],
    "solutions": [
        {
            "id": "sol-10-1",
            "ex_id": "ex-10-1",
            "num": "Solución 10.1:",
            "title": "Identidad de Red Estable y Despliegue Secuencial (web-0, web-1)",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Los StatefulSets exigen obligatoriamente un Headless Service declarado en el campo <code>serviceName</code>. Cada Pod recibe una entrada DNS estable con el formato: <code>&lt;pod-name&gt;.&lt;service-name&gt;.&lt;namespace&gt;.svc.cluster.local</code>.</p>

<p><strong>Manifiesto YAML:</strong></p>
<pre><code>apiVersion: v1
kind: Namespace
metadata:
  name: lab-statefulsets
---
apiVersion: v1
kind: Service
metadata:
  name: svc-stateful-web
  namespace: lab-statefulsets
spec:
  clusterIP: None
  selector:
    app: stateful-web
  ports:
    - port: 80
      name: web
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: sts-web
  namespace: lab-statefulsets
spec:
  serviceName: "svc-stateful-web"
  replicas: 3
  selector:
    matchLabels:
      app: stateful-web
  template:
    metadata:
      labels:
        app: stateful-web
    spec:
      containers:
        - name: nginx
          image: nginx:1.25-alpine
          ports:
            - containerPort: 80
              name: web</code></pre>

<p><strong>Validación:</strong></p>
<pre><code>kubectl apply -f sts-basic.yaml
kubectl get pods -n lab-statefulsets -w</code></pre>
"""
        },
        {
            "id": "sol-10-2",
            "ex_id": "ex-10-2",
            "num": "Solución 10.2:",
            "title": "Aprovisionamiento Dinámico de Almacenamiento con volumeClaimTemplates",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Cada entrada en <code>volumeClaimTemplates</code> genera un PVC independiente para cada Pod, siguiendo la convención <code>&lt;claim-name&gt;-&lt;statefulset-name&gt;-&lt;index&gt;</code>.</p>

<p><strong>Manifiesto YAML con volumeClaimTemplates:</strong></p>
<pre><code>apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: sts-data
  namespace: lab-statefulsets
spec:
  serviceName: "svc-stateful-web"
  replicas: 3
  selector:
    matchLabels:
      app: stateful-data
  template:
    metadata:
      labels:
        app: stateful-data
    spec:
      containers:
        - name: web
          image: nginx:1.25-alpine
          volumeMounts:
            - name: data-vol
              mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
    - metadata:
        name: data-vol
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 1Gi</code></pre>

<p><strong>Validación:</strong></p>
<pre><code>kubectl apply -f sts-storage.yaml
kubectl get pvc -n lab-statefulsets</code></pre>
"""
        },
        {
            "id": "sol-10-3",
            "ex_id": "ex-10-3",
            "num": "Solución 10.3:",
            "title": "Escalado Ordenado Inverso y Política de Preservación de PVCs",
            "content_html": """
<p><strong>Explicación Técnica:</strong> Por diseño, Kubernetes NUNCA borra los PVCs generados por un StatefulSet al reducir réplicas. Esto evita que una operación de scale down destruya datos de un nodo maestro/esclavo de base de datos.</p>

<p><strong>Comandos de Escalado y Verificación:</strong></p>
<pre><code># 1. Reducir réplicas a 1
kubectl scale sts sts-data -n lab-statefulsets --replicas=1

# 2. Comprobar que sts-data-2 termina antes que sts-data-1
kubectl get pods -n lab-statefulsets -w

# 3. Comprobar que los PVCs continúan existiendo (no se han borrado)
kubectl get pvc -n lab-statefulsets

# 4. Volver a escalar a 3 réplicas:
#    los nuevos Pods reutilizarán sus discos previos
kubectl scale sts sts-data -n lab-statefulsets --replicas=3
kubectl get pods -n lab-statefulsets</code></pre>
"""
        }
    ]
}

MODULES_ADVANCED = [MODULE_JOBS, MODULE_DAEMONSETS, MODULE_STATEFULSETS]
