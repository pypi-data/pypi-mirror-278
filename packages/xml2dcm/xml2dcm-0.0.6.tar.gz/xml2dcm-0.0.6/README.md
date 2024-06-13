---
# XML2DCM

XML2DCM은 XML 형태의 데이터를 DICOM 형태로 바꾸는 패키지 입니다. ( 여기서 XML 데이터는 ECG 데이터를 담고 있습니다. )

XML2DCM is a package that converts XML formatted data into DICOM format. ( the XML data contains ECG information. )

---

# XML Structure

XML 파일을 DCM 파일로 변환하기 위해서는 XML 파일의 구조가 정해진 [형식](https://github.com/SeungHoJUN/XML2DCM/blob/main/xml_format.txt)을 따라야 합니다. 변환을 진행하기 전에, 파일이 이 구조를 제대로 갖추고 있는지 확인해야 합니다.

To convert an XML file into a DCM file, the structure of the XML file must adhere to a specified [format](https://github.com/SeungHoJUN/XML2DCM/blob/main/xml_format.txt). Before proceeding with the conversion, it is necessary to verify that the file conforms to this structure.

---

# To start using xml2dcm

## Install

### PIP
```
pip install xml2dcm
```

```
python -m pip install --upgrade xml2dcm
```


## Using the XML2DCM Library in Python
```
from xml2dcm import xml2dcm

# Convert XML file to DICOM file
# Output folder is optional. If not set, it defaults to 'generated_dicom_from_xml'
xml2dcm.create_dicom_file('path/to/your/XML_file.xml', 'path/to/your/output_folder')

# Check the structure of the DICOM file
xml2dcm.read_dicom('path/to/your/DICOM.dcm')
```

---

# license

This software is licensed under the Apache 2 license, quoted below

Copyright 2024 SNUH https://www.snuh.org

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
