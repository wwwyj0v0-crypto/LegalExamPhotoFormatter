# LegalExamPhotoFormatter

## Automatic Photo Formatting System for the National Unified Legal Professional Qualification Examination

LegalExamPhotoFormatter is a Python-based image processing system that automatically converts ID photos of arbitrary specifications into registration photos that comply with the requirements of the **National Unified Legal Professional Qualification Examination**.

The system is designed to simplify the photo preparation process for examination registration by automatically adjusting portrait composition, output resolution, background expansion, and file size according to the official registration specifications.

---

## Features

* Convert ID photos of arbitrary specifications into examination-compliant registration photos
* Automatic face detection using OpenCV Haar Cascade
* Intelligent crop region calculation based on examination photo requirements
* Automatic canvas expansion to prevent head clipping
* Background color estimation using KMeans clustering
* Fixed output resolution: **413 × 626 pixels**
* JPEG binary-search compression to satisfy file size requirements (40 KB – 100 KB)
* Local Web interface built with FastAPI

---

## Application

This project is specifically designed for preparing registration photos for the **National Unified Legal Professional Qualification Examination**.

Input:

* ID photos of arbitrary specifications
* JPG / JPEG / PNG / BMP / WEBP

Output:

* JPEG format
* 413 × 626 pixels
* 40 KB – 100 KB
* Registration photo compliant with the examination requirements

---

## Algorithm Pipeline

Input ID Photo

↓

Face Detection (OpenCV Haar Cascade)

↓

Crop Region Calculation

↓

Canvas Expansion

↓

Background Color Estimation (KMeans)

↓

Resize to 413 × 626

↓

JPEG Binary Search Compression

↓

National Unified Legal Professional Qualification Examination Registration Photo

---

## Tech Stack

* Python 3.12
* OpenCV
* NumPy
* Pillow
* scikit-learn
* FastAPI
* Jinja2

---

## Project Structure

```text
LegalExamPhotoFormatter/
│
├── app.py
├── processor.py
├── config.py
├── requirements.txt
├── README.md
│
├── templates/
├── static/
├── uploads/
└── outputs/
```

---

## Future Work

* Support additional examination photo specifications
* Automatic photo quality assessment
* Face landmark-based crop optimization
* Blur and exposure detection
* Batch image processing

---

## License

MIT License
