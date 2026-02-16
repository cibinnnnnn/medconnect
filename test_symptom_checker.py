#!/usr/bin/env python
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medconnect.settings')
django.setup()

from core.ai_utils import symptom_analyzer

def test_symptom_checker():
    print("=== AI Symptom Checker Deep Analysis ===\n")
    
    # Test cases with different complexity levels
    test_cases = [
        {
            "name": "Simple Cardiology Case",
            "symptoms": "I have chest pain and heart palpitations",
            "age": 45,
            "gender": "male"
        },
        {
            "name": "Complex Neurology Case", 
            "symptoms": "I've been having severe headaches with nausea and some vision problems for the past 3 days",
            "age": 32,
            "gender": "female"
        },
        {
            "name": "Emergency Case",
            "symptoms": "I have severe chest pain and difficulty breathing, I think it might be a heart attack",
            "age": 65,
            "gender": "male"
        },
        {
            "name": "Dermatology Case",
            "symptoms": "I have a red rash on my arms that's very itchy",
            "age": 28,
            "gender": "female"
        },
        {
            "name": "General Medicine",
            "symptoms": "I feel tired and have a fever with body aches",
            "age": 35,
            "gender": "male"
        },
        {
            "name": "Pediatric Case",
            "symptoms": "My child has a high fever and cough",
            "age": 6,
            "gender": "male"
        },
        {
            "name": "Multiple Symptoms",
            "symptoms": "I have stomach pain, nausea, and also feeling dizzy with headache",
            "age": 40,
            "gender": "female"
        },
        {
            "name": "Vague Symptoms",
            "symptoms": "I don't feel well",
            "age": 30,
            "gender": "female"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test Case {i}: {test_case['name']}")
        print(f"Symptoms: \"{test_case['symptoms']}\"")
        print(f"Patient: {test_case['age']} years old, {test_case['gender']}")
        print("-" * 60)
        
        # Analyze symptoms
        result = symptom_analyzer.analyze_symptoms(
            test_case['symptoms'],
            test_case['age'],
            test_case['gender']
        )
        
        print(f"Recommended Specialization: {result['recommended_specialization']}")
        print(f"Confidence Score: {result['confidence']:.2f}")
        print(f"Severity Level: {result['severity']}")
        print(f"Matched Symptoms: {result['matched_symptoms']}")
        print(f"Alternative Specializations: {result['alternative_specializations']}")
        
        print("\nRecommendations:")
        for j, rec in enumerate(result['recommendations'], 1):
            print(f"  {j}. {rec}")
        
        print("\n" + "="*80 + "\n")
    
    # Test the underlying model components
    print("=== Model Analysis ===\n")
    
    print("1. Knowledge Base Size:")
    total_symptoms = sum(len(symptoms) for symptoms in symptom_analyzer.symptom_specialization_map.values())
    print(f"   Total Specializations: {len(symptom_analyzer.symptom_specialization_map)}")
    print(f"   Total Symptom Patterns: {total_symptoms}")
    
    print("\n2. Specialization Coverage:")
    for spec, symptoms in symptom_analyzer.symptom_specialization_map.items():
        print(f"   {spec}: {len(symptoms)} symptom patterns")
    
    print("\n3. TF-IDF Vectorizer Configuration:")
    print(f"   N-gram Range: {symptom_analyzer.vectorizer.ngram_range}")
    print(f"   Max Features: {symptom_analyzer.vectorizer.max_features}")
    print(f"   Vocabulary Size: {len(symptom_analyzer.vectorizer.vocabulary_)}")
    
    print("\n4. Corpus Size:")
    print(f"   Corpus Texts: {len(symptom_analyzer.corpus_texts)}")
    print(f"   Corpus Labels: {len(symptom_analyzer.corpus_labels)}")
    
    print("\n5. Urgency Keywords:")
    print(f"   High Urgency: {len(symptom_analyzer.high_urgency_keywords)} keywords")
    print(f"   Moderate Urgency: {len(symptom_analyzer.moderate_urgency_keywords)} keywords")
    
    # Test preprocessing
    print("\n6. Text Preprocessing Example:")
    sample_text = "I have severe chest pain and difficulty breathing!"
    processed = symptom_analyzer.preprocess_text(sample_text)
    print(f"   Original: '{sample_text}'")
    print(f"   Processed: '{processed}'")

if __name__ == "__main__":
    test_symptom_checker()
