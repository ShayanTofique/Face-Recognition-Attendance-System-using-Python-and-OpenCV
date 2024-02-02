# Facial Recognition Attendance System

## Overview

This is a simple Python-based Facial Recognition Attendance System using OpenCV and face_recognition libraries. The system captures faces through a webcam, recognizes enrolled students, and marks their attendance in a CSV file.

## Prerequisites

Make sure you have the required libraries installed before running the system. You can install them using:

```bash
pip install requirements.txt
```

## Setup

1. Place student images in the `student_images` folder. Each image should correspond to a student, and the file names will be used as their names in the attendance records.

2. Run the script using:

```bash
python face_recognize.py
```

## Configuration

Adjust the `delay_time` variable to set the delay (in seconds) before allowing another entry for the same person.

## Output

The system generates an `attendance.csv` file with the columns "Name" and "Time" to keep track of attendance records.

## Usage

- When a recognized face is detected, the system marks the attendance for that person.
- Press 'q' to exit the system.

Please note that the system may need proper lighting and clear facial images for accurate recognition.