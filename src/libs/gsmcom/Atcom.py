 # -*- coding: UTF-8 -*-
import serial
from time import sleep
from libs.defines.defines import *
from libs.log.slog import slog

# TODO Remove all the magic numbers and make macros #
#     from the strings parameters. PLEASE!! I can't #
#     live with that...                             #
TIME_BETWEEN_AT = 0.2 # seconds #
SEND_SMS_DELAY = 20  # seconds #

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
        Return: OK if could send the content; ERROR otherwise.
        """        
        try:
            self.serial.write(msg+"\r")
            sleep(TIME_BETWEEN_AT)

        except IOError, emsg:
            self.log.LOG(LOG_ERROR, "gsmcom._send()", "An error occurred when sending data in the serial buffer.")
            return ERROR

        #self.log.LOG(LOG_INFO, "gsmcom", "Command sent: [%s]\n" % msg)    
        # get response # * the answer is taking too long
        # uncomment the lines bellow to register the module answers
        #r_msg = self._read()
        return OK

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

        self._read()
        self._send("ATI")
        ret = self._read()
        self._close_port()
        # TODO do this thing more acurrate
        if ret.find(AT_OK) <= ERROR:
            return ERROR
        else:
            return OK

    def info (self):
        """
        Brief: Return the configuration parameters to be used.
        """
        return "Configured values: %s %s %s " % (self.wport, self.bitrate, self.mtype)

    def configureModule(self):
        """
        Brief: Set module configurations to send and recevive SMS.
        Return: OK if the alarm was sent; ERROR in whatever
              other case.
        """
        if self._open_port() == ERROR:
            return ERROR

        # Put the modem in SMS text mode #
        self._send("AT+CMGF=1")
        self._read() # AT+CMGF? -> +CMGF: 1 #
        # Preferred Message Storage #
        self._send("AT+CPMS=\"SM\",\"SM\",\"SM\"") # validate the answer bellow #
        self._read() # AT+CPMS? -> +CPMS: "SM",0,50,"SM",0,50,"SM",0,50 #

        self._close_port()
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
        # Starting the command #
        self._send("AT+CMGS=\"%s\"" % destination)
        # Writing the content #
        self._send("%s" % content)
        # Confirm the command #
        self._send("\032")

        sleep(SEND_SMS_DELAY)
        answer = self._read()
        self._close_port()

        # TODO this verification does not really work
        #if answer.find(AT_ERROR_ST) >= OK:
        #    self.log.LOG(LOG_ERROR, "gsmcom.sendSMS()", "Failed to send message. Answer Content: %s" % answer)
        #    return INVALID
        return OK

    def getAllNewMessages(self):
        """
        Brief: Ask the module by "REC UNREAD" (read: NEW) messages.
        Return: Should returns a dictionary with the new messages.
        """

        if self._open_port() == ERROR:
            return ERROR

        self._read()
        self._send("AT+CMGL=\"REC UNREAD\"")
        ret = self._read()
        # TODO mount an array with the orig, code, message #
        self._close_port()
        return ret

    def getMessagesCount(self):
        """
        Brief: Ask the module for the SMS messages number.
        Return: The SMS messages number.
        """
        if self._open_port() == ERROR:
            return ERROR

        ANSWER_EXPECTED_FIELDS = 9

        try:
            self._read()
            self._send("AT+CPMS?")
            answer = self._read() # 'at+cpms?\r+CPMS: "SM",3,50,"SM",3,50,"SM",3,50\r\n0\r' #

            # handle the answer #
            answer = answer.split() # ['at+cpms?', '+CPMS:', '"SM",3,50,"SM",3,50,"SM",3,50', '0'] #
            answer = answer[2].split(",") # ['"SM"', '3', '50', '"SM"', '3', '50', '"SM"', '3', '50'] #

            if len(answer) != ANSWER_EXPECTED_FIELDS: 
                self.log.LOG(LOG_ERROR, "gsmcom.getMessagesCount()", "Unexpected length in +CPMS answer. Expected: %d; Receive: %d" % (ANSWER_EXPECTED_FIELDS, len(answer)))
                self._close_port()
                return ERROR

            # ensures that the correct column will be returned #
            for index in range(len(answer)):
                if answer[index] == '"SM"':
                    return int(answer[index+1])

        except Exception, exc:
            self._close_port()
            self.log.LOG(LOG_ERROR, "gsmcom.getMessagesCount()", "%s: %s" % (exc.__class__.__name__, exc))
            return ERROR

        self._close_port()
        return ERROR

    def getMessageByIndex(self, msg_index):
        """
        Brief: Ask the module for a specific message.
        Param: msg_index The position of the message in the module.
        Return: A dict with the data from the recovered message.
        """
        if self._open_port() == ERROR:
            return ERROR

        SMS_HEADER_FIELDS = 5 # header + command status (OK/ERROR)
        SMS_MSG_OFFSET = 4

        try:
            self._read()
            self._send("AT+CMGR=%d" % msg_index)
            answer = self._read()
            answer = answer.split() # ['at+cmgr=1', '+CMGR:', '"REC', 'UNREAD","04896710721",,"12/03/15,12:34:20-12"', 'vitor:', 'dosiajdadada', '0'] #
            answer_sub = answer[3].split(",") # ['UNREAD"', '"04896710721"', '', '"12/03/15', '12:34:20-12"'] #
            orig = answer_sub[1].split("\"")[1][3:] # '96710721' #
            date = answer_sub[3].split("\"")[1] + " " + answer_sub[4].split("\"")[0] # '12/03/15 12:34:20-12' #
            msg = ""
            msg_blocks = len(answer) - SMS_HEADER_FIELDS #

            for count in range(msg_blocks):
                msg += answer[SMS_MSG_OFFSET+count] # vitor:dosiajdadada #
                if count < msg_blocks: # put spaces between the content, except in the last block. #
                    msg += " "

            self._close_port()
            return  {DATA_ORIG:orig, DATA_DATE:date, DATA_MSG:msg}

        except Exception, exc:
            self.log.LOG(LOG_ERROR, "gsmcom.getMessageByIndex()", "%s: %s" % (exc.__class__.__name__, exc))
            return ERROR

    def deleteMessage(self, msg_index):
        """
        Brief: Delete message by its index.
        Return: OK if could delete the message;
                ERROR otherwise.
        """
        if self._open_port() == ERROR:
            return ERROR

        self._send("AT+CMGD=%d" % msg_index)
        answer = self._read()

        # TODO validate answer #

        self._close_port()
        return OK
