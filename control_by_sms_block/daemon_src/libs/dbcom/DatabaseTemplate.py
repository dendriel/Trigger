# -*-coding:utf-8-*-
#################################################################
#  This template should be used to abstract the database access #
# of the main class.                                            #
#################################################################
from libs.defines.defines import *

class DatabaseTemplate:

    def checkConnection(self):
        """
        Brief: Test the connection and parameters for database access.
        Return: OK if could establish a connection and access the database; ERROR otherwise.
        """
        return INVALID

    def checkTables(self, user_tables):
        """
        Brief: Verifies that there are the standard tables and create it if there are no tables.
        """
        return INVALID

    def registerRequisition(self, data):
        """
        Brief: Insert a new row for the new requisiton.
        Param: data The data for the new row.
        Return: OK if the new entry was successful inserted. ERROR if something went wrong.
        """
        return INVALID

    def getRequisitions(self, status):
        """
        Brief: Ask database by a list of the specified requisition status.
        Param: status The status for searching for the requisitions.
        Return: An list with the ocurrence of the specified requisition status.
        """
        return INVALID

    def changeRequisitionStatus(self, req_id, status):
        """
        Brief: Change a requisition status in database.
        Param: req_id The requisition to be modified.
        Param: status The new status for the requisition.
        Return: OK if could change the requisition status;
                ERROR if something whent wrong.
        """
        return INVALID

    def getDataFromRequisition(self, req_id):
        """
        brief: Retrive data from database to complete the requisition.
        Param: req_id The id to select the requisition.
        Return: A dictionay with the necessary data.
        """
        return INVALID

