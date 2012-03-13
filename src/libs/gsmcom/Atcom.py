 # -*- coding: UTF-8 -*-
import sys
import serial
from time import sleep
from mx.DateTime import now
from libs.defines.defines import *
from libs.log.slog import slog

TIME_BETWEEN_AT = 0.2

class Atcom:

    def __init__(self, log_obj="", wport="/dev/ttyACM0", bitrate="115200", mtype="default"):

        self.wport = wport
        self.bitrate = bitrate
        self.mtype = mtype
        self.log = log_obj
        self.serial = ''

    def _open_port (self):
        """
        Brief: Open a serial port to communicate with the module.
        """
        try:
            self.serial = serial.Serial(self.wport, self.bitrate, timeout=1)
            return OK

        except IOError, emsg:
            self.log.LOG(LOG_CRITICAL, "gsmcom._open_port()", "An error occurred when opening %s port with %s of bitrate. Error: %s" % (self.wport, self.bitrate, emsg))
            return ERROR

    def _close_port(self):
        """
        Brief: Close the communication serial port.
        """
        try:
            self.serial.close()
            return OK
        except IOError, emsg:
            self.log.LOG(LOG_ERROR, "gsmcom", "Attempt to close the serial port failed. Error: %s" % emsg)
            return ERROR

    def _read(self):
        """
        Brief: Read content of serial buffer.
        Return: The data of the serial buffer if exist; 
              ERROR if something went wrong.
        """
        try:
            msg = ""
            while(self.serial.inWaiting() > 0):
                msg += self.serial.readline()

            return msg

        except IOError, emsg:
            self.log.LOG(LOG_ERROR, "gsmcom._read()", "An error occurred while reading the serial buffer. Error: %s" % emsg)
            return ERROR

    def _send(self, msg):
        """
        Brief: Send content in serial buffer.
        Param: msg The content to be sent.
        Return: The answer content;
        """        
        try:
            self.serial.write(msg+'\n\r')
            sleep(TIME_BETWEEN_AT)

        except IOError, emsg:
            self.log.LOG(LOG_ERROR, "gsmcom._send()", "An error occurred when sending data in the serial buffer.")
            return ERROR

        #self.log.LOG(LOG_INFO, "gsmcom", "Command sent: [%s]\n" % msg)    
        # get response # * the answer is taking too long
        # uncomment the lines bellow to register the module answers
        #r_msg = self._read()
        return OK

    def info (self):
        """
        Brief: Return the configuration parameters to be used.
        """
        return "Valores utilizados: %s %s %s " % (self.wport, self.bitrate, self.mtype)

###########################
# Specific functions      #
###########################
    def testCommunication(self):
        """
        Brief: Test if the gsm module is avaliable.
        Return: OK if the module is communicable;
                INVALID if is not communicable.
        """
        if self._open_port() == ERROR:
            return ERROR

        ret = OK

        self._read()
        self._send("ATD")
        ret = self._read()
        self.log.LOG(content="answer [%s]" % ret)

        self._close_port()
        if ret.find("OK") < 0 and ret.find("ok") < 0:
            return INVALID
        else:
            return OK
        

    def sendSMS(self, destination, content):
        """
        Brief: Send a sms.
        Param: destination The destination extension to were
              the sms will be sent.
        Param: content The message that the sms will load.
        Return: OK if the alarm was sent; ERROR in whatever
              other case.
        """
        if self._open_port() == ERROR:
            return ERROR
        
        # Clear the content of the rx buffer #
        self._read()
        # Setting something important #
        self._send("AT+CMGF=1")
        # Starting the command #
        self._send("AT+CMGS=\"%s\"" % destination)
        # Writing the content #
        self._send("%s" % content)
        # Confirm the command #
        self._send("\032")

        answer = self._read()

        if answer.find("ERROR") > 0: #|| answer.find("+CMGS: 73") < 0:
            self.log.LOG(LOG_ERROR, "gsmcom.sendSMS()", "Unexpected answer from module. Content: %s" % answer)
            return INVALID

        self.log.LOG(LOG_INFO, "gsmcom.sendSMS()", "Answer: %s" % answer)

        self._close_port()
        return OK
