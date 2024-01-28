# weatherstation

## PI Zero version

## Set up i2c
```sudo raspi-config```
Select interfaces -> i2c and enable it

## Installation
```
mkdir src
cd src
git clone https://github.com/jeffspiinthesky/weatherstation.git
cd weatherstation/zero
pip3 install -r requirements.txt
```

## Connect the BME280 to the PI
* Vin -> GPIO 1
* SD1 -> GPIO 3
* SCK -> GPIO 5
* Ground -> GPIO 9

## Test
```
python3 weatherstation.py
```
You should see temperature, pressure and humidity returned

## Run the app
```
mkdir -p ~.config/lxsession/LXDE-pi
cp autostart ~/.config/lxsession/LXDE-pi/
chmod +x ~/.config/lxsession/LXDE-pi/autostart
sudo cp run_app.sh /usr/local/bin/
sudo chmod +x /usr/local/bin/run_app.sh
sudo apt install firefox-esr unclutter
```
Once that is all done, reboot. Everything should then work fine! You can access the app from a browser with:
```http://<PI IP Address>:5000```