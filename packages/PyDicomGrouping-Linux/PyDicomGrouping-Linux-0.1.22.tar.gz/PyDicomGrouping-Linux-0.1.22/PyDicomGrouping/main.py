import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),"dicom_standard_scrapping"))
import pydicom.multival
import pydicom.valuerep
import pandas as pd
import numpy as np
import pydicom
from pydicom.pixel_data_handlers import apply_rescale
from pathlib import Path
from typing import Union
from typing import Optional
from datetime import datetime
import logging
from .utils import *
import inspect
from PyDicomGrouping.dicom_standard_scrapping.webscraping import DicomStandardTemplate
from PyDicomGrouping.dicom_standard_scrapping.DicomStandardEnums import DicomStandardTreeNode, DicomModuleItem, DicomAttributeItem, IODModuleUsage, DicomTagType
from alive_progress import alive_bar,alive_it
from typing import List

#test
def dicom_grouping(project_path: Union[str, Path,os.PathLike],
                     data_root_path: Union[str, Path, os.PathLike],
                     save_path: Union[str, Path, os.PathLike],
                     survey_excel_path: Union[str, Path, os.PathLike] = None,
                     survey_log_path: Union[str, Path, os.PathLike] = None,
                     remove_processing_cache: bool = False,           # break-point
                     remove_dataloader_cache: bool = False,
                     IODFilters: List = None,
                     save_raw_dicoms: bool = True):
    # PyDicomGroupingEngine
    # data_root_path:
    # dataformat requirement:
    #   - PatientIDs
    #       - MRIScans
    #           - Sequences [i.e. seperated or mixed]
    #
    #
    # if survey_excel_path is not specified, we use the default instead.
    output_log_dir = os.path.join(project_path, 'logs')
    output_cache_dir = os.path.join(project_path, 'CacheFiles')
    survey_excel_dir = os.path.join(project_path, 'Survey_excels')
    studies_cache_path = os.path.join(output_cache_dir,'Caches_' + os.path.basename(data_root_path) + '.pkl')
    dataloader_cachefile_path = os.path.join(output_cache_dir, 'dataloader_cache_' + os.path.basename(data_root_path) + '.pkl')
    if not os.path.exists(output_log_dir):
        os.makedirs(output_log_dir)
    if not os.path.exists(output_cache_dir):
        os.makedirs(output_cache_dir)
    if not os.path.exists(survey_excel_dir):
        os.makedirs(survey_excel_dir)
    if not survey_excel_path:
        survey_excel_path = os.path.join(survey_excel_dir,'Survey_Excel_' + datetime.now().strftime(r'%Y_%m_%d') + '_' +os.path.basename(data_root_path)+'.xlsx')
        survey_json_path = os.path.join(survey_excel_dir,'Survey_Excel_' + datetime.now().strftime(r'%Y_%m_%d') + '_' +os.path.basename(data_root_path)+'.json')
    # if survey_log_path is not specified, we use the default instead
    if not survey_log_path:
        survey_log_path = os.path.join(output_log_dir,'Survey_log_'+datetime.now().strftime(r'%Y_%m_%d') + '_' +os.path.basename(data_root_path)+'.log')
    if remove_processing_cache:
        if os.path.isfile(survey_log_path):
            os.remove(survey_log_path)
        if os.path.isfile(survey_excel_path):
            os.remove(survey_excel_path)
            os.remove(survey_json_path)
        if os.path.isfile(studies_cache_path):
            os.remove(studies_cache_path)
    if remove_dataloader_cache:
        if os.path.isfile(dataloader_cachefile_path):
            os.remove(dataloader_cachefile_path)
    logger = logging.getLogger(inspect.currentframe().f_code.co_name)
    logging.basicConfig(filename=survey_log_path,
                       level = logging.INFO,
                       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                       datefmt='%m-%d-%Y %H:%M:%S'
                       )
    logging.root.setLevel(logging.NOTSET)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    #reload studies_cache_path
    if not os.path.exists(studies_cache_path):
        studies_cache = {}
        os.makedirs(os.path.dirname(studies_cache_path),exist_ok=True)
        pickle_dump(studies_cache,studies_cache_path)
    else:
        studies_cache = pickle_load(studies_cache_path)
    #init dicom template caches
    dicomStandardTemplateCache = DicomStandardTemplate()
    if not IODFilters:
        IODFilters = ["MR Image IOD", "CT Image IOD", "Enhanced MR Image IOD"] # default for MR
    # In case of mixed study for different patients or different study from same patienr, coarse group is necessary
    #-----------------------------
    #Exec PyDicomCoarseGrouping
    #-----------------------------
    studies = dict()
    studies["buffer"] = [] #add buffer
    if not os.path.exists(dataloader_cachefile_path):
        dicoms = []
        for home, dirs, files in os.walk(data_root_path):
            for filename in files:
                dicoms.append(os.path.join(home,filename))
        with alive_bar(len(dicoms)) as bar:
            for idx, dicom in enumerate(dicoms):
                PyDicomCoarseGrouping(dicom_path = dicom,
                                    studies = studies)
                bar()
        pickle_dump(studies, dataloader_cachefile_path)
    else:
        #data complete check
        studies = pickle_load(dataloader_cachefile_path)
    studies.pop("buffer") #remove buffer
    # ignore processed dataset
    studies = {key:val for key,val in studies.items() if key not in studies_cache.keys()}
    #empty studies check
    studies = {key:val for key,val in studies.items() if val}
    logger.info(f"{len(list(studies.keys()))} studies were found, {len(studies)} studies would be processed.")    
    #Main
    for studyInsUID, dicoms in sorted(studies.items()):
        logger.info(f'**************Processing study data-set with StudyInstanseUID:{studyInsUID}***************************')
        logger.info(f'//=============================Start==================================')
        #print first dicom image
        logger.info(f"First dicom path: {dicoms[0]}.")
        study_cache = dict()
        raw_study_dataset = {}    #patient_dataset for one patient
        proc_study_dataset = {}
        raw_dicoms = {}
        logger.info(f"***************{len(dicoms)} dicom files are found, start loading dicoms**********************")
        dicoms_bar = alive_it(dicoms)
        for dicom in dicoms_bar:
            dicoms_bar.text("Processing dicom: " + os.path.basename(dicom))
            if not PyDicomExtractingEngine_main(dicom_path = dicom,
                                                raw_dicoms = raw_dicoms,
                                                study_dataset = raw_study_dataset,
                                                dicomStandardTemplateCache = dicomStandardTemplateCache,
                                                IODFilters = IODFilters):
                logger.warning(f"Error in de-coding dicom {dicom}.")
        raw_dicoms = dict(sorted(raw_dicoms.items(), key = lambda x:x[0]))
        logger.info("***************loading dicoms finished**********************")
        # raw_study_dataset = pickle_load("pydicom_test.pkl")
        # raw_dicoms = pickle_load("raw_dicoms.pkl")
        logger.info(f"***************{len(raw_study_dataset.keys())} dicom series are found, start stacking dicoms series**********************")
        PyDicomGroupingEngine_main(raw_study_dataset = raw_study_dataset,
                                    proc_study_dataset = proc_study_dataset)
        logger.info(f"***************dicom series stacking finished**********************")
        # pickle_dump(raw_study_dataset, "pydicom_test.pkl")
        # pickle_dump(raw_dicoms, "raw_dicoms.pkl")
        # pickle_dump(proc_study_dataset, "proc_study_dataset")
        #after patient-MRI scan data processing complete, start data storage engine
        # #TODO: both raw dicom and splited nifti should be stored.
        PyDicomGroupingSummary_main(proc_study_dataset=proc_study_dataset,
                                    study_cache = study_cache)
        logger.info(f"***************{len(proc_study_dataset.keys())} completed dicom series are found, start saving dicoms series**********************")
        PyDicomStorageEngine_main(proc_study_dataset=proc_study_dataset,
                                  raw_dicoms = raw_dicoms,
                                  save_path = os.path.join(save_path, studyInsUID),
                                  save_raw_dicoms = save_raw_dicoms)
        logger.info(f"***************completed dicom series saving finished**********************")
        study_cache["study_save_path"] = save_path
        #update studies_cache for every MRIstudies
        studies_cache = pickle_load(studies_cache_path)
        if studyInsUID not in studies_cache.keys():
            studies_cache[studyInsUID] = study_cache
        else:
            logger.warning(f"Duplicated StudyInsUID was found in studies_cache, and the original study will be updated.")
            studies_cache[studyInsUID].update(study_cache)
        pickle_dump(studies_cache,studies_cache_path)

        aborted_sequences = [key for key in raw_study_dataset.keys() if key not in proc_study_dataset.keys()]
        logger.info(f'Processing finished in Study {studyInsUID}.')
        logger.info(f'//*****************************Summary********************************')
        logger.info(f'{len(raw_study_dataset.keys())} sequences are extracted and {len(aborted_sequences)} sequences are aborted.')
        for sequence in aborted_sequences:
            logger.warning(f'{sequence} is aborted.')
        logger.info(f'//=============================End====================================')
    #remove empty studies_caches
    studies_cache = {key:val for key,val in sorted(studies_cache.items()) if "study_pars" in val.keys()}
    #save survey dict to excel by pd
    pd.DataFrame.from_dict([studies_cache[key]["study_pars"] for key in studies_cache.keys()]).to_excel(survey_excel_path)
    json_dump(studies_cache, survey_json_path)

    print('dirty trick')

def PyDicomCoarseGrouping(dicom_path: Union[str, Path, os.PathLike],
                          studies: dict):
    #function used for coarsely grouping dicom files according to studyUID
    logger = logging.getLogger(inspect.currentframe().f_code.co_name)
    try:
        dcmdata = pydicom.dcmread(dicom_path, specific_tags = [[0x0020,0x000D],[0x0008,0x0018]], force=True)
        StudyInstanceUID = dcmdata[0x0020,0x000D].value # this tag is consistant in all CIODs
        SOPInstanceUID = dcmdata[0x0008,0x0018].value # this tag is consistant in all CIODs
        if StudyInstanceUID not in studies.keys():
            studies[StudyInstanceUID] = []
            studies[StudyInstanceUID].append(dicom_path)
            studies["buffer"].append(SOPInstanceUID)
        elif StudyInstanceUID in studies.keys() and SOPInstanceUID not in studies["buffer"]:
            studies[StudyInstanceUID].append(dicom_path)
            studies["buffer"].append(SOPInstanceUID)
        return True
    except Exception as exception:
        logger.error(exception)
        return False
    
def PyDicomSurvey(dcmdata,
                  dicomStandardDict: dict,
                  dicomStandardTemplateCache: DicomStandardTemplate = None,
                  IODFilters: List = None):
    #function used for survey dcmdata according to dicomStandardTemplate
    logger = logging.getLogger(inspect.currentframe().f_code.co_name)
    try:
        if not dicomStandardTemplateCache:
            dicomStandardTemplateCache = DicomStandardTemplate()
            logger.info(f"Initialize DicomStandardTemplate.")
        FMIHeader_dict = dict()
        dicomStandardTemplateCache.getFMIHeaderTreeNode().dicomSurvey(FMIHeader_dict,dcmdata.file_meta)
        SOPClassUID = FMIHeader_dict['FileMetaInformation']['MediaStorageSOPClassUID']
        if (IODFilters and dicomStandardTemplateCache.getIODSpecificationByMediaStorageSOPClassUID(SOPClassUID) not in IODFilters):
            raise ValueError(f"SOPClass: {dicomStandardTemplateCache.getIODSpecificationByMediaStorageSOPClassUID(SOPClassUID)} not meet the criteria of IODFilters: {IODFilters}.")
        #check if DicomStandard is alreadly load in caches
        if SOPClassUID not in dicomStandardTemplateCache.SOPClassUIDList:
            dicomStandardTemplateCache.loadBySOPClassUID(SOPClassUID)
        #extract dicom pars
        dicomStandardTemplateCache.getIODTreeNodeByMediaStorageSOPClassUID(SOPClassUID).dicomSurvey(dicomStandardDict, dcmdata)
        return True
    except Exception as exception:
        logger.error(exception)
        return False

def PyDicomExtractingEngine_main(dicom_path: Union[str, Path, os.PathLike],
                                 raw_dicoms: dict,
                                 study_dataset: dict,
                                 dicomStandardTemplateCache: DicomStandardTemplate,
                                 IODFilters: List = None):
    # dicoms-in -> dictionary out
    # for sequence_storage_mode == seperate, the num_slice is inferenced from dicom files number
    #
    # if patientID or RISID is not given, use the information from dicom, otherwise, use the given one
    # print('processing dicom files:' + os.path.basename(dicom_path))
    try:
        logger = logging.getLogger(inspect.currentframe().f_code.co_name)
        dicomStandardDict = dict()
        #dicom filetype check
        dcmdata = pydicom.dcmread(dicom_path)
        # check if pixel array is existed.
        pixel_array = dcmdata.pixel_array
        #Mapping dcmdata Tags to standard dicom tag dict
        if not PyDicomSurvey(dcmdata = dcmdata,
                               dicomStandardDict = dicomStandardDict,
                               dicomStandardTemplateCache = dicomStandardTemplateCache,
                               IODFilters = IODFilters):
            #if dicom file is not decoded correctly, skip
            raise ValueError(f"Error occured in decoding {dicom_path} by PyDicomSurvey")
        CIODKeyWord = list(dicomStandardDict.keys())[0]
        #remove pixel data
        if dicomStandardDict[CIODKeyWord]["ImagePixel"]["PixelData"] != "":
            dicomStandardDict[CIODKeyWord]["ImagePixel"]["PixelData"] = ""
        manufacturer = None
        protocol = None
        if CIODKeyWord == 'MRImage':
            #In CIOD of MRImage, we make manufacturer check first
            manufacturer = dicomStandardDict[CIODKeyWord]['GeneralEquipment']['Manufacturer']
            if manufacturer and 'GE' not in manufacturer and 'Philips' not in manufacturer and 'UIH' not in manufacturer and 'SIEMENS' not in manufacturer:
                raise ValueError(f'un-supported manufacturer {manufacturer}, dicom file is skipped.')
            try:
                #get protocol, TODO: using GUI to discriminate sequences
                series_date = dicomStandardDict[CIODKeyWord]["GeneralSeries"]["SeriesDate"]
                series_time = dicomStandardDict[CIODKeyWord]["GeneralSeries"]["SeriesTime"]
                series_time_str = datetime.strptime(series_date+series_time[:6],r'%Y%m%d%H%M%S').strftime(r'%Y_%m_%d_%H_%M_%S')
                series_desc = dicomStandardDict[CIODKeyWord]["GeneralSeries"]["SeriesDescription"]
                if series_desc != '':
                    protocol = series_time_str + '_' + series_desc.replace(' ','').replace('(','_').replace(')','').replace('\\','_').replace('/','_').replace(':','_').replace('<','_').replace('>','_').replace('^','_').replace('-','_').replace('*','_').replace('?','').replace("'",'')
                else:
                    #if series descriptuon not existed, use the seriesInsUID instead
                    protocol = dicomStandardDict[CIODKeyWord]["GeneralSeries"]["SeriesInstanceUID"]
            except:
                logger.warning(f"Extracting series time error, we use SeriesInstanceUID instead.")
                protocol = dicomStandardDict[CIODKeyWord]["GeneralSeries"]["SeriesInstanceUID"]
        elif CIODKeyWord == 'CTImage':
            #In CIOD of CTImage, we make manufacturer check first
            manufacturer = dicomStandardDict[CIODKeyWord]['GeneralEquipment']['Manufacturer']
            if manufacturer and 'GE' not in manufacturer and 'Philips' not in manufacturer and 'UIH' not in manufacturer and 'SIEMENS' not in manufacturer:
                raise ValueError(f'un-supported manufacturer {manufacturer}, dicom file is skipped.')
            protocol = dicomStandardDict[CIODKeyWord]["GeneralSeries"]["SeriesInstanceUID"]
        #extract Vendor specific Module
        VerdorPrivateTagDict = dict()
        VendorPrivateTreeNode = globals()["_".join(["retrieveVendorPrivateTreeNode",CIODKeyWord])](manufacturer = manufacturer)
        VendorPrivateTreeNode.dicomSurvey(VerdorPrivateTagDict, dcmdata)
        dicomStandardDict[CIODKeyWord][VendorPrivateTreeNode.keyWord()] = VerdorPrivateTagDict[VendorPrivateTreeNode.keyWord()]
        RescaleSlope = float(VerdorPrivateTagDict[list(VerdorPrivateTagDict.keys())[0]]["RescaleSlope"]) if VerdorPrivateTagDict[list(VerdorPrivateTagDict.keys())[0]]["RescaleSlope"] != "" else 1.0
        RescaleIntercept = float(VerdorPrivateTagDict[list(VerdorPrivateTagDict.keys())[0]]["RescaleIntercept"]) if VerdorPrivateTagDict[list(VerdorPrivateTagDict.keys())[0]]["RescaleIntercept"] != "" else 0.0
        pixel_array = dcmdata.pixel_array * RescaleSlope + RescaleIntercept
        #update RescaleSlope and RescaleIntercept
        if RescaleSlope != VerdorPrivateTagDict[VendorPrivateTreeNode.keyWord()]["RescaleSlope"]:
            dicomStandardDict[CIODKeyWord][VendorPrivateTreeNode.keyWord()]["RescaleSlope"] = RescaleSlope
        if RescaleIntercept != VerdorPrivateTagDict[VendorPrivateTreeNode.keyWord()]["RescaleIntercept"]:
            dicomStandardDict[CIODKeyWord][VendorPrivateTreeNode.keyWord()]["RescaleIntercept"] = RescaleIntercept
        #save data and parameters to study dataset
        if protocol not in study_dataset.keys():
            study_dataset[protocol] = dict()
            raw_dicoms[protocol] = []
            study_dataset[protocol]["data"] = []
            study_dataset[protocol]["pars"] = []
            study_dataset[protocol]["data"].append(pixel_array)
            study_dataset[protocol]["pars"].append(dicomStandardDict)
        else:
            study_dataset[protocol]["data"].append(pixel_array)
            study_dataset[protocol]["pars"].append(dicomStandardDict)
            raw_dicoms[protocol].append((dicom_path, dicomStandardDict[CIODKeyWord]["SOPCommon"]["SOPInstanceUID"]))
        # make-sure everything has been processed correctly
        return True
    except Exception as exception:
        logger.error(exception)
        return False

def PyDicomGroupingEngine_main(raw_study_dataset: dict,
                               proc_study_dataset: dict):
    # PyDoGE: dicom-in, dictionary out
    # for sequence_storage_mode == seperate, the num_slice is inferenced from dicom files number
    logger = logging.getLogger(inspect.currentframe().f_code.co_name)
    logger.info(f"{len(raw_study_dataset.keys())} sequences found.")
    
    bar = alive_it(sorted(raw_study_dataset.keys()))
    for idx, protocol in enumerate(bar):
        try:
            bar.text("Stacking series: " + protocol)
            #consistent CIOD class check, all the image in one sequence should be same
            CIODKeyWords = [list(item.keys())[0] for item in raw_study_dataset[protocol]['pars']]
            unique_CIODKeyWord = np.unique(CIODKeyWords)
            if len(unique_CIODKeyWord) > 1:
                raise ValueError(f"more than one CIOD was found in {idx}th with series name: {protocol}")
            CIODKeyWord = unique_CIODKeyWord[0]
            logger.info(f"Stacking the {idx}-th sequence: {protocol}")
            if not globals()["_".join(["PyDicomGroupingEngine",CIODKeyWord])](study_dataset_dict = raw_study_dataset,
                                                                    protocol = protocol,
                                                                    proc_study_dataset = proc_study_dataset):
                raise ValueError(f"Error in stacking {idx}th series: {protocol}")
        except Exception as exception:
            logger.error(exception)
            continue

def PyDicomGroupingEngine_MRImage(study_dataset_dict: dict,
                                  protocol: str,
                                  proc_study_dataset: dict):     
    try:
        CIODKeyWord = inspect.currentframe().f_code.co_name.split('_')[-1]
        logger = logging.getLogger(inspect.currentframe().f_code.co_name)
        sorted_dict = dict()
        instance_numbers = [item[CIODKeyWord]["GeneralImage"]["InstanceNumber"] for item in study_dataset_dict[protocol]['pars']]
        idx_list = np.argsort(instance_numbers)
        sorted_dict['pars'] = [study_dataset_dict[protocol]['pars'][idx] for idx in idx_list]
        sorted_dict['data'] = [study_dataset_dict[protocol]['data'][idx] for idx in idx_list]
        image_orientations = [item[CIODKeyWord]["ImagePlane"]["ImageOrientationPatient"] for item in sorted_dict['pars']]
        #################################
        #
        # Slice orientation check
        #
        #################################
        unique_image_orientation, slice_packages_indexs = extractUniqueSliceOrientation(image_orientations)
        slice_packages = []
        for slice_packages_index, slice_package_indexs in enumerate(slice_packages_indexs):
            try:
                slice_package = dict()
                parsDicts = [sorted_dict['pars'][index] for index in slice_package_indexs]
                dataList = [sorted_dict['data'][index] for index in slice_package_indexs]
                merged_pars_dict = mergeParsDict(parsDicts)
                #ImagePositionPatient is mandatory 
                if merged_pars_dict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"] == "":
                    raise ValueError(f"ImagePositionPatient is mandatory according to Dicom Standard, we skip this series.")
                #retrieve unique slice position and location
                if isinstance(merged_pars_dict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], List):
                    unique_image_position = [list(item) for item in dict.fromkeys(tuple(item) for item in merged_pars_dict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"])]
                elif isinstance(merged_pars_dict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], pydicom.multival.MultiValue):
                    unique_image_position = [merged_pars_dict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"]]           
                #sorting image position
                ori_str, norm_vec = calc_image_ori(unique_image_orientation[slice_packages_index])
                unique_slice_location = [np.dot(image_position, norm_vec) for image_position in unique_image_position]
                unique_image_position, unique_slice_location = zip(*sorted(zip(unique_image_position, unique_slice_location), key = lambda x:x[1]))
                #unique slice gap check  ---> make sure continous slices
                slice_gaps = [item[CIODKeyWord]["ImagePlane"]["SpacingBetweenSlices"] for item in parsDicts]
                diff_image_position = [np.sqrt(np.sum(np.square(np.array(unique_image_position[slice_id]) - np.array(unique_image_position[slice_id - 1])))) for slice_id in range(1, len(unique_image_position))]
                if len(np.unique(slice_gaps)) > 1:
                    raise ValueError(f"spacing between slices is expected to be same, we skip this series with orientation {ori_str}.")
                elif len(diff_image_position) > 1:
                    if np.sum([np.abs(np.array(diff_image_position[slice_id]) - np.array(diff_image_position[slice_id - 1]))>1e-2 for slice_id in range(1, len(diff_image_position))]) > 0:
                        raise ValueError(f"spacing between slices is expected to be same, we skip this series with orientation {ori_str}.")
                #Spacing between slice check
                if merged_pars_dict[CIODKeyWord]["ImagePlane"]["SpacingBetweenSlices"] == "" or float(merged_pars_dict[CIODKeyWord]["ImagePlane"]["SpacingBetweenSlices"]) == 0.0 :
                    if len(unique_slice_location) > 1:
                        #update parsDict
                        for parsDict in parsDicts:
                            parsDict[CIODKeyWord]["ImagePlane"]["SpacingBetweenSlices"] = np.mean(diff_image_position)
                    elif len(unique_slice_location) == 1:
                        #replaced by SliceThickness or default value of 1
                        if merged_pars_dict[CIODKeyWord]["ImagePlane"]["SliceThickness"] != "" and float(merged_pars_dict[CIODKeyWord]["ImagePlane"]["SliceThickness"]) != 0.0:
                            for parsDict in parsDicts:
                                parsDict[CIODKeyWord]["ImagePlane"]["SpacingBetweenSlices"] = merged_pars_dict[CIODKeyWord]["ImagePlane"]["SliceThickness"] # use slice thickness
                        else:
                            for parsDict in parsDicts:
                                parsDict[CIODKeyWord]["ImagePlane"]["SpacingBetweenSlices"] = 1 # default 1
                    logger.warning(f"Empty SpacingBetweenSlices are found, we use the derived one instead.")
                #Slice Location check
                if merged_pars_dict[CIODKeyWord]["ImagePlane"]["SliceLocation"] == "":
                    for parsDict in parsDicts:
                        parsDict[CIODKeyWord]["ImagePlane"]["SliceLocation"] = np.dot(parsDict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)
                    logger.warning(f"Empty SliceLocation are found, we use the derived one instead.")
                num_slice = len(unique_slice_location)
                num_modality = 1 #default value
                num_temporal_position = 1 #default value
                stackingOrders = []
                leading_modality = []
                #unique row check
                Rows = merged_pars_dict[CIODKeyWord]["ImagePixel"]["Rows"]
                Columns = merged_pars_dict[CIODKeyWord]["ImagePixel"]["Columns"]
                PhotometricInterpretation = merged_pars_dict[CIODKeyWord]["ImagePixel"]["PhotometricInterpretation"]
                Manufacturer = merged_pars_dict[CIODKeyWord]["GeneralEquipment"]["Manufacturer"]
                ImageTypes = merged_pars_dict[CIODKeyWord]["GeneralImage"]["ImageType"]
                if isinstance(Rows, List):
                    raise ValueError(f"{protocol} length of unique row is larger than 1.")
                if isinstance(Columns, List):
                    raise ValueError(f"{protocol} length of unique column is larger than 1.")
                if isinstance(PhotometricInterpretation, List):
                    raise ValueError(f"{protocol} length of unique photometricInterp is larger than 1.")
                if isinstance(Manufacturer, List):
                    raise ValueError(f"{protocol} length of unique manufacturer is larger than 1.")
                if np.mod(len(slice_package_indexs), num_slice) == 0:
                    if len(slice_package_indexs)/num_slice == 1 and isinstance(ImageTypes, pydicom.multival.MultiValue):
                        #stacking by image position, in case of one imagetype and 1 modality, one repetation
                        modality_idx = 0
                        temporal_position_index = 0
                        stackingOrders = [[unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                            modality_idx, \
                                                temporal_position_index] for idx in slice_package_indexs]
                    elif len(slice_package_indexs)/num_slice > 1 and isinstance(ImageTypes, pydicom.multival.MultiValue):
                        # if len()
                        #DWI?multi-echo?
                        if "Philips" in Manufacturer:
                            # ImageType check for DWI, same Philips ImageType has been found for raw DWI scan and Reg_DWI scan
                            if isinstance(merged_pars_dict[CIODKeyWord]["VendorPrivateModule"]["DWIBVal"], list):
                                leading_modality = sorted(merged_pars_dict[CIODKeyWord]["VendorPrivateModule"]["DWIBVal"])
                                num_modality = int(len(leading_modality))
                                num_temporal_position = len(slice_package_indexs)/num_slice/num_modality
                                if not num_temporal_position.is_integer():
                                    raise ValueError(f"{protocol} length of num_temporal_position is not integer.")
                                else:
                                    num_temporal_position = int(num_temporal_position)
                                    temporal_position_idx = 0
                                    for idx in slice_package_indexs:
                                        slice_idx = unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec))
                                        modality_idx = leading_modality.index(sorted_dict['pars'][idx][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"])
                                        temp_stackingOrder = [slice_idx, modality_idx, temporal_position_idx]
                                        if temp_stackingOrder not in stackingOrders:
                                            stackingOrders.append(temp_stackingOrder)
                                        else:
                                            temporal_position_idx = temporal_position_idx + 1
                                            temp_stackingOrder = [slice_idx, modality_idx, temporal_position_idx]
                                            stackingOrders.append(temp_stackingOrder)
                            elif isinstance(merged_pars_dict[CIODKeyWord]["MRImage"]["EchoNumbers"], List) and np.mod(len(slice_package_indexs)/num_slice, len(merged_pars_dict[CIODKeyWord]["MRImage"]["EchoNumbers"])) == 0:
                                leading_modality = merged_pars_dict[CIODKeyWord]["MRImage"]["EchoNumbers"]
                                num_modality = int(len(leading_modality))
                                num_temporal_position = int(len(slice_package_indexs)/num_slice/num_modality)
                                tempos_idx = 0
                                for idx in slice_package_indexs:
                                    stackingOrder = [unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                        leading_modality.index(sorted_dict['pars'][idx][CIODKeyWord]["MRImage"]["EchoNumbers"]), \
                                                        tempos_idx]
                                    if stackingOrder not in stackingOrders:
                                        stackingOrders.append(stackingOrder)
                                    else:
                                        tempos_idx = tempos_idx + 1
                                        stackingOrder = [unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                        leading_modality.index(sorted_dict['pars'][idx][CIODKeyWord]["MRImage"]["EchoNumbers"]), \
                                                            tempos_idx]
                                        stackingOrders.append(stackingOrder)
                            # Multiple dynamic scan
                            else:
                                num_temporal_position = len(slice_package_indexs)/num_slice/num_modality
                                if not num_temporal_position.is_integer():
                                    raise ValueError(f"{protocol} length of num_temporal_position is not integer.")
                                modality_idx = 0
                                # TemporalPositionIdentifier already known
                                if merged_pars_dict[CIODKeyWord]["MRImage"]["TemporalPositionIdentifier"] != "" and merged_pars_dict[CIODKeyWord]["MRImage"]["NumberOfTemporalPositions"] != "" and \
                                    int(num_temporal_position) == int(merged_pars_dict[CIODKeyWord]["MRImage"]["NumberOfTemporalPositions"]) and \
                                        int(num_temporal_position) == int(len(merged_pars_dict[CIODKeyWord]["MRImage"]["TemporalPositionIdentifier"])):
                                        num_temporal_position = int(merged_pars_dict[CIODKeyWord]["MRImage"]["NumberOfTemporalPositions"])
                                        stackingOrders = [[unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                            modality_idx, \
                                                            merged_pars_dict[CIODKeyWord]["MRImage"]["TemporalPositionIdentifier"].index(sorted_dict['pars'][idx][CIODKeyWord]["MRImage"]["TemporalPositionIdentifier"])] \
                                                                for idx in slice_package_indexs]
                                else:
                                    # TemporalPositionIdentifier unknown
                                    logger.warning(f"{protocol} derived num_temporal_position is not equal to acquired NumberOfTemporalPositions in dicoms, we use derived instead.")
                                    num_temporal_position = int(num_temporal_position)
                                    temporal_position_idx = 0
                                    modality_idx = 0
                                    for idx in slice_package_indexs:
                                        slice_idx = unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec))
                                        temp_stackingOrder = [slice_idx, modality_idx, temporal_position_idx]
                                        if temp_stackingOrder not in stackingOrders:
                                            stackingOrders.append(temp_stackingOrder)
                                        else:
                                            temporal_position_idx = temporal_position_idx + 1
                                            temp_stackingOrder = [slice_idx, modality_idx, temporal_position_idx]
                                            stackingOrders.append(temp_stackingOrder)
                        elif "SIEMENS" in Manufacturer:
                            # a diffusion study
                            if "DIFFUSION" in ImageTypes:
                                if isinstance(merged_pars_dict[CIODKeyWord]["VendorPrivateModule"]["DWIBVal"], List):
                                    DWIBValList = sorted(merged_pars_dict[CIODKeyWord]["VendorPrivateModule"]["DWIBVal"])
                                    # exactly equal to b_val images, ADC scan
                                    if "ISOTROPIC" == merged_pars_dict[CIODKeyWord]["VendorPrivateModule"]["DWIDiffusionDirection"]:
                                        if len(DWIBValList) == len(slice_package_indexs)/num_slice:
                                            tempos_idx = 0
                                            num_modality = int(len(DWIBValList))
                                            stackingOrders = [[unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                            DWIBValList.index(sorted_dict['pars'][idx][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"]), \
                                                                tempos_idx] for idx in slice_package_indexs]
                                        #in multi-dynamic case, time are append at last
                                        elif np.mod(len(slice_package_indexs)/num_slice, len(DWIBValList)) == 0 and len(slice_package_indexs)/num_slice/len(DWIBValList) > 1:
                                            tempos_idx = 0
                                            num_modality = int(len(DWIBValList))
                                            num_temporal_position = int(len(slice_package_indexs)/num_slice/len(DWIBValList))
                                            for idx in slice_package_indexs:
                                                stackingOrder = [unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                                DWIBValList.index(sorted_dict['pars'][idx][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"]), \
                                                                    tempos_idx]
                                                if stackingOrder not in stackingOrders:
                                                    stackingOrders.append(stackingOrder)
                                                else:
                                                    tempos_idx = tempos_idx + 1
                                                    stackingOrder = [unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                                    DWIBValList.index(sorted_dict['pars'][idx][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"]), \
                                                                        tempos_idx]
                                                    stackingOrders.append(stackingOrder)
                                    #TODO: DTI
                                    else:
                                        pass
                            elif isinstance(merged_pars_dict[CIODKeyWord]["MRImage"]["EchoNumbers"], List) and np.mod(len(slice_package_indexs)/num_slice, len(merged_pars_dict[CIODKeyWord]["MRImage"]["EchoNumbers"])) == 0:
                                leading_modality = merged_pars_dict[CIODKeyWord]["MRImage"]["EchoNumbers"]
                                num_modality = int(len(leading_modality))
                                num_temporal_position = int(len(slice_package_indexs)/num_slice/num_modality)
                                tempos_idx = 0
                                for idx in slice_package_indexs:
                                    stackingOrder = [unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                        leading_modality.index(sorted_dict['pars'][idx][CIODKeyWord]["MRImage"]["EchoNumbers"]), \
                                                        tempos_idx]
                                    if stackingOrder not in stackingOrders:
                                        stackingOrders.append(stackingOrder)
                                    else:
                                        tempos_idx = tempos_idx + 1
                                        stackingOrder = [unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                        leading_modality.index(sorted_dict['pars'][idx][CIODKeyWord]["MRImage"]["EchoNumbers"]), \
                                                            tempos_idx]
                                        stackingOrders.append(stackingOrder)
                            # original-primary image with multiple dynamics
                            else:
                                if isinstance(merged_pars_dict[CIODKeyWord]["GeneralAcquisition"]["AcquisitionTime"], List):
                                    if len(merged_pars_dict[CIODKeyWord]["GeneralAcquisition"]["AcquisitionTime"]) == len(slice_package_indexs)/num_slice:
                                        AcquisitionTimeList = sorted(merged_pars_dict[CIODKeyWord]["GeneralAcquisition"]["AcquisitionTime"])
                                        modality_idx = 0
                                        num_temporal_position = int(len(slice_package_indexs)/num_slice)
                                        stackingOrders = [[unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                            modality_idx, \
                                                                AcquisitionTimeList.index(sorted_dict['pars'][idx][CIODKeyWord]["GeneralAcquisition"]["AcquisitionTime"])] for idx in slice_package_indexs]
                                elif isinstance(merged_pars_dict[CIODKeyWord]["GeneralAcquisition"]["AcquisitionNumber"], List):
                                    if len(merged_pars_dict[CIODKeyWord]["GeneralAcquisition"]["AcquisitionNumber"]) == len(slice_package_indexs)/num_slice:
                                        AcquisitionNumberList = sorted(merged_pars_dict[CIODKeyWord]["GeneralAcquisition"]["AcquisitionNumber"])
                                        modality_idx = 0
                                        num_temporal_position = int(len(slice_package_indexs)/num_slice)
                                        stackingOrders = [[unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                            modality_idx, \
                                                                AcquisitionNumberList.index(sorted_dict['pars'][idx][CIODKeyWord]["GeneralAcquisition"]["AcquisitionNumber"])] for idx in slice_package_indexs]
                                else:
                                    #using instanceID order
                                    tempos_idx = 0
                                    modality_idx = 0
                                    num_temporal_position = int(len(slice_package_indexs)/num_slice)
                                    for idx in slice_package_indexs:
                                        stackingOrder = [unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                            modality_idx, \
                                                            tempos_idx]
                                        if stackingOrder not in stackingOrders:
                                            stackingOrders.append(stackingOrder)
                                        else:
                                            tempos_idx = tempos_idx + 1
                                            stackingOrder = [unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                                modality_idx, \
                                                                tempos_idx]
                                            stackingOrders.append(stackingOrder)
                        elif "UIH" in Manufacturer:
                            #multi-dynamic scan
                            if isinstance(merged_pars_dict[CIODKeyWord]["GeneralAcquisition"]["AcquisitionTime"], List):
                                if len(merged_pars_dict[CIODKeyWord]["GeneralAcquisition"]["AcquisitionTime"]) == len(slice_package_indexs)/num_slice:
                                    AcquisitionTimeList = sorted(merged_pars_dict[CIODKeyWord]["GeneralAcquisition"]["AcquisitionTime"])
                                    modality_idx = 0
                                    num_temporal_position = int(len(slice_package_indexs)/num_slice)
                                    stackingOrders = [[unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                        modality_idx, \
                                                            AcquisitionTimeList.index(sorted_dict['pars'][idx][CIODKeyWord]["GeneralAcquisition"]["AcquisitionTime"])] for idx in slice_package_indexs]
                            elif isinstance(merged_pars_dict[CIODKeyWord]["GeneralAcquisition"]["AcquisitionNumber"], List):
                                if len(merged_pars_dict[CIODKeyWord]["GeneralAcquisition"]["AcquisitionNumber"]) == len(slice_package_indexs)/num_slice:
                                    AcquisitionNumberList = sorted(merged_pars_dict[CIODKeyWord]["GeneralAcquisition"]["AcquisitionNumber"])
                                    modality_idx = 0
                                    num_temporal_position = int(len(slice_package_indexs)/num_slice)
                                    stackingOrders = [[unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                        modality_idx, \
                                                            AcquisitionNumberList.index(sorted_dict['pars'][idx][CIODKeyWord]["GeneralAcquisition"]["AcquisitionNumber"])] for idx in slice_package_indexs]
                            elif isinstance(merged_pars_dict[CIODKeyWord]["MRImage"]["EchoNumbers"], List) and np.mod(len(slice_package_indexs)/num_slice, len(merged_pars_dict[CIODKeyWord]["MRImage"]["EchoNumbers"])) == 0:
                                leading_modality = merged_pars_dict[CIODKeyWord]["MRImage"]["EchoNumbers"]
                                num_modality = int(len(leading_modality))
                                num_temporal_position = int(len(slice_package_indexs)/num_slice/num_modality)
                                tempos_idx = 0
                                for idx in slice_package_indexs:
                                    stackingOrder = [unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                        leading_modality.index(sorted_dict['pars'][idx][CIODKeyWord]["MRImage"]["EchoNumbers"]), \
                                                        tempos_idx]
                                    if stackingOrder not in stackingOrders:
                                        stackingOrders.append(stackingOrder)
                                    else:
                                        tempos_idx = tempos_idx + 1
                                        stackingOrder = [unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                        leading_modality.index(sorted_dict['pars'][idx][CIODKeyWord]["MRImage"]["EchoNumbers"]), \
                                                            tempos_idx]
                                        stackingOrders.append(stackingOrder)
                            else:
                                #using instanceID order
                                tempos_idx = 0
                                modality_idx = 0
                                num_temporal_position = int(len(slice_package_indexs)/num_slice)
                                for idx in slice_package_indexs:
                                    stackingOrder = [unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                        modality_idx, \
                                                        tempos_idx]
                                    if stackingOrder not in stackingOrders:
                                        stackingOrders.append(stackingOrder)
                                    else:
                                        tempos_idx = tempos_idx + 1
                                        stackingOrder = [unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                            modality_idx, \
                                                            tempos_idx]
                                        stackingOrders.append(stackingOrder)
                        elif "GE" in Manufacturer:
                            # dixon image with multiple-dynamics, EPI with multiple B-values or Dixon multiple-dynamics
                            ScanningSequence = merged_pars_dict[CIODKeyWord]["MRImage"]["ScanningSequence"]
                            ScanOptions = merged_pars_dict[CIODKeyWord]["MRImage"]["ScanOptions"]
                            if "EPI_GEMS" in ScanOptions and "EP" in ScanningSequence:
                                #DWI scan
                                if isinstance(parsDicts[0][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"], float) or isinstance(parsDicts[0][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"], str):
                                    DWIBValList = sorted(list(set([parsDict[CIODKeyWord]["VendorPrivateModule"]["DWIBVal"] for parsDict in parsDicts])))
                                elif isinstance(parsDicts[0][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"], List) or isinstance(parsDicts[0][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"], pydicom.multival.MultiValue):
                                    DWIBValList = sorted([list(item) for item in dict.fromkeys(tuple(parsDict[CIODKeyWord]["VendorPrivateModule"]["DWIBVal"]) for parsDict in parsDicts)], key = lambda x: x[0])
                                num_modality = int(len(DWIBValList))
                                # shrink remained dimension to temposition
                                if np.mod(len(slice_package_indexs)/num_slice, num_modality) == 0:
                                    num_temporal_position = int(len(slice_package_indexs)/num_slice/num_modality)
                                else:
                                    raise ValueError(f"Incomplete dataset with whole slice package includes {len(slice_package_indexs)}, {num_slice} slices, and {num_modality} modality, but {len(slice_package_indexs)/num_slice/num_modality} dynamics.")
                                tempos_idx = 0
                                for idx in slice_package_indexs:
                                    stackingOrder = [unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                        DWIBValList.index(sorted_dict['pars'][idx][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"]), \
                                                        tempos_idx]
                                    if stackingOrder not in stackingOrders:
                                        stackingOrders.append(stackingOrder)
                                    else:
                                        tempos_idx = tempos_idx + 1
                                        stackingOrder = [unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                        DWIBValList.index(sorted_dict['pars'][idx][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"]), \
                                                            tempos_idx]
                                        stackingOrders.append(stackingOrder)
                            #dual echo images
                            elif isinstance(merged_pars_dict[CIODKeyWord]["MRImage"]["EchoNumbers"], List) and np.mod(len(slice_package_indexs)/num_slice, len(merged_pars_dict[CIODKeyWord]["MRImage"]["EchoNumbers"])) == 0:
                                leading_modality = merged_pars_dict[CIODKeyWord]["MRImage"]["EchoNumbers"]
                                num_modality = int(len(leading_modality))
                                num_temporal_position = int(len(slice_package_indexs)/num_slice/num_modality)
                                tempos_idx = 0
                                for idx in slice_package_indexs:
                                    stackingOrder = [unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                        leading_modality.index(sorted_dict['pars'][idx][CIODKeyWord]["MRImage"]["EchoNumbers"]), \
                                                        tempos_idx]
                                    if stackingOrder not in stackingOrders:
                                        stackingOrders.append(stackingOrder)
                                    else:
                                        tempos_idx = tempos_idx + 1
                                        stackingOrder = [unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                        leading_modality.index(sorted_dict['pars'][idx][CIODKeyWord]["MRImage"]["EchoNumbers"]), \
                                                            tempos_idx]
                                        stackingOrders.append(stackingOrder)
                            else:
                                #dynamics imaging
                                modality_idx = 0
                                tempos_idx = 0
                                if np.mod(len(slice_package_indexs)/num_slice, num_modality) == 0:
                                    num_temporal_position = int(len(slice_package_indexs)/num_slice/num_modality)
                                else:
                                    raise ValueError(f"Incomplete dataset with whole slice package includes {len(slice_package_indexs)}, {num_slice} slices, and {num_modality} modality, but {len(slice_package_indexs)/num_slice/num_modality} dynamics.")
                                for idx in slice_package_indexs:
                                    stackingOrder = [unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                    modality_idx, \
                                                        tempos_idx]
                                    if stackingOrder not in stackingOrders:
                                        stackingOrders.append(stackingOrder)
                                    else:
                                        tempos_idx = tempos_idx + 1
                                        stackingOrder = [unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                        modality_idx, \
                                                            tempos_idx]
                                        stackingOrders.append(stackingOrder)

                    elif len(slice_package_indexs)/num_slice > 1 and isinstance(ImageTypes, List) and len(ImageTypes) > 1:
                        #dixon?
                        if "Philips" in Manufacturer:
                            PhilipsDixonQuantImageTypeList = ['W','F','IP','OP','T2_STAR','R2_STAR','FF']
                            #Image Type Check
                            if all([any([item in PhilipsDixonQuantImageTypeList for item in ImageType]) for ImageType in ImageTypes]) and all(["DERIVED" in ImageType for ImageType in ImageTypes]):
                                unique_ImageType = [PhilipsDixonQuantImageTypeList[[ImageTypeItem in ImageType for ImageTypeItem in PhilipsDixonQuantImageTypeList].index(True)] for ImageType in ImageTypes]
                                sorted_ImageType = sorted(unique_ImageType, key = lambda x: PhilipsDixonQuantImageTypeList.index(x))
                                sub_parsDicts = [[parsDict for parsDict in parsDicts if ImageType in parsDict[CIODKeyWord]["MRImage"]["ImageType"]] for ImageType in sorted_ImageType]
                                sub_image_positions = [sorted([np.dot(parsDict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec) for parsDict in sub_parsDict]) for sub_parsDict in sub_parsDicts]
                                #data completeness check
                                if not all([sorted(sub_image_position) == sorted(int(len(sub_image_position)/len(unique_slice_location)) * unique_slice_location) for sub_image_position in sub_image_positions]):
                                    raise ValueError(f"Incomplete dataset were found in protocol: {protocol}")
                                num_rep_per_slice_package_per_image_type = [int(len(sub_image_position)/len(unique_slice_location)) for sub_image_position in sub_image_positions]
                                #this is a Philips Dixon sequence, temporal-position check
                                if len(np.unique(num_rep_per_slice_package_per_image_type)) > 1:
                                    raise ValueError(f"Philips-Dixon error: In-consistent repetation for each image type: {num_rep_per_slice_package_per_image_type}.")
                                leading_modality = sorted_ImageType
                                num_modality = len(leading_modality)
                                num_temporal_position = int(len(slice_package_indexs)/num_slice/num_modality)
                                temporal_position_idx = 0
                                for idx in slice_package_indexs:
                                    slice_idx = unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec))
                                    modality_idx = leading_modality.index([item for item in sorted_dict['pars'][idx][CIODKeyWord]["MRImage"]["ImageType"] if item in leading_modality])
                                    temp_stackingOrder = [slice_idx, modality_idx, temporal_position_idx]
                                    if temp_stackingOrder not in stackingOrders:
                                        stackingOrders.append(temp_stackingOrder)
                                    else:
                                        temporal_position_idx = temporal_position_idx + 1
                                        temp_stackingOrder = [slice_idx, modality_idx, temporal_position_idx]
                                        stackingOrders.append(temp_stackingOrder)
                            elif "APTW" in merged_pars_dict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"] and "M" in merged_pars_dict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"]:
                                PhilipsAPTQuantImageTypeList = ["M","APTW"]
                                unique_ImageType = merged_pars_dict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"]
                                sorted_ImageType = sorted(unique_ImageType, key = lambda x: PhilipsAPTQuantImageTypeList.index(x))
                                sub_parsDicts = [[parsDict for parsDict in parsDicts if ImageType == parsDict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"]] for ImageType in sorted_ImageType]
                                sub_image_positions = [sorted([np.dot(parsDict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec) for parsDict in sub_parsDict]) for sub_parsDict in sub_parsDicts]
                                #data completeness check
                                if not all([sorted(sub_image_position) == sorted(int(len(sub_image_position)/len(unique_slice_location)) * unique_slice_location) for sub_image_position in sub_image_positions]):
                                    raise ValueError(f"Incomplete dataset were found in protocol: {protocol}")
                                num_rep_per_slice_package_per_image_type = [int(len(sub_image_position)/len(unique_slice_location)) for sub_image_position in sub_image_positions]
                                #this is a Philips APTW sequence, temporal-position check
                                if len(np.unique(num_rep_per_slice_package_per_image_type)) > 1:
                                    raise ValueError(f"Philips-APT error: In-consistent repetation for each image type: {num_rep_per_slice_package_per_image_type}.")
                                leading_modality = sorted_ImageType
                                num_modality = len(leading_modality)
                                num_temporal_position = int(len(slice_package_indexs)/num_slice/num_modality)
                                temporal_position_idx = 0
                                for idx in slice_package_indexs:
                                    slice_idx = unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec))
                                    modality_idx = leading_modality.index(sorted_dict['pars'][idx][CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"])
                                    temp_stackingOrder = [slice_idx, modality_idx, temporal_position_idx]
                                    if temp_stackingOrder not in stackingOrders:
                                        stackingOrders.append(temp_stackingOrder)
                                    else:
                                        temporal_position_idx = temporal_position_idx + 1
                                        temp_stackingOrder = [slice_idx, modality_idx, temporal_position_idx]
                                        stackingOrders.append(temp_stackingOrder)
                            elif "T1" in merged_pars_dict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"] and "M" in merged_pars_dict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"]:
                                PhilipsT1mapQuantImageTypeList = ["M","T1"]
                                unique_ImageType = merged_pars_dict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"]
                                sorted_ImageType = sorted(unique_ImageType, key = lambda x: PhilipsT1mapQuantImageTypeList.index(x))
                                sub_parsDicts = [[parsDict for parsDict in parsDicts if ImageType == parsDict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"]] for ImageType in sorted_ImageType]
                                sub_image_positions = [sorted([np.dot(parsDict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec) for parsDict in sub_parsDict]) for sub_parsDict in sub_parsDicts]
                                #data completeness check
                                if not all([sorted(sub_image_position) == sorted(int(len(sub_image_position)/len(unique_slice_location)) * unique_slice_location) for sub_image_position in sub_image_positions]):
                                    raise ValueError(f"Incomplete dataset were found in protocol: {protocol}")
                                num_rep_per_slice_package_per_image_type = [int(len(sub_image_position)/len(unique_slice_location)) for sub_image_position in sub_image_positions]
                                #process Magnitude Image
                                M_merged_parsDict = mergeParsDict([parsDict for parsDict in parsDicts if parsDict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"] == "M"])
                                #Inversion time check
                                if len(M_merged_parsDict[CIODKeyWord]["VendorPrivateModule"]["InversionDelayNumber"]) != int(M_merged_parsDict[CIODKeyWord]["VendorPrivateModule"]["NumberOfInversionDelays"]):
                                    raise ValueError(f"Philips T1Map error: in-consistent InversionDelayNumber {M_merged_parsDict[CIODKeyWord]['VendorPrivateModule']['InversionDelayNumber']} vs. NumberOfInversionDelays {M_merged_parsDict[CIODKeyWord]['VendorPrivateModule']['NumberOfInversionDelays']}.")
                                T1MAP_merged_parsDict = mergeParsDict([parsDict for parsDict in parsDicts if parsDict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"] == "T1"])
                                leading_modality.extend(['_'.join([str(M_merged_parsDict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"]),str(item)]) for item in sorted(M_merged_parsDict[CIODKeyWord]["VendorPrivateModule"]["InversionDelayNumber"])])
                                leading_modality.extend(['_'.join([str(T1MAP_merged_parsDict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"]), str(item)]) for item in sorted(T1MAP_merged_parsDict[CIODKeyWord]["VendorPrivateModule"]["InversionDelayNumber"])])
                                num_modality = len(leading_modality)
                                num_temporal_position = int(len(slice_package_indexs)/num_slice/num_modality)
                                temporal_position_idx = 0
                                for idx in slice_package_indexs:
                                    slice_idx = unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec))
                                    modality_idx = leading_modality.index('_'.join([str(sorted_dict['pars'][idx][CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"]),\
                                                                                    str(sorted_dict['pars'][idx][CIODKeyWord]["VendorPrivateModule"]["InversionDelayNumber"])]))
                                    temp_stackingOrder = [slice_idx, modality_idx, temporal_position_idx]
                                    if temp_stackingOrder not in stackingOrders:
                                        stackingOrders.append(temp_stackingOrder)
                                    else:
                                        temporal_position_idx = temporal_position_idx + 1
                                        temp_stackingOrder = [slice_idx, modality_idx, temporal_position_idx]
                                        stackingOrders.append(temp_stackingOrder)
                            elif ("T2" in merged_pars_dict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"] or \
                                "R2" in merged_pars_dict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"]) and \
                                "M" in merged_pars_dict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"]:
                                PhilipsT2mapQuantImageTypeList = ["M","T2","R2"]
                                unique_ImageType = merged_pars_dict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"]
                                sorted_ImageType = sorted(unique_ImageType, key = lambda x: PhilipsT2mapQuantImageTypeList.index(x))
                                sub_parsDicts = [[parsDict for parsDict in parsDicts if ImageType == parsDict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"]] for ImageType in sorted_ImageType]
                                sub_image_positions = [sorted([np.dot(parsDict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec) for parsDict in sub_parsDict]) for sub_parsDict in sub_parsDicts]
                                #data completeness check
                                if not all([sorted(sub_image_position) == sorted(int(len(sub_image_position)/len(unique_slice_location)) * unique_slice_location) for sub_image_position in sub_image_positions]):
                                    raise ValueError(f"Incomplete dataset were found in protocol: {protocol}")
                                num_rep_per_slice_package_per_image_type = [int(len(sub_image_position)/len(unique_slice_location)) for sub_image_position in sub_image_positions]
                                M_merged_parsDict = mergeParsDict([parsDict for parsDict in parsDicts if parsDict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"] == "M"])
                                #Inversion time check
                                if len(M_merged_parsDict[CIODKeyWord]["MRImage"]["EchoNumbers"]) != len(M_merged_parsDict[CIODKeyWord]["MRImage"]["EchoTime"]) or \
                                    len(M_merged_parsDict[CIODKeyWord]["MRImage"]["EchoNumbers"]) != num_rep_per_slice_package_per_image_type[0]:
                                    logger.error(f"Philips T1Map error: in-consistent InversionDelayNumber {M_merged_parsDict[CIODKeyWord]['VendorPrivateModule']['InversionDelayNumber']} vs. NumberOfInversionDelays {M_merged_parsDict[CIODKeyWord]['VendorPrivateModule']['NumberOfInversionDelays']}.")
                                leading_modality.extend(['_'.join([str(M_merged_parsDict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"]), "EchoTime", str(item)]) for item in sorted(M_merged_parsDict[CIODKeyWord]["MRImage"]["EchoNumbers"])])
                                if "T2" in merged_pars_dict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"]:
                                    T2MAP_merged_parsDict = mergeParsDict([parsDict for parsDict in parsDicts if parsDict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"] == "T2"])
                                    if isinstance(T2MAP_merged_parsDict[CIODKeyWord]["MRImage"]["EchoNumbers"], List):
                                        leading_modality.extend(['_'.join([str(T2MAP_merged_parsDict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"]), "EchoTime", str(item)]) for item in sorted(T2MAP_merged_parsDict[CIODKeyWord]["MRImage"]["EchoNumbers"])])
                                    else:
                                        leading_modality.append('_'.join([str(T2MAP_merged_parsDict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"]), "EchoTime", str(T2MAP_merged_parsDict[CIODKeyWord]["MRImage"]["EchoNumbers"])]))
                                if "R2" in merged_pars_dict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"]:
                                    R2MAP_merged_parsDict = mergeParsDict([parsDict for parsDict in parsDicts if parsDict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"] == "R2"])
                                    if isinstance(R2MAP_merged_parsDict[CIODKeyWord]["MRImage"]["EchoNumbers"], List):
                                        leading_modality.extend(['_'.join([str(R2MAP_merged_parsDict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"]), "EchoTime", str(item)]) for item in sorted(R2MAP_merged_parsDict[CIODKeyWord]["MRImage"]["EchoNumbers"])])
                                    else:
                                        leading_modality.append('_'.join([str(R2MAP_merged_parsDict[CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"]), "EchoTime", str(R2MAP_merged_parsDict[CIODKeyWord]["MRImage"]["EchoNumbers"])]))
                                num_modality = len(leading_modality)
                                num_temporal_position = int(len(slice_package_indexs)/num_slice/num_modality)
                                temporal_position_idx = 0
                                for idx in slice_package_indexs:
                                    slice_idx = unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec))
                                    modality_idx = leading_modality.index('_'.join([str(sorted_dict['pars'][idx][CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"]),\
                                                                                    "EchoTime",\
                                                                                    str(sorted_dict['pars'][idx][CIODKeyWord]["MRImage"]["EchoNumbers"])]))
                                    temp_stackingOrder = [slice_idx, modality_idx, temporal_position_idx]
                                    if temp_stackingOrder not in stackingOrders:
                                        stackingOrders.append(temp_stackingOrder)
                                    else:
                                        temporal_position_idx = temporal_position_idx + 1
                                        temp_stackingOrder = [slice_idx, modality_idx, temporal_position_idx]
                                        stackingOrders.append(temp_stackingOrder)
                        elif "SIEMENS" in Manufacturer:
                            sub_parsDicts = [[parsDict for parsDict in parsDicts if ImageType == parsDict[CIODKeyWord]["MRImage"]["ImageType"]] for ImageType in ImageTypes]
                            sub_image_positions = [sorted([np.dot(parsDict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec) for parsDict in sub_parsDict]) for sub_parsDict in sub_parsDicts]
                            if not all([sorted(sub_image_position) == sorted(int(len(sub_image_position)/len(unique_slice_location)) * unique_slice_location) for sub_image_position in sub_image_positions]):
                                raise ValueError(f"Incomplete dataset were found in protocol: {protocol}")
                            sub_merged_pars_dicts = [mergeParsDict([parsDict for parsDict in sub_parsDict]) for sub_parsDict in sub_parsDicts]
                            QSMImageTypes = ["M","P"] # QSM have both M and P
                            if all([isinstance(sub_merged_pars_dict[CIODKeyWord]["MRImage"]["EchoNumbers"], List) for sub_merged_pars_dict in sub_merged_pars_dicts]) and \
                                all([QSMImageType in ImageType for ImageType in ImageTypes] for QSMImageType in QSMImageTypes) and \
                                    all([np.mod(len(sub_parsDict)/len(unique_slice_location), len(sub_merged_pars_dict[CIODKeyWord]["MRImage"]["EchoNumbers"]))==0 for sub_merged_pars_dict,sub_parsDict in zip(sub_merged_pars_dicts, sub_parsDicts)]):
                                    leading_modality = ['_'.join([QSMImageType, "EchoTime",str(echoNumbers)]) for QSMImageType in QSMImageTypes for sub_merged_pars_dict in sub_merged_pars_dicts for echoNumbers in sub_merged_pars_dict[CIODKeyWord]["MRImage"]["EchoNumbers"]  if QSMImageType in sub_merged_pars_dict[CIODKeyWord]["MRImage"]["ImageType"]]
                                    num_modality = int(len(leading_modality))
                                    num_temporal_position = int(len(slice_package_indexs)/num_slice/num_modality)
                                    temporal_position_idx = 0
                                    for idx in slice_package_indexs:
                                        slice_idx = unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec))
                                        modality_idx = leading_modality.index('_'.join([str([imageType for imageType in sorted_dict['pars'][idx][CIODKeyWord]["MRImage"]["ImageType"] if imageType in QSMImageTypes][0]),\
                                                                                        "EchoTime",\
                                                                                        str(sorted_dict['pars'][idx][CIODKeyWord]["MRImage"]["EchoNumbers"])]))
                                        temp_stackingOrder = [slice_idx, modality_idx, temporal_position_idx]
                                        if temp_stackingOrder not in stackingOrders:
                                            stackingOrders.append(temp_stackingOrder)
                                        else:
                                            temporal_position_idx = temporal_position_idx + 1
                                            temp_stackingOrder = [slice_idx, modality_idx, temporal_position_idx]
                                            stackingOrders.append(temp_stackingOrder)

                else:
                    raise ValueError(f'{protocol} Incomplete Dataset Error: {len(slice_package_indexs)} dicom files were found, but {num_slice} slices were derived.')

                if PhotometricInterpretation == "MONOCHROME2":
                    stack_data = np.zeros((Rows, Columns, num_slice, num_modality, num_temporal_position))
                elif PhotometricInterpretation == "RGB":
                    stack_data = np.zeros((Rows, Columns, 3, num_slice, num_modality, num_temporal_position))

                if stackingOrders:
                    #stacking pars dict and data
                    stack_parsDict = mergeParsDict(parsDicts, stackingOrders)
                else:
                    raise ValueError(f"StackingOrders Error: Empty stackingOrders were found in protocol {protocol}")
                #data size check
                if num_slice * num_modality * num_temporal_position != len(dataList):
                    raise ValueError(f"Datasize mismatch error: num_slice-by-num_modality-by-num_temporal_position: {num_slice}-by-{num_modality}-by-{num_temporal_position} is not equal to total datasize {len(dataList)}.")
                for data, stackingOrder in zip(dataList, stackingOrders):
                    stack_data[...,stackingOrder[0], stackingOrder[1], stackingOrder[2]] = data
                slice_package["pars"] = stack_parsDict
                slice_package["data"] = stack_data
                slice_packages.append(slice_package)
            except Exception as exception:
                logger.error(exception)
                continue
        if not slice_packages:
            raise ValueError(f"Empty Slice Packages Error: After series stacking, empty slice_packages were found for protocol {protocol}.")
        proc_study_dataset[protocol] = slice_packages
        return True
    except Exception as exception:
            logger.error(exception)
            return False

def PyDicomGroupingEngine_CTImage(study_dataset_dict: dict,
                                  protocol: str,
                                  proc_study_dataset: dict):
    try:
        CIODKeyWord = inspect.currentframe().f_code.co_name.split('_')[-1]
        logger = logging.getLogger(inspect.currentframe().f_code.co_name)
        sorted_dict = dict()
        instance_numbers = [item[CIODKeyWord]["GeneralImage"]["InstanceNumber"] for item in study_dataset_dict[protocol]['pars']]
        idx_list = np.argsort(instance_numbers)
        sorted_dict['pars'] = [study_dataset_dict[protocol]['pars'][idx] for idx in idx_list]
        sorted_dict['data'] = [study_dataset_dict[protocol]['data'][idx] for idx in idx_list]
        image_orientations = [item[CIODKeyWord]["ImagePlane"]["ImageOrientationPatient"] for item in sorted_dict['pars']]
        #################################
        #
        # Slice orientation check
        #
        #################################
        unique_image_orientation, slice_packages_indexs = extractUniqueSliceOrientation(image_orientations)
        slice_packages = []
        for slice_packages_index, slice_package_indexs in enumerate(slice_packages_indexs):
            try:
                slice_package = dict()
                parsDicts = [sorted_dict['pars'][index] for index in slice_package_indexs]
                dataList = [sorted_dict['data'][index] for index in slice_package_indexs]
                merged_pars_dict = mergeParsDict(parsDicts)
                #ImagePositionPatient and SliceLocation are mandatory 
                if merged_pars_dict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"] == "":
                    raise ValueError(f"ImagePositionPatient is mandatory according to Dicom Standard, we skip this series.")
                #retrieve unique slice position and location
                if isinstance(merged_pars_dict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], List):
                    unique_image_position = [list(item) for item in dict.fromkeys(tuple(item) for item in merged_pars_dict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"])]
                elif isinstance(merged_pars_dict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], pydicom.multival.MultiValue):
                    unique_image_position = [merged_pars_dict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"]]           
                #sorting image position
                ori_str, norm_vec = calc_image_ori(unique_image_orientation[slice_packages_index])
                unique_slice_location = [np.dot(image_position, norm_vec) for image_position in unique_image_position]
                unique_image_position, unique_slice_location = zip(*sorted(zip(unique_image_position, unique_slice_location), key = lambda x:x[1]))
                #unique slice gap check  ---> make sure continous slices
                slice_gaps = [item[CIODKeyWord]["ImagePlane"]["SpacingBetweenSlices"] for item in parsDicts]
                diff_image_position = [np.sqrt(np.sum(np.square(np.array(unique_image_position[slice_id]) - np.array(unique_image_position[slice_id - 1])))) for slice_id in range(1, len(unique_image_position))]
                if len(np.unique(slice_gaps)) > 1:
                    raise ValueError(f"spacing between slices is expected to be same, we skip this series with orientation {ori_str}.")
                elif len(diff_image_position) > 1:
                    if np.sum([(np.array(diff_image_position[slice_id]) - np.array(diff_image_position[slice_id - 1]))>1e-1 for slice_id in range(1, len(diff_image_position))]) > 0:
                        raise ValueError(f"spacing between slices is expected to be same, we skip this series with orientation {ori_str}.")
                #Spacing between slice check
                if merged_pars_dict[CIODKeyWord]["ImagePlane"]["SpacingBetweenSlices"] == "" or float(merged_pars_dict[CIODKeyWord]["ImagePlane"]["SpacingBetweenSlices"]) == 0.0 :
                    if len(unique_slice_location) > 1:
                        #update parsDict
                        for parsDict in parsDicts:
                            parsDict[CIODKeyWord]["ImagePlane"]["SpacingBetweenSlices"] = np.mean(diff_image_position)
                    elif len(unique_slice_location) == 1:
                        #replaced by SliceThickness or default value of 1
                        if merged_pars_dict[CIODKeyWord]["ImagePlane"]["SliceThickness"] != "" and float(merged_pars_dict[CIODKeyWord]["ImagePlane"]["SliceThickness"]) != 0.0:
                            for parsDict in parsDicts:
                                parsDict[CIODKeyWord]["ImagePlane"]["SpacingBetweenSlices"] = merged_pars_dict[CIODKeyWord]["ImagePlane"]["SliceThickness"] # use slice thickness
                        else:
                            for parsDict in parsDicts:
                                parsDict[CIODKeyWord]["ImagePlane"]["SpacingBetweenSlices"] = 1 # default 1
                    logger.warning(f"Since empty SpacingBetweenSlices are found, we use the derived one instead.")
                #Slice Location check
                if merged_pars_dict[CIODKeyWord]["ImagePlane"]["SliceLocation"] == "":
                    for parsDict in parsDicts:
                        parsDict[CIODKeyWord]["ImagePlane"]["SliceLocation"] = np.dot(parsDict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)
                    logger.warning(f"Since empty SliceLocation are found, we use the derived one instead.")
                num_slice = len(unique_slice_location)
                num_modality = 1 #default value
                num_temporal_position = 1 #default value
                stackingOrders = []
                #unique row check
                Rows = merged_pars_dict[CIODKeyWord]["ImagePixel"]["Rows"]
                Columns = merged_pars_dict[CIODKeyWord]["ImagePixel"]["Columns"]
                PhotometricInterpretation = merged_pars_dict[CIODKeyWord]["ImagePixel"]["PhotometricInterpretation"]
                Manufacturer = merged_pars_dict[CIODKeyWord]["GeneralEquipment"]["Manufacturer"]
                ImageTypes = merged_pars_dict[CIODKeyWord]["GeneralImage"]["ImageType"]
                if isinstance(Rows, List):
                    raise ValueError(f"{protocol} length of unique row is larger than 1.")
                if isinstance(Columns, List):
                    raise ValueError(f"{protocol} length of unique column is larger than 1.")
                if isinstance(PhotometricInterpretation, List):
                    raise ValueError(f"{protocol} length of unique photometricInterp is larger than 1.")
                if isinstance(Manufacturer, List):
                    raise ValueError(f"{protocol} length of unique manufacturer is larger than 1.")
                if np.mod(len(slice_package_indexs), num_slice) == 0:
                    if len(slice_package_indexs)/num_slice == 1 and isinstance(ImageTypes, pydicom.multival.MultiValue):
                        #stacking by image position, in case of one imagetype and 1 modality, one repetation
                        modality_idx = 0
                        temporal_position_index = 0
                        stackingOrders = [[unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                            modality_idx, \
                                                temporal_position_index] for idx in slice_package_indexs]
                    elif len(slice_package_indexs)/num_slice > 1 and isinstance(ImageTypes, pydicom.multival.MultiValue):
                        #muklti-dynamic image
                        num_modality = 1
                        num_temporal_position = len(slice_package_indexs)/num_slice/num_modality
                        if not num_temporal_position.is_integer():
                            raise ValueError(f"{protocol} length of num_temporal_position is not integer.")
                        else:
                            num_temporal_position = int(num_temporal_position)
                            temporal_position_idx = 0
                            modality_idx = 0
                            for idx in slice_package_indexs:
                                slice_idx = unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec))
                                temp_stackingOrder = [slice_idx, modality_idx, temporal_position_idx]
                                if temp_stackingOrder not in stackingOrders:
                                    stackingOrders.append(temp_stackingOrder)
                                else:
                                    temporal_position_idx = temporal_position_idx + 1
                                    temp_stackingOrder = [slice_idx, modality_idx, temporal_position_idx]
                                    stackingOrders.append(temp_stackingOrder)
                    elif len(slice_package_indexs)/num_slice > 1 and isinstance(ImageTypes, List):
                        if isinstance(merged_pars_dict[CIODKeyWord]["CTImage"]["AcquisitionNumber"], List):
                            AcquisitionNumber = sorted(merged_pars_dict[CIODKeyWord]["CTImage"]["AcquisitionNumber"])
                            if np.mod(len(slice_package_indexs)/num_slice, len(AcquisitionNumber)) == 0:
                                num_modality = int(len(AcquisitionNumber))
                                num_temporal_position = int(len(slice_package_indexs)/num_slice/num_modality)
                                temporal_position_idx = 0
                                for idx in slice_package_indexs:
                                    slice_idx = unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec))
                                    modality_idx = AcquisitionNumber.index(sorted_dict['pars'][idx][CIODKeyWord]["CTImage"]["AcquisitionNumber"])
                                    temp_stackingOrder = [slice_idx, modality_idx, temporal_position_idx]
                                    if temp_stackingOrder not in stackingOrders:
                                        stackingOrders.append(temp_stackingOrder)
                                    else:
                                        temporal_position_idx = temporal_position_idx + 1
                                        temp_stackingOrder = [slice_idx, modality_idx, temporal_position_idx]
                                        stackingOrders.append(temp_stackingOrder)
                else:
                    raise ValueError(f'{protocol} Incomplete Dataset Error: {len(slice_package_indexs)} dicom files were found, but {num_slice} slices were derived.')

                if PhotometricInterpretation == "MONOCHROME2":
                    stack_data = np.zeros((Rows, Columns, num_slice, num_modality, num_temporal_position))
                elif PhotometricInterpretation == "RGB":
                    stack_data = np.zeros((Rows, Columns, 3, num_slice, num_modality, num_temporal_position))

                if stackingOrders:
                    #stacking pars dict and data
                    stack_parsDict = mergeParsDict(parsDicts, stackingOrders)
                else:
                    raise ValueError(f"StackingOrders Error: Empty stackingOrders were found in protocol {protocol}")
                #data size check
                if num_slice * num_modality * num_temporal_position != len(dataList):
                    raise ValueError(f"Datasize mismatch error: num_slice-by-num_modality-by-num_temporal_position: {num_slice}-by-{num_modality}-by-{num_temporal_position} is not equal to total datasize {len(dataList)}.")
                for data, stackingOrder in zip(dataList, stackingOrders):
                    stack_data[...,stackingOrder[0], stackingOrder[1], stackingOrder[2]] = data
                slice_package['pars'] = stack_parsDict
                slice_package['data'] = stack_data
                slice_packages.append(slice_package)
            except Exception as exception:
                logger.error(exception)
                continue
        if not slice_packages:
            raise ValueError(f"Empty Slice Packages Error: After series stacking, empty slice_packages were found for protocol {protocol}.")
        proc_study_dataset[protocol] = slice_packages
        return True
    except Exception as exception:
            logger.error(exception)
            return False

def PyDicomStorageEngine_main(proc_study_dataset: dict,
                         raw_dicoms: dict,
                         save_path: Union[str, Path, os.PathLike],
                         save_raw_dicoms: bool = True):
    #Store 
    logger = logging.getLogger(inspect.currentframe().f_code.co_name)
    #save raw_dicoms
    if save_raw_dicoms:
        bar = alive_it(sorted(raw_dicoms.keys()))
        for protocol in bar:
            bar.text("Saving raw_dicom for protocol: " + protocol)
            if raw_dicoms[protocol]:
                logger.info(f"Saving raw_dicom for protocol {protocol}")
                if not saveRawDicoms(raw_dicom = raw_dicoms[protocol], \
                                        save_path = os.path.join(save_path, "raw_dicoms", protocol)):
                    logger.error(f"Error occured in saving raw_dicoms of {protocol}.")
    #save stacked_nifti
    bar = alive_it(sorted(proc_study_dataset.keys()))
    for protocol in bar:
        bar.text("Saving stacked_nifti for protocol: " + protocol)
        if proc_study_dataset[protocol]:
            logger.info(f'Saving stacked_nifti protocol {protocol}')
            #save stacked nifti
            CIODKeyWord = list(proc_study_dataset[protocol][0]["pars"].keys())[0]
            if not globals()["_".join(["PyDicomStorageEngine",CIODKeyWord])](proc_seq_dataset = proc_study_dataset[protocol], \
                                                                                save_path = os.path.join(save_path, 'stacked_nifti'), \
                                                                                protocol = protocol):
                logger.error(f"Error occured in saving stacked_nifti of {protocol}.")
                
def PyDicomStorageEngine_MRImage(proc_seq_dataset: List,
                                 save_path: Union[str, Path, os.PathLike],
                                 protocol: str):
    try:
        logger = logging.getLogger(inspect.currentframe().f_code.co_name)
        CIODKeyWord = inspect.currentframe().f_code.co_name.split('_')[-1]
        nifti_data_path = os.path.join(save_path, "data")
        nifti_pars_path = os.path.join(save_path, "pars")
        os.makedirs(nifti_data_path, exist_ok = True)
        os.makedirs(nifti_pars_path, exist_ok = True)
        for slice_package_idx, slice_package in enumerate(proc_seq_dataset):
            try:
                PixelSpacing = slice_package["pars"][CIODKeyWord]["ImagePlane"]["PixelSpacing"]
                ImageOrientationPatient = slice_package["pars"][CIODKeyWord]["ImagePlane"]["ImageOrientationPatient"]
                ImagePositionPatient = slice_package["pars"][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"]
                SpacingBetweenSlices = slice_package["pars"][CIODKeyWord]["ImagePlane"]["SpacingBetweenSlices"]
                affine_matrix = np.zeros((4,4))
                #PixelSpacing check
                if not isinstance(PixelSpacing, pydicom.multival.MultiValue):
                    if np.max([np.sqrt(np.sum(np.square(np.array(PixelSpacing[slice_id]) - np.array(PixelSpacing[slice_id-1])))) for slice_id in range(1, len(PixelSpacing))]) < 1e-3:
                        PixelSpacing = PixelSpacing[0][0][0]
                    else:
                        raise ValueError(f"{len(PixelSpacing)} PixelSpacing were found with different value")
                #ImageOrientationPatient check
                if isinstance(ImageOrientationPatient, List):
                    if np.max([np.sqrt(np.sum(np.square(np.array(ImageOrientationPatient[slice_id]) - np.array(ImageOrientationPatient[slice_id-1])))) for slice_id in range(1, len(ImageOrientationPatient))]) < 1e-5:
                        ImageOrientationPatient = ImageOrientationPatient[0][0][0]
                    else:
                        raise ValueError(f"{len(ImageOrientationPatient)} ImageOrientationPatient were found with different value")
                #ImagePositionPatient check
                if isinstance(ImagePositionPatient, List):
                    ImagePositionPatient = np.array(ImagePositionPatient[0][0][0])
                elif isinstance(ImagePositionPatient, pydicom.multival.MultiValue):
                    ImagePositionPatient = np.array(ImagePositionPatient)
                #SpacingBetweenSlices check
                if isinstance(SpacingBetweenSlices, List):
                    if np.max([np.sqrt(np.sum(np.square(np.array(SpacingBetweenSlices[slice_id]) - np.array(SpacingBetweenSlices[slice_id-1])))) for slice_id in range(1, len(SpacingBetweenSlices))]) < 1e-3:
                        SpacingBetweenSlices = SpacingBetweenSlices[0][0][0]
                    else:
                        raise ValueError(f"{len(SpacingBetweenSlices)} ImageOrientationPatient were found with different value")
                affine_matrix[:3,0] = np.array(ImageOrientationPatient[:3]) * PixelSpacing[0]
                affine_matrix[:3,1] = np.array(ImageOrientationPatient[3:]) * PixelSpacing[1]
                affine_matrix[:3,2] = np.cross(ImageOrientationPatient[:3], ImageOrientationPatient[3:]) * SpacingBetweenSlices
                affine_matrix[:3,3] = np.array(ImagePositionPatient)
                affine_matrix[3,3] = 1
                affine_matrix = np.diag([-1,-1,1,1]).dot(affine_matrix)
                nifti_filename = protocol
                if len(proc_seq_dataset) > 1:
                    nifti_filename = nifti_filename + '_spack' + str(slice_package_idx)
                #dump slice package data
                fileExistCheck(os.path.join(nifti_data_path, nifti_filename + '.nii.gz'), logger)
                dump_nifti(nifti_path = os.path.join(nifti_data_path, nifti_filename + '.nii.gz'),
                        affine_matrix = affine_matrix,
                        ndarray = slice_package["data"])
                #dump slice pars
                fileExistCheck(os.path.join(nifti_pars_path, nifti_filename + '.pkl'), logger)
                pickle_dump(obj = slice_package["pars"],
                        path = os.path.join(nifti_pars_path, nifti_filename + '.pkl'))
            except Exception as exception:
                logger.error(exception)
                continue
        return True
    except Exception as exception:
        logger.error(exception)
        return False

def PyDicomStorageEngine_CTImage(proc_seq_dataset: List,
                                 save_path: Union[str, Path, os.PathLike],
                                 protocol: str):
    try:
        logger = logging.getLogger(inspect.currentframe().f_code.co_name)
        CIODKeyWord = inspect.currentframe().f_code.co_name.split('_')[-1]
        nifti_data_path = os.path.join(save_path, "data")
        nifti_pars_path = os.path.join(save_path, "pars")
        os.makedirs(nifti_data_path, exist_ok = True)
        os.makedirs(nifti_pars_path, exist_ok = True)
        for slice_package_idx, slice_package in enumerate(proc_seq_dataset):
            try:
                PixelSpacing = slice_package["pars"][CIODKeyWord]["ImagePlane"]["PixelSpacing"]
                ImageOrientationPatient = slice_package["pars"][CIODKeyWord]["ImagePlane"]["ImageOrientationPatient"]
                ImagePositionPatient = slice_package["pars"][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"]
                SpacingBetweenSlices = slice_package["pars"][CIODKeyWord]["ImagePlane"]["SpacingBetweenSlices"]
                #PixelSpacing check
                if not isinstance(PixelSpacing, pydicom.multival.MultiValue):
                    if np.max([np.sqrt(np.sum(np.square(np.array(PixelSpacing[slice_id]) - np.array(PixelSpacing[slice_id-1])))) for slice_id in range(1, len(PixelSpacing))]) < 1e-3:
                        PixelSpacing = PixelSpacing[0][0][0]
                    else:
                        raise ValueError(f"{len(PixelSpacing)} PixelSpacing were found with different value")
                #ImageOrientationPatient check
                if isinstance(ImageOrientationPatient, List):
                    if np.max([np.sqrt(np.sum(np.square(np.array(ImageOrientationPatient[slice_id]) - np.array(ImageOrientationPatient[slice_id-1])))) for slice_id in range(1, len(ImageOrientationPatient))]) < 1e-5:
                        ImageOrientationPatient = ImageOrientationPatient[0][0][0]
                    else:
                        raise ValueError(f"{len(ImageOrientationPatient)} ImageOrientationPatient were found with different value")
                #ImagePositionPatient check
                if isinstance(ImagePositionPatient, List):
                    ImagePositionPatient = np.array(ImagePositionPatient[0][0][0])
                elif isinstance(ImagePositionPatient, pydicom.multival.MultiValue):
                    ImagePositionPatient = np.array(ImagePositionPatient)
                #SpacingBetweenSlices check
                if isinstance(SpacingBetweenSlices, List):
                    if np.max([np.sqrt(np.sum(np.square(np.array(SpacingBetweenSlices[slice_id]) - np.array(SpacingBetweenSlices[slice_id-1])))) for slice_id in range(1, len(SpacingBetweenSlices))]) < 1e-3:
                        SpacingBetweenSlices = SpacingBetweenSlices[0][0][0]
                    else:
                        raise ValueError(f"{len(SpacingBetweenSlices)} ImageOrientationPatient were found with different value")
                affine_matrix = np.zeros((4,4))
                affine_matrix[:3,0] = np.array(ImageOrientationPatient[:3]) * PixelSpacing[0]
                affine_matrix[:3,1] = np.array(ImageOrientationPatient[3:]) * PixelSpacing[1]
                affine_matrix[:3,2] = np.cross(ImageOrientationPatient[:3], ImageOrientationPatient[3:]) * SpacingBetweenSlices
                # TODO: BUG to be fixed by ITKSnap
                # affine_matrix[:3,3] = np.array(ImagePositionPatient)
                affine_matrix[3,3] = 1
                affine_matrix = np.diag([-1,-1,1,1]).dot(affine_matrix)
                nifti_filename = protocol
                if len(proc_seq_dataset) > 1:
                    nifti_filename = nifti_filename + '_spack' + str(slice_package_idx)
                #dump slice package data
                fileExistCheck(os.path.join(nifti_data_path, nifti_filename + '.nii.gz'), logger)
                dump_nifti(nifti_path = os.path.join(nifti_data_path, nifti_filename + '.nii.gz'),
                        affine_matrix = affine_matrix,
                        ndarray = slice_package["data"])
                #dump slice pars
                fileExistCheck(os.path.join(nifti_pars_path, nifti_filename + '.pkl'), logger)
                pickle_dump(obj = slice_package["pars"],
                    path = os.path.join(nifti_pars_path, nifti_filename + '.pkl'))
            except Exception as exception:
                logger.error(exception)
                continue
        return True
    except Exception as exception:
        logger.error(exception)
        return False
        
def PyDicomGroupingSummary_main(proc_study_dataset: dict,
                                study_cache: dict):
    try:
        logger = logging.getLogger(inspect.currentframe().f_code.co_name)
        sequences_pars_list = []
        study_cache["sequences"] = dict()
        #double check
        for protocol in proc_study_dataset.keys():
            try:
                logger.info(f'Summarizing protocol {protocol}')
                #save stacked nifti
                CIODKeyWord = list(proc_study_dataset[protocol][0]["pars"].keys())[0]
                sequence_pars = dict()
                sequence_pars = globals()["_".join(["PyDicomGroupingSummary",CIODKeyWord])](slice_packages = proc_study_dataset[protocol])
                if sequence_pars:
                    sequences_pars_list.append(sequence_pars) #to be merged
                else:
                    raise ValueError(f"error in generating grouping summary of protocol {protocol}")
                sequence_prop = globals()["_".join(["extractSequencesProperty",CIODKeyWord])](slice_packages = proc_study_dataset[protocol])
                if sequence_prop:
                    study_cache["sequences"][protocol] = dict()
                    study_cache["sequences"][protocol]["property"] = sequence_prop
                else:
                    raise ValueError(f"error in extract sequence property of protocol {protocol}")
            except Exception as exception:
                logger.error(exception)
                continue
        if sequences_pars_list:
            study_pars = mergeParsDict(sequences_pars_list)
            study_cache["study_pars"] = study_pars
        return True
    except Exception as exception:
        logger.error(exception)
        return False

def PyDicomGroupingSummary_MRImage(slice_packages: List):
    try:
        CIODKeyWord = inspect.currentframe().f_code.co_name.split('_')[-1]
        logger = logging.getLogger(inspect.currentframe().f_code.co_name)
        slice_packages_pars_list = []
        for slice_package in slice_packages:
            try:
                slice_package_pars = dict()
                #patient Module
                slice_package_pars["PatientName"] = slice_package["pars"][CIODKeyWord]["Patient"]["PatientName"].original_string.decode()
                slice_package_pars["PatientID"] = slice_package["pars"][CIODKeyWord]["Patient"]["PatientID"]
                slice_package_pars["PatientBirthDate"] = slice_package["pars"][CIODKeyWord]["Patient"]["PatientBirthDate"]
                slice_package_pars["PatientSex"] = slice_package["pars"][CIODKeyWord]["Patient"]["PatientSex"]
                #patientStudy Module
                slice_package_pars["PatientAge"] = slice_package["pars"][CIODKeyWord]["PatientStudy"]["PatientAge"]
                slice_package_pars["PatientWeight"] = slice_package["pars"][CIODKeyWord]["PatientStudy"]["PatientWeight"]
                slice_package_pars["PregnancyStatus"] = slice_package["pars"][CIODKeyWord]["PatientStudy"]["PregnancyStatus"]
                #GeneralStudy Module
                slice_package_pars["StudyInstanceUID"] = slice_package["pars"][CIODKeyWord]["GeneralStudy"]["StudyInstanceUID"]
                slice_package_pars["AccessionNumber"] = slice_package["pars"][CIODKeyWord]["GeneralStudy"]["AccessionNumber"]
                slice_package_pars["StudyID"] = slice_package["pars"][CIODKeyWord]["GeneralStudy"]["StudyID"]
                #GeneralSeries Module
                slice_package_pars["Modality"] = slice_package["pars"][CIODKeyWord]["GeneralSeries"]["Modality"]
                slice_package_pars["BodyPartExamined"] = slice_package["pars"][CIODKeyWord]["GeneralSeries"]["BodyPartExamined"]
                #GeneralEquipment Module
                slice_package_pars["Manufacturer"] = slice_package["pars"][CIODKeyWord]["GeneralEquipment"]["Manufacturer"]
                slice_package_pars["InstitutionName"] = slice_package["pars"][CIODKeyWord]["GeneralEquipment"]["InstitutionName"]
                slice_package_pars["StationName"] = slice_package["pars"][CIODKeyWord]["GeneralEquipment"]["StationName"]
                slice_package_pars["InstitutionalDepartmentName"] = slice_package["pars"][CIODKeyWord]["GeneralEquipment"]["InstitutionalDepartmentName"]
                slice_package_pars["ManufacturerModelName"] = slice_package["pars"][CIODKeyWord]["GeneralEquipment"]["ManufacturerModelName"]
                #MRImage Module
                slice_package_pars["MagneticFieldStrength"] = slice_package["pars"][CIODKeyWord]["MRImage"]["MagneticFieldStrength"]
                slice_packages_pars_list.append(slice_package_pars)
            except Exception as exception:
                logger.error(exception)
                continue
        #merge slice-package dict
        sequence_pars = mergeParsDict(slice_packages_pars_list)
        for key, value in sequence_pars.items():
            if isinstance(value, List):
                raise ValueError(f'{key} is expected to be same in slice-packages.')
        return sequence_pars
    except Exception as exception:
        logger.error(exception)
        return False

def PyDicomGroupingSummary_CTImage(slice_packages: List):
    try:
        CIODKeyWord = inspect.currentframe().f_code.co_name.split('_')[-1]
        logger = logging.getLogger(inspect.currentframe().f_code.co_name)
        slice_packages_pars_list = []
        for slice_package in slice_packages:
            try:
                slice_package_pars = dict()
                #patient Module
                slice_package_pars["PatientName"] = slice_package["pars"][CIODKeyWord]["Patient"]["PatientName"].original_string.decode()
                slice_package_pars["PatientID"] = slice_package["pars"][CIODKeyWord]["Patient"]["PatientID"]
                slice_package_pars["PatientBirthDate"] = slice_package["pars"][CIODKeyWord]["Patient"]["PatientBirthDate"]
                slice_package_pars["PatientSex"] = slice_package["pars"][CIODKeyWord]["Patient"]["PatientSex"]
                #patientStudy Module
                slice_package_pars["PatientAge"] = slice_package["pars"][CIODKeyWord]["PatientStudy"]["PatientAge"]
                slice_package_pars["PatientWeight"] = slice_package["pars"][CIODKeyWord]["PatientStudy"]["PatientWeight"]
                slice_package_pars["PregnancyStatus"] = slice_package["pars"][CIODKeyWord]["PatientStudy"]["PregnancyStatus"]
                #GeneralStudy Module
                slice_package_pars["StudyInstanceUID"] = slice_package["pars"][CIODKeyWord]["GeneralStudy"]["StudyInstanceUID"]
                slice_package_pars["AccessionNumber"] = slice_package["pars"][CIODKeyWord]["GeneralStudy"]["AccessionNumber"]
                slice_package_pars["StudyID"] = slice_package["pars"][CIODKeyWord]["GeneralStudy"]["StudyID"]
                #GeneralSeries Module
                slice_package_pars["Modality"] = slice_package["pars"][CIODKeyWord]["GeneralSeries"]["Modality"]
                slice_package_pars["BodyPartExamined"] = slice_package["pars"][CIODKeyWord]["GeneralSeries"]["BodyPartExamined"]
                #GeneralEquipment Module
                slice_package_pars["Manufacturer"] = slice_package["pars"][CIODKeyWord]["GeneralEquipment"]["Manufacturer"]
                slice_package_pars["InstitutionName"] = slice_package["pars"][CIODKeyWord]["GeneralEquipment"]["InstitutionName"]
                slice_package_pars["StationName"] = slice_package["pars"][CIODKeyWord]["GeneralEquipment"]["StationName"]
                slice_package_pars["InstitutionalDepartmentName"] = slice_package["pars"][CIODKeyWord]["GeneralEquipment"]["InstitutionalDepartmentName"]
                slice_package_pars["ManufacturerModelName"] = slice_package["pars"][CIODKeyWord]["GeneralEquipment"]["ManufacturerModelName"]
                #MRImage Module
                slice_package_pars["SingleCollimationWidth"] = slice_package["pars"][CIODKeyWord]["CTImage"]["SingleCollimationWidth"]
                slice_package_pars["TotalCollimationWidth"] = slice_package["pars"][CIODKeyWord]["CTImage"]["TotalCollimationWidth"]
                if slice_package_pars["SingleCollimationWidth"] !="" and slice_package_pars["TotalCollimationWidth"] != "":
                    slice_package_pars["NumberOfDetectorRows"] = int(slice_package_pars["TotalCollimationWidth"]/slice_package_pars["SingleCollimationWidth"])
                else:
                    slice_package_pars["NumberOfDetectorRows"] = "unknow"
                slice_packages_pars_list.append(slice_package_pars)
            except Exception as exception:
                logger.error(exception)
                continue
        #merge slice-package dict
        sequence_pars = mergeParsDict(slice_packages_pars_list)
        for key, value in sequence_pars.items():
            if isinstance(value, List):
                raise ValueError(f'{key} is expected to be same in slice-packages.')
        return sequence_pars
    except Exception as exception:
        logger.error(exception)
        return False

def extractSequencesProperty_CTImage(slice_packages: List):
    try:
        CIODKeyWord = inspect.currentframe().f_code.co_name.split('_')[-1]
        logger = logging.getLogger(inspect.currentframe().f_code.co_name)
        slice_packages_property = dict()
        slice_packages_property["slice_package_property"] = []
        slice_package_property = None
        #configure standard dixon quant map
        for slice_package in slice_packages:
            slice_package_property = globals()["_".join(["extractSequenceProperty",CIODKeyWord])](slice_package)
            if slice_package_property:
                slice_packages_property["slice_package_property"].append(slice_package_property)
            else:
                raise ValueError("Error occured in extracting sequences properties.")
        slice_packages_property["SeriesDescription"] = slice_packages[0]["pars"][CIODKeyWord]["GeneralSeries"]["SeriesDescription"]
        slice_packages_property["SeriesDate"] = slice_packages[0]["pars"][CIODKeyWord]["GeneralSeries"]["SeriesDate"]
        slice_packages_property["SeriesTime"] = slice_packages[0]["pars"][CIODKeyWord]["GeneralSeries"]["SeriesTime"]
        slice_packages_property["SeriesInstanceUID"] = slice_packages[0]["pars"][CIODKeyWord]["GeneralSeries"]["SeriesInstanceUID"]
        slice_packages_property["BodyPartExamined"] = slice_packages[0]["pars"][CIODKeyWord]["GeneralSeries"]["BodyPartExamined"]
        slice_packages_property["orientation"] = slice_package_property["orientation"]
        slice_packages_property["SliceThickness"] = slice_package_property["SliceThickness"]
        slice_packages_property["slice_package_type"] = slice_package_property["slice_package_type"]
        
        return slice_packages_property
    except Exception as exception:
        logger.error(exception)
        return False

def extractSequenceProperty_CTImage(slice_package: dict):
    CIODKeyWord = inspect.currentframe().f_code.co_name.split('_')[-1]
    #in case GE with similar image Orientation
    if isinstance(slice_package["pars"][CIODKeyWord]["ImagePlane"]["ImageOrientationPatient"][0], List):
        # if multiple similar image orientation, we update to mean orientation
        slice_package["pars"][CIODKeyWord]["ImagePlane"]["ImageOrientationPatient"] = np.mean(slice_package["pars"][CIODKeyWord]["ImagePlane"]["ImageOrientationPatient"],axis = (0,1,2))

    image_oris = calc_image_ori(slice_package["pars"][CIODKeyWord]["ImagePlane"]["ImageOrientationPatient"])[0]
    SliceThickness = slice_package["pars"][CIODKeyWord]["ImagePlane"]["SliceThickness"]
    #init output
    slice_package_property = dict()
    slice_package_property["orientation"] = image_oris
    slice_package_property["SliceThickness"] = SliceThickness
    if slice_package["data"].shape[4] > 1: # more than one dynamics
        slice_package_property["slice_package_type"] = "multi_dynamics"
    else:
        slice_package_property["slice_package_type"] = "single_dynamics"
    return slice_package_property

def extractSequencesProperty_MRImage(slice_packages: List):
    try:
        CIODKeyWord = inspect.currentframe().f_code.co_name.split('_')[-1]
        logger = logging.getLogger(inspect.currentframe().f_code.co_name)
        slice_packages_property = dict()
        slice_packages_property["slice_package_property"] = []
        slice_packages_property["SeriesDescription"] = slice_packages[0]["pars"][CIODKeyWord]["GeneralSeries"]["SeriesDescription"]
        slice_packages_property["SeriesDate"] = slice_packages[0]["pars"][CIODKeyWord]["GeneralSeries"]["SeriesDate"]
        slice_packages_property["SeriesTime"] = slice_packages[0]["pars"][CIODKeyWord]["GeneralSeries"]["SeriesTime"]
        slice_packages_property["SeriesInstanceUID"] = slice_packages[0]["pars"][CIODKeyWord]["GeneralSeries"]["SeriesInstanceUID"]
        slice_package_property = None
        #configure standard dixon quant map
        for slice_package in slice_packages:
            slice_package_property = globals()["_".join(["extractSequenceProperty",CIODKeyWord])](slice_package)
            if slice_package_property:
                slice_packages_property["slice_package_property"].append(slice_package_property)
            else:
                raise ValueError("Error occured in extracting sequences properties.")
        if len(slice_packages) > 1:
            MRAcquisitionTypes = list(set([slice_package_property["MRAcquisitionType"] for slice_package_property in slice_packages_property["slice_package_property"]]))
            slice_package_types = [list(item) for item in dict.fromkeys(tuple(slice_package_property["slice_package_type"]) for slice_package_property in slice_packages_property["slice_package_property"])]
            orientations = list(set([slice_package_property["orientation"] for slice_package_property in slice_packages_property["slice_package_property"]]))
            #same MRAcquisitionType, same slice_package_type and more than one orientation
            if len(orientations) > 1 and len(MRAcquisitionTypes) == 1 and len(slice_package_types) == 1 and len(orientations) == len(slice_packages):
                slice_packages_property["orientation"] = orientations
                slice_packages_property["MRAcquisitionType"] = MRAcquisitionTypes[0]
                slice_packages_property["slice_package_type"] = "Localizer"
        elif len(slice_packages) == 1:
            slice_packages_property["orientation"] = slice_package_property["orientation"]
            slice_packages_property["MRAcquisitionType"] = slice_package_property["MRAcquisitionType"]
            slice_packages_property["slice_package_type"] = slice_package_property["slice_package_type"]
        return slice_packages_property
    except Exception as exception:
        logger.error(exception)
        return False

def extractSequenceProperty_MRImage(slice_package: dict):
    try:
        CIODKeyWord = inspect.currentframe().f_code.co_name.split('_')[-1]
        logger = logging.getLogger(inspect.currentframe().f_code.co_name)
        #in case GE with similar image Orientation
        if isinstance(slice_package["pars"][CIODKeyWord]["ImagePlane"]["ImageOrientationPatient"][0], List):
            # if multiple similar image orientation, we update to mean orientation
            slice_package["pars"][CIODKeyWord]["ImagePlane"]["ImageOrientationPatient"] = np.mean(slice_package["pars"][CIODKeyWord]["ImagePlane"]["ImageOrientationPatient"],axis = (0,1,2))

        image_oris = calc_image_ori(slice_package["pars"][CIODKeyWord]["ImagePlane"]["ImageOrientationPatient"])[0]
        Manufacturer = slice_package["pars"][CIODKeyWord]["GeneralEquipment"]["Manufacturer"]
        ImageType = slice_package["pars"][CIODKeyWord]["GeneralImage"]["ImageType"]
        if isinstance(ImageType, List):
            ImageType = [list(item) for item in dict.fromkeys([tuple(temposition) for slices in slice_package["pars"][CIODKeyWord]["MRImage"]["ImageType"] for modality in slices for temposition in modality])]
        ScanningSequence = slice_package["pars"][CIODKeyWord]["MRImage"]["ScanningSequence"]
        MRAcquisitionType = slice_package["pars"][CIODKeyWord]["MRImage"]["MRAcquisitionType"]
        SequenceName = slice_package["pars"][CIODKeyWord]["MRImage"]["SequenceName"]
        ScanOptions = slice_package["pars"][CIODKeyWord]["MRImage"]["ScanOptions"]
        SeriesDescription = slice_package["pars"][CIODKeyWord]["GeneralSeries"]["SeriesDescription"]
        StandardDixonQuantImageType = ["W","F","IP","OP","T2_STAR","R2_STAR","FF"]
        AcquisitionContrast = slice_package["pars"][CIODKeyWord]["VendorPrivateModule"]["AcquisitionContrast"]
        if isinstance(AcquisitionContrast, List):
            AcquisitionContrast = list(set([temposition for slices in slice_package["pars"][CIODKeyWord]["VendorPrivateModule"]["AcquisitionContrast"] for modality in slices for temposition in modality]))
        if "Philips" in Manufacturer:
            MRImageTypeMR = slice_package["pars"][CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"]
            if isinstance(MRImageTypeMR, List):
                MRImageTypeMR = list(set([temposition for slices in slice_package["pars"][CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"] for modality in slices for temposition in modality]))
        #init output
        slice_package_property = dict()
        slice_package_property["orientation"] = image_oris
        slice_package_property["MRAcquisitionType"] = MRAcquisitionType
        slice_package_property["slice_package_type"] = []

        #Fat saturation type
        if "Philips" in Manufacturer or "UIH" in Manufacturer or "GE" in Manufacturer:
            if "FS" in ScanOptions:
                slice_package_property["slice_package_type"].append("FS")
        elif "SIEMENS" in Manufacturer:
            if "SFS" in ScanOptions or "SAT2" in ScanOptions:
                slice_package_property["slice_package_type"].append("FS")
        #Image Contrast Type
        if not isinstance(AcquisitionContrast, List) and AcquisitionContrast != "":
            if AcquisitionContrast == "T1":
                if "Philips" in Manufacturer:
                    if "M" in MRImageTypeMR and "T1" in MRImageTypeMR:
                        slice_package_property["slice_package_type"].append("T1 Mapping")
                    else:
                        slice_package_property["slice_package_type"].append("Unknow")
                else:
                    slice_package_property["slice_package_type"].append("T1WI")
            elif AcquisitionContrast == "T2":
                slice_package_property["slice_package_type"].append("T2WI")
            elif AcquisitionContrast == "DIFFUSION":
                slice_package_property["slice_package_type"].append("DWI")
            elif AcquisitionContrast == "PROTON_DENSITY":
                if "Philips" in Manufacturer:
                    if "APTW" in MRImageTypeMR and "M" in MRImageTypeMR:
                        slice_package_property["slice_package_type"].append("APTW")
                    else:
                        slice_package_property["slice_package_type"].append("Unknow")
                else:
                    slice_package_property["slice_package_type"].append("PROTON_DENSITY")
            else:
                slice_package_property["slice_package_type"].append("Unknow")
                raise ValueError
        elif isinstance(AcquisitionContrast, List):
            if "PROTON_DENSITY" in AcquisitionContrast and "T2" in AcquisitionContrast:
                if "M" in MRImageTypeMR and ("T2" in MRImageTypeMR or "R2" in MRImageTypeMR):
                    slice_package_property["slice_package_type"].append("T2 Mapping")
        else:
            #if Scanner parameter is not avaliable, use the derived one
            if isinstance(ImageType, pydicom.multival.MultiValue):
                if "Philips" in Manufacturer:
                    PhilipsDixonQuantImageTypeList = ["W","F","IP","OP","T2_STAR","R2_STAR","FF"]
                    # T2WI + DWI
                    if "SE" in ScanningSequence or "RM" in ScanningSequence: # magnitude SE images
                        if isinstance(slice_package["pars"][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"], float) and \
                            slice_package["pars"][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"] == 0.0:
                                slice_package_property["slice_package_type"].append("T2WI")
                        elif (isinstance(slice_package["pars"][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"], float) and \
                            slice_package["pars"][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"] > 0) or \
                            isinstance(slice_package["pars"][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"], List):
                            slice_package_property["slice_package_type"].append("DWI")
                    elif "GR" in ScanningSequence or "RM" in ScanningSequence:
                        if any([item in PhilipsDixonQuantImageTypeList for item in ImageType]) and "DERIVED" in ImageType:
                            slice_package_property["slice_package_type"].append("Dixon " + "[" +  ImageType[[item in PhilipsDixonQuantImageTypeList for item in ImageType].index(True)] + "]")
                        else:
                            slice_package_property["slice_package_type"].append("T1WI")
                    elif "IR" in ScanningSequence:
                        slice_package_property["slice_package_type"].append("T1WI")
                    elif "EP" in ScanningSequence:
                        slice_package_property["slice_package_type"].append("DWI")
                    else:
                        slice_package_property["slice_package_type"].append("unknow")
                        raise ValueError
                elif "UIH" in Manufacturer:
                    # GRE 3D and T2WI all have one imageType
                    UIHQuantImageType = ["W", "F", "IP", "OP"]
                    if ((ScanningSequence!="" and ScanningSequence!="NONE" and "SE" in ScanningSequence) or "fse" in SequenceName or "grase" in SequenceName) and "EP" not in ScanningSequence:
                        slice_package_property["slice_package_type"].append("T2WI")
                    elif "GR" in ScanningSequence or "IR" in ScanningSequence:
                        if any([item in UIHQuantImageType for item in ImageType]):
                            slice_package_property["slice_package_type"].append("Dixon " + "[" + ImageType[[item in UIHQuantImageType for item in ImageType].index(True)] + "]")
                        else:
                            slice_package_property["slice_package_type"].append("T1WI")
                    elif "EP" in ScanningSequence:
                        slice_package_property["slice_package_type"].append("DWI")

                    else:
                        slice_package_property["slice_package_type"] = "unknow"
                        raise ValueError
                elif "SIEMENS" in Manufacturer:
                    SIEMENSQuantImageType = ["WATER", "FAT", "IN_PHASE", "OUT_PHASE"]
                    #T2WI
                    if "SE" in ScanningSequence and "EP" not in ScanningSequence and "DIFFUSION" not in ImageType:
                        slice_package_property["slice_package_type"].append("T2WI")
                    #Dixon or T1WI
                    elif "GR" in ScanningSequence or "IR" in ScanningSequence:
                        if any([item in SIEMENSQuantImageType for item in ImageType]):
                            slice_package_property["slice_package_type"].append("Dixon " + "[" + StandardDixonQuantImageType[SIEMENSQuantImageType.index(ImageType[[item in SIEMENSQuantImageType for item in ImageType].index(True)])] + "]")
                        else:
                            slice_package_property["slice_package_type"].append("T1WI")
                    #DWI
                    elif "EP" in ScanningSequence and "DIFFUSION" in ImageType:
                        slice_package_property["slice_package_type"].append("DWI")
                    else:
                        slice_package_property["slice_package_type"] = "unknow"
                        raise ValueError
                elif "GE" in Manufacturer:
                    #multi-echo fse scan, i.e. T2WI
                    if ("SE" in ScanningSequence or "RM" in ScanningSequence) and "EPI_GEMS" not in ScanOptions:
                        slice_package_property["slice_package_type"].append("T2WI")
                    #Dixon scan
                    elif "GR" in ScanningSequence:
                        if "FLEX_GEMS" in ScanOptions:
                            SeriesDescription = slice_package["pars"][CIODKeyWord]["GeneralSeries"]["SeriesDescription"]
                            GEQuantImageTypes = ["WATER", "FAT", "InPhase", "OutPhase"]
                            if any([GEQuantImageType in  SeriesDescription for GEQuantImageType in GEQuantImageTypes]):
                                slice_package_property["slice_package_type"].append("Dixon " + "[" + StandardDixonQuantImageType[[GEQuantImageType in  SeriesDescription for GEQuantImageType in GEQuantImageTypes].index(True)] + "]")
                        else:
                            slice_package_property["slice_package_type"].append("T1WI")
                    elif "EP" in ScanningSequence and "EPI_GEMS" in ScanOptions:
                        slice_package_property["slice_package_type"].append("DWI")
                    else:
                        slice_package_property["slice_package_type"] = "unknow"
                        raise ValueError
            elif isinstance(ImageType, List):
                if "Philips" in Manufacturer:
                    PhilipsDixonQuantImageTypeList = ['W','F','IP','OP','T2_STAR','R2_STAR','FF']
                    unique_ImageTypes = [list(item) for item in dict.fromkeys(tuple(item) for item in [temposition for slices in ImageType for modality in slices for temposition in modality])]
                    unique_MRImageTypeMR = [list(item) for item in dict.fromkeys(tuple(item) for item in [temposition for slices in slice_package["pars"][CIODKeyWord]["VendorPrivateModule"]["MRImageTypeMR"] for modality in slices for temposition in modality])]
                    if all([any([item in PhilipsDixonQuantImageTypeList for item in unique_ImageType]) for unique_ImageType in unique_ImageTypes]) and all(["DERIVED" in unique_ImageType for unique_ImageType in unique_ImageTypes]):
                            modality = [unique_ImageType[[ImageTypeItem in PhilipsDixonQuantImageTypeList for ImageTypeItem in unique_ImageType].index(True)] for unique_ImageType in unique_ImageTypes]
                            slice_package_property["slice_package_type"].append("Dixon " + "[" + ",".join(modality) + "]")
                    elif "M" in unique_MRImageTypeMR and "APTW" in unique_MRImageTypeMR:
                        slice_package_property["slice_package_type"].append("APTW")
                    elif "M" in unique_MRImageTypeMR and "T1" in unique_MRImageTypeMR:
                        slice_package_property["slice_package_type"].append("T1 Mapping")
                    elif "M" in unique_MRImageTypeMR and ("R2" in unique_MRImageTypeMR or "T2" in unique_MRImageTypeMR):
                        slice_package_property["slice_package_type"].append("T2 Mapping")
                    else:
                        slice_package_property["slice_package_type"] = "unknow"
            else:
                raise ValueError
        #Post processing check
        if isinstance(ImageType, pydicom.multival.MultiValue):
            if "DWI" in slice_package_property["slice_package_type"]:
                if "ADC" in ImageType or "EADC" in ImageType:
                    slice_package_property["slice_package_type"].append("ADC")
            if "REFORMATTED" in ImageType:
                slice_package_property["slice_package_type"].append("REFORMATTED")
            if "MPR" in ImageType:
                slice_package_property["slice_package_type"].append("MPR")
            if "PROJECTION IMAGE" in ImageType:
                slice_package_property["slice_package_type"].append("PROJECTION IMAGE")
        elif isinstance(ImageType, List):
            if all(["REFORMATTED" in item for item in ImageType]):
                slice_package_property["slice_package_type"].append("REFORMATTED")
            if all(["MPR" in item for item in ImageType]):
                slice_package_property["slice_package_type"].append("MPR")
            if all(["PROJECTION IMAGE" in item for item in ImageType]):
                slice_package_property["slice_package_type"].append("PROJECTION IMAGE")                
        return slice_package_property
    except Exception as exception:
        logger.error(exception)
        return False




