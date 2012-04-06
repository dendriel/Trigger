# -*-coding:utf-8-*-
#################################################################
#  This template should be used to abstract the gsm/sms methods #
# of the main class.                                            #
#################################################################
from libs.defines.defines import *

class GsmTemplate:

    def testCommunication(self):
        """
        Brief: Test if the gsm module is avaliable.
        Return: OK if the module is communicable;
                INVALID if is not communicable.
        """
        return INVALID

    def info (self):
        """
        Brief: Return the configuration parameters to be used.
        """
        return INVALID

    def configureModule(self):
        """
        Brief: Set module configurations to send and recevive SMS.
        Return: OK if the alarm was sent; ERROR in whatever
              other case.
        """
        return INVALID

    def sendSMS(self, destination, content):
        """
        Brief: Send a sms.
        Param: destination The destination extension to were
              the sms will be sent.
        Param: content The message that the sms will load.
        Return: OK if the alarm was sent; ERROR in whatever
              other case.
        """
        return INVALID

    def getAllNewMessages(self):
        """
        Brief: Ask the module by "REC UNREAD" (read: NEW) messages.
        Return: Should returns a dictionary with the new messages.
        """
        return INVALID

    def getMessagesCount(self):
        """
        Brief: Ask the module for the SMS messages number.
        Return: The SMS messages count.
        """
        return INVALID

    def getMessageByIndex(self, msg_index):
        """
        Brief: Ask the module for a specific message.
        Param: msg_index The position of the message in the module.
        Return: A dict with the data from the recovered message.
        """
        return INVALID

    def deleteMessage(self, msg_index):
        """
        Brief: Delete message by its index.
        Return: OK if could delete the message;
                ERROR otherwise.
        """
        return INVALID

