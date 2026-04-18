from flask import Flask, request, jsonify, render_template
import pickle
import re

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))
tfidf = pickle.load(open('tfidf.pkl', 'rb'))

def check_red_flags(text):
    red_flags = []
    text_lower = text.lower()
    
    # ---- DOCUMENT REQUESTS ----
    doc_keywords = [
        'aadhar', 'aadhaar', 'pan card', 'pan number',
        'passport photo', 'passport size',
        'bank account', 'bank details', 'account number',
        'ifsc', 'driving licence', 'driving license',
        'identity proof', 'id proof', 'kyc'
    ]
    for kw in doc_keywords:
        if kw in text_lower:
            red_flags.append(f"Asks for personal documents or bank details ({kw})")
            break

    # ---- PERSONAL EMAIL ----
    personal_email_pattern = r'[a-zA-Z0-9._%+-]+@(gmail|yahoo|hotmail|outlook|rediffmail|ymail|live)\.com'
    if re.search(personal_email_pattern, text_lower):
        red_flags.append("Uses personal email address instead of official company domain")

    # ---- UPFRONT PAYMENT ----
    payment_keywords = [
        'registration fee', 'processing fee',
        'security deposit', 'training fee',
        'pay first', 'advance payment',
        'refundable deposit', 'joining fee'
    ]
    for kw in payment_keywords:
        if kw in text_lower:
            red_flags.append(f"Asks for upfront payment or fees ({kw})")
            break

    # ---- UNREALISTIC SALARY ----
    salary_keywords = [
        'earn from home', 'work from home earn',
        'per day earn', 'daily earning',
        'unlimited earning', 'no target',
        'earn up to 5000 per day',
        'earn 50000 per month without experience'
    ]
    for kw in salary_keywords:
        if kw in text_lower:
            red_flags.append(f"Unrealistic earning claims ({kw})")
            break

    # ---- URGENCY TACTICS ----
    urgency_keywords = [
        'limited seats', 'apply immediately',
        'urgent hiring', 'last date today',
        'only today', 'hurry up', 'walk in interview',
        'immediate joiner', 'join today'
    ]
    for kw in urgency_keywords:
        if kw in text_lower:
            red_flags.append(f"Creates false urgency ({kw})")
            break

    # ---- NO COMPANY VERIFICATION ----
    vague_keywords = [
        'fast growing', 'fast-growing', 'growing company',
        'reputed company', 'reputed firm',
        'multinational company', 'leading company',
        'trusted company'
    ]
    has_vague = any(kw in text_lower for kw in vague_keywords)
    has_website = any(kw in text_lower for kw in ['www.', 'http', '.com', 'website', 'visit us'])
    if has_vague and not has_website:
        red_flags.append("Vague company description with no verifiable website or contact")

    # ---- WHATSAPP/TELEGRAM CONTACT ----
    contact_keywords = [
        'whatsapp', 'telegram', 'watsapp',
        'contact on whatsapp', 'msg on whatsapp'
    ]
    for kw in contact_keywords:
        if kw in text_lower:
            red_flags.append(f"Asks to contact via unofficial channel ({kw})")
            break

    return red_flags


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    job_text = request.form.get('job_text', '')

    if not job_text.strip():
        return render_template('index.html', 
                             error="Please paste a job description first.")

    # ML Prediction
    text_tfidf = tfidf.transform([job_text])
    ml_prediction = model.predict(text_tfidf)[0]
    probability = model.predict_proba(text_tfidf)[0]
    ml_confidence = max(probability) * 100

    # Rule Based Red Flags
    red_flags = check_red_flags(job_text)
    flag_count = len(red_flags)

    print(f"\n--- DEBUG ---")
    print(f"ML Prediction: {ml_prediction}")
    print(f"ML Confidence: {ml_confidence:.2f}%")
    print(f"Red Flags Found: {flag_count}")
    for f in red_flags:
        print(f"  -> {f}")
    print(f"-------------\n")

    # Final Decision Logic
    final_confidence = f"{ml_confidence:.1f}%"
    
    if flag_count >= 2:
        final_prediction = 'FAKE JOB'
        risk_level = 'HIGH RISK'
        css_class = 'fake'
        final_confidence = "100% (Rule-Based Detection)"
    elif flag_count == 1:
        final_prediction = 'SUSPICIOUS JOB'
        risk_level = 'MEDIUM RISK'
        css_class = 'suspicious'
        final_confidence = f"Rule-Based (ML Context: {ml_confidence:.1f}%)"
    elif ml_prediction == 1:
        final_prediction = 'FAKE JOB'
        risk_level = 'HIGH RISK'
        css_class = 'fake'
    else:
        final_prediction = 'REAL JOB'
        risk_level = 'LOW RISK'
        css_class = 'real'

    result = {
        'prediction': final_prediction,
        'confidence': final_confidence,
        'risk_level': risk_level,
        'red_flags': red_flags,
        'flag_count': flag_count,
        'css_class': css_class
    }

    return render_template('index.html',
                           result=result,
                           job_text=job_text)


if __name__ == '__main__':
    app.run(debug=True)