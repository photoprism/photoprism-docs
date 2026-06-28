# Running PhotoPrism on a QNAP NAS

Before setting up PhotoPrism on your NAS, we recommend that you check the [QNAP product database](https://www.qnap.com/en/product) for the CPU and memory configuration of your device.

For a good user experience, it should be a 64-bit system with [at least 2 cores and 3 GB of RAM](../index.md#system-requirements). Indexing large photo and video collections also benefits greatly from [using SSD storage](../troubleshooting/performance.md#storage), especially for the database and cache files.

!!! tldr ""
    Should you experience problems with the installation, we recommend that you ask the QNAP community for advice, as we cannot provide support for third-party software and services.
    Also note that [RAW image conversion and TensorFlow are disabled](../../user-guide/settings/advanced.md) on devices with 1 GB or less memory, and that high-resolution panoramic images may require [additional swap space](../troubleshooting/docker.md#adding-swap) and/or physical memory above the [recommended minimum](../index.md#system-requirements).

## Setup

### Setup using Portainer ###

If you have [Portainer](https://www.portainer.io/) set up on your device, you can follow our [step-by-step guide](../portainer/index.md) to install PhotoPrism. [Learn more ›](../portainer/index.md)

### Setup using QNAP Container Station (GUI)

Follow these steps if you prefer [Container Station’s](https://www.qnap.com/en-us/software/container-station) graphical workflow on [QTS 5](https://www.qnap.com/qts/5.0/en/) / [QuTS hero](https://www.qnap.com/en/operating-system/quts-hero). The interface treats PhotoPrism and its MariaDB dependency as a single “Application” defined by a Docker Compose file.

#### 1. Prepare your NAS

1. Install **[Container Station](https://www.qnap.com/en-us/software/container-station)** from the App Center, then launch it and accept the first-launch prompts (downloads the base images it requires).
2. Update QTS/QuTS hero to the latest release, then reboot so Kernel patches and Docker updates are applied before you deploy storage-heavy apps.
3. Decide where the PhotoPrism workspace should live. Most users keep everything under `/share/Container/photoprism`, while the actual originals may stay in `/share/Multimedia` or another existing volume.
4. Optional but recommended: enable SSH (Control Panel ▸ Network & File Services ▸ Telnet/SSH) so you can run `docker compose` commands for troubleshooting later.

#### 2. Create persistent folders

Use File Station or SSH to create the directories Container Station will mount:

```sh
mkdir -p /share/Container/photoprism/{storage,import,database}
```

- `storage` holds the application cache, sidecars, and backups (SSD recommended).
- `database` stores MariaDB data files.
- `originals` should point to the share that already contains your photo library (for example `/share/Multimedia`). Create `/share/Container/photoprism/originals` only if you plan to copy photos into a new folder later.
- `import` is optional but useful if you upload archives that should be reorganized by PhotoPrism before landing in Originals.

#### 3. Create the Compose application

1. Open **Container Station ▸ Applications ▸ Create**.
2. Enter an application name such as `photoprism`.
3. Paste the Compose configuration below into the YAML editor and adjust passwords and paths before clicking **Validate** and **Create**:

    ```yaml
    services:
      mariadb:
        image: mariadb:12.3
        restart: unless-stopped
        environment:
          MARIADB_AUTO_UPGRADE: "1"
          MARIADB_INITDB_SKIP_TZINFO: "1"
          MARIADB_ROOT_PASSWORD: "supersecret"
          MARIADB_DATABASE: photoprism
          MARIADB_USER: photoprism
          MARIADB_PASSWORD: "change-me"
        volumes:
          # persistent MariaDB data on the NAS
          - /share/Container/photoprism/database:/var/lib/mysql

      photoprism:
        image: photoprism/photoprism:latest
        depends_on:
          - mariadb
        restart: unless-stopped
        ports:
          - "2342:2342"
        environment:
          # initial admin password (8-72 characters)
          PHOTOPRISM_ADMIN_PASSWORD: "choose-a-strong-password"
          # public URL so links and redirects use the correct origin
          PHOTOPRISM_SITE_URL: "http://YOUR_NAS_IP:2342/"
          # disables built-in HTTPS/TLS when set to "true"
          PHOTOPRISM_DISABLE_TLS: "false"
          # uses a self-signed certificate if the site URL starts with https://
          PHOTOPRISM_DEFAULT_TLS: "true"
          # default UI language (e.g., en, de, fr)
          PHOTOPRISM_DEFAULT_LOCALE: "en"
          # location language (local, en, de, …)
          PHOTOPRISM_PLACES_LOCALE: "local"
          # write YAML sidecars with asset metadata
          PHOTOPRISM_SIDECAR_YAML: "true"
          # back up album metadata periodically
          PHOTOPRISM_BACKUP_ALBUMS: "true"
          # enable automatic database backups
          PHOTOPRISM_BACKUP_DATABASE: "true"
          # cron entry or shortcut (daily, weekly) for backups
          PHOTOPRISM_BACKUP_SCHEDULE: "daily"
          # cron syntax or "" to disable scheduled indexing
          PHOTOPRISM_INDEX_SCHEDULE: ""
          # delay (seconds) before indexing WebDAV uploads
          PHOTOPRISM_AUTO_INDEX: 300
          # delay (seconds) before importing WebDAV uploads
          PHOTOPRISM_AUTO_IMPORT: -1
          # auto-flag potentially offensive content (TensorFlow required)
          PHOTOPRISM_DETECT_NSFW: "false"
          # allow uploads that might be offensive
          PHOTOPRISM_UPLOAD_NSFW: "true"
          # restrict uploads to listed extensions (leave blank to allow all)
          PHOTOPRISM_UPLOAD_ALLOW: ""
          # allow zip uploads (extracted before import)
          PHOTOPRISM_UPLOAD_ARCHIVES: "true"
          # max upload size in MB
          PHOTOPRISM_UPLOAD_LIMIT: 5000
          # max originals size in MB (larger files are skipped)
          PHOTOPRISM_ORIGINALS_LIMIT: 5000
          # enable zstd and gzip to reduce bandwidth
          PHOTOPRISM_HTTP_COMPRESSION: "zstd,gzip"
          # database driver / connection settings
          PHOTOPRISM_DATABASE_DRIVER: "mysql"
          PHOTOPRISM_DATABASE_SERVER: "mariadb:3306"
          PHOTOPRISM_DATABASE_NAME: "photoprism"
          PHOTOPRISM_DATABASE_USER: "photoprism"
          PHOTOPRISM_DATABASE_PASSWORD: "change-me"
        volumes:
          # config, cache, and backups (use SSD-backed storage if available)
          - /share/Container/photoprism/storage:/photoprism/storage
          # existing media; replace /share/Multimedia with your actual path
          - /share/Multimedia:/photoprism/originals
          # optional staging folder for the Import tool
          - /share/Container/photoprism/import:/photoprism/import
    ```

     By default, our Docker images use the volume mount paths `/photoprism/storage` and `/photoprism/originals`, so no [additional variables](../config-options.md#storage) are required to configure them.

4. Double-check that each host path points to the correct absolute `/share/...` location so you don't lose data when updating or redeploying the stack. After the application is created, open **Applications ▸ photoprism ▸ Settings** and set a default web port shortcut (Service `photoprism`, Port `2342`) so the “Open” button launches the UI.

    If you want HTTPS on your NAS, we recommend using a [reverse proxy](../proxies/traefik.md) and then changing `PHOTOPRISM_SITE_URL` to the external `https://` address.

#### 4. Start and verify

1. Select the new application and click **Start**. Container Station will pull both images and create the containers.
2. Watch the application logs for `Starting PhotoPrism...` and `database system is ready to accept connections`.
3. Visit `http://<NAS-IP>:2342/`, sign in with the admin password you set, and follow the welcome wizard to point PhotoPrism at your originals folder if you mounted a parent directory.
4. Trigger **Library ▸ Index ▸ Start** once to create previews and metadata. Keep the browser tab open until the queue drains.

#### 5. Keep it updated

- When new releases ship, open **Applications ▸ photoprism**, click **Stop**, then **Update Images** to pull the latest tags, and start the application again.
- Regularly download the MariaDB backups from `/share/Container/photoprism/storage/backups` or replicate the entire folder to another disk.
- If Container Station reports YAML errors, click **Applications ▸ photoprism ▸ Edit YAML** to fix indentation or update environment variables without recreating the project.
- Our [First Steps 👣](../../user-guide/first-steps.md) tutorial guides you through the user interface and settings to ensure your library is indexed according to your individual preferences.

### Setup using Docker Compose (CLI)

Prefer the terminal? The community tutorial below walks through the same deployment via SSH:

↪ <https://safjan.com/install-photoprism-on-qnap-nas-using-docker-compose/>

## Troubleshooting ##

If your device runs out of memory or other system resources:

- [ ] Try [reducing the number of workers](../config-options.md#indexing) by setting `PHOTOPRISM_WORKERS` to a reasonably small value in your `compose.yaml` file, depending on the performance of your device
- [ ] Make sure [your device has at least 4 GB of swap space](../troubleshooting/docker.md#adding-swap) so that indexing doesn't cause restarts when memory usage spikes; RAW image conversion and video transcoding are especially demanding
- [ ] If you are using SQLite, switch to MariaDB, which is [better optimized for high concurrency](../faq.md#should-i-use-sqlite-mariadb-or-mysql)
- [ ] As a last measure, you can [disable image classification and facial recognition](../config-options.md#feature-flags) 

Other issues? Our [troubleshooting checklists](../troubleshooting/index.md) help you quickly diagnose and resolve them.

!!! example ""
    **Help improve these docs!** You can contribute by clicking :material-file-edit-outline: to send a pull request with your changes.
