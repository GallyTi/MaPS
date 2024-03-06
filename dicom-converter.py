import os
import zipfile
import pydicom
from pydicom.dataset import Dataset, FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian, generate_uid
from PIL import Image
import numpy as np

zip_path = 'D:/School/MaPS/Datasets/archive.zip'  # Dataset
extract_to_path = 'D:/School/MaPS/DICOM Dataset'  # Kam uložiť DICOM

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
                
                # Dynamické generovanie atribútov
                unique_identifier = os.path.basename(root) + "_" + file.split('.')[0]
                ds = Dataset()
                ds.PatientName = "Patient_" + unique_identifier
                ds.PatientID = unique_identifier
                ds.PixelData = image_array.tobytes()
                ds.Rows, ds.Columns = image_array.shape
                ds.InstanceNumber = 1
                ds.Modality = 'OT'

                # Nastavenie potrebných atribútov pre pixelové dáta
                ds.BitsAllocated = 8
                ds.BitsStored = 8
                ds.HighBit = 7
                ds.SamplesPerPixel = 1
                ds.PhotometricInterpretation = "MONOCHROME2"
                ds.PixelRepresentation = 0

                # Doplnenie atribútov pre Image Plane Module
                ds.PixelSpacing = [1, 1]
                ds.SliceThickness = 1 
                ds.SpacingBetweenSlices = 1 
                
                file_meta = FileMetaDataset()
                file_meta.MediaStorageSOPClassUID = generate_uid()
                file_meta.MediaStorageSOPInstanceUID = generate_uid()
                file_meta.ImplementationClassUID = generate_uid()
                file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
                ds.file_meta = file_meta
                ds.is_little_endian = True
                ds.is_implicit_VR = False
                
                dicom_file_path = os.path.join(root, unique_identifier + '.dcm')
                pydicom.filewriter.dcmwrite(dicom_file_path, ds, write_like_original=False)
                
                os.remove(image_path)
                
                print(f"Converted and removed {image_path}.")

# Spustenie extrahovania a konverzie
extract_zip(zip_path, extract_to_path)
convert_images_to_dicom_and_remove_originals(extract_to_path)
