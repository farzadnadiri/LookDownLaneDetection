# Look Down Lane Detection in Self-Driving Cars

This repository contains the implementation of the "Look Down Method" for lane detection in self-driving cars. The project captures video frames, removes unnecessary data, and performs lane detection using masking and filtering techniques provided by OpenCV.

[![Watch the video](https://img.youtube.com/vi/TuawiVMbt_c/0.jpg)](https://www.youtube.com/watch?v=TuawiVMbt_c)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Workflow](#workflow)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Accurate lane detection is a critical component in the development of self-driving cars. This project implements a simple yet effective lane detection algorithm using the "Look Down Method." By capturing and processing video frames, unnecessary data is removed to isolate the road, and lanes are detected using color masks and edge detection in OpenCV.

## Features

- **Real-time Frame Capture:** Captures and processes video frames from a camera feed in real-time.
- **Data Filtering:** Removes irrelevant data (e.g., sky, surroundings) to focus on the road surface.
- **Lane Detection:** Detects lane lines using a combination of color masking and edge detection.
- **Customizable:** Adjustable parameters, including HSV values, to fine-tune lane detection.

## Installation

To get started, clone the repository and install the required dependencies:

```bash
git clone https://github.com/farzadnadiri/LookDownLaneDetection.git
cd LookDownLaneDetection
pip install -r requirements.txt
