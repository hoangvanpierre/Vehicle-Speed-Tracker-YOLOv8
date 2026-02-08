# 🚗 Vehicle Speed Tracker using YOLOv8

A **production-oriented computer vision project** that performs real-time vehicle detection, tracking, and speed estimation from video streams.  
This system demonstrates practical skills in **object detection, multi-object tracking, geometric calibration, and data engineering**, suitable for real-world traffic monitoring scenarios.

---

## 🎯 Project Objective

The goal of this project is to build an **end-to-end traffic analytics pipeline** capable of:

- Detecting multiple vehicle classes in real time
- Tracking vehicles consistently across frames
- Estimating vehicle speed using physical distance calibration
- Logging structured data for downstream analysis

This project focuses on **engineering correctness, performance, and data reliability**, rather than only model inference.

---

## 🚀 Key Features

### 🔍 Multi-Class Vehicle Detection
- Utilizes **YOLOv8 (Ultralytics)** for high-accuracy detection
- Supports common traffic vehicle classes:
  - Car
  - Truck
  - Bus
  - Motorcycle

### 🔁 Persistent Object Tracking
- Custom **Euclidean distance–based tracker**
- Maintains **unique vehicle IDs** across frames
- Supports **bidirectional traffic flow** (Up / Down)

### 📏 Real-World Speed Estimation
- Speed is computed using:
  - Two calibrated virtual reference lines
  - Frame-based time measurement
  - Real-world distance conversion
- Output speed unit: **km/h**
- Designed to be resolution- and FPS-aware

### 🖥️ Real-Time Visualization
- Live overlay on video stream including:
  - Bounding boxes
  - Vehicle ID
  - Direction of movement
  - Estimated speed
- Directional counters for traffic flow analysis

### 🗂️ Structured Data Logging
- Automatically exports vehicle telemetry to `vehicle_data.csv`
- Each record includes:
  - Vehicle ID
  - Vehicle Type
  - Movement Direction
  - Speed (km/h)

### 🖱️ Interactive Calibration
- Mouse callback utility for:
  - Selecting line coordinates
  - Adjusting distance calibration
- Enables flexible deployment on different camera setups

---

## 🛠️ Technology Stack

| Category | Tools / Libraries |
|--------|------------------|
| Language | Python |
| Object Detection | YOLOv8 (Ultralytics) |
| Computer Vision | OpenCV |
| Tracking | Custom Euclidean Distance Algorithm |
| Data Processing | NumPy, Pandas |
| Data Export | CSV |

---

## 🧠 System Architecture

```text
Video Stream
     ↓
YOLOv8 Detection
     ↓
Object Tracking (ID Assignment)
     ↓
Line-Crossing Event Detection
     ↓
Speed Calculation (Distance / Time)
     ↓
Visualization + CSV Logging
