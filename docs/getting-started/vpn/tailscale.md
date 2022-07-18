# Tailscale VPN

!!! quote ""
    Help improve these docs! You can contribute by clicking :material-pencil: to send a pull request with your changes.

1. Open the [Tailscale website](https://tailscale.com/) and Select Use Tailscale button. 

2. Sign up with an email address or using any of your other accounts and install Tailscale on all the relevant devices. Detailed and clear instructions are available to guide your through the process depending on the operating system.

    ![](img/tailscale-1.png){ class="shadow" }

    For example below the instruction for [**Linux**](https://tailscale.com/download/linux) and [**Android**](https://tailscale.com/download/android)

    ![](img/tailscale-3.png){: style="width:50%" class="shadow" }![](img/tailscale-2.png){: style="width:50%" class="shadow" }

3. When the devices have Tailscale installed (and logged in via the same account) they all appear in the overview as in the printscreen below.

    ![](img/tailscale-4.png){ class="shadow" }

4. Each device gets an IP address allocated (100.xxx.xxx.xxx), which can be used to reach them via the VPN network. This IP address with addition of the port number where Photoprism is run on can be used to reach Photoprism outside the home network. 

   ![](img/tailscale-5.png){ class="shadow" }