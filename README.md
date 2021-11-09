### Elechouse Voice Recognition 

This guide for using Elechouse Voice Recognation with python. I recommend for use virtualenv.

1. Install virtualenv

`$ sudo apt-get install virtualenv`

2. Clone ElechouseVR3 project

`$ git clone https://github.com/boengkar2020/ElechouseVR3.git`

3. Create virtual enviroment

`$ cd ElechouseVR3`

`$ virtualenv -p python3 venv`

`$ source venv/bin/activate`

4. Install pyserial

`(venv) $ pip install pyserial`

Now you can run train.py for record command voice.

`(venv) $ python train.py -r 0 -s On /dev/ttyUSB0`

follow instruction on the screen until success

`(venv) $ python train.py -r 1 -s Off /dev/ttyUSB0`

follow instruction on the screen until success

Actualy you can add more command voice (please read user manual module).

Run example.py for receive command voice

`(venv) $ python example.py`

