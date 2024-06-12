##############################
#   
#       Dicom Standard Enums(DICOM PS3.6 version 2013c)
#for detiled dicom tags, please refer to: https://dicom.nema.org/dicom/2013/output/chtml/part04/sect_i.4.html
#                                         https://dicom.innolitics.com/ciods
#       2024/04/08 by Kaixuan,Zhao in Canton
##############################
from enum import Enum
from collections import namedtuple
from typing import Dict
import json
import pickle
from pathlib import Path
from typing import Union
import json
import os

class IODModuleUsage(Enum):
    Mandatory = ("Mandatory (M)", -1, "M")                                                                       #'M'
    Conditional = ("Conditional (C)", 0, "C")                                                                    #'C'
    UserOption = ("User Optional (U)", 1, "U")                                                                   #'U'
    
    def __init__(self, description, priority, abbreviation):
        self._description = description
        self._priority = priority
        self._abbreviation = abbreviation
    
    @property
    def description(self):
        return self._description
    
    @property
    def priority(self):
        return self._priority
    
    @property
    def abbreviation(self):
        return self._abbreviation
    
class DicomTagType(Enum):
    Required = ("Required (1)", -1, "1")                                                                            #'1'
    ConditionalRequired = ("Conditionally Required (1C)", 0, "1C")                                                  #'1C
    RequiredWithEmptyIfUnknow = ("Required, Empty if Unknown (2)", 1, "2")                                          #'2'
    ConditionalRequiredWithEmptyIfUnknow = ("Conditionally Required, Empty if Unknown (2C)",2, "2C")                #'2C'
    Optional = ("Optional (3)", 3, "3")                                                                             #'3'  

    def __init__(self, description, priority,abbreviation):
        self._description = description
        self._priority = priority
        self._abbreviation = abbreviation
    
    @property
    def description(self):
        return self._description
    
    @property
    def priority(self):
        return self._priority
    
    @property
    def abbreviation(self):
        return self._abbreviation

class DicomCIODItem:
    def __init__(self, 
                 **kwargs):
        self.CIODName = None
        self.Interpretation = None
        self.DicomStandardSyncTime = None
        if "CIODName" in kwargs:
            self.CIODName = kwargs["CIODName"]
        else:
            raise ValueError("Element not found.")
        if "Interpretation" in kwargs:
            self.Interpretation = kwargs["Interpretation"]
        else:
            raise ValueError("Element not found.")
        if "DicomStandardSyncTime" in kwargs:
            self.DicomStandardSyncTime = kwargs["DicomStandardSyncTime"]
        else:
            raise ValueError("Element not found.")

class DicomModuleItem:
    def __init__(self, 
                **kwargs):
        self.ModuleName = None
        self.InformationEntity = None
        self.Usage = None
        self.ConditionalStatement = None
        self.Interpretation = None

        if "ModuleName" in kwargs:
            self.ModuleName = kwargs["ModuleName"]
        else:
            raise ValueError("Element not found.")
        if "InformationEntity" in kwargs:
            self.InformationEntity = kwargs["InformationEntity"]
        else:
            raise ValueError("Element not found.")
        if "Usage" in kwargs:
            self.Usage = kwargs["Usage"]
        else:
            raise ValueError("Element not found.")
        if "ConditionalStatement" in kwargs:
            self.ConditionalStatement = kwargs["ConditionalStatement"]
        else:
            raise ValueError("Element not found.")
        if "Interpretation" in kwargs:
            self.Interpretation = kwargs["Interpretation"]
        else:
            raise ValueError("Element not found.")

class DicomAttributeItem:
    def __init__(self, 
                **kwargs):
        self.AttributeName = None
        self.Tag = None
        self.Type = None
        self.Keyword = None
        self.ValueMultiplicity = None
        self.ValueRepresentation = None
        self.ExampleValues = None
        self.Interpretation = None

        if "AttributeName" in kwargs:
            self.AttributeName = kwargs["AttributeName"]
        else:
            raise ValueError("Element not found.")
        if "Tag" in kwargs:
            self.Tag = kwargs["Tag"]
        else:
            raise ValueError("Element not found.")
        if "Type" in kwargs:
            self.Type = kwargs["Type"]
        else:
            raise ValueError("Element not found.")
        if "Keyword" in kwargs:
            self.Keyword = kwargs["Keyword"]
        else:
            raise ValueError("Element not found.")
        if "ValueMultiplicity" in kwargs:
            self.ValueMultiplicity = kwargs["ValueMultiplicity"]
        else:
            raise ValueError("Element not found.")
        if "ValueRepresentation" in kwargs:
            self.ValueRepresentation = kwargs["ValueRepresentation"]
        else:
            raise ValueError("Element not found.")
        if "ExampleValues" in kwargs:
            self.ExampleValues = kwargs["ExampleValues"]
        else:
            raise ValueError("Element not found.")
        if "Interpretation" in kwargs:
            self.Interpretation = kwargs["Interpretation"]
        else:
            raise ValueError("Element not found.")

class DicomStandardTreeNode:
    def __init__(self, data = None):
        self.data = data
        self.children = []

    def addChild(self,child):
        self.children.append(child)

    def jsonLoad(self, jsonFilePath: Union[str, Path, os.PathLike]):
        with open(jsonFilePath, 'r') as f:
            jsonDict = json.load(f)
        #start from CIOD root
        self.dict2Node(jsonDict[list(jsonDict.keys())[0]])
        return self

    def jsonDump(self, jsonFilePath: Union[str, Path, os.PathLike]):
        jsonDict = dict()
        self.node2dict(jsonDict)
        with open(jsonFilePath,'w') as f:
            json.dump(jsonDict, f, indent=4)

    def pickleLoad(self, pickleFilePath: Union[str, Path, os.PathLike]):
        with open(pickleFilePath, 'rb') as f:
            return pickle.load(f)

    def pickleDump(self, pickleFilePath: Union[str, Path, os.PathLike]):
        with open(pickleFilePath, 'wb') as f:
            pickle.dump(self, f)

    def nodeName(self):
        if isinstance(self.data, DicomCIODItem):
            return self.data.CIODName
        elif isinstance(self.data, DicomModuleItem):
            return self.data.ModuleName
        elif isinstance(self.data, DicomAttributeItem):
            return self.data.AttributeName
    
    def keyWord(self):
        if isinstance(self.data, DicomCIODItem):
            return self.data.CIODName.replace(' ','')
        elif isinstance(self.data, DicomModuleItem):
            return self.data.ModuleName.replace(' ','')
        elif isinstance(self.data, DicomAttributeItem):
            return self.data.Keyword.replace(' ','')
        
    def node2dict(self, DicomStandardDict: Dict):
        DicomStandardDict[self.nodeName()] = dict()
        DicomStandardDict[self.nodeName()]['data'] = dict()
        DicomStandardDict[self.nodeName()]['children'] = dict()
        if isinstance(self.data, DicomCIODItem):
            DicomStandardDict[self.nodeName()]['data']['CIODName'] = self.data.CIODName
            DicomStandardDict[self.nodeName()]['data']['data_type'] = type(self.data).__name__
            DicomStandardDict[self.nodeName()]['data']['DicomStandardSyncTime'] = self.data.DicomStandardSyncTime           # for version control
        elif isinstance(self.data, DicomModuleItem):
            DicomStandardDict[self.nodeName()]['data']['ModuleName'] = self.data.ModuleName
            DicomStandardDict[self.nodeName()]['data']['data_type'] = type(self.data).__name__
            DicomStandardDict[self.nodeName()]['data']['InformationEntity'] = self.data.InformationEntity
            DicomStandardDict[self.nodeName()]['data']['Usage'] = self.data.Usage
            DicomStandardDict[self.nodeName()]['data']['ConditionalStatement'] = self.data.ConditionalStatement
        elif isinstance(self.data, DicomAttributeItem):
            DicomStandardDict[self.nodeName()]['data']['AttributeName'] = self.data.AttributeName
            DicomStandardDict[self.nodeName()]['data']['data_type'] = type(self.data).__name__
            DicomStandardDict[self.nodeName()]['data']['Tag'] = self.data.Tag
            DicomStandardDict[self.nodeName()]['data']['Type'] = self.data.Type
            DicomStandardDict[self.nodeName()]['data']['Keyword'] = self.data.Keyword
            DicomStandardDict[self.nodeName()]['data']['ValueMultiplicity'] = self.data.ValueMultiplicity
            DicomStandardDict[self.nodeName()]['data']['ValueRepresentation'] = self.data.ValueRepresentation
            DicomStandardDict[self.nodeName()]['data']['ExampleValues'] = self.data.ExampleValues
        DicomStandardDict[self.nodeName()]['data']['Interpretation'] = self.data.Interpretation
        if self.children:
            for child in self.children:
                child.node2dict(DicomStandardDict[self.nodeName()]['children'])
    
    def dict2Node(self, DicomStandardDict):
        if DicomStandardDict['data']['data_type'] == 'DicomCIODItem':
            self.data = DicomCIODItem(**DicomStandardDict['data'])
        elif  DicomStandardDict['data']['data_type'] == 'DicomModuleItem':
            self.data = DicomModuleItem(**DicomStandardDict['data'])
        elif  DicomStandardDict['data']['data_type'] == 'DicomAttributeItem':
            self.data = DicomAttributeItem(**DicomStandardDict['data'])
        if DicomStandardDict['children']:
            for child in DicomStandardDict['children'].keys():
                self.children.append(DicomStandardTreeNode().dict2Node(DicomStandardDict['children'][child]))
        return self

    def traversePrint(self, indent = ''):
        print(indent + str(self.nodeName()))
        indent = indent + ' '*8
        for child in self.children:
            child.traversePrint(indent)
    
    def filledWithEmptyDict(self, DicomStandardDict):
        if self.children:
            DicomStandardDict[self.keyWord()] = dict()
            for child in self.children:
                child.filledWithEmptyDict(DicomStandardDict[self.keyWord()])
        else:
            DicomStandardDict[self.keyWord()] = ''
    
    def dicomSurvey(self, DicomStandardDict:Dict, dicomData):
        #function for survey dicom data and save to dict
        if self.children:
            DicomStandardDict[self.keyWord()] = dict()
            for child in self.children:
                if isinstance(self.data, DicomCIODItem) or isinstance(self.data, DicomModuleItem):
                    child.dicomSurvey(DicomStandardDict[self.keyWord()], dicomData)
                elif isinstance(self.data, DicomAttributeItem): #tree node module
                    try:
                        child.dicomSurvey(DicomStandardDict[self.keyWord()], dicomData[[int(self.data.Tag.replace('(','').replace(')','')[:4],16), int(self.data.Tag.replace('(','').replace(')','')[5:],16)]].value[0])
                    except:
                        child.filledWithEmptyDict(DicomStandardDict[self.keyWord()])  
        elif not self.children and isinstance(self.data, DicomAttributeItem):
            try:
                DicomStandardDict[self.keyWord()] = dicomData[[int(self.data.Tag.replace('(','').replace(')','')[:4],16), int(self.data.Tag.replace('(','').replace(')','')[5:],16)]].value
            except:
                DicomStandardDict[self.keyWord()] = ''

class UniversalEntityIDTypeEnum(Enum):
    DNS = "DNS"             #An Internet dotted name. Either in ASCII or as integers
    EUI64 = "EUI64"         #An IEEE Extended Unique Identifier
    ISO = "ISO"             #An International Standards Organization Object Identifier
    URI = "URI"             #Uniform Resource Identifier
    UUID = "UUID"           #The DCE Universal Unique Identifier
    X400 = "X400"           #An X.400 MHS identifier
    X500 = "X500"           #An X.500 directory name

class ScanningSquenceEnum(Enum):
    SpinEcho = "SE"
    InversionRecovery = "IR"
    GradientRecalled = "GR"
    EchoPlanar = "EP"
    ResearchMode = "RM"

class SequenceVariantEnum(Enum):
    SegmentedKSpace = "SK"
    MagnetizationTransferContrast = "MTC"
    SteadyState = "SS"
    TimeReversedSteadyState = "TRSS"
    Spoiled = "SP"
    MAGPrepared = "MP"
    OversamplingPhase = "OSP"
    NoSequenceVariant = "NONE"

class ScanOptionsEnum(Enum):
    PhaseEncodeReordering = "PER"
    RespiratoryGating = "RG"
    CardiacGating = "CG"
    PeripheralPulseGating = "PPG"
    FlowCompensation = "FC"
    PartialFourierFrequency = "PFF"
    PartialFourierPhase = "PFP"
    SpatialPresaturation = "SP"
    FatSaturation = "FS"

class MRAcquisitionTypeEnum(Enum):
    _2D = "2D"
    _3D = "3D"

if __name__ == '__main__':
    DicomTagType.Required
    print('dirty trick')