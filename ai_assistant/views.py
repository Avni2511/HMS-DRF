import google.generativeai as genai

from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def symptom_checker(request):

    result = None

    if request.method == 'POST':

        symptoms = request.POST.get('symptoms')

        try:

            genai.configure(
                api_key=settings.GEMINI_API_KEY
            )

            model = genai.GenerativeModel(
                'gemini-2.0-flash'
            )

            prompt = f"""
            A patient has these symptoms:

            {symptoms}

            Give:
            1. Possible diseases
            2. Basic precautions

            Keep response short.
            """

            response = model.generate_content(prompt)
            result = response.text

        except Exception:

            symptom_lower = symptoms.lower()

            if "fever" in symptom_lower:
                result = """
Possible Conditions:
• Viral Fever
• Dengue
• Typhoid
• Flu

Advice:
• Drink plenty of fluids
• Take proper rest
• Monitor temperature
"""

            elif "cough" in symptom_lower:
                result = """
Possible Conditions:
• Common Cold
• Viral Infection
• Bronchitis
• Allergies

Advice:
• Stay hydrated
• Avoid cold drinks
"""

            elif "headache" in symptom_lower:
                result = """
Possible Conditions:
• Migraine
• Stress
• Dehydration
• Lack of Sleep

Advice:
• Drink water
• Take proper rest
"""

            elif "stomach" in symptom_lower:
                result = """
Possible Conditions:
• Acidity
• Food Poisoning
• Gastric Problem
• Indigestion

Advice:
• Eat light food
• Drink water
"""

            elif "chest pain" in symptom_lower:
                result = """
Possible Conditions:
• Muscle Strain
• Acid Reflux
• Heart Related Issue

Advice:
• Seek medical help immediately.
"""

            else:
                result = """
Possible Conditions:
• Common Cold
• Viral Fever
• Seasonal Infection

Advice:
• Rest properly
• Drink plenty of water
• Consult a doctor

Disclaimer:
This is not a medical diagnosis.
"""

    return render(
        request,
        'ai_assistant/symptom_checker.html',
        {
            'result': result
        }
    )