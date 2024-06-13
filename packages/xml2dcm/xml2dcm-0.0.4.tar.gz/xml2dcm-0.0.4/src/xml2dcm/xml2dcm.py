import os
import base64
import xml.etree.ElementTree as ET
import numpy as np
import pydicom
from pydicom.dataset import Dataset, FileDataset
from pydicom.sequence import Sequence
from pydicom.uid import ExplicitVRLittleEndian, generate_uid, PYDICOM_IMPLEMENTATION_UID
from datetime import datetime
import traceback

def create_dicom_file(xml_file_path, output_folder = 'generated_dicom_from_xml'):
    """
    Converts an XML file containing ECG data into a DICOM file format. The function 
    checks for the necessary XML elements, parses patient and test data, and uses this
    information to construct a DICOM file with ECG waveform data.

    Input:
        xml_file_path: str - The path to the XML file containing the ECG data.
        output_folder: str, optional - The directory where the generated DICOM file will be saved.
                                      Defaults to 'generated_dicom_from_xml'.

    Output:
        None - The DICOM file is written to the specified output folder. If the file already
               exists, the function will skip writing and print a message. If there is an error
               during processing, it will print an error message.
    """
    # Check if the output folder exists, create if not
    os.makedirs('generated_dicom_from_xml', exist_ok=True)
    
    # Lists of expected and derived ECG leads
    expected_leads = ['I', 'II', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
    derived_leads = ['III', 'aVR', 'aVL', 'aVF']
    final_leads = expected_leads + derived_leads

    # functions to format date and time from strings
    def format_date(date_str):
        return datetime.strptime(date_str, '%m-%d-%Y').strftime('%Y%m%d') if date_str is not None else None

    def format_time(time_str):
        return time_str.replace(':', '') if time_str is not None else None

    # Extract text from an XML element
    def safe_find_text(element, path):
        found = element.find(path)
        return found.text if found is not None else None

    try:
        output_file_name = f"{os.path.splitext(os.path.basename(xml_file_path))[0]}.dcm"
        output_file_path = os.path.join(output_folder, output_file_name)
        
        # Skip if DICOM file already exists
        if os.path.exists(output_file_path):
            print(f'File {output_file_path} already exists. Skipping...')
            return
        print(f'File {output_file_path} adding')
        
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        patient_info = root.find('.//PatientDemographics')
        test_info = root.find('.//TestDemographics')
        
        # Processing date and time information
        edit_date = format_date(safe_find_text(test_info, 'EditDate'))
        acquisition_date = format_date(safe_find_text(test_info, 'AcquisitionDate'))
        edit_time = format_time(safe_find_text(test_info, 'EditTime'))
        acquisition_time = format_time(safe_find_text(test_info, 'AcquisitionTime'))
        acquisition_datetime = acquisition_date + acquisition_time

        # Parse XML and collect lead data
        lead_data = {}
        for lead_element in tree.iter('LeadData'):
            sample_count = int(safe_find_text(lead_element, 'LeadSampleCountTotal'))
            amplitude = float(safe_find_text(lead_element, 'LeadAmplitudeUnitsPerBit'))
            lead_name = safe_find_text(lead_element, 'LeadID')

            if sample_count == 5000 and amplitude == 4.88 and lead_name in expected_leads:
                waveform_data = base64.b64decode(safe_find_text(lead_element, 'WaveFormData'))
                lead_waveform = np.frombuffer(waveform_data, dtype='<i2', count=sample_count) * amplitude
                lead_data[lead_name] = lead_waveform

        # Check if all expected leads are present
        if set(expected_leads) <= set(lead_data.keys()):
            # Calculate derived leads
            lead_data['III'] = lead_data['II'] - lead_data['I']
            lead_data['aVR'] = -(lead_data['I'] + lead_data['II']) / 2
            lead_data['aVL'] = lead_data['I'] - lead_data['II'] / 2
            lead_data['aVF'] = lead_data['II'] - lead_data['I'] / 2

            # Add all leads to the array in the right order
            stacked_waveforms = np.stack([lead_data[lead] for lead in final_leads], axis=1)

             # Create waveform sequence item for DICOM
            file_meta = Dataset()
            file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.9.1.1'
            file_meta.MediaStorageSOPInstanceUID = generate_uid()
            file_meta.ImplementationClassUID = PYDICOM_IMPLEMENTATION_UID
            file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

            ds = FileDataset("ecg.dcm", {}, file_meta=file_meta, preamble=b"\0" * 128)
            
            # Set DICOM properties
            attributes = {
                "SpecificCharacterSet" : "ISO-8859-1",
                "PatientName": f"{safe_find_text(patient_info, 'PatientLastName')}^{safe_find_text(patient_info, 'PatientFirstName')}" if safe_find_text(patient_info, 'PatientLastName') is not None and safe_find_text(patient_info, 'PatientFirstName') is not None else None,
                "PatientID": safe_find_text(patient_info, 'PatientID'),
                "PatientAge" : f"{int(safe_find_text(patient_info, 'PatientAge')):03d}{safe_find_text(patient_info, 'AgeUnits')[0]}" if safe_find_text(patient_info, 'PatientAge') is not None and safe_find_text(patient_info, 'AgeUnits') is not None else None,
                "PatientSex": safe_find_text(patient_info, 'Gender'),
                "Modality": "ECG",
                "InstanceCreationDate": edit_date,
                "InstanceCreationTime": edit_time,
                "AcquisitionDateTime": acquisition_datetime,
                "StudyInstanceUID": generate_uid(),
                "SeriesInstanceUID": generate_uid(),
                "SOPInstanceUID": generate_uid(),
                "SOPClassUID": "12-lead ECG Waveform Storage",
                "Manufacturer": "GE HealthCare",
                "ManufacturerModelName": safe_find_text(test_info, 'AcquisitionDevice'),
                "InstitutionName": safe_find_text(test_info, 'SiteName'),
                "NameOfPhysiciansReadingStudy": f"{safe_find_text(test_info, 'OverreaderFirstName')}^{safe_find_text(test_info, 'OverreaderLastName')}" if safe_find_text(test_info, 'OverreaderFirstName') is not None and safe_find_text(test_info, 'OverreaderLastName') is not None else None,
                "StudyDescription": "ECG",
                "SoftwareVersions": safe_find_text(test_info, 'AcquisitionSoftwareVersion'),
                "CurrentPatientLocation": safe_find_text(test_info, 'LocationName'),
                "ReferringPhysicianName": safe_find_text(test_info, 'OverreaderID'),
                "StationName": safe_find_text(test_info, 'RoomID'),
                "OperatorsName": f"{safe_find_text(test_info, 'AcquisitionTechFirstName')}^{safe_find_text(test_info, 'AcquisitionTechLastName')}" if safe_find_text(test_info, 'AcquisitionTechFirstName') is not None and safe_find_text(test_info, 'AcquisitionTechLastName') is not None else None, 
            }

            for attr, value in attributes.items():
                if value is not None:
                    setattr(ds, attr, value)

            # Create waveform sequence item for DICOM
            waveform_sequence_item = Dataset()
            waveform_sequence_item.WaveformOriginality = "ORIGINAL"
            waveform_sequence_item.NumberOfWaveformChannels = 12
            waveform_sequence_item.NumberOfWaveformSamples = stacked_waveforms.shape[0]
            waveform_sequence_item.SamplingFrequency = 500.0  # Adjusted for a 10-second recording
            waveform_sequence_item.WaveformBitsAllocated = 8
            waveform_sequence_item.WaveformSampleInterpretation = 'SS'

            # Set channel definition sequence
            waveform_sequence_item.ChannelDefinitionSequence = []
            for i, lead in enumerate(final_leads):
                channel_def = Dataset()
                channel_def.ChannelSensitivity = 10
                channel_def.ChannelSensitivityUnitsSequence = [Dataset()]
                channel_def.ChannelSampleSkew = "0"
                channel_def.WaveformBitsStored = 8
                channel_def.ChannelSourceSequence = [Dataset()]
                source = channel_def.ChannelSourceSequence[0]
                source.CodeValue = str(i + 1)
                source.CodingSchemeDesignator = "PYDICOM"
                source.CodingSchemeVersion = "1.0"
                source.CodeMeaning = lead
                waveform_sequence_item.ChannelDefinitionSequence.append(channel_def)

            # Normalize and scale each lead
            scaled_waveform_array = np.stack(
                [(np.interp(lead, (lead.min(), lead.max()), (0, 255))).astype(np.int8) for lead in stacked_waveforms.T], axis=1)

            # convert to bytes for DICOM dataset
            waveform_sequence_item.WaveformData = scaled_waveform_array.tobytes()
            ds.WaveformSequence = Sequence([waveform_sequence_item])
            
            # Save DICOM file
            ds.is_little_endian = True
            ds.is_implicit_VR = False
            ds.save_as(output_file_path, write_like_original=False)

            print(f'DICOM file saved to {output_file_path}')
    except Exception as e:
        print(f'Error processing file {xml_file_path}: {e}')
        print(traceback.format_exc())


def read_dicom(dicom_path):
    """
    Reads a DICOM file from the specified path and returns the DICOM dataset. This function 
    is primarily used for accessing the underlying data within a DICOM file which includes 
    metadata and potentially images or other medical information.

    Input:
        dicom_path: str - The file path to the DICOM file that is to be read.

    Output:
        dicom_data: FileDataset - The DICOM dataset object containing all the data stored in 
                    the DICOM file. This includes patient information, imaging or waveform data, 
                    and metadata such as study details and technical parameters.
    """
    dicom_data = pydicom.dcmread(dicom_path)
    print('Dicom files are formatted as follows :\n')
    return dicom_data