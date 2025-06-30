import json
from datetime import date
import os

CERT_DB = "certificates.json"
BASE_URL = "https://github.com/kaustubhsawant-it/certificates/blob/main/certs/"

def load_certs():
    if os.path.exists(CERT_DB):
        with open(CERT_DB, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []  # file exists but is empty or corrupted
    return []


def save_certs(data):
    with open(CERT_DB, "w") as f:
        json.dump(data, f, indent=4)

def generate_course_code(topic):
    return ''.join([word[0].upper() for word in topic.strip().split()])

def generate_cert_id(course_code, year, existing):
    count = sum(1 for cert in existing if cert["course_code"] == course_code)
    return f"{course_code}-{year}-{count+1:06d}"

def register_certificate(name, topic, week, module):
    certs = load_certs()
    year = date.today().year
    course_code = generate_course_code(topic)
    cert_id = generate_cert_id(course_code, year, certs)
    filename = f"{cert_id}_{name.replace(' ', '_')}.png"
    verify_url = BASE_URL + filename

    cert_entry = {
        "name": name,
        "topic": topic,
        "week": week,
        "module": module,
        "course_code": course_code,
        "date": str(date.today()),
        "cert_id": cert_id,
        "verify_url": verify_url
    }

    certs.append(cert_entry)
    save_certs(certs)

    print("\n✅ Certificate Issued!")
    print(f"Name: {name}")
    print(f"Cert ID: {cert_id}")
    print(f"Verify URL: {verify_url}\n")

    return cert_entry

# === INPUT MODE ===
if __name__ == "__main__":
    name = input("Enter full name: ")
    topic = input("Enter course topic (e.g., 'Linear Algebra'): ")
    week = input("Enter week info (e.g., 'Week 1'): ")
    module = input("Enter module name (e.g., 'Matrix Basics'): ")

    register_certificate(name, topic, week, module)
