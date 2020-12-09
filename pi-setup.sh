#/bin/bash

# login pi:raspberry

set -eo pipefail

echo Enable wlan, i2c, [ssh]
read

raspi-config

cat <<EOF > /home/pi/start.sh
#/bin/bash

python3 /home/pi/vr-walking-sensor/test.py
EOF

echo Add \"bash /home/pi/start.sh \&\" before exit 0
read
nano /etc/rc.local

apt update --allow-releaseinfo-change
apt-get install -y python3-pip python3-pil
pip3 install adafruit-circuitpython-ssd1306

