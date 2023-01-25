# Running PhotoPrism with Kubernetes

*For advanced users only. You can contribute by clicking :material-file-edit-outline: to send a pull request with your changes.*

Running PhotoPrism on a Kubernetes cluster is straightforward.

At a minimum, you can just define a Kubernetes `Service` and a `StatefulSet` and be up and running.
For more real-world usage, you'll probably want to at least include persistent storage,
and possibly some `Ingress` rules for exposing PhotoPrism outside your cluster.

For those familiar with [Helm](https://helm.sh), a PhotoPrism Helm chart [is available](https://github.com/p80n/photoprism-helm).

Once you've got PhotoPrism deployed, you can `exec` into the running container and `photoprism import` your photos.

Here's an [example of a YAML file](../../developer-guide/technologies/yaml.md) that creates the
following Kubernetes objects:

- `Namespace`
- `Service` exposing PhotoPrism on port 80
- `StatefulSet` with persistent NFS volumes
- `Secret` which stores the database DSN and admin password
- `Ingress` rule for a Kubernetes [ingress controller](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/)
- Annotations for a Kubernetes [`Certificate Manager`](https://github.com/jetstack/cert-manager)

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: photoprism
---
apiVersion: v1
kind: Secret
metadata:
  name: photoprism-secrets
  namespace: photoprism
stringData:
  PHOTOPRISM_ADMIN_PASSWORD: <your admin password here>
  PHOTOPRISM_DATABASE_DSN: username:password@tcp(db-server-address:3306)/dbname?charset=utf8mb4,utf8&parseTime=true
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: photoprism
  namespace: photoprism
spec:
  selector:
    matchLabels:
      app: photoprism
  serviceName: photoprism
  replicas: 1
  template:
    metadata:
      labels:
        app: photoprism
    spec:
      containers:
      - name: photoprism
        image: photoprism/photoprism:latest
        env:
        - name: PHOTOPRISM_DEBUG
          value: "true"
        - name: PHOTOPRISM_CACHE_PATH
          value: /assets/cache
        - name: PHOTOPRISM_IMPORT_PATH
          value: /assets/photos/import
        - name: PHOTOPRISM_EXPORT_PATH
          value: /assets/photos/export
        - name: PHOTOPRISM_ORIGINALS_PATH
          value: /assets/photos/originals
        - name: PHOTOPRISM_DATABASE_DRIVER
          value: mysql
        - name: PHOTOPRISM_HTTP_HOST
          value: 0.0.0.0
        - name: PHOTOPRISM_HTTP_PORT
          value: "2342"
        # Load database DSN & admin password from secret
        envFrom:
        - secretRef:
            name: photoprism-secrets
            optional: false
        ports:
        - containerPort: 2342
          name: http
        volumeMounts:
        - mountPath: /assets/photos/originals
          name: originals
          subPath: media/photos
        - mountPath: /assets/cache
          name: photoprism
          subPath: cache
        - mountPath: /assets/photos/import
          name: photoprism
          subPath: import
        - mountPath: /assets/photos/export
          name: photoprism
          subPath: export
        readinessProbe:
          httpGet:
            path: /api/v1/status
            port: http
      volumes:
      - name: originals
        nfs:
          path: /share
          readOnly: true
          server: my.nas.host
      - name: photoprism
        nfs:
          path: /photoprism
          server: my.nas.host
---
apiVersion: v1
kind: Service
metadata:
  name: photoprism
  namespace: photoprism
spec:
  ports:
  - name: http
    port: 80
    protocol: TCP
    targetPort: http
  selector:
    app: photoprism
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    # For nginx ingress controller:
    kubernetes.io/ingress.class: nginx
    # Default is very low so most photo uploads will fail
    nginx.ingress.kubernetes.io/proxy-body-size: "512M"
    # If using cert-manager:
    certmanager.k8s.io/cluster-issuer: letsencrypt-prod
    kubernetes.io/tls-acme: "true"
  name: photoprism
  namespace: photoprism
spec:
  rules:
  - host: photoprism.my.domain
    http:
      paths:
      - backend:
          service:
            name: photoprism
            port:
              name: http
        path: /
        pathType: Prefix
  tls:
  - hosts:
    - photoprism.my.domain
    secretName: photoprism-cert
```

To run this locally, you can use [minikube](https://minikube.sigs.k8s.io/docs/start/)
or a similar local cluster deployer.

Once your cluster is up and running with your `kubectl` commands. Simply copy the above YAML
markup to a file, make the necessary changes, and use the `kubectl` CLI command to deploy:

```bash
kubectl create -f photoprism.yaml
```

If you prefer to use helm, see https://github.com/p80n/photoprism-helm.
