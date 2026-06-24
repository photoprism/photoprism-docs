# Deploying PhotoPrism on Kubernetes

PhotoPrism provides [Helm charts](https://charts.photoprism.app/photoprism) for advanced users to deploy our [Personal](https://www.photoprism.app/editions/#compare) and [Team Editions](https://www.photoprism.app/teams/#compare) on Kubernetes, offering the same configuration options as the official Docker images.

The `photoprism-plus` chart is publicly accessible and allows you to install our [Personal Editions](https://www.photoprism.app/editions/#compare) with the option to [activate membership features](https://www.photoprism.app/kb/activation/), similar to the installation with [Docker Compose](../docker-compose.md).

Before proceeding, ensure that your Kubernetes nodes have at least [8 GB of memory](../troubleshooting/docker.md#adding-swap) and avoid enforcing a [hard memory limit](../faq.md#why-is-my-configured-memory-limit-exceeded-when-indexing-even-though-photoprism-doesnt-actually-seem-to-use-that-much-memory). Indexing RAW files or large panoramas may require additional swap space or RAM beyond the [recommended minimum](../index.md#system-requirements).

!!! info "PhotoPrism® Pro"
    [Business customers](https://www.photoprism.app/teams/#compare) can deploy the `photoprism-pro` chart from the same repository. [Learn more ›](https://www.photoprism.app/pro/kb/kubernetes/)

## Add the Charts Repository

```bash
helm repo add photoprism https://charts.photoprism.app/photoprism
helm repo update photoprism
helm search repo photoprism
```

`photoprism/photoprism-plus` ships safe defaults (non-root UID/GID 1000, SQLite, two PersistentVolumeClaims, and optional ingress/service templates). Use
`helm show values photoprism/photoprism-plus` to inspect every option before overriding it in your own `values.plus.yaml` file.

## Quick Install (SQLite)

```bash
helm upgrade --install photos photoprism/photoprism-plus \
  --namespace photos --create-namespace \
  --set adminUser=admin
```

* Helm prints the release name; Kubernetes stores auto-generated secrets in `secret/<release>-photoprism-secrets` when `adminPassword` is omitted.
* Retrieve the password so you can log in and activate membership features:

  ```bash
  kubectl get secret photos-photoprism-secrets -n photos \
    -o jsonpath='{.data.PHOTOPRISM_ADMIN_PASSWORD}' | base64 --decode && echo
  ```

* Run PhotoPrism CLI commands via `kubectl exec` when you need to import or trigger background tasks:

  ```bash
  kubectl exec -n photos deploy/photos-photoprism-plus -- \
    photoprism import --path /photoprism/import
  ```

## Persist Originals and Data

The chart always provisions `/photoprism/storage` (5 GiB by default) because it contains the database, cache, and logs. Originals default to a 10 GiB PVC but you can disable or remap them, for example:

```yaml
# values.plus.yaml
persistence:
  # storageClassName: fast-nvme   # override default class
  storage:
    size: 20Gi
  originals:
    enabled: true
    size: 2Ti
    nfs:
      enabled: true
      server: nas.local
      path: /tank/photos
```

Apply the overrides:

```bash
helm upgrade --install photos photoprism/photoprism-plus \
  --namespace photos --create-namespace \
  -f values.plus.yaml
```

## Using MariaDB

SQLite is convenient for quick tests, but larger libraries benefit from an external database. Set the database block to point at your cluster’s MariaDB or  MySQL service:

```bash
helm upgrade --install photos photoprism/photoprism-plus \
  --namespace photos \
  --set database.driver=mysql \
  --set database.server=mariadb.default.svc.cluster.local:3306 \
  --set database.name=photoprism \
  --set database.user=photoprism \
  --set database.password=change-me-now
```

Store credentials in Kubernetes secrets when possible and reference them via the `extraEnvFrom` pattern (see `templates/secret.yaml` in the chart) if your  security requirements prohibit plain values in `values.yaml`.

## Networking and TLS

The chart exposes PhotoPrism on TCP 2342 through a ClusterIP service. You can override the service type or enable an Ingress resource when you terminate TLS  in the cluster edge:

```yaml
service:
  type: ClusterIP
  port: 2342

ingress:
  enabled: true
  className: traefik
  hosts:
    - host: photos.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - hosts:
        - photos.example.com
      secretName: photos-tls
```

Because TLS typically terminates at the ingress or proxy layer, the chart keeps `PHOTOPRISM_DISABLE_TLS` set to `true`. Only enable PhotoPrism’s internal TLS if your cluster design requires end-to-end encryption and you manage the certificates yourself. If your ingress controller reaches PhotoPrism from an address outside the trusted proxy ranges, set `config.PHOTOPRISM_TRUSTED_PROXY` accordingly so forwarded client and protocol headers are accepted.

## PhotoPrism® Plus

Our members can activate [additional features](https://link.photoprism.app/membership) by logging in with the [admin user created during setup](../config-options.md#authentication) and then following the steps [described in our activation guide](https://www.photoprism.app/kb/activation/). Thank you for your support, which has been and continues to be essential to the success of the project! :octicons-heart-fill-24:{ .heart .purple }

[Compare Memberships ›](https://link.photoprism.app/membership){ class="pr-3 block-xs" } [View Membership FAQ ›](https://www.photoprism.app/membership/faq/) 

!!! example ""
    We recommend that new users install our free Community Edition before [signing up for a membership](https://link.photoprism.app/membership).

## Advanced Values

`values.yaml` exposes the same environment variables documented throughout this site:

- `config.*` maps to PhotoPrism configuration flags (app metadata, quotas, backup schedule, CDN/CORS, etc.).
- `resources` sets requests/limits (defaults: 500 m / 1 GiB request, 4000 m / 6 GiB limit). Tune these to match your workloads.
- `oidc.*` mirrors the options covered in [Single Sign-On via OpenID Connect](openid-connect.md); set `PHOTOPRISM_DISABLE_OIDC=false` to enable federated logins.
- `cluster.integration` lets you pull shared values from an existing PhotoPrism® Portal secret if you run Portal in the same cluster. Leave it disabled for standalone deployments. 

Whenever you change values, redeploy with `helm upgrade --install ... -f` so the `StatefulSet` picks up the new configuration. Use `kubectl rollout status` to trace progress and `helm history photos` to view revisions.

## Maintenance Checklist

- [ ] Update the repo (`helm repo update photoprism`) before each upgrade so you get the latest chart.
- [ ] Monitor PVC usage (`kubectl get pvc -n photos`) and resize volumes or switch to external storage before running out of space.
- [ ] Back up both the database (`config.PHOTOPRISM_BACKUP_*`) and `/photoprism/storage` using your preferred snapshot tool.
- [ ] Keep nodes patched and ensure swap/virtual memory stays within recommended bounds to avoid unexpected restarts.

With these steps, you can deploy PhotoPrism® CE, Essentials, or Plus on Kubernetes using a supported, first-party Helm chart while keeping parity with the Docker workflow documented throughout this guide.
