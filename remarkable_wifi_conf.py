import sys
import getpass
import tempfile
from PyQt5.QtCore import QSettings

def create_tmp_file(contents):
    tmp = tempfile.NamedTemporaryFile(mode='w+t')
    tmp.write(contents)
    tmp.flush()

    return tmp

def prompt(tty, label, read_fn):
    while True:
        tty.write(f'{label}: '.encode())
        tty.flush()

        value = read_fn().rstrip()
        if value != '': return value

def write_qsettings(file_path, ssid, password):
    conf = QSettings(file_path, QSettings.IniFormat)
    network = {
        'ssid': ssid,
        'password': password,
        'protocol': 'psk'
    }

    conf.setValue(f"wifinetworks/{network['ssid']}", network)
    conf.sync()

def main():
    try:
        # QSettings can only work with files, so write stdin to a tmpfile first
        tmp = create_tmp_file(sys.stdin.read())

        # Read input
        tty = open('/dev/tty', 'rb+', buffering=0)
        ssid = prompt(tty, 'SSID', lambda: tty.readline().decode())
        password = prompt(tty, 'Password', lambda: getpass.getpass(prompt=''))

        # Write Remarkable config file (QT settings)
        write_qsettings(tmp.name, ssid, password)

        # Print tmp file contents to stdout
        tmp = open(tmp.name, 'r+')
        print(tmp.read(), end='')
    finally:
        # Clean up tmp file
        tmp.close()

if __name__ == "__main__":
    main()
