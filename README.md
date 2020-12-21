# Remarkable-wifi-conf

`remarkable-wifi-conf` is a small utility to configure WiFi on [Remarkable](https://remarkable.com) devices.  
The Remarkable only supports a limited set of characters on its on-screen keyboard. If your WiFi password happens to contain a character that is not supported by the Remarkable keyboard, [you're out of luck](https://support.remarkable.com/hc/en-us/articles/360016347897-Network-password-requires-special-characters).

Well, until this tool :-)

## Prerequisites

* SSH access to your Remarkable. See [remarkablewiki.com](https://remarkablewiki.com/tech/ssh) for details.
* Python >= 3

## Usage

1. Clone this repo.
2. Install Python dependencies (`pip install -r ./requirements.txt`)

Now depending on how much you trust this script you can either follow a manual process where you update your `xochitl.conf` manually, or follow the fully automated process.

## Manual process

The Remarkable OS stores WiFi credentials in `/home/root/.config/remarkable/xochitl.conf`. The WiFi configuration part looks something like this:

```ini
[wifinetworks]
MyNetwork=@Variant(\0\0\0\b\0\0\0\x3\0\0\0\b\0s\0s\0i\0\x64\0\0\0\n\0\0\0\x6\0\x66\0o\0o\0\0\0\x10\0p\0r\0o\0t\0o\0\x63\0o\0l\0\0\0\n\0\0\0\x6\0p\0s\0k\0\0\0\x10\0p\0\x61\0s\0s\0w\0o\0r\0\x64\0\0\0\n\0\0\0\x6\0\x62\0\x61\0r)
```

To generate this for your network run the following command:

```sh
echo '' | python ./remarkable_wifi_conf.py
```

The script will ask your WiFi SSID (network name) and password and print a `wifinetworks` section. Now SSH into your Remarkable and open `/home/root/.config/remarkable/xochitl.conf` with a text editor. Scroll down until you find a `[wifinetworks]` section and append the generated line containing the WiFi configuration.

Now restart the Remarkable system (`systemctl restart xochitl`) and presto! Your Remarkable will be able to connect to your WiFi network. Depending on how many WiFi networks you have configured you might need to go into the system settings to select your WiFi network. You will not have to enter a password at this point.

## Automated process

If you trust this script and my Linux fu you can run the oneliner below.

Note that if you haven't set up SSH keys, you'll be prompted for your password 3 times.

```sh
export remarkable=remarkable; ssh $remarkable 'cp /home/root/.config/remarkable/xochitl.conf{,.bak} && cat /home/root/.config/remarkable/xochitl.conf' | python ./remarkable_wifi_conf.py > >(ssh $remarkable 'cat > /tmp/rmwifi') && ssh $remarkable 'mv /tmp/rmwifi /home/root/.config/remarkable/xochitl.conf && systemctl restart xochitl'
```

This will:

1. Make a backup of your `xochitl.conf` in `/home/root/.config/remarkable/xochitl.conf.bak`, just in case.
2. Prompt for your WiFi SSID (network name) and password.
3. Update `xochitl.conf` with a configuration for your network.
4. Restart the xochitl service so the configuration changes become effective.

Presto! Your Remarkable will be able to connect to your WiFi network. Depending on how many WiFi networks you have configured you might need to go into the system settings to select your WiFi network. You will not have to enter a password at this point.

## Credits

Credits to GitHub user Evidlo for their example [here](https://github.com/Evidlo/examples/blob/b5305ee8db00e4b0b43bd35a6b01228290172502/python/xochitl_conf.py).
