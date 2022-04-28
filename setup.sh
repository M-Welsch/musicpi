enable_i2c () {
  echo "enabling i2c interface"
  sudo raspi-config nonint do_i2c 0  # yes, 0 means "activating"!
}

install_required_packages () {
  sudo apt update
  sudo apt install python3-pip cifs-utils libopenjp2-7 mpd -y
  pip install -r requirements/raspi
}

install_bluetooth_speaker_emulation () {
  echo "this will be skipped. Goto setup.sh and install it by yourself."
  # install bluetooth stuff
  #cd /home/pi
  #git clone https://github.com/nicokaiser/rpi-audio-receiver.git  # from https://www.tutonaut.de/raspberry-pi-als-bluetooth-airplay-empfaenger-kombi/#comment-252880
  #cd rpi-audio-receiver
  #sudo ./install.sh  # interactively
}

configure_mpd () {
  echo "Configure mpd: open config-file with 'sudo vim /etc/mpd.conf' and set keys 'music_directory' and 'audio_output/device' to 'hw:1,0'. Make sure 'hw:1,0' is correct. Check with 'aplay -l'"
}

create_service_file () {
  servicefile_location="/etc/systemd/system/musicpi-hmi.service"
  echo "creating service file in $servicefile_location"
  echo '[Unit]
Description="HMI for musicpi"

[Service]
User=max
Group=max
Type=Simple
WorkingDirectory=/home/max/musicpi_hmi
ExecStart=/usr/bin/python .

[Install]
WantedBy=multi-user.target
' | sudo tee $servicefile_location > /dev/null
  sudo systemctl enable musicpi-hmi
  sudo systemctl daemon-reload
}

install_required_packages
install_bluetooth_speaker_emulation
configure_mpd
create_service_file
enable_i2c

echo "please reboot before use."