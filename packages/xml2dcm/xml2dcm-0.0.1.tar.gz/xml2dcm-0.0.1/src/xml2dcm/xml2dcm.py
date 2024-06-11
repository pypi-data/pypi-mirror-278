import os
import base64
import xml.etree.ElementTree as ET
import numpy as np
import pydicom
from pydicom.dataset import Dataset, FileDataset
from pydicom.sequence import Sequence
from pydicom.uid import ExplicitVRLittleEndian, generate_uid, PYDICOM_IMPLEMENTATION_UID
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import traceback

# DICOM 파일 생성 함수
def create_dicom_file(xml_file_path, output_folder = 'generated_dicom_from_xml'):
    # 출력 폴더가 존재하지 않으면 생성
    os.makedirs('generated_dicom_from_xml', exist_ok=True)
    
    # 필요한 리드 목록
    expected_leads = ['I', 'II', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
    derived_leads = ['III', 'aVR', 'aVL', 'aVF']
    final_leads = expected_leads + derived_leads

    # 날짜와 시간 형식 변환 함수
    def format_date(date_str):
        return datetime.strptime(date_str, '%m-%d-%Y').strftime('%Y%m%d') if date_str is not None else None

    def format_time(time_str):
        return time_str.replace(':', '') if time_str is not None else None

    # 텍스트 요소를 안전하게 추출하는 함수
    def safe_find_text(element, path):
        found = element.find(path)
        return found.text if found is not None else None

    try:
        output_file_name = f"{os.path.splitext(os.path.basename(xml_file_path))[0]}.dcm"
        output_file_path = os.path.join(output_folder, output_file_name)
        
        # DICOM 파일이 이미 존재하면 건너뛰기
        if os.path.exists(output_file_path):
            print(f'File {output_file_path} already exists. Skipping...')
            return
        print(f'File {output_file_path} adding')
        
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        patient_info = root.find('.//PatientDemographics')
        test_info = root.find('.//TestDemographics')

        edit_date = format_date(safe_find_text(test_info, 'EditDate'))
        acquisition_date = format_date(safe_find_text(test_info, 'AcquisitionDate'))
        edit_time = format_time(safe_find_text(test_info, 'EditTime'))
        acquisition_time = format_time(safe_find_text(test_info, 'AcquisitionTime'))
        acquisition_datetime = acquisition_date + acquisition_time

        # XML 데이터 파싱 및 리드 데이터 수집
        lead_data = {}
        for lead_element in tree.iter('LeadData'):
            sample_count = int(safe_find_text(lead_element, 'LeadSampleCountTotal'))
            amplitude = float(safe_find_text(lead_element, 'LeadAmplitudeUnitsPerBit'))
            lead_name = safe_find_text(lead_element, 'LeadID')

            if sample_count == 5000 and amplitude == 4.88 and lead_name in expected_leads:
                waveform_data = base64.b64decode(safe_find_text(lead_element, 'WaveFormData'))
                lead_waveform = np.frombuffer(waveform_data, dtype='<i2', count=sample_count) * amplitude
                lead_data[lead_name] = lead_waveform

        # 필요한 리드가 모두 있는지 확인
        if set(expected_leads) <= set(lead_data.keys()):
            # 파생 리드 계산
            lead_data['III'] = lead_data['II'] - lead_data['I']
            lead_data['aVR'] = -(lead_data['I'] + lead_data['II']) / 2
            lead_data['aVL'] = lead_data['I'] - lead_data['II'] / 2
            lead_data['aVF'] = lead_data['II'] - lead_data['I'] / 2

            # 모든 리드를 원하는 순서로 배열에 추가
            stacked_waveforms = np.stack([lead_data[lead] for lead in final_leads], axis=1)

            # DICOM 파일 생성
            file_meta = Dataset()
            file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.9.1.1'
            file_meta.MediaStorageSOPInstanceUID = generate_uid()
            file_meta.ImplementationClassUID = PYDICOM_IMPLEMENTATION_UID
            file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

            ds = FileDataset("ecg.dcm", {}, file_meta=file_meta, preamble=b"\0" * 128)
            
            # DICOM 속성 설정
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

            # 웨이브폼 시퀀스 항목 생성
            waveform_sequence_item = Dataset()
            waveform_sequence_item.WaveformOriginality = "ORIGINAL"
            waveform_sequence_item.NumberOfWaveformChannels = 12
            waveform_sequence_item.NumberOfWaveformSamples = stacked_waveforms.shape[0]
            waveform_sequence_item.SamplingFrequency = 500.0  # 10초 기록 기간에 맞추어 조정
            waveform_sequence_item.WaveformBitsAllocated = 8
            waveform_sequence_item.WaveformSampleInterpretation = 'SS'

            # 채널 정의 시퀀스 설정
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

            # 각 리드를 정규화 및 스케일링
            scaled_waveform_array = np.stack(
                [(np.interp(lead, (lead.min(), lead.max()), (0, 255))).astype(np.int8) for lead in stacked_waveforms.T], axis=1)

            # 바이트로 변환하여 DICOM 데이터셋에 추가
            waveform_sequence_item.WaveformData = scaled_waveform_array.tobytes()
            ds.WaveformSequence = Sequence([waveform_sequence_item])
            
            # DICOM 파일 저장
            ds.is_little_endian = True
            ds.is_implicit_VR = False
            ds.save_as(output_file_path, write_like_original=False)

            print(f'DICOM file saved to {output_file_path}')
    except Exception as e:
        print(f'Error processing file {xml_file_path}: {e}')
        print(traceback.format_exc())