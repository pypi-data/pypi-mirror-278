# pylint: disable=[missing-module-docstring] # only single class in module
import time
from threading import Thread
import serial
import numpy as np
from PyQt6.QtWidgets import QMessageBox, QApplication
from esibd.plugins import Device
from esibd.core import Parameter, PluginManager, Channel, parameterDict, PRINT, DeviceController, getDarkMode, getTestMode

def providePlugins():
    return [Temperature]

class Temperature(Device):
    """Device that reads the temperature of a silicon diode sensor via Sunpower CryoTel controller.
    It allows to switch units between K and °C."""
    documentation = None # use __doc__

    name = 'Temperature'
    version = '1.0'
    supportedVersion = '0.6'
    pluginType = PluginManager.TYPE.INPUTDEVICE
    unit = 'K'

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.channelType = TemperatureChannel
        self.controller = TemperatureController(device=self)

    def initGUI(self):
        super().initGUI()
        self.addStateAction(func=self.changeUnit, toolTipFalse='Change to °C', iconFalse=self.makeIcon('tempC.png'),
                                               toolTipTrue='Change to K', iconTrue=self.makeIcon('tempK.png'), attr='displayC')

    def finalizeInit(self, aboutFunc=None):
        # use stateAction.state instead of attribute as attribute would be added to DeviceManager rather than self
        self.onAction = self.pluginManager.DeviceManager.addStateAction(func=self.cryoON, toolTipFalse='Cryo on.', iconFalse=self.getIcon(), toolTipTrue='Cryo off.',
                                                                  iconTrue=self.makeIcon('temperature_on.png'), before=self.pluginManager.DeviceManager.aboutAction)
        super().finalizeInit(aboutFunc)

    def getIcon(self):
        return self.makeIcon('temperature_dark.png') if getDarkMode() else self.makeIcon('temperature_light.png')

    def changeUnit(self):
        if self.liveDisplayActive():
            self.resetPlot()
            self.liveDisplay.plot()
        if self.staticDisplayActive():
            self.staticDisplay.plot()

    def getDefaultSettings(self):
        ds = super().getDefaultSettings()
        ds[f'{self.name}/Interval'][Parameter.VALUE] = 5000 # overwrite default value
        ds[f'{self.name}/CryoTel COM'] = parameterDict(value='COM3', toolTip='COM port of Sunpower CryoTel.', items=','.join([f'COM{x}' for x in range(1, 25)]),
                                          widgetType=Parameter.TYPE.COMBO, attr='CRYOTELCOM')
        ds[f'{self.name}/Toggle threshold'] = parameterDict(value=15, toolTip='Cooler is toggled on and off to stay within threshold from set value.',
                                          widgetType=Parameter.TYPE.INT, attr='toggleThreshold')
        ds[f'{self.name}/{self.MAXDATAPOINTS}'][Parameter.VALUE] = 1E6 # overwrite default value
        return ds

    def getInitializedChannels(self):
        return [d for d in self.channels if (d.enabled and (self.controller.port is not None or self.getTestMode())) or not d.active]

    def init(self):
        super().init()
        self.controller.restart = self.onAction.state
        self.controller.init()

    def startAcquisition(self):
        self.controller.startAcquisition()

    def stopAcquisition(self):
        super().stopAcquisition()
        self.controller.stopAcquisition()

    def stop(self):
        super().stop()
        self.controller.close()

    def initialized(self):
        return self.controller.initialized

    def close(self):
        self.controller.close()
        super().close()

    def convertDataDisplay(self, data):
        if self.displayC:
            return data - 273.15
        else:
            return data

    def getUnit(self):
        """Overwrite if you want to change units dynamically."""
        return '°C' if self.displayC else self.unit

    def cryoON(self):
        if self.initialized():
            self.controller.cryoON(self.onAction.state)
        else:
            self.init()

    def apply(self, apply=False): # pylint: disable = unused-argument # keep default signature
        for c in self.channels:
            c.setTemperature() # only actually sets voltage if configured and value has changed

    def updateTheme(self):
        super().updateTheme()
        self.onAction.iconFalse = self.getIcon()
        self.onAction.updateIcon(self.onAction.state) # self.on not available on start

class TemperatureChannel(Channel):
    """UI for pressure with integrated functionality"""

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.warningStyleSheet = f'background: rgb({255},{0},{0})'
        self.defaultStyleSheet = None # will be initialized when color is set

    def initGUI(self, item):
        super().initGUI(item)
        _min = self.getParameterByName(self.MIN)
        _min.spin.setMinimum(-5000)
        _min.spin.setMaximum(5000)
        _max = self.getParameterByName(self.MAX)
        _max.spin.setMinimum(-5000)
        _max.spin.setMaximum(5000)

    MONITOR   = 'Monitor'
    CONTROLER = 'Controler'
    CRYOTEL = 'CryoTel'

    def getDefaultChannel(self):
        """Gets default settings and values."""
        channel = super().getDefaultChannel()
        channel[self.VALUE][Parameter.HEADER ] = 'Temp (K)' # overwrite existing parameter to change header
        channel[self.MONITOR ] = parameterDict(value=0, widgetType=Parameter.TYPE.FLOAT, advanced=False,
                                    event=self.monitorChanged, indicator=True, attr='monitor')
        channel[self.CONTROLER] = parameterDict(value='None', widgetType=Parameter.TYPE.COMBO, advanced=True,
                                        items=f'{self.CRYOTEL}, None', attr='controler')
        return channel

    def setDisplayedParameters(self):
        super().setDisplayedParameters()
        self.insertDisplayedParameter(self.MONITOR, before=self.MIN)
        self.insertDisplayedParameter(self.CONTROLER, before=self.COLOR)

    def enabledChanged(self): # overwrite parent method
        """Handle changes while acquisition is running. All other changes will be handled when acquisition starts."""
        if self.device.liveDisplayActive() and self.device.pluginManager.DeviceManager.recording:
            self.device.init()

    def setTemperature(self): # this actually sets the voltage on the powersupply!
        if self.real:
            self.device.controller.setTemperature(self)

    def updateColor(self):
        color = super().updateColor()
        self.defaultStyleSheet = f'background-color: {color.name()}'

    def monitorChanged(self):
        if self.enabled and self.device.controller.initialized and ((self.device.controller.ON and abs(self.monitor - self.value) > 1)):
            self.getParameterByName(self.MONITOR).getWidget().setStyleSheet(self.warningStyleSheet)
        else:
            self.getParameterByName(self.MONITOR).getWidget().setStyleSheet(self.defaultStyleSheet)

    def appendValue(self, lenT):
        # super().appendValue() # overwrite to use readbacks
        self.values.add(self.monitor, lenT)

class TemperatureController(DeviceController):
    # need to inherit from QObject to allow use of signals
    """Implements serial communication with RBD 9103.
    While this is kept as general as possible, some access to the management and UI parts are required for proper integration."""

    def __init__(self, device):
        super().__init__(parent=device)
        #setup port
        self.device = device
        self.ON = False
        # self.init() only init once explicitly called
        self.restart=False
        self.temperatures = []
        self.qm = QMessageBox(QMessageBox.Icon.Information, 'Water cooling!', 'Water cooling!', buttons=QMessageBox.StandardButton.Ok)

    def stop(self):
        self.device.stop()

    def close(self):
        super().close()
        if self.ON:
            self.cryoON(on=False)
        if self.port is not None:
            with self.lock.acquire_timeout(2) as acquired:
                if acquired:
                    self.port.close()
                else:
                    self.print('Cannot acquire lock to close port.', PRINT.WARNING)
        self.initialized = False

    def stopAcquisition(self):
        if super().stopAcquisition():
            if self.device.pluginManager.closing:
                time.sleep(.1)

    def runInitialization(self):
        """Initializes serial port in paralel thread"""
        if getTestMode():
            self.signalComm.initCompleteSignal.emit()
        else:
            self.initializing = True
            try:
                self.port=serial.Serial(
                    self.device.CRYOTELCOM,
                    baudrate=9600, # used to be 4800
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    xonxoff=False,
                    timeout=3)
                # self.CryoTelWriteRead('SET TBAND=5') # set temperature band
                # self.CryoTelWriteRead('SET PID=2')# set temperature control mode
                # self.CryoTelWriteRead('SET SSTOPM=0') # enable use of SET SSTOP
                # self.CryoTelWriteRead('SENSOR') # test if configured for correct temperature sensor DT-670
                # self.CryoTelWriteRead('SENSOR=DT-670') # set Sensor if applicable
                self.signalComm.initCompleteSignal.emit()
            except Exception as e: # pylint: disable=[broad-except]
                self.print(f'Error while initializing: {e}', PRINT.ERROR)
            finally:
                self.initializing = False

    def initComplete(self):
        self.temperatures = [c.value for c in self.device.channels]
        super().initComplete()
        if getTestMode():
            self.print('Faking values for testing!', PRINT.WARNING)
        if self.restart:
            self.cryoON(True)
            self.restart = False

    def startAcquisition(self):
        # only run if init succesful, or in test mode. if channel is not active it will calculate value independently
        if self.port is not None or getTestMode():
            super().startAcquisition()

    def runAcquisition(self, acquiring):
        # runs in parallel thread
        while acquiring():
            if getTestMode():
                self.fakeNumbers()
            else:
                self.readNumbers()
            self.signalComm.updateValueSignal.emit()
            time.sleep(self.device.interval/1000)

    toggleCounter = 0
    def readNumbers(self):
        """Reads the temperature."""
        for i, c in enumerate(self.device.channels):
            if c.controler == c.CRYOTEL:
                v = self.CryoTelWriteRead(message='TC') # Display Cold-Tip Temperature (same on old and new controller)
                try:
                    v = float(v)
                    self.temperatures[i] = v
                except ValueError as e:
                    self.print(f'Error while reading temp: {e}', PRINT.ERROR)
                    self.temperatures[i] = np.nan
            else:
                self.temperatures[i] = np.nan

        # toggle cryo on off to stabilize at temperatures above what is possible with minimal power
        # temporary mode. to be replaced by temperature regulation using heater.
        # only test once a minute as cooler takes 30 s to turn on or off
        # in case of overcurrent error the cooler won't turn on and there is no need for additional safety check
        self.toggleCounter += 1
        if self.ON and np.mod(self.toggleCounter, int(60000/self.device.interval)) == 0 and self.device.channels[0].monitor != 0 and self.device.channels[0].monitor != np.nan:
            if self.device.channels[0].monitor < self.device.channels[0].value - self.device.toggleThreshold:
                self.print(f'Toggle cooler off. {self.device.channels[0].monitor} K is under lower threshold of {self.device.channels[0].value - self.device.toggleThreshold} K.')
                self.CryoTelWriteRead(message='COOLER=OFF')
            elif self.device.channels[0].monitor > self.device.channels[0].value + self.device.toggleThreshold:
                if self.CryoTelWriteRead('COOLER') != 'POWER': # avoid sending command repeatedly
                    self.print(f'Toggle cooler on. {self.device.channels[0].monitor} K is over upper threshold of {self.device.channels[0].value + self.device.toggleThreshold} K.')
                    self.CryoTelWriteRead(message='COOLER=POWER')

    def fakeNumbers(self):
        for i, c in enumerate(self.device.channels):
            # exponentially approach target or room temp + small fluctuation
            self.temperatures[i] = max((self.temperatures[i]+np.random.uniform(-1, 1)) + 0.1*((c.value if self.device.onAction.state else 300)-self.temperatures[i]),0)

    def rndTemperature(self):
        return np.random.uniform(0, 400)

    def updateValue(self):
        for c, p in zip(self.device.channels, self.temperatures):
            c.monitor = p

    def cryoON(self, on=False):
        self.ON = on
        if not getTestMode() and self.initialized:
            if on:
                self.CryoTelWriteRead(message='COOLER=POWER') # 'COOLER=ON' start (used to be 'SET SSTOP=0')
            else:
                self.CryoTelWriteRead(message='COOLER=OFF') # stop (used to be 'SET SSTOP=1')
        self.qm.setText(f"Remember to turn water cooling {'on' if on else 'off'} and gas ballast {'off' if on else 'on'}!")
        self.qm.setWindowIcon(self.device.getIcon())
        if not self.device.pluginManager.testing:
            self.qm.open() # show non blocking, defined outsided cryoON so it does not get eliminated when the function completes.
            self.qm.raise_()
        QApplication.processEvents()

    def setTemperature(self, channel):
        if not getTestMode() and self.initialized:
            if channel.controler == channel.CRYOTEL:
                Thread(target=self.setTemperatureFromThread, args=(channel,), name=f'{self.device.name} setTemperatureFromThreadThread').start()

    def setTemperatureFromThread(self, channel):
        self.CryoTelWriteRead(message=f'TTARGET={channel.value}') # used to be SET TTARGET=

    # use following from internal console for testing
    # Temperature.controller.lock.CryoTelWriteRead('TC')

    def CryoTelWriteRead(self, message):
        """Allows to write and read while using lock with timeout."""
        readback = ''
        with self.lock.acquire_timeout(2) as acquired:
            if acquired:
                self.CryoTelWrite(message)
                readback = self.CryoTelRead() # reads return value
            else:
                self.print(f'Cannot acquire lock for CryoTel communication. Query: {message}', PRINT.WARNING)
        return readback

    def CryoTelWrite(self, message):
        self.serialWrite(self.port, f'{message}\r')
        self.CryoTelRead() # repeats query

    def CryoTelRead(self):
        return self.serialRead(self.port)
