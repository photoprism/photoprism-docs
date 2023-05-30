# Troubleshooting Raspberry Pi Problems

!!! info ""
    You are welcome to ask for help in our [community chat](https://link.photoprism.app/chat).
    [Sponsors](https://www.photoprism.app/membership) receive direct [technical support](https://www.photoprism.app/contact) via email.
    Before [submitting a support request](../../user-guide/index.md#getting-support), try to [determine the cause of your problem](index.md).

## Hardware Watchdog Initiates Reboot

A watchdog timer is an electronic timer that is used to detect and correct computer malfunctions. When activated, it can trigger a reboot when the computer is under heavy load, e.g. when indexing pictures. 

Should your Raspberry Pi fail to reset the timer before it expires, the WDT signal will reboot it.
It is [disabled by default in the firmware](https://github.com/raspberrypi/firmware/blob/f694bbe7c6f142e0c1a5033f0f6c15528fd6c98c/boot/overlays/README#L277).

Users can set up "dtparam" also known as Device Tree config files for Raspberry Pi's in `/boot/config.txt`, which will enable the kernel module.

It is the responsibility of the user to [set the parameters of the watchdog daemon correctly](https://linux.die.net/man/5/watchdog.conf).

A common parameter that users set is the average CPU load for 1, 5, or 15 minutes. The default value for the 1 minute span is 24

```bash
max-load-1 = 24
```

The average load is the sum of the queue length and the number of jobs currently running on the CPUs. You can use the following commands to view load average statistics:

```
uptime, procinfo, w, top
```

Raspberry Pi users who have the hardware watchdog enabled need to set a more appropriate value for the 1-minute span for the maximum load than the default value.
As a workaround, you can log the average workload to a file:

```bash
#!/bin/bash

while true; do
echo $(cat /proc/loadavg) >> test_file.log
sleep 10
done
```

This will write a log with a timestamp every 10 seconds. Run the above script while performing intensive tasks that would normally trigger a reboot, such as tagging faces. With this information, you can now set a new value that is greater than the recorded maximum.

!!! example ""
    **Help improve these docs!** You can contribute by clicking :material-file-edit-outline: to send a pull request with your changes.
