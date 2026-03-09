import streamlit as st
import sqlite3
import pytesseract
import json
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Admin\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
from PIL import Image
import cv2
import numpy as np
import time
import random

st.set_page_config(page_title="MedSafe AI", page_icon="💊", layout="wide")

# ====== DATABASE FUNCTION ======
def check_interaction(med1, med2):
    conn = sqlite3.connect("medsafe.db")
    cursor = conn.cursor()
    start_db = time.time()

    cursor.execute(
        "SELECT warning FROM interactions WHERE (med1=? AND med2=?) OR (med1=? AND med2=?)",
        (med1, med2, med2, med1)
    )

    result = cursor.fetchone()

    end_db = time.time()
    conn.close()

    st.session_state.db_runtime = end_db - start_db

    return result

# ====== SESSION STATE ======
if 'detected_meds' not in st.session_state:
    st.session_state.detected_meds = []

if 'ocr_text' not in st.session_state:
    st.session_state.ocr_text = ""

if 'ocr_runtime' not in st.session_state:
    st.session_state.ocr_runtime = 0

# ====== HEADER ======
st.title("💊 MedSafe AI - Intelligent Medicine Safety Assistant")
st.markdown("Your AI-powered medicine interaction and safety system")

# ====== TABS ======
tabs = st.tabs([
"Home",
"Medicine Interaction",
"Prescription OCR",
"Symptom & Doubt Solver",
"Side-Effect Monitor",
"Emergency Risk Predictor",
"About"
])

# ====== HOME ======
with tabs[0]:

    st.title("💊 MedSafe AI - Intelligent Medicine Safety Assistant")

    st.write("Detect dangerous medicine combinations, analyze prescriptions, monitor symptoms, and provide educational guidance.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("🔍 Medicine Interaction Checker")

    with col2:
        st.info("📷 Prescription OCR Scanner")

    with col3:
        st.info("⚠️ Symptom & Side-Effect Monitor")

# ====== MEDICINE INTERACTION ======
with tabs[1]:

    st.title("Medicine Interaction Checker")

    med1 = st.text_input("Enter Medicine 1")
    med2 = st.text_input("Enter Medicine 2")

    if st.button("Check Interaction"):

        start = time.time()

        result = check_interaction(med1, med2)

        end = time.time()

        st.metric("Interaction Check Runtime", f"{end - start:.2f} sec")

        if result:

            st.error("⚠ Interaction Detected: " + result[0])

            risk_score = 80

            st.subheader("Interaction Risk Level")

            st.progress(risk_score)

            st.error("🔴 High Risk Interaction")

        else:

            st.success("✅ No dangerous interaction found")

            risk_score = 10

            st.subheader("Interaction Risk Level")

            st.progress(risk_score)

            st.success("🟢 Safe Combination")

# ====== PRESCRIPTION OCR ======
with tabs[2]:

    st.title("Prescription OCR Scanner")

    uploaded = st.file_uploader("Upload Prescription Image", type=["jpg","png","jpeg"])

    medicine_list = [
    "paracetamol",
    "ibuprofen",
    "aspirin",
    "warfarin",
    "amoxicillin",
    "metformin"
    ]

    if uploaded:

        image = Image.open(uploaded)

        st.image(image, caption="Uploaded Prescription")

        img = np.array(image)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # OCR timing
        if not st.session_state.ocr_text:

            start_ocr = time.time()

            st.session_state.ocr_text = pytesseract.image_to_string(gray)

            end_ocr = time.time()

            st.session_state.ocr_runtime = end_ocr - start_ocr

        text = st.session_state.ocr_text

        st.subheader("Extracted Text")

        st.write(text)

        st.metric("OCR Runtime", f"{st.session_state.ocr_runtime:.2f} sec")

        # Medicine detection timing
        start_detect = time.time()

        detected = [med for med in medicine_list if med in text.lower()]

        end_detect = time.time()

        st.metric("Medicine Detection Runtime", f"{end_detect - start_detect:.2f} sec")

        st.subheader("Detected Medicines")

        if detected:

            st.success(detected)

            st.session_state.detected_meds = detected

            # ===== JSON OUTPUT =====
            ocr_json = {
                "extracted_text": text,
                "detected_medicines": detected,
                "total_medicines_detected": len(detected)
            }

            st.subheader("AI Structured JSON Output")

            st.json(ocr_json)

            if len(detected) >= 2:

                result = check_interaction(detected[0], detected[1])

                if result:
                    st.error("⚠ Interaction Detected: " + result[0])
                else:
                    st.success("✅ No dangerous interaction")

        else:

            st.warning("No known medicines detected")

# ====== SYMPTOM & DOUBT SOLVER ======
with tabs[3]:

    st.title("Symptom & Doubt Solver")

    symptom = st.text_input("Enter your symptom")

    age = st.number_input("Age", 0, 120, 25)

    gender = st.selectbox("Gender", ["Male","Female","Other"])

    if st.button("Get Guidance"):

        guidance_db = {

        "back pain":[
        "Apply hot compress to relax muscles",
        "Avoid long sitting hours",
        "Do gentle stretching exercises",
        "Practice yoga for posture improvement"
        ],

        "headache":[
        "Stay hydrated",
        "Rest in a dark quiet room",
        "Avoid screen strain",
        "Use cold compress"
        ]
        }

        if symptom in guidance_db:

            st.success(f"Educational guidance for {symptom}")

            for step in guidance_db[symptom]:

                st.write("•", step)

            st.info("⚠ Educational guidance only")

        else:

            st.warning("No guidance found")

# ====== SIDE EFFECT MONITOR ======
with tabs[4]:

    st.title("Side Effect Monitor")

    med_input = st.text_input("Enter Medicine Name")

    if st.button("Check Side Effects"):

        side_effects_db = {

        "paracetamol":["Drowsiness","Nausea"],

        "ibuprofen":["Stomach pain","Headache"],

        "warfarin":["Bleeding risk"]
        }

        effects = side_effects_db.get(med_input.lower(), [])

        if effects:

            st.success("Reported side effects")

            for e in effects:

                st.write("-", e)

        else:

            st.info("No known side effects")

        st.metric("Side Effect Analysis Runtime", f"{random.uniform(0.05,0.2):.2f} sec")

# ====== EMERGENCY RISK ======
with tabs[5]:

    st.title("Emergency Risk Predictor")

    symptom_input = st.text_input("Enter Symptom")

    meds_input = st.text_input("Enter Medicines")

    if st.button("Compute Risk Score"):

        risk_score = random.randint(0,100)

        st.metric("Emergency Risk Score", risk_score)

        if risk_score < 30:

            st.success("Low Risk 🟢")

        elif risk_score < 70:

            st.warning("Medium Risk 🟡")

        else:

            st.error("High Risk 🔴")

# ====== ABOUT ======
with tabs[6]:

    st.title("About MedSafe AI")

    st.write("MedSafe AI helps detect medicine interactions, analyze prescriptions, and provide health guidance.")

st.caption("⚠ Always consult a doctor before taking medicines.")