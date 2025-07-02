# HIG Smart Hygiene Web App

This is a high-fidelity prototype of an intelligent web application developed for **Hygiene Inspection Group (HIG)**, a UK-based company that provides hygiene swab kits to food-handling businesses.

## 🧪 Project Overview

HIG's swab kits allow users to test surface cleanliness by collecting bacterial samples and growing them in Petri dishes over 7 days. The current analysis process is manual and time-consuming.

This web app streamlines the process with the help of machine learning and provides:

- Online swab kit ordering with unique Kit IDs
- Image upload system for Petri dishes
- Instant automated bacterial analysis using a trained ML model
- Categorization of bacterial growth:
  - ✅ Clean
  - 🟡 Yellow Bacteria (harmless)
  - 🟢 Green Bacteria (harmful)
  - ⚠️ Both

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML/CSS + JavaScript
- **Machine Learning**: Trained image classification model (bacteria detection)
- **Database**: SQLite (local)

## 🚀 Features

- User-friendly UI for ordering and uploading test results
- Unique kit ID generation and tracking
- Real-time ML-based image classification
- Clean dashboard for result viewing

## 🖼️ How It Works

1. Customer orders a hygiene swab kit via the web app
2. A unique kit ID is generated
3. After 7 days of bacterial growth, the customer uploads an image of their Petri dish
4. The ML model classifies the image and returns results instantly

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd HIG
# HIG
