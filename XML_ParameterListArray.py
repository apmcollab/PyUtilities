#!/usr/bin/env python3

#############################################################################
#                         XML_ParameterListArray.py 
#
# A copy of PyUtilities/XML_ParameterListArray.py 
#
# Author: C. Anderson
# Origin date                   : June 12, 2020 
# Updated to use lxml parser    : Nov  11, 2025 (cra) 
# Version 1.0.2
#############################################################################
#
# Copyright  2025- Chris Anderson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# For a copy of the GNU General Public License see
# <http://www.gnu.org/licenses/>.
#
#############################################################################
 
import sys

import lxml.etree as ET

TRUE_VALS  = ( '1', 'true',  'True', 'TRUE',  'y', 'yes', 'Y', 'Yes', 'YES','ON',"on","On")
FALSE_VALS = ( '0', 'false', 'False', 'FALSE','n', 'no',  'N', 'No',   'NO',"OFF","off","Off")

class XML_ParameterListArray:
    def __init__(self,fileName = None):
        self.tree     = None
        self.root     = None
        self.fileName = fileName
        
        if(self.fileName != None):
            self.tree = ET.parse(fileName)
            self.root = self.tree.getroot()
            
    def deepcopy(self,xml_ParameterListArray):
        self.tree = deepcopy(xml_ParameterListArray)
        self.root = self.tree.getroot()
        
    def createParameterListArray(self,listArrayName):
        self.tree = ET.ElementTree(ET.Element(listArrayName))
        self.root = self.tree.getroot()
    
    def addParameterList(self,paramListName):
        if(self.tree.find(paramListName) != None):
            raise Exception("Duplicate parameter lists not allowed",paramListName)
        self.root.append(ET.Element(paramListName))
    #
    # The type of the parameter is determined by the value specified. If
    # None is specified, then the type and value attributes are not set
    #   
    def addParameter(self,value,parameterName, parameterListName):
        parameterList = self.tree.find(parameterListName)
        if(parameterList == None):
            raise Exception("Insertion of parameter in non-existent parameter list : ",parameterListName)
        
        if(value == None): 
            parameterList.append(ET.Element(parameterName))
            return
        
        valStr,typeStr = self.getValueAndTypeAsStringCPP(value)
        parameterList.append(ET.Element(parameterName,dict(type=typeStr,value=valStr)))
    
    def getParameterValue(self,parameterName, parameterListName):
        parameterList = self.tree.find(parameterListName)
        if(parameterList == None):
            raise Exception("\n ParameterList not found \n ParameterList specified  : " + parameterListName)
        instance = parameterList.find(parameterName)
        if(instance == None):
            raise Exception("\n Parameter not found in ParameterList \n ParmeterList : " + parameterListName \
                             + "\n Parameter    : " + parameterName)

        return self.getValue(instance)
    
    #
    # Version of set parameters to set the type of Python float values 
    # as "float" and integer values as int 
    #
    def setParameterValue(self, paramValue, parameterName, parameterListName):
        parameterList = self.tree.find(parameterListName)
        if(parameterList == None):
            raise Exception("\n ParameterList not found \n ParameterList specified  : " + parameterListName)
        instance = parameterList.find(parameterName)
        if(instance == None):
            raise Exception("\n Parameter not found in ParameterList \n ParmeterList : " + parameterListName \
                             + "\n Parameter    : " + parameterName)       
        originalValue = self.getParameterValue(parameterName, parameterListName)
        originalType  = type(originalValue)
        valType       = type(paramValue)
        errorFlag     = False 
        
        if(valType == None):
            instance.set("value",self.getValueAndTypeAsStringCPP(paramValue)[0])
            instance.set("type", self.getValueAndTypeAsStringCPP(paramValue)[1])
            return
        else:
            if(originalType is int):
                if(valType is int):
                    instance.set("value",self.getValueAndTypeAsStringCPP(paramValue)[0])
                    instance.set("type", "int")
                else: 
                    errorFlag = True
                    
            if(originalType is float):
                if(valType is float):
                    instance.set("value",self.getValueAndTypeAsStringCPP(paramValue)[0])
                    instance.set("type", "float")
                else: 
                    errorFlag = True      

            if(originalType is str):
                if(valType is str):
                    instance.set("value",self.getValueAndTypeAsStringCPP(paramValue)[0])
                    instance.set("type", "string")
                else: 
                    errorFlag = True
    
            if(originalType is bool):
                if(valType is bool):
                    instance.set("value",self.getValueAndTypeAsStringCPP(paramValue)[0])
                    instance.set("type", "bool")
                else:
                    errorFlag = True
                              
        if(errorFlag):
            raise Exception("\nsetParameterValueCPP value specification type not consistent with existing "  \
            + "parameter type specification." \
            + "\nParameterList  : " + parameterListName \
            + "\nParameterName  : " + parameterName \
            + "\nParameterType  : " + str(originalType) \
            + "\nValueInputType : " + str(valType))          
             
    #
    # Version of set parameters to set the type of Python float values 
    # as "double" and and integer values as long 
    #
    def setParameterValueCPP(self, paramValue, parameterName, parameterListName):
        parameterList = self.tree.find(parameterListName)
        if(parameterList == None):
            raise Exception("\n ParameterList not found \n ParameterList specified  : " + parameterListName)
        instance = parameterList.find(parameterName)
        if(instance == None):
            raise Exception("\n Parameter not found in ParameterList \n ParmeterList : " + parameterListName \
                             + "\n Parameter    : " + parameterName)       
        originalValue = self.getParameterValue(parameterName, parameterListName)
        originalType  = type(originalValue)
        valType       = type(paramValue)
        errorFlag     = False
        
        if(valType == None):
            instance.set("value",self.getValueAndTypeAsStringCPP(paramValue)[0])
            instance.set("type", self.getValueAndTypeAsStringCPP(paramValue)[1])
            return
        else:
            if(originalType is int):
                if(valType is int):
                    instance.set("value",self.getValueAndTypeAsStringCPP(paramValue)[0])
                    instance.set("type", "long")
                else: 
                    errorFlag = True  
                    
            if(originalType is float):
                if(valType is float):
                    instance.set("value",self.getValueAndTypeAsStringCPP(paramValue)[0])
                    instance.set("type", "double")
                else: 
                    errorFlag = True   

            if(originalType is str):
                if(valType is str):
                    instance.set("value",self.getValueAndTypeAsStringCPP(paramValue)[0])
                    instance.set("type", "string")
                else: 
                    errorFlag = True  
    
            if(originalType is bool):
                if(valType is bool):
                    instance.set("value",self.getValueAndTypeAsStringCPP(paramValue)[0])
                    instance.set("type", "bool")
                else: 
                    errorFlag = True  
                             
        if(errorFlag):
            raise Exception("\nsetParameterValueCPP value specification type not consistent with existing "  \
            + "parameter type specification." \
            + "\nParameterList  : " + parameterListName \
            + "\nParameterName  : " + parameterName \
            + "\nParameterType  : " + str(originalType) \
            + "\nValueInputType : " + str(valType))
    #
    # Version of set parameters to set the type of Python float values 
    # as "double" and and integer values as long 
    #
    def setInstanceValueCPP(self, paramValue, originalValue, instance,parameterChild,parameterName,parameterListName):
        originalType  = type(originalValue)
        valType       = type(paramValue)
        errorFlag     = False
        if(valType == None):
            instance.set("value",self.getValueAndTypeAsStringCPP(paramValue)[0])
            instance.set("type", self.getValueAndTypeAsStringCPP(paramValue)[1])
            return
        else:
            if(originalType is int):
                if(valType is int):
                    instance.set("value",self.getValueAndTypeAsStringCPP(paramValue)[0])
                    instance.set("type", "long")
                else: 
                    errorFlag = True
            if(originalType is float):
                if(valType is float):
                    instance.set("value",self.getValueAndTypeAsStringCPP(paramValue)[0])
                    instance.set("type", "double")
                else: 
                    errorFlag = True  

            if(originalType is str):
                if(valType is str):
                    instance.set("value",self.getValueAndTypeAsStringCPP(paramValue)[0])
                    instance.set("type", "string")
                else: 
                    errorFlag = True
    
            if(originalType is bool):
                if(valType is bool):
                    instance.set("value",self.getValueAndTypeAsStringCPP(paramValue)[0])
                    instance.set("type", "bool")
                else: 
                    errorFlag = True 
        if(errorFlag):
            raise Exception("\nsetParameterValueCPP value specification type not consistent with existing "  \
            + "parameter type specification." \
            + "\nParameterList  : " + parameterListName \
            + "\nParameterName  : " + parameterName \
            + "\nParameterChild : " + parameterChild \
            + "\nParameterType  : " + str(originalType) \
            + "\nValueInputType : " + str(valType))
    #    
    # Sets the value of the child of the parameter parameterName. If there is more than 
    # one parameterName parameters in the parameterList then this only sets the first instance
    # value. 
    #            
    def setParameterChildValueCPP(self,paramValue,parameterChildName,parameterName,parameterListName):
        parameterList = self.tree.find(parameterListName)
        if(parameterList == None):
            raise Exception("\n ParameterList not found \n ParameterList specified  : " + parameterListName)
        instances = parameterList.findall(parameterName)
        if(instances == None):
            raise Exception("\n Parameter not found in ParameterList \n ParmeterList : " + parameterListName \
                             + "\n Parameter    : " + parameterName)
        if(len(instances) > 1):
            raise Exception("\n Multiple parameters with identical names found  \n ParmeterList   : " \
                             + parameterListName \
                             + "\n Parameter      : "  + parameterName   \
                             + "\n ChildParameter : " + parameterChildName \
                             + "\n Use setParameterInstanceChildValueCPP ") 
        childParam = instances[0].findall(parameterChildName) 
        if(childParam == []):
            raise Exception("\n Child parameter not found  \n ParmeterList   : " + parameterListName \
                             + "\n Parameter      : "  + parameterName   \
                             + "\n ChildParameter : " + parameterChildName)  
        originalValue = self.getValue(childParam[0])
        self.setInstanceValueCPP(paramValue, originalValue,childParam[0], parameterChildName, parameterName,parameterListName)
       
    def setParameterInstanceChildValueCPP(self,paramValue,instanceIndex,parameterChildName,parameterName,parameterListName):
        parameterList = self.tree.find(parameterListName)
        if(parameterList == None):
            raise Exception("\n ParameterList not found \n ParameterList specified  : " + parameterListName)
        instances = parameterList.findall(parameterName)
        if(instances == None):
            raise Exception("\n Parameter not found in ParameterList \n ParmeterList : " + parameterListName \
                             + "\n Parameter    : " + parameterName)
        
        childParam = instances[instanceIndex].find(parameterChildName) 
        if(childParam == []):
            raise Exception("\n Child parameter not found  \n ParmeterList   : " + parameterListName \
                             + "\n Parameter      : "  + parameterName   \
                             + "\n ChildParameter : " + parameterChildName)  
        
        originalValue = self.getValue(childParam)
        self.setInstanceValueCPP(paramValue, originalValue,childParam,parameterChildName,parameterName,parameterListName)

    def getParameterValueOrText(self,parameterName, parameterListName):
        parameterList = self.tree.find(parameterListName)
        if(parameterList == None):
            raise Exception("\n ParameterList not found \n ParameterList specified  : " + parameterListName)
        instance = parameterList.find(parameterName)
        if(instance == None):
            raise Exception("\n Parameter not found in ParameterList \n ParmeterList : " + parameterListName \
                             + "\n Parameter    : " + parameterName)
        return self.getValueOrText(instance)
    
    def getParameterText(self,parameterName, parameterListName):
        parameterList = self.tree.find(parameterListName)
        if(parameterList == None):
            raise Exception("\n ParameterList not found \n ParameterList specified  : " + parameterListName)
        instance = parameterList.find(parameterName)
        if(instance == None):
            raise Exception("\n Parameter not found in ParameterList \n ParmeterList : " + parameterListName \
                             + "\n Parameter    : " + parameterName)

        return instance.text.strip()
      
    def getParameterAll(self,parameterName, parameterListName):
        parameterList = self.tree.find(parameterListName)
        if(parameterList == None):
            raise Exception("\n ParameterList not found \n ParameterList specified  : " + parameterListName)
        parameters = parameterList.findall(parameterName)
        if(parameters == None):
            raise Exception("\n Parameter not found in ParameterList \n ParmeterList : " + parameterListName \
                             + "\n Parameter    : " + parameterName)

        return parameters

    def getParameterValueOrDefault(self,parameterName, parameterListName,defaultValue):
        parameterList = self.tree.find(parameterListName)
        if(parameterList == None):
            raise Exception("\n ParameterList not found \n ParameterList specified  : " + parameterListName)
        instance = parameterList.find(parameterName)
        parameterValue = defaultValue;
        if(instance != None):
            parameterValue = self.getValue(instance)  
        return parameterValue
    
    def getParameterNames(self,parameterListName):
        parameterList = self.tree.find(parameterListName)
        if(parameterList == None):
            raise Exception("\n ParameterList not found \n ParameterList specified  : " + parameterListName)
        parameterNames = []
        for parameter in parameterList:
            if not (parameter.tag is ET.Comment):
                parameterNames.append(parameter.tag)
        return parameterNames
    
    def isParameterList(self,parameterListName):
        parameterList = self.tree.find(parameterListName)
        if(parameterList == None): return False       
        return True
    
    def isParameter(self,parameterName,parameterListName):
        parameterList = self.tree.find(parameterListName)
        if(parameterList == None):
            raise Exception("\n ParameterList not found \n ParameterList specified  : " + parameterListName)
        instance = parameterList.find(parameterName)
        if(instance == None): return False
        return True
    
    def getParameterList(self,parameterListName):
        parameterList = self.tree.find(parameterListName)
        if(parameterList == None):
            raise Exception("\n ParameterList not found \n ParameterList specified  : " + parameterListName)
        
        return parameterList
        
    def getParameterListAll(self, parameterListName):
        parameterList = self.tree.findall(parameterListName)
        if(parameterList == None):
            raise Exception("\n ParameterList not found \n ParameterList specified  : " + parameterListName)
        
        return parameterList
    
    def getParameterChildNames(self,parameterName,parameterListName):
        parameterList = self.tree.find(parameterListName)
        if(parameterList == None):
            raise Exception("\n ParameterList not found \n ParameterList specified  : " + parameterListName)
        instance = parameterList.find(parameterName)
        if(instance == None):
            raise Exception("\n Parameter not found in ParameterList \n ParmeterList : " + parameterListName \
                             + "\n Parameter    : " + parameterName)
        childNames = []
        for childParam  in instance:
            if not (childParam.tag is ET.Comment):
                childNames.append(childParam.tag)
        return childNames
    
    def getParameterChildValues(self,parameterChildName,parameterName,parameterListName):
        parameterList = self.tree.find(parameterListName)
        if(parameterList == None):
            raise Exception("\n ParameterList not found \n ParameterList specified  : " + parameterListName)
        instance = parameterList.find(parameterName)
        if(instance == None):
            raise Exception("\n Parameter not found in ParameterList \n ParmeterList : " + parameterListName \
                             + "\n Parameter    : " + parameterName)
        
        childParams = instance.findall(parameterChildName)
        if(childParams == []):
            raise Exception("\n Child parameter not found  \n ParmeterList   : " + parameterListName \
                             + "\n Parameter      : "  + parameterName   \
                             + "\n ChildParameter : " + parameterChildName)  
        childValues = []
        for p  in childParams:
            childValues.append(self.getValue(p))
        return childValues

    #
    # Adds a child value to all instances of the specified parameter in the
    # specified parameterList.
    #
    # If the parameter specified does not exist, then it is created
    #
    def addParameterChild(self, value, childName, parameterName, parameterListName): 
        parameterList = self.root.find(parameterListName)
        if(parameterList.findall(parameterName) == []):
            self.addParameter(None,parameterName,parameterListName)
    
        for instance in parameterList.findall(parameterName):
            if(instance.get("value") != None):
                raise Exception("Adding child to a parameter with value not allowed",childName,parameterName,parameterListName)
            if(value == None):
                if(instance.find(childName) != None):
                    raise Exception("Duplicate child parameters not allowed",childName,parameterName,parameterListName)
                else:
                    instance.append(ET.Element(childName))
            else:
                if(instance.find(childName)!= None):
                    raise Exception("Duplicate child parameters not allowed",childName,parameterName,parameterListName)
                else:
                    valStr,typeStr = self.getValueAndTypeAsStringCPP(value)
                    instance.append(ET.Element(childName,dict(type=typeStr,value=valStr)))
    
    #addParameterInstanceChild(XML_dataType value, int instanceIndex, const char* parameterChildName,
    #const char* parameterName, const char* parameterListName)       
                
    def getValueAndTypeAsString(self,value):
        if(type(value) is float): 
            typeStr = "float"
            valStr  = '{0:16.15e}'.format(value)
        elif(type(value) is bool) : 
            typeStr = "bool"
            if(value): valStr = "true"
            else:      valStr = "false"
        elif(type(value) is int) : 
            typeStr = "int"
            valStr  = '{0:d}'.format(value)
        elif(type(value) is str) : 
            typeStr = "string"
            valStr  = value
        else:
            raise Exception("Unacceptable value for parameter ",value,type(value))
        
        return valStr,typeStr
    
    def getValueAndTypeAsStringCPP(self,value):
        if(type(value) is float): 
            typeStr = "double"
            valStr  = '{0:16.15e}'.format(value)
        elif(type(value) is bool) : 
            typeStr = "bool"
            if(value): valStr = "true"
            else:      valStr = "false"
        elif(type(value) is int) : 
            typeStr = "long"
            valStr  = '{0:d}'.format(value)
        elif(type(value) is str) : 
            typeStr = "string"
            valStr  = value
        else:
            raise Exception("Unacceptable value for parameter ",value,type(value))
        
        return valStr,typeStr
    
    def run(self):
        self.tree = ET.parse('XMLoutput.xml')
        #root = ET.fromstring(country_data_as_string)
        self.root = self.tree.getroot()
        
        # Returns the name of the containing XML node
        
        print(self.root.tag)
        
        # Returns the names of the parameter lists (there are no attributes)
        
        for parameterList in self.root:
            # prints the parameter list name 
            
            print ("ParameterListName: ",parameterList.tag)
            
            # Print the parameter name and attributes
 
            for parameter in parameterList:
                if(len(list(parameter)) == 0):
                    valueType = self.getType(parameter)
                    parameter.set('type',valueType)
                    print("    Parameter : ",parameter.tag,parameter.attrib,self.getValue(parameter),valueType)
                    
                else:
                    print("    Parameter : ",parameter.tag)
                    for child in parameter:
                        valueType = self.getType(child)
                        child.set('type',valueType)
                        print("         ",child.tag,child.attrib,self.getValue(child),valueType)
        
        self.outputToFile("XMLoutput2.xml")
    
    
    def outputToScreen(self):
        print(ET.tostring(self.tree, pretty_print=True, encoding='utf-8').decode())
        
    def outputToFile(self,fileName):
        self.tree.write(fileName, pretty_print=True, encoding="utf-8", xml_declaration=True)
             
    def getType(self,paramElement):
        valType = paramElement.get("type",None)
        if(valType != None) : 
            if(valType == "double"): return "float"
            if(valType == "long"):   return "long"
            return valType
        
        strVal = paramElement.get("value",None)
        if(strVal == None):
            raise ValueError("value attribute not specified in ",paramElement)
        
        try:
            float(strVal)
            if(strVal.find(".") >= 0) : return "float"
            else:                       return "int"
        except ValueError:
            if( (strVal in TRUE_VALS) or (strVal in FALSE_VALS)): 
                return "bool"
            return "string"    
    
    def hasValueSpecified(self,paramElement):
        strVal  = paramElement.get("value",None)
        if(strVal == None): return False
        return True
    
    def getTextSpecification(self,paramElement):
        valType = paramElement.get('type',None)
        strVal  = paramElement.text
        if(strVal == None):
            raise ValueError("value attribute not specified in ",paramElement)
        
        if(valType != None) : 
            try:
                if(valType == "string"): return strVal
                if(valType == "float") : return float(strVal)
                if(valType == "double"): return float(strVal)
                if(valType == "int")   : return int(strVal)
                if(valType == "long")  : return int(strVal)
                if(valType == "bool")  : 
                    if(strVal in TRUE_VALS) : return True
                    if(strVal in FALSE_VALS): return False
            except:
                raise ValueError("type inconsistent with value specified or type un-supported",\
                                 paramElement).with_traceback(sys.exc_info()[2])
        
        try:
            float(strVal)
            if(strVal.find(".") >= 0) : return float(strVal) 
            else:                       return int(strVal)
        except ValueError:
            if(strVal in TRUE_VALS):
                return True 
            if(strVal in FALSE_VALS) : 
                return False 
            return strVal 

    def getValueOrText(self,paramElement):
        val = paramElement.get('value',None)
        if(val == None):
            if(paramElement.text != None):
               if(len(paramElement.text.strip()) != 0) : return paramElement.text.strip()
               return None
        else:
            if(len(val.strip()) != 0) : return val.strip()
            return None
 
           
    def getValue(self,paramElement):
        valType = paramElement.get('type',None)
        strVal  = paramElement.get("value",None)
        if(strVal == None):
            raise ValueError("value attribute not specified in ",paramElement)
        
        if(valType != None) : 
            try:
                if(valType == "string"): return strVal
                if(valType == "float") : return float(strVal)
                if(valType == "double"): return float(strVal)
                if(valType == "int")   : return int(strVal)
                if(valType == "long")  : return int(strVal)
                if(valType == "bool")  : 
                    if(strVal in TRUE_VALS) : return True
                    if(strVal in FALSE_VALS): return False
            except:
                raise ValueError("type inconsistent with value specified or type un-supported",\
                                 paramElement).with_traceback(sys.exc_info()[2])
        
        try:
            float(strVal)
            if(strVal.find(".") >= 0) : return float(strVal) 
            else:                       return int(strVal)
        except ValueError:
            if(strVal in TRUE_VALS):
                return True 
            if(strVal in FALSE_VALS) : 
                return False 
            return strVal 
    
        
if __name__ == '__main__':
    xml_ParameterListArray = XML_ParameterListArray()
    xml_ParameterListArray.createParameterListArray("NewArray")
    xml_ParameterListArray.addParameterList("NewParameterList")
    xml_ParameterListArray.addParameterChild("10","Age","NewParameter","NewParameterList")
    ET.dump(xml_ParameterListArray.root)
    

        
