medicine_list = [
    "paracetamol",
    "ibuprofen",
    "aspirin",
    "warfarin",
    "amoxicillin",
    "metformin"
]

def detect_medicines(text):

    detected = []

    for med in medicine_list:
        if med in text.lower():
            detected.append(med)

    return detected