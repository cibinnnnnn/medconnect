#!/usr/bin/env python
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medconnect.settings')
django.setup()

from core.ai_utils import symptom_analyzer

def test_general_medicine_predictions():
    print("=== General Medicine Prediction Testing ===\n")
    
    # General Medicine Knowledge Base
    gm_symptoms = symptom_analyzer.symptom_specialization_map['general_medicine']
    print(f"General Medicine Symptom Patterns: {len(gm_symptoms)}")
    print("Patterns:", gm_symptoms)
    print("\n" + "="*60 + "\n")
    
    # Test cases specifically for general medicine
    test_cases = [
        {
            "name": "Classic Flu Symptoms",
            "symptoms": "I have fever, body ache, and feel very tired",
            "age": 35,
            "gender": "male",
            "expected": "general_medicine"
        },
        {
            "name": "Common Cold",
            "symptoms": "I have a cold and feel weak",
            "age": 28,
            "gender": "female",
            "expected": "general_medicine"
        },
        {
            "name": "Fatigue Only",
            "symptoms": "I feel very tired and weak",
            "age": 40,
            "gender": "male",
            "expected": "general_medicine"
        },
        {
            "name": "General Malaise",
            "symptoms": "I don't feel well, just general malaise",
            "age": 45,
            "gender": "female",
            "expected": "general_medicine"
        },
        {
            "name": "Infection Symptoms",
            "symptoms": "I think I have an infection with fever",
            "age": 30,
            "gender": "male",
            "expected": "general_medicine"
        },
        {
            "name": "Checkup Request",
            "symptoms": "I need a general checkup",
            "age": 50,
            "gender": "female",
            "expected": "general_medicine"
        },
        {
            "name": "Multiple Mild Symptoms",
            "symptoms": "I have mild fever, some fatigue, and body ache",
            "age": 25,
            "gender": "male",
            "expected": "general_medicine"
        },
        {
            "name": "Tiredness",
            "symptoms": "I'm feeling tired",
            "age": 38,
            "gender": "female",
            "expected": "general_medicine"
        },
        {
            "name": "Weakness",
            "symptoms": "I feel weak",
            "age": 33,
            "gender": "male",
            "expected": "general_medicine"
        },
        {
            "name": "Fever Only",
            "symptoms": "I have fever",
            "age": 27,
            "gender": "female",
            "expected": "general_medicine"
        }
    ]
    
    # Track predictions
    correct_predictions = 0
    total_tests = len(test_cases)
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['name']}")
        print(f"Symptoms: \"{test_case['symptoms']}\"")
        print(f"Expected: {test_case['expected']}")
        print("-" * 40)
        
        # Analyze symptoms
        result = symptom_analyzer.analyze_symptoms(
            test_case['symptoms'],
            test_case['age'],
            test_case['gender']
        )
        
        predicted = result['recommended_specialization']
        confidence = result['confidence']
        severity = result['severity']
        matched = result['matched_symptoms']
        alternatives = result['alternative_specializations']
        
        print(f"Predicted: {predicted}")
        print(f"Confidence: {confidence:.2f}")
        print(f"Severity: {severity}")
        print(f"Matched Symptoms: {matched}")
        print(f"Alternatives: {alternatives}")
        
        # Check if prediction is correct
        is_correct = predicted == test_case['expected']
        if is_correct:
            correct_predictions += 1
            print("✅ CORRECT")
        else:
            print("❌ INCORRECT")
        
        results.append({
            'test': test_case['name'],
            'symptoms': test_case['symptoms'],
            'expected': test_case['expected'],
            'predicted': predicted,
            'confidence': confidence,
            'correct': is_correct
        })
        
        print("\n" + "="*60 + "\n")
    
    # Summary Statistics
    print("=== PREDICTION SUMMARY ===")
    print(f"Total Tests: {total_tests}")
    print(f"Correct Predictions: {correct_predictions}")
    print(f"Accuracy: {correct_predictions/total_tests*100:.1f}%")
    
    print("\n=== DETAILED RESULTS ===")
    for result in results:
        status = "✅" if result['correct'] else "❌"
        print(f"{status} {result['test']}")
        print(f"   Symptoms: \"{result['symptoms']}\"")
        print(f"   Expected: {result['expected']} | Predicted: {result['predicted']} (Confidence: {result['confidence']:.2f})")
        print()
    
    # Analyze confidence scores
    confidences = [r['confidence'] for r in results]
    avg_confidence = sum(confidences) / len(confidences)
    min_confidence = min(confidences)
    max_confidence = max(confidences)
    
    print("=== CONFIDENCE ANALYSIS ===")
    print(f"Average Confidence: {avg_confidence:.2f}")
    print(f"Min Confidence: {min_confidence:.2f}")
    print(f"Max Confidence: {max_confidence:.2f}")
    
    # Test edge cases that might NOT go to general medicine
    print("\n=== EDGE CASE TESTING ===")
    edge_cases = [
        {
            "name": "Severe Chest Pain",
            "symptoms": "I have severe chest pain",
            "should_not_be": "general_medicine"
        },
        {
            "name": "Skin Rash",
            "symptoms": "I have a skin rash",
            "should_not_be": "general_medicine"
        },
        {
            "name": "Headache Migraine",
            "symptoms": "I have severe migraine headache",
            "should_not_be": "general_medicine"
        }
    ]
    
    for edge_case in edge_cases:
        result = symptom_analyzer.analyze_symptoms(edge_case['symptoms'])
        predicted = result['recommended_specialization']
        correctly_redirected = predicted != edge_case['should_not_be']
        
        print(f"Edge Case: {edge_case['name']}")
        print(f"Symptoms: \"{edge_case['symptoms']}\"")
        print(f"Predicted: {predicted}")
        print(f"Correctly redirected from general medicine: {'✅' if correctly_redirected else '❌'}")
        print()

if __name__ == "__main__":
    test_general_medicine_predictions()
