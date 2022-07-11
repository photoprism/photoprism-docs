# Running PhotoPrism On FreeBSD

For FreeBSD / FreeNAS users, an unofficial [PhotoPrism port](https://github.com/huo-ju/photoprism-freebsd-port) 
is available.

The port will compile and install libtensorflow 1.15.2 and build `photoprism` from source on FreeBSD.

!!! info ""
    You are welcome to ask for help in our [community chat](https://link.photoprism.app/chat).
    [Sponsors](https://photoprism.app/membership) receive direct [technical support](https://photoprism.app/contact) via email.
    Before submitting a support request, try to [determine the cause of your problem](troubleshooting/index.md).

!!! quote ""
    Help improve this page! You can contribute by clicking :material-pencil: to send a pull request with your changes.

**1. Clone or download the port:**

```bash
git clone https://github.com/huo-ju/photoprism-freebsd-port
```

**2. Build TensorFlow and PhotoPrism from source, then install:**

```bash
cd photoprism-freebsd-port
make config
make && make install
```

When running the make config command, a CPU feature options dialog will be presented, and the default option is NONE.

**3. Add entries to rc.conf:**

```bash
photoprism_enable="YES"
photoprism_assetspath="/var/photoprism/assets"
photoprism_storagepath="/var/photoprism/storage"
```

You can add more command line parameters into photoprism_flags="" in the rc.conf

`photoprism config` shows all config parameters. 

**4. Start the service:**

```bash
service photoprism start
```

Done!