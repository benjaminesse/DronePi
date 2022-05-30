# PiSpec
Capture and analyse UV spectra in real-time using a mobile Raspberry Pi.

## Installation

Install vertualenv if it not already in the base environment:
```
pip3 install virtualenv
```

Clone the repository and enter:
```
git clone https://github.com/benjaminesse/PiSpec.git
cd PiSpec
```

Create the virtual environment and activate:
```
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies:
```
pip3 install numpy scipy pandas plotly Flask dash dash-bootstrap-components utm gunicorn PyYAML seabreeze pyserial
```

To install the spectrometer driver files, run
```
seabreeze_os_setup
```
Note this may have to be in a new console!

## Testing

To test the server run:
```
cd /home/pi/PiSpec/
source venv/bin/activate
gunicorn -w 4 -b 0.0.0.0:4000 app:app --log-file=gunicorn.log
```

Then open `[PiSpec IP Address]:4000` in a browser on the same network as the Raspberry Pi, you should see the landing page. If not, check the `gunicorn.log` file.

## Set to run automatically

To automatically turn on the server on boot open crontab using:

```
crontab -e
```

You may have to select a text editor the first time, I would recommend nano. Then add the following line to the bottom:

```
@reboot cd /home/pi/PiSpec/ && source venv/bin/activate && gunicorn -w 4 -b 0.0.0.0:4000 app:app -D --log-file=gunicorn.log &
```

Then reboot the Raspberry Pi using `sudo reboot`. When the Pi reboots the server should be available on the network at `[PiSpec IP Address]:4000`.
