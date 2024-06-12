import os
from PyDicomGrouping.dicom_standard_scrapping.DicomStandardEnums import DicomStandardTreeNode,DicomCIODItem,DicomModuleItem,DicomAttributeItem,DicomTagType
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import re
import pandas as pd
import logging
import inspect
from datetime import datetime
from PyDicomGrouping.dicom_standard_scrapping.tree_node_encryptor import Encryptor
import glob
import pickle
############################
#
# Webscraping code for retrieve Dicomstandard from https://dicom.innolitics.com/ciods
#       
#       By Kaixuan, Zhao in Canton, 2024/04/19
###########################

class DicomStandardTemplate:
    def __init__(self,
                 IODSpecification: str = 'MR Image IOD'):
        #init logPath
        logPath = os.path.join(os.path.dirname(os.path.abspath(__file__)),'logs')
        if not os.path.exists(logPath):
            os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)),'logs'), exist_ok=True)
        surveyLogPath = os.path.join(os.path.dirname(os.path.abspath(__file__)),'logs','Survey_log_'+datetime.now().strftime(r'%Y_%m_%d')+'.log')
        logger = logging.getLogger(inspect.currentframe().f_code.co_name)
        logging.basicConfig(filename=surveyLogPath,
                       level = logging.INFO,
                       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                       datefmt='%m-%d-%Y %H:%M:%S'
                       )
        self.savePath = os.path.join(os.path.dirname(os.path.abspath(__file__)),'DicomStandardTreeNodeCaches')
        self.encryptSavePath = os.path.join(os.path.dirname(os.path.abspath(__file__)),'EncryptDicomStandardTreeNodeCaches')
        self.encrypSOPClassesPath = os.path.join(self.savePath, 'SOPClasses.xz')
        self.encryptValueRepresentationsPath = os.path.join(self.savePath, 'ValueRepresentations.xz')
        self.encryptFMIHeadertreeNodePath = os.path.join(self.savePath, 'FileMetaInformation.xz')
        
        self.SOPClassesPath = os.path.join(self.savePath, 'SOPClasses.xlsx')
        self.ValueRepresentationsPath = os.path.join(self.savePath, 'ValueRepresentations.xlsx')
        self.FMIHeadertreeNodePath = os.path.join(self.savePath, 'FileMetaInformation.pkl')

        if not os.path.exists(self.encrypSOPClassesPath) or \
             not os.path.exists(self.encryptValueRepresentationsPath) or not os.path.exists(self.encryptFMIHeadertreeNodePath):
            self.config()
        self.SOPClasses = pickle.loads(Encryptor().decrypt(Encryptor().key_create(),self.encrypSOPClassesPath))
        self.ValueRepresentations = pickle.loads(Encryptor().decrypt(Encryptor().key_create(),self.encryptValueRepresentationsPath))
        self.FMIHeadertreeNode = pickle.loads(Encryptor().decrypt(Encryptor().key_create(),self.encryptFMIHeadertreeNodePath))
        #load FMI header tree node 

        self.IODSpecificationList = []
        self.SOPClassUIDList = []
        self.IODTreeNode = dict()
        if IODSpecification:
            self.loadByIODSpecification(IODSpecification)
    
    def config(self):
        logger = logging.getLogger(inspect.currentframe().f_code.co_name)
        if not os.path.exists(self.savePath):
            #make sure dicomstandardTemplate savepath exist
            os.makedirs(self.savePath, exist_ok = True)
        if not os.path.isfile(self.SOPClassesPath):
            logger.warning(f'Standard SOP Classes Cahce not found, we re-run web scraping code to extract. ')
            self.extractStandardSOPClasses()
        if not os.path.isfile(self.FMIHeadertreeNodePath):
            logger.warning(f'File Meta Header Cahce not found, we re-run web scraping code to extract. ')
            self.extractDicomMetaFileInformation()
        if not os.path.isfile(self.ValueRepresentationsPath):
            logger.warning(f'Value Representation Cahce not found, we re-run web scraping code to extract. ')
            self.extractValueRepresentations()
        #encrypt all
        self.encrypt()
    
    def encrypt(self):
        encryptor = Encryptor()
        self.encryptKey = encryptor.key_create()
        #encrypt all treeNodeCache
        treeNodeCaches = glob.glob(os.path.join(self.savePath,"*.pkl"))
        for treeNodeCache in treeNodeCaches:
            encryptor.file_encrypt(self.encryptKey, 
                                   treeNodeCache, 
                                   os.path.join(os.path.dirname(treeNodeCache), os.path.basename(treeNodeCache).split(".")[0] + ".xz"))
        #encrypt all xlsx
        SOPClassesPklPath = os.path.join(os.path.dirname(self.SOPClassesPath), os.path.basename(self.SOPClassesPath).split('.')[0] + ".pkl")
        pd.read_excel(self.SOPClassesPath).to_pickle(SOPClassesPklPath)
        encryptor.file_encrypt(self.encryptKey,
                                SOPClassesPklPath,
                                  self.encrypSOPClassesPath)
        ValueRepresentationsPklPath = os.path.join(os.path.dirname(self.ValueRepresentationsPath), os.path.basename(self.ValueRepresentationsPath).split('.')[0] + ".pkl")
        pd.read_excel(self.ValueRepresentationsPath).to_pickle(ValueRepresentationsPklPath)
        encryptor.file_encrypt(self.encryptKey,
                                ValueRepresentationsPklPath,
                                  self.encryptValueRepresentationsPath)
        encryptor.file_encrypt(self.encryptKey, self.FMIHeadertreeNodePath, self.encryptFMIHeadertreeNodePath)
        print("dirty trick")

    def getIODTreeNodeByIODSpecification(self, IODSpecification):
        return self.IODTreeNode[IODSpecification]

    def getIODTreeNodeByMediaStorageSOPClassUID(self, MediaStorageSOPClassUID):
        return self.IODTreeNode[self.getIODSpecificationByMediaStorageSOPClassUID(MediaStorageSOPClassUID)]
    
    def getFMIHeaderTreeNode(self):
        return self.FMIHeadertreeNode

    def getIODSpecificationByMediaStorageSOPClassUID(self, MediaStorageSOPClassUID):
        return self.SOPClasses.loc[self.SOPClasses["SOP Class UID"] == MediaStorageSOPClassUID]["IOD Specification (defined in PS3.3)"].values[0]

    def loadBySOPClassUID(self, MediaStorageSOPClassUID:str):
        logger = logging.getLogger(inspect.currentframe().f_code.co_name)
        IODSpecification = self.SOPClasses.loc[self.SOPClasses["SOP Class UID"] == MediaStorageSOPClassUID]["IOD Specification (defined in PS3.3)"].values[0]
        if IODSpecification and IODSpecification not in self.IODSpecificationList:
            IODSpecificationSavePath = os.path.join(self.savePath, IODSpecification.replace(" ","")[:-3] + '.xz')
            if os.path.exists(IODSpecificationSavePath): #to remove white space and surfix of IOD
                #add IOD speficiation
                self.IODTreeNode[IODSpecification] = pickle.loads(Encryptor().decrypt(Encryptor().key_create(),IODSpecificationSavePath))
                self.IODSpecificationList.append(IODSpecification)
                self.SOPClassUIDList.append(MediaStorageSOPClassUID)
            else:
                logger.info(f"IOD Specification {IODSpecification} not found in cache folder, re-extraction excuted.")
                self.extractDicomStandardCIODs(CIODSpecification=IODSpecification[:-3]) #in DicomStandardBrowser, there is no IOD surfix
                self.loadBySOPClassUID(MediaStorageSOPClassUID)

    def loadByIODSpecification(self, IODSpecification:str):
        logger = logging.getLogger(inspect.currentframe().f_code.co_name)
        MediaStorageSOPClassUID = self.SOPClasses.loc[self.SOPClasses["IOD Specification (defined in PS3.3)"] == IODSpecification]["SOP Class UID"].values[0]
        if MediaStorageSOPClassUID and MediaStorageSOPClassUID not in self.SOPClassUIDList:
            IODSpecificationSavePath = os.path.join(self.savePath, IODSpecification.replace(" ","")[:-3] + '.xz')
            if os.path.exists(IODSpecificationSavePath): #to remove white space and surfix of IOD
                #add IOD speficiation
                # self.IODTreeNode[IODSpecification] = DicomStandardTreeNode().pickleLoad(IODSpecificationSavePath)
                self.IODTreeNode[IODSpecification] = pickle.loads(Encryptor().decrypt(Encryptor().key_create(),IODSpecificationSavePath))
                self.IODSpecificationList.append(IODSpecification)
                self.SOPClassUIDList.append(MediaStorageSOPClassUID)
            else:
                logger.info(f"IOD Specification {IODSpecification} not found in cache folder, re-extraction excuted.")
                self.extractDicomStandardCIODs(CIODSpecification=IODSpecification[:-3]) #in DicomStandardBrowser, there is no IOD surfix
                self.loadByIODSpecification(IODSpecification)

    def extractValueRepresentations(self, NEMADocURL = r'https://dicom.nema.org/medical/dicom/current/output/chtml/part05/sect_6.2.html'):
        logger = logging.getLogger(inspect.currentframe().f_code.co_name)
        logger.info(f'Start extracting Dicom Meta File Information from {NEMADocURL}')
        driver = webdriver.Chrome()
        driver.get(NEMADocURL)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "section"))
            )
            driver_tables = driver.find_element(By.CLASS_NAME,"section").find_elements(By.CLASS_NAME,"table")
            for driver_table in driver_tables:
                try:
                    driver_table.find_element(By.ID,"table_6.2-1")
                    theads = driver_table.find_element(By.TAG_NAME,"thead").find_elements(By.TAG_NAME,"th")
                    thead_list = []
                    for thead in theads:
                        thead_list.append(thead.text)
                    trs = driver_table.find_element(By.TAG_NAME,"tbody").find_elements(By.TAG_NAME,"tr")
                    self.ValueRepresentationDict = []
                    for tr in trs:
                        tds = tr.find_elements(By.TAG_NAME,"td")
                        td_list = []
                        for idx,td in enumerate(tds):
                            if idx == 0:
                                parag_elements = td.find_elements(By.TAG_NAME,'p')
                                if len(parag_elements) == 2:
                                    td_list.append(parag_elements[1].text + ' (' + parag_elements[0].text + ')')
                                elif len(parag_elements) == 1:
                                    td_list.append(td.text)
                            else:
                                td_list.append(td.text)
                        self.ValueRepresentationDict.append(td_list)
                    #save to excel
                    df = pd.DataFrame(self.ValueRepresentationDict)
                    df.columns = thead_list
                    df.to_excel(self.ValueRepresentationsPath)
                except NoSuchElementException:
                    continue
        finally:
            logger.info(f'Extracting Value Representation Dict from {NEMADocURL} finished!')

    def extractDicomMetaFileInformation(self, NEMADocURL = r'https://dicom.nema.org/medical/dicom/current/output/html/part10.html'):
        logger = logging.getLogger(inspect.currentframe().f_code.co_name)
        logger.info(f'Start extracting Dicom Meta File Information from {NEMADocURL}')
        driver = webdriver.Chrome()
        driver.get(NEMADocURL)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "book"))
            )

            driver_chapters = driver.find_elements(By.CLASS_NAME,"chapter")
            for driver_chapter in driver_chapters:
                try:
                    #find by ID
                    driver_chapter.find_element(By.ID, "table_7.1-1")
                    #init CIOD class
                    dicomCIODItemDict = dict()
                    dicomCIODItemDict['CIODName'] = "File Meta Information"
                    dicomCIODItemDict['Interpretation'] = driver_chapter.find_element(By.CLASS_NAME,'section').find_element(By.TAG_NAME,"p").text
                    dicomCIODItemDict['DicomStandardSyncTime'] = driver.find_element(By.CLASS_NAME,'titlepage').find_element(By.CLASS_NAME,'subtitle').text
                    dicomStandardTreeNode = DicomStandardTreeNode(DicomCIODItem(**dicomCIODItemDict))
                    
                    driver_chapter.find_element(By.CLASS_NAME,'section').find_element(By.CLASS_NAME,"table").find_element(By.ID, "table_7.1-1")
                    driver_table = driver_chapter.find_element(By.CLASS_NAME,'section').find_element(By.CLASS_NAME,"table")
                    theads = driver_table.find_element(By.TAG_NAME,"thead").find_elements(By.TAG_NAME,"th")
                    thead_list = []
                    for thead in theads:
                        thead_list.append(thead.text)
                    trs = driver_table.find_element(By.TAG_NAME,"tbody").find_elements(By.TAG_NAME,"tr")
                    for tr in trs:
                        tds = tr.find_elements(By.TAG_NAME,"td")
                        dicomAttributeDict = dict()
                        for head_name, td in zip(thead_list, tds):
                            if head_name == "Attribute Name":
                                dicomAttributeDict[head_name.replace(' ','')] = td.text
                                dicomAttributeDict['Keyword'] = td.text.replace(' ','')
                            elif head_name == "Attribute Description":
                                dicomAttributeDict["Interpretation"] = td.text
                            elif head_name == 'Type':
                                dicomAttributeDict[head_name] = [item.description for _,item in DicomTagType.__members__.items()][[item.abbreviation for _,item in DicomTagType.__members__.items()].index(td.text)]
                            else:
                                dicomAttributeDict[head_name] = td.text
                        dicomAttributeDict["AttributeName"] = dicomAttributeDict["Tag"] + ' ' + dicomAttributeDict["AttributeName"]
                        dicomAttributeDict['ValueMultiplicity'] = None
                        dicomAttributeDict['ValueRepresentation'] = None
                        dicomAttributeDict['ExampleValues'] = None
                        dicomStandardTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**dicomAttributeDict)))
                    dicomStandardTreeNode.pickleDump(os.path.join(self.savePath, dicomStandardTreeNode.keyWord() + '.pkl'))
                    dicomStandardTreeNode.jsonDump(os.path.join(self.savePath, dicomStandardTreeNode.keyWord() + '.json'))
                except NoSuchElementException:
                    continue
        finally:
            logger.info(f'Extracting Dicom Meta File Information from {NEMADocURL} finished!')

    def extractStandardSOPClasses(self,NEMADocURL = r'https://dicom.nema.org/medical/dicom/current/output/html/part04.html#sect_B.5'):
        logger = logging.getLogger(inspect.currentframe().f_code.co_name)
        logger.info(f'Start extracting standard SOP classes from {NEMADocURL}')
        driver = webdriver.Chrome()
        driver.get(NEMADocURL)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "book"))
            )
            driver_tables = driver.find_element(By.CLASS_NAME,"book").find_elements(By.CLASS_NAME,"table")
            for driver_table in driver_tables:
                try:
                    driver_table.find_element(By.ID,"table_B.5-1")
                    theads = driver_table.find_element(By.TAG_NAME,"thead").find_elements(By.TAG_NAME,"th")
                    thead_list = []
                    for thead in theads:
                        thead_list.append(thead.text)
                    trs = driver_table.find_element(By.TAG_NAME,"tbody").find_elements(By.TAG_NAME,"tr")
                    self.StandardSOPClassDict = []
                    for tr in trs:
                        tds = tr.find_elements(By.TAG_NAME,"td")
                        td_list = []
                        for idx,td in enumerate(tds):
                            td_list.append(td.text)
                        self.StandardSOPClassDict.append(td_list)
                    #save to excel
                    df = pd.DataFrame(self.StandardSOPClassDict)
                    df.columns = thead_list
                    df.to_excel(self.SOPClassesPath)
                except NoSuchElementException:
                    continue
        finally:
            logger.info(f'Extracting standard SOP classes from {NEMADocURL} finished!')

    def extractDicomStandardCIODs(self, CIODSpecification: str = 'all', DicomStandardBrowserURL: str = r'https://dicom.innolitics.com'):
        logger = logging.getLogger(inspect.currentframe().f_code.co_name)
        logger.info(f'Start extracting Dicom standard CIOD {CIODSpecification} classes from {DicomStandardBrowserURL}')
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(DicomStandardBrowserURL)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "pane-container"))
            )
            #locate all table tree ciods
            driver_trs = driver.find_element(By.CLASS_NAME,"pane-primary").find_element(By.CLASS_NAME,"tree-table").find_elements(By.TAG_NAME,'tr')
            print(f'{len(driver_trs)} CIOD found. ')
            CIODSpecifications = [tr_item.find_element(By.CLASS_NAME,'row-name').text for tr_item in driver.find_element(By.CLASS_NAME,"pane-primary").find_element(By.CLASS_NAME,"tree-table").find_elements(By.TAG_NAME,'tr')]
            if CIODSpecification != 'all':
                if CIODSpecification not in CIODSpecifications:
                    raise ValueError(f'CIODSpecification {CIODSpecification} not found in url:{DicomStandardBrowserURL}')
                else:
                    indexes = [CIODSpecifications.index(CIODSpecification)]
            else:
                indexes = range(len(driver_trs))

            for idx in indexes:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "pane-container"))
                    )
                #simulate click
                driver.find_element(By.CLASS_NAME,"pane-primary").find_element(By.CLASS_NAME,"tree-table").find_elements(By.TAG_NAME,'tr')[idx].find_element(By.CLASS_NAME,'row-name').click()
                #create CIOD Item
                dicomCIODItemDict = dict()
                dicomCIODItemDict['CIODName'] = driver.find_element(By.CLASS_NAME,"pane-primary").find_element(By.CLASS_NAME,"tree-table").find_elements(By.TAG_NAME,'tr')[idx].find_element(By.CLASS_NAME,'row-name').text
                dicomCIODItemDict['Interpretation'] = driver.find_element(By.CLASS_NAME,'detail-pane').find_element(By.TAG_NAME,'p').text
                #find DicomStandard Sync Time
                footnote_text = driver.find_element(By.CLASS_NAME,"pane-primary").find_element(By.CLASS_NAME,"m-x-1").text
                pattern = re.compile(r"\w{1,2} \w+ \d{4}")
                dicomCIODItemDict['DicomStandardSyncTime'] = pattern.findall(footnote_text)[0]
                dicomStandardTreeNode = DicomStandardTreeNode(DicomCIODItem(**dicomCIODItemDict))
                # sub-module existed
                if len(driver.find_element(By.CLASS_NAME,"pane-primary").find_element(By.CLASS_NAME,"tree-table").find_elements(By.TAG_NAME,'tr')[idx].find_elements(By.CLASS_NAME,'arrow')) > 0:
                    #open sub-module
                    driver.find_element(By.CLASS_NAME,"pane-primary").find_element(By.CLASS_NAME,"tree-table").find_elements(By.TAG_NAME,'tr')[idx].find_element(By.CLASS_NAME,'arrow').click()
                    #process modules
                    self.extractDicomStandardModules(driver,
                                                    dicomStandardTreeNode,
                                                    startIdx = idx + 1,
                                                    stopIdx= idx + 1 + len(driver.find_element(By.CLASS_NAME,"tree-table").find_elements(By.TAG_NAME,'tr')) - len(driver_trs))
                    #close sub-module
                    driver.find_element(By.CLASS_NAME,"tree-table").find_elements(By.CLASS_NAME, "arrow.open")[-1].click()
                #save current treeNone
                #pickle Dump
                dicomStandardTreeNode.pickleDump(os.path.join(self.savePath, dicomStandardTreeNode.keyWord() + '.pkl'))
                #Json Dump
                dicomStandardTreeNode.jsonDump(os.path.join(self.savePath, dicomStandardTreeNode.keyWord() + '.json'))
        finally:
            logger.info(f'Extracting Dicom standard CIOD {CIODSpecification} finished!')

    def extractDicomStandardModules(self, driver, dicomStandardTreeNode, startIdx, stopIdx):
        for idx in range(startIdx, stopIdx):
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "pane-container"))
            )
            driver.find_element(By.CLASS_NAME, "pane-primary").find_element(By.CLASS_NAME,"tree-table").find_elements(By.TAG_NAME,'tr')[idx].find_element(By.CLASS_NAME,'row-name').click()
            #create Module Item
            dicomModuleDict = dict()
            dicomModuleDict['ModuleName'] = driver.find_element(By.CLASS_NAME, "pane-primary").find_element(By.CLASS_NAME,"tree-table").find_elements(By.TAG_NAME,'tr')[idx].find_element(By.CLASS_NAME,'row-name').text
            pane_secondary = driver.find_element(By.CLASS_NAME, "pane-secondary").find_element(By.CLASS_NAME, "node-details-table")
            tableItems = pane_secondary.find_elements(By.TAG_NAME,'tr')
            for tableItem in tableItems:
                dicomModuleDict[tableItem.find_element(By.TAG_NAME, 'th').text.replace(' ','')] = tableItem.find_element(By.TAG_NAME, 'td').text
            dicomModuleDict['Interpretation'] = driver.find_element(By.CLASS_NAME,'detail-pane').find_element(By.TAG_NAME,'p').text
            if 'ConditionalStatement' not in dicomModuleDict.keys():
                dicomModuleDict['ConditionalStatement'] = ''
            #append tree node
            dicomStandardTreeNode.addChild(DicomStandardTreeNode(DicomModuleItem(**dicomModuleDict)))
            if len(driver.find_element(By.CLASS_NAME, "pane-primary").find_element(By.CLASS_NAME,"tree-table").find_elements(By.TAG_NAME,'tr')[idx].find_elements(By.CLASS_NAME,'arrow')) > 0:
                trs_prev = len(driver.find_element(By.CLASS_NAME, "pane-primary").find_element(By.CLASS_NAME,"tree-table").find_elements(By.TAG_NAME,'tr'))
                #open sub-module
                driver.find_element(By.CLASS_NAME, "pane-primary").find_element(By.CLASS_NAME,"tree-table").find_elements(By.TAG_NAME,'tr')[idx].find_element(By.CLASS_NAME,'arrow').click()
                #process modules
                self.extractDicomStandardAttributes(driver,
                                                dicomStandardTreeNode.children[-1],
                                                startIdx = idx + 1,
                                                stopIdx= idx + 1 + len(driver.find_element(By.CLASS_NAME,"tree-table").find_elements(By.TAG_NAME,'tr')) - trs_prev)
                #close sub-module
                driver.find_element(By.CLASS_NAME,"tree-table").find_elements(By.CLASS_NAME, "arrow.open")[-1].click()

    def extractDicomStandardAttributes(self, driver, dicomStandardTreeNode, startIdx, stopIdx):
        for idx in range(startIdx, stopIdx):
            driver.find_element(By.CLASS_NAME, "pane-primary").find_element(By.CLASS_NAME,"tree-table").find_elements(By.TAG_NAME,'tr')[idx].find_element(By.CLASS_NAME,'row-name').click()
            #create Module Item
            dicomAttributeDict = dict()
            dicomAttributeDict['AttributeName'] = driver.find_element(By.CLASS_NAME, "pane-primary").find_element(By.CLASS_NAME,"tree-table").find_elements(By.TAG_NAME,'tr')[idx].find_element(By.CLASS_NAME,'row-name').text
            pane_secondary = driver.find_element(By.CLASS_NAME, "pane-secondary").find_element(By.CLASS_NAME, "node-details-table")
            tableItems = pane_secondary.find_elements(By.TAG_NAME,'tr')
            for tableItem in tableItems:
                dicomAttributeDict[tableItem.find_element(By.TAG_NAME, 'th').text.replace(' ','')] = tableItem.find_element(By.TAG_NAME, 'td').text
            dicomAttributeDict['Interpretation'] = driver.find_element(By.CLASS_NAME,'detail-pane').find_element(By.TAG_NAME,'p').text
            if 'ExampleValues' not in dicomAttributeDict.keys():
                dicomAttributeDict['ExampleValues'] = ''
            #append tree node
            dicomStandardTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**dicomAttributeDict)))
            if len(driver.find_element(By.CLASS_NAME, "pane-primary").find_element(By.CLASS_NAME,"tree-table").find_elements(By.TAG_NAME,'tr')[idx].find_elements(By.CLASS_NAME,'arrow')) > 0:
                trs_prev = len(driver.find_element(By.CLASS_NAME, "pane-primary").find_element(By.CLASS_NAME,"tree-table").find_elements(By.TAG_NAME,'tr'))
                #open sub-module
                driver.find_element(By.CLASS_NAME, "pane-primary").find_element(By.CLASS_NAME,"tree-table").find_elements(By.TAG_NAME,'tr')[idx].find_element(By.CLASS_NAME,'arrow').click()
                #process modules
                self.extractDicomStandardAttributes(driver,
                                                dicomStandardTreeNode.children[-1],
                                                startIdx = idx + 1,
                                                stopIdx= idx + 1 + len(driver.find_element(By.CLASS_NAME,"tree-table").find_elements(By.TAG_NAME,'tr')) - trs_prev)
                #close sub-module
                driver.find_element(By.CLASS_NAME,"tree-table").find_elements(By.CLASS_NAME, "arrow.open")[-1].click()

if __name__ == '__main__':
    # MRITreeNode = DicomStandardTemplate().get('1.2.840.10008.5.1.4.1.1.4')
    # DicomStandardTemplate().extractStandardSOPClasses()
    # DicomStandardTemplate().extractDicomStandardCIODs()
    # DicomStandardTemplate().extractValueRepresentations()
    treeNode = DicomStandardTreeNode(1)
    mydict = dict()
    import json
    with open('test.json','w') as f:
        json.dump(mydict,f, indent=4)
    print('dirty trick')

