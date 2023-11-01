# Running PhotoPrism On FreeBSD

!!! danger ""
    Please note that third-party apps may not provide access to the docker-compose.yml file or the command line, and therefore you may not be able to use all of PhotoPrism's features and config options.

!!! tldr ""
    Should you experience problems with the installation, we recommend that you ask the FreeBSD community for advice, as we cannot provide support for third-party software and services. You can contribute by clicking :material-file-edit-outline: to send a pull request with your changes.

For FreeBSD and TrueNAS CORE (formerly FreeNAS) users, an [unofficial port is available](https://github.com/huo-ju/photoprism-freebsd-port) that builds PhotoPrism from source. It also compiles and installs the required TensorFlow libraries for you.

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

## When should I perform a complete rescan?

We recommend performing a [complete rescan](../../user-guide/library/originals.md#when-should-complete-rescan-be-selected) after major updates to take advantage of new search filters and sorting options. Be sure to [read the notes for each release](../../release-notes.md) to see what changes have been made and if they might affect your library, for example, because of the file types you have or because new search features have been added. If you encounter problems that you cannot solve otherwise (i.e. before reporting a bug), please also try a rescan and see if it solves the problem.

You can start a [rescan from the user interface](../../user-guide/library/originals.md) by navigating to *Library* > *Index*, selecting "Complete Rescan", and then clicking "Start".

!!! tldr ""
    Manually entered information such as labels, people, titles or descriptions will not be modified when indexing, even if you perform a "complete rescan". Be careful not to start multiple indexing processes at the same time, as this will lead to a high server load.
