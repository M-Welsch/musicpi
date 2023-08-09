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
After=syslog.target network.target mpd.service

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

edit_fstab () {
  echo "//192.168.0.2/Multimedia /home/max/Multimedia cifs credentials=/etc/win-credentials,uid=1000,gid=1000,user,rw,vers=3.0 0 0" | tee "/etc/fstab" > /dev/null
  echo "username=max
password
domain=WORKGROUP" | tee /etc/win-credentials > /dev/null
}

install_mympd () {
  git clone https://github.com/jcorporation/myMPD.git
  cd myMPD
  sudo ./build.sh installdeps
  ./build.sh release
  sudo ./build.sh install
  cd ~
  sudo systemctl daemon-reload
  sudo systemctl enable mympd
  sudo systemctl start mympd
}

install_required_packages
install_bluetooth_speaker_emulation
install_mympd
configure_mpd
edit_fstab
create_service_file
enable_i2c

echo "please reboot before use."
