import pydicom

# Cesta k vášmu DICOM súboru
dicom_file_path = 'D:\School\MaPS\DICOM Datasets\Testing\glioma\Te-gl_0010.dcm'

# Načítanie DICOM súboru
ds = pydicom.dcmread(dicom_file_path)

# Vypísanie základných metadát
print("Bits Allocated:", ds.BitsAllocated)
print("Bits Stored:", ds.BitsStored)
print("High Bit:", ds.HighBit)
print("Samples Per Pixel:", ds.SamplesPerPixel)
print("Photometric Interpretation:", ds.PhotometricInterpretation)

# Kontrola, či súbor obsahuje pixelové dáta
if hasattr(ds, 'PixelData'):
    print("Pixel Data: Present")
else:
    print("Pixel Data: Not present")