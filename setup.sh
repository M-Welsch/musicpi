echo "enabling i2c interface"
sudo raspi-config nonint do_i2c 0  # yes, 0 means "activating"!

sudo apt update
sudo apt install python3-pip cifs-utils libopenjp2-7 mpd -y


pip install -r requirements.txt

# install bluetooth stuff
#cd /home/pi
#git clone https://github.com/nicokaiser/rpi-audio-receiver.git  # from https://www.tutonaut.de/raspberry-pi-als-bluetooth-airplay-empfaenger-kombi/#comment-252880
#cd rpi-audio-receiver
#sudo ./install.sh  # interactively