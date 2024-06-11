<p align="center"><img src="pyjisalogo.svg"/></p>

# PyJISA

Python package for easily setting up [JISA](https://github.com/OE-FET/JISA) for use in a CPython (i.e. normal Python) environment using JPype.

## Installation

You can install this package by using PIP like so:

```
pip install git+https://github.com/OE-FET/PyJISA.git
```

## Importing and Use

Now whenever you want to use JISA in Python, simply import `pyjisa.autoload`, like so:

```python
import pyjisa.autoload
```

The first time you do this, it will download the JISA.jar file (which may take a
few seconds). Also, if pyjisa is unable to find one installed on your system, it
may also download a Java Runtime Environment (JRE):

```
>>> import pyjisa.autoload
Downloading latest JISA.jar library... Done.
No Java Runtime Environment found on system, downloading JRE 11... Done.
>>> _
```

After this, you're good to import `JISA` classes as if they were written in Python. For instance, the following "Hello World!" script should act as a good test of whether all is working as it should:

```python
import pyjisa.autoload
from jisa.gui import GUI

GUI.infoAlert("Hello World!")
```

<p align="center"><img src="https://i.imgur.com/qpjpMHx.png"/><p>

and, of course, you should be able to connect to and control your instruments:

```python
import pyjisa.autoload
from jisa.devices.smu import K2612B
from jisa.addresses import TCPIPAddress

keithley = K2612B(TCPIPAddress("192.168.0.5", 5656))

channelA = keithley.getSMU(0)
channelB = keithley.getSMU(1)

channelA.setVoltage(5.0)
channelB.setCurrent(500e-3)

channelA.turnOn()
channelB.turnOn()
```

## GUI Elements

If you have GUI elements open and are hopeing to have your program continue
running until said elements are closed, you may need to make use of
`GUI.waitForExit()` like so:

```python
import pyjisa.autoload

from jisa.gui import GUI, Plot

plot = Plot("Title", "X", "Y")
plot.setExitOnClose(True)
plot.show()

# If we don't do this, python will quit and close the GUI immediately
GUI.waitForExit()
```

This is because when reaching the end of a script, Python will exit even though
the GUI thread is till running, as it cannot see running Java threads.

To manually select which Java installation to use, just import `pyjisa` (not `pyjisa.autoload`), and call `pyjisa.load(...)` directly, supplying the path like so:

## Manually Select Java Runtime

```python
import pyjisa
pyjisa.load("/usr/lib/jvm/java-13-openjdk-amd64")
```

or

```python
import pyjisa
pyjisa.load("C:\\Program Files\\AdoptOpenJDK\\jdk-13.0.2.8-hotspot")
```

## Updating JISA.jar

You can tell pyjisa to download the latest version of the JISA.jar library by
only importing `pyjisa` and calling `pyjisa.updateJISA()`:

```
>>> import pyjisa
>>> pyjisa.updateJISA()
Downloading latest JISA.jar library... Done.
>>> _
```
