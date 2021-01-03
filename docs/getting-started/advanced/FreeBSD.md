# Running PhotoPrism On FreeBSD

*Note: This is contributed content and may be outdated. 

For FreeBSD/FreeNAS users, a unofficial [PhotoPrism port](https://github.com/huo-ju/photoprism-freebsd-port) is available.

The port will compile and install libtensorflow 1.15.2 and build photoprism from source on FreeBSD.

1. clone or download the port 

```
git clone https://github.com/huo-ju/photoprism-freebsd-port
```

2. Build TensorFlow and PhotoPrism from source, then Install

```
cd photoprism-freebsd-port
make config
make && make install
```

When running the make config command, a CPU feature options dialog will be presented, and the default option is NONE.

3. Add entries to rc.conf

```
photoprism_enable="YES"
photoprism_assetspath="/var/photoprism/assets"
photoprism_storagepath="/var/photoprism/storage"
```

You can add more command line parameters into photoprism_flags="" in the rc.conf

`photoprism config` shows all config parameters. 

4. Run the service

```
service photoprism start
```
