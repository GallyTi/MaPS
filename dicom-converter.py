import os
import zipfile
import pydicom
from pydicom.dataset import Dataset, FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian, generate_uid
from PIL import Image
import numpy as np

zip_path = 'D:/School/MaPS2/dataset/archive.zip'  # Dataset
extract_to_path = 'D:/School/MaPS2/dataset/DICOM Dataset'  # Kam uložiť DICOM

def extract_zip(zip_path, extract_to_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_path)
        print(f"Extracted ZIP to {extract_to_path}")

def convert_images_to_dicom_and_remove_originals(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                image = Image.open(image_path).convert('L')
                image_array = np.array(image)
                
                # Dynamically generating attributes
                unique_identifier = os.path.basename(root) + "_" + file.split('.')[0]
                ds = Dataset()
                
                # Extracting the tumor type and dataset type from the directory structure
                path_parts = root.split(os.sep)
                tumor_type = path_parts[-1]  # The tumor type is the last directory in the path
                dataset_type = path_parts[-2]  # The dataset type (testing or training) is the second last

                ds.PatientName = "Patient_" + unique_identifier
                ds.PatientID = unique_identifier
                ds.PixelData = image_array.tobytes()
                ds.Rows, ds.Columns = image_array.shape
                ds.InstanceNumber = 1
                ds.Modality = 'OT'

                # SOPInstanceUID, StudyInstanceUID, and SeriesInstanceUID generation
                sop_instance_uid = generate_uid()
                ds.SOPInstanceUID = sop_instance_uid
                ds.StudyInstanceUID = generate_uid()
                ds.SeriesInstanceUID = generate_uid()

                # Setting necessary attributes for pixel data
                ds.BitsAllocated = 8
                ds.BitsStored = 8
                ds.HighBit = 7
                ds.SamplesPerPixel = 1
                ds.PhotometricInterpretation = "MONOCHROME2"
                ds.PixelRepresentation = 0

                # Adding attributes for Image Plane Module
                ds.PixelSpacing = [1, 1]
                ds.SliceThickness = 1 
                ds.SpacingBetweenSlices = 1 
                
                # Using standard tags for tumor type and dataset type
                ds.StudyDescription = dataset_type  # Using StudyDescription for dataset type
                ds.SeriesDescription = tumor_type  # Using SeriesDescription for tumor type

                # FileMeta information
                file_meta = FileMetaDataset()
                file_meta.MediaStorageSOPClassUID = generate_uid()
                file_meta.MediaStorageSOPInstanceUID = sop_instance_uid
                file_meta.ImplementationClassUID = generate_uid()
                file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
                ds.file_meta = file_meta

                dicom_file_path = os.path.join(root, unique_identifier + '.dcm')
                pydicom.filewriter.dcmwrite(dicom_file_path, ds, write_like_original=False)
                
                os.remove(image_path)
                
                print(f"Converted and removed {image_path}, Tumor Type: {tumor_type}, Dataset Type: {dataset_type}.")

# Spustenie extrahovania a konverzie
extract_zip(zip_path, extract_to_path)
convert_images_to_dicom_and_remove_originals(extract_to_path)
