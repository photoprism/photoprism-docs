# Running PhotoPrism with Kubernetes

*Note: This is contributed content and may be outdated.*

Running PhotoPrism on a Kubernetes cluster is straightforward. 

At a minimum, you can just define a Kubernetes `Service` and a `StatefulSet` and be up and running.
For more real-world usage, you'll probably want to at least include persistent storage, 
and possibly some `Ingress` rules for exposing PhotoPrism outside your cluster.

For those familiar with [Helm](https://helm.sh), a PhotoPrism Helm chart [is available](https://github.com/p80n/photoprism-helm).

Once you've got PhotoPrism deployed, you can `exec` into the running container and `photoprism import` your photos.

Here's an example YAML file that creates a Kubernetes:

- `Namespace`
- `Service` exposing PhotoPrism on port 80
- `StatefulSet` with persistent NFS volumes
- `Ingress` rule for a Kubernetes [ingress controller](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/)
- Annotations for a Kubernetes [`Certificate Manager`](https://github.com/jetstack/cert-manager)

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: photoprism
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
        image: photoprism/photoprism:20190522
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
          vale: /assets/photos/originals
        - name: PHOTOPRISM_DATABASE_DRIVER
          value: mysql
        - name: PHOTOPRISM_DATABASE_DSN
          value: photoprism:photoprism@tcp(mariadb.db:3306)/photoprism?parseTime=true
        - name: PHOTOPRISM_HTTP_HOST
          value: 0.0.0.0
        - name: PHOTOPRISM_HTTP_PORT
          value: 2342
        resources:
          requests:
            memory: 2Gi
        ports:
        - containerPort: 2342
          name: http
        volumeMounts:
        - mountPath: /assets/photos/originals
          name: originals
          subPath: media/photos
        - mountPath: /asssets/cache
          name: photoprism
          subPath: cache
        - mountPath: /assets/photos/import
          name: photoprism
          subPath: import
        - mountPath: /assets/photos/export
          name: photoprism
          subPath: export
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
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  annotations:
    certmanager.k8s.io/cluster-issuer: letsencrypt-prod
    kubernetes.io/ingress.class: nginx
    kubernetes.io/tls-acme: "true"
  name: photoprism
  namespace: photoprism
spec:
  rules:
  - host: photoprism.my.domain
    http:
      paths:
      - backend:
          serviceName: photoprism
          servicePort: http
        path: /
  tls:
  - hosts:
    - photoprism.my.domain
    secretName: photoprism-cert
```

See also: https://github.com/p80n/photoprism-helm
