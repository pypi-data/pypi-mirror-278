# PyDicomGrouping Project

## About

Deep learning is presently widely used for clinical data science and has been adopted in a huge amount of research projects. In the deep-learning(or artificial intelligence, AI) + medical imaging area, there is still lacking tools for managing the 2-dimensional DICOM files and stacking them into ordered 3D volumes for further analysis, and this greatly prevents the development of more advanced deep learning algorithms for medical imaging area, especially for non-biomedical engineer background participants. In this project, we developed an automatic stacking pipeline for grouping and managing DICOMS files by using Python language. Conventional radiological image data, including computer tomography (CT) and magnetic resonance imaging (MRI), from vendors including Siemens, GE, Philips and UIH, has been tested by our software.

For any issues and suggestions, please send your email to kaixuan_zhao@163.com

## Installation

Installation of PyDicomGrouping can be done by using pip, according to the platform of your system, i.e. Linux, Mac, or Windows.

```
pip install PyDicomGrouping-Linux
pip install PyDicomGrouping-Mac
pip install PyDicomGrouping-Win
```

Or via the offline method, by downloading the .tar files and unzipping to local, navigating to the PyDicomGrouping root directory and run

```python
pip install -e .
```

```

```

## Examples

Here is a code example for PyDicomGrouping

```python
from PyDicomGrouping.main import dicom_grouping
import os 
project_path = r"E:\my_project"
data_root_path = r"E:\my_data_root_path"
dicom_grouping(project_path = project_path,
                data_root_path = data_root_path,
                save_path = os.path.join(project_path,"processed")
                )
```

## Licenses

PyDicomGrouping is MIT-licensed, as found in the LICENSE file