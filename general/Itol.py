#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
#       Itol.py
#
#PYTHON ITOL API
#Modified by Fabian Zimmer (f.zimmer@uni-muenster.de)
#Adopted from:
#Albert Wang (albertyw@mit.edu), Updated March 2011
#With Complements to:
#iTOL (Interactive Tree of Life) at http://itol.embl.de/
#urllib2_file by Fabien Seisen


import os
import Comm


class Itol:
    """
    This class handles the main itol functionality
    """
    def __init__(self):
        """
        Initialize a few required variables
        """
        self.upload_params = {}
        self.export_params = {}
        self.comm = Comm.Comm()

    def add_export_param_dict(self, param_dict):
        """
        Add a dictionary of parameters to the parameters to be used when exporting
        @param: dictionary of parameters to be used
        """
        self.export_params.update(param_dict)

    def set_export_param(self, key, value):
        """
        Add a value to the dictionary of parameters to be used when exporting
        @param: dictionary of parameters to be used
        """
        self.export_params[key] = value

    def get_export_params(self):
        """
        Get the dictionary of parameters to tbe used when exporting
        @return: export the Parameters
        """
        return self.export_params

    def set_upload_param(self, variable_name, variable_value):
        """
        Add a variable and its value to this upload.  This function includes
        some basic variable checking and should be used instead of directly
        modifying the variables dictionary
        """
        # Variable checking
        if not isinstance(variable_name, str):
            raise TypeError('variable name is not a string')
        if not isinstance(variable_value, str):
            raise TypeError('variable value should be a string')
        if self.is_file(variable_name):
            if not os.path.isfile(variable_value):
                raise IOError('variable name ' + variable_name + \
                    ' indicates value should be a file')
            variable_value = open(variable_value, 'r')
        # Add the variable
        self.upload_params[variable_name] = variable_value
        return True

    def delete_upload_param(self, variable_name):
        """
        Remove a variable from the dictionary of set variables
        """
        if variable_name in self.upload_params:
            del self.upload_params[variable_name]

    def print_upload_params(self):
        """
        Print the variables that have been set so far
        """
        for variable_name, variable_value in self.upload_params.items():
            if isinstance(variable_value, file):
                print variable_name + ': ' + variable_value.name
            else:
                print variable_name + ': ' + variable_value

    def is_file(self, variable_name):
        """
        This returns a boolean whether the string in variable_name is a file
        This is determined by looking at whether "File" is a substring of
        variable_name; this assumes that variable_name is a string
        """
        if variable_name.find('File') != -1:
            return True
        else:
            return False

    def upload(self):
        """
        Upload the variables to the iTOL server and return an ItolExport object
        """
        good_upload = self.comm.upload_tree(self.upload_params)
        if good_upload:
            return self.comm.tree_id
        else:
            self.comm.tree_id = 0
            return False

    def export(self, filename=None):
        if filename is None:
            output = self.comm.export(self.export_params)
            return output
        else:
            file = open(filename, "w")
            output = self.comm.export(self.export_params)
            file.write(output)
            file.close()

    def get_webpage(self):
        """
        Get the web page where you can download the Itol tree
        """
        webpage = "http://itol.embl.de/external.cgi?tree=" + \
            str(self.comm.tree_id) + "&restore_saved=1"
        return webpage
