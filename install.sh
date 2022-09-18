set -e
set -x

cat <<EOF >/lib/systemd/system/wscan.service
[Unit]
Description=Wlan scan
After=graphical.target

[Service]
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/pi/.Xauthority
ExecStart=/usr/bin/python3 /home/pi/wlan_scan/main.py
Restart=always
RestartSec=5s
KillMode=process
TimeoutSec=infinity

[Install]
WantedBy=graphical.target
EOF

chmod a+x /lib/systemd/system/wscan.service
systemctl daemon-reload
systemctl enable wscan
systemctl start wscan

