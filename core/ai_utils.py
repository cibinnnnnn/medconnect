"""
AI Utilities for MedConnect
Provides NLP-based symptom analysis and smart doctor allocation
"""

import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from datetime import datetime, timedelta
from django.db.models import Count, Q

# Download required NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt_tab', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)


class SymptomAnalyzer:
    """
    NLP-based symptom analyzer using TF-IDF and pattern matching
    Can be extended with TensorFlow models for more advanced analysis
    """
    
    def __init__(self):
        # Medical knowledge base: symptoms mapped to specializations
        self.symptom_specialization_map = {
            'cardiology': [
                'chest pain', 'heart pain', 'palpitations', 'irregular heartbeat',
                'shortness of breath', 'heart attack', 'angina', 'hypertension',
                'high blood pressure', 'heart pounding', 'dizzy', 'faint',
                'heartburn', 'acid reflux'  # Added common cardiac symptoms
            ],
            'neurology': [
                'headache', 'migraine', 'seizure', 'numbness', 'tingling',
                'memory loss', 'confusion', 'dizziness', 'vertigo', 'tremor',
                'paralysis', 'weakness', 'stroke', 'brain', 'nerve pain',
                'brain fog', 'concentration problems', 'focus issues'  # Added common neurological symptoms
            ],
            'orthopedics': [
                'joint pain', 'back pain', 'knee pain', 'arthritis', 'fracture',
                'sprain', 'bone pain', 'muscle pain', 'hip pain', 'shoulder pain',
                'neck pain', 'injury', 'sports injury', 'mobility issues', 'leg pain'
            ],
            'dermatology': [
                'rash', 'skin rash', 'itching', 'acne', 'eczema', 'psoriasis',
                'skin lesion', 'moles', 'hives', 'skin infection', 'burn',
                'skin discoloration', 'dry skin', 'oily skin'
            ],
            'gastroenterology': [
                'stomach pain', 'abdominal pain', 'nausea', 'vomiting', 'diarrhea',
                'constipation', 'bloating', 'acid reflux', 'heartburn', 'ulcer',
                'indigestion', 'bowel', 'digestive issues', 'cramps'
            ],
            'pulmonology': [
                'cough', 'breathing difficulty', 'wheezing', 'asthma', 'bronchitis',
                'pneumonia', 'lung pain', 'respiratory', 'chest congestion',
                'phlegm', 'tuberculosis', 'covid', 'shortness of breath',
                'chest tightness', 'difficulty breathing'  # Added respiratory symptoms
            ],
            'ent': [
                'ear pain', 'sore throat', 'throat pain', 'hearing loss', 'tinnitus',
                'nasal congestion', 'sinus', 'nose bleeding', 'throat infection',
                'voice loss', 'ear infection', 'tonsillitis', 'sinusitis'
            ],
            'ophthalmology': [
                'eye pain', 'vision problems', 'blurry vision', 'double vision',
                'eye redness', 'eye discharge', 'eye infection', 'cataract',
                'glaucoma', 'dry eyes', 'watery eyes', 'light sensitivity'
            ],
            'gynecology': [
                'menstrual pain', 'period pain', 'irregular periods', 'pelvic pain',
                'vaginal discharge', 'pregnancy', 'menopause', 'cramps',
                'heavy bleeding', 'missed period', 'reproductive', 'ovarian'
            ],
            'pediatrics': [
                'child fever', 'infant', 'baby', 'vaccination', 'growth issues',
                'developmental delay', 'child cough', 'child rash', 'newborn'
            ],
            'psychiatry': [
                'depression', 'anxiety', 'stress', 'panic attack', 'insomnia',
                'sleep problems', 'mood swings', 'mental health', 'ptsd',
                'bipolar', 'schizophrenia', 'suicidal thoughts'
            ],
            'general_medicine': [
                'fever', 'fatigue', 'weakness', 'cold', 'flu', 'infection',
                'body ache', 'tiredness', 'general checkup', 'malaise'
            ]
        }
        
        # Urgency keywords for severity assessment
        self.high_urgency_keywords = [
            'severe', 'unbearable', 'extreme', 'critical', 'emergency',
            'heart attack', 'stroke', 'bleeding heavily',
            'unconscious', 'seizure', 'suicidal', 'difficulty breathing',
            'chest pain severe', 'cannot breathe'  # More specific high urgency
        ]
        
        self.moderate_urgency_keywords = [
            'moderate', 'persistent', 'recurring', 'worsening', 'painful',
            'high fever', 'vomiting blood', 'severe pain',
            'difficulty breathing mild', 'chest discomfort'  # More specific moderate urgency
        ]
        
        # Initialize TF-IDF vectorizer for symptom matching
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),  # Reduced from 1-3 for better matching
            #stop_words='english',
            max_features=1000,
            lowercase=True,
            strip_accents='ascii'
        )
        
        # Build corpus from symptom knowledge base
        self._build_symptom_corpus()
    
    def _build_symptom_corpus(self):
        """Build a corpus of all symptoms for TF-IDF matching"""
        self.corpus_texts = []
        self.corpus_labels = []
        
        for specialization, symptoms in self.symptom_specialization_map.items():
            for symptom in symptoms:
                self.corpus_texts.append(symptom)
                self.corpus_labels.append(specialization)
        
        # Fit the vectorizer on the corpus
        if self.corpus_texts:
            self.vectorizer.fit(self.corpus_texts)
        else:
            # Handle empty corpus case with fallback
            self.corpus_texts = ['general medicine']
            self.corpus_labels = ['general_medicine']
            self.vectorizer.fit(self.corpus_texts)
    
    def preprocess_text(self, text):
        """Clean and preprocess symptom text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters except spaces
        text = re.sub(r'[^a-z0-9\s]', '', text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        tokens = [t for t in tokens if t not in stop_words]
        
        return ' '.join(tokens)
    
    def analyze_symptoms(self, symptom_text, patient_age=None, patient_gender=None):
        """
        Analyze patient symptoms using NLP and return recommendations
        
        Args:
            symptom_text: Patient's description of symptoms
            patient_age: Patient age (optional, for better recommendations)
            patient_gender: Patient gender (optional, for better recommendations)
        
        Returns:
            dict with specialization, severity, confidence, and recommendations
        """
        # Preprocess the input
        processed_text = self.preprocess_text(symptom_text)
        
        if not processed_text:
            return {
                'recommended_specialization': 'general_medicine',
                'severity': 'low',
                'confidence': 0.5,
                'recommendations': ['Please provide more details about your symptoms.'],
                'matched_symptoms': []
            }
        
        # Calculate TF-IDF similarity with symptom corpus
        symptom_vector = self.vectorizer.transform([processed_text])
        corpus_vectors = self.vectorizer.transform(self.corpus_texts)
        similarities = cosine_similarity(symptom_vector, corpus_vectors)[0]
        
        # Get top matches with improved threshold
        top_indices = np.argsort(similarities)[-5:][::-1]
        top_specializations = [self.corpus_labels[i] for i in top_indices]
        top_similarities = [similarities[i] for i in top_indices]
        
        # Use adaptive threshold for matched symptoms
        max_similarity = max(similarities) if similarities.size > 0 else 0
        adaptive_threshold = max(0.1, max_similarity * 0.3)  # 30% of max similarity
        matched_symptoms = [self.corpus_texts[i] for i in top_indices if similarities[i] > adaptive_threshold]
        
        # Determine primary specialization using improved confidence calculation
        if top_similarities[0] > 0:
            specialization_scores = {}
            
            # Calculate weighted scores for each specialization
            for i, spec in enumerate(top_specializations):
                similarity = top_similarities[i]
                
                # Base score is the similarity value
                score = similarity
                
                # Apply multiple factors for scoring
                # Boost score if multiple symptoms match this specialization
                spec_matches = [j for j, s in enumerate(top_specializations) if s == spec]
                if len(spec_matches) > 1:
                    score *= 1.1  # Reduced boost for multiple matches
                
                specialization_scores[spec] = specialization_scores.get(spec, 0) + score
            
            # Get best specialization
            if specialization_scores:
                recommended_spec = max(specialization_scores.items(), key=lambda x: x[1])[0]
                
                # Calculate proper confidence using multiple factors
                confidence = self._calculate_confidence(
                    top_similarities, 
                    top_specializations, 
                    recommended_spec,
                    similarities
                )
            else:
                recommended_spec = 'general_medicine'
                confidence = 0.3  # Low confidence for fallback
        else:
            recommended_spec = 'general_medicine'
            confidence = 0.2  # Very low confidence for no matches
        
        # Assess severity based on urgency keywords
        severity = self._assess_severity(symptom_text.lower())
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            recommended_spec, 
            severity, 
            patient_age, 
            patient_gender
        )
        
        # Generate alternative specializations with similarity threshold
        alternative_specs = []
        seen_specs = set()
        
        for i in range(1, min(len(top_specializations), 4)):
            spec = top_specializations[i]
            similarity = top_similarities[i]
            
            # Add if different from recommended and above threshold
            if spec != recommended_spec and spec not in seen_specs and similarity > 0.2:
                alternative_specs.append(spec)
                seen_specs.add(spec)
        
        return {
            'recommended_specialization': recommended_spec,
            'severity': severity,
            'confidence': round(confidence, 2),
            'recommendations': recommendations,
            'matched_symptoms': matched_symptoms[:3],
            'alternative_specializations': alternative_specs
        }
    
    def _assess_severity(self, text):
        """Assess symptom severity based on keywords"""
        # Check for high urgency keywords with word boundaries
        high_urgency_patterns = [
            r'\b' + re.escape(keyword) + r'\b' 
            for keyword in self.high_urgency_keywords
        ]
        
        for pattern in high_urgency_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return 'high'
        
        # Check for moderate urgency keywords with word boundaries
        moderate_urgency_patterns = [
            r'\b' + re.escape(keyword) + r'\b' 
            for keyword in self.moderate_urgency_keywords
        ]
        
        for pattern in moderate_urgency_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return 'moderate'
        
        return 'low'
    
    def _calculate_confidence(self, top_similarities, top_specializations, recommended_spec, all_similarities):
        """
        Calculate realistic confidence score using multiple factors
        
        Args:
            top_similarities: Similarities of top 5 matches
            top_specializations: Specializations of top 5 matches
            recommended_spec: Recommended specialization
            all_similarities: All similarity scores from corpus
            
        Returns:
            float: Confidence score between 0.0 and 1.0
        """
        try:
            # Factor 1: Average similarity of top 3 matches (40% weight)
            top_3_similarities = top_similarities[:3]
            avg_similarity = np.mean(top_3_similarities) if top_3_similarities else 0
            
            # Factor 2: Consistency across matches (25% weight)
            # Lower standard deviation = more consistent matches
            consistency = 1.0 - min(np.std(top_3_similarities) if len(top_3_similarities) > 1 else 0, 1.0)
            
            # Factor 3: Number of quality matches (20% weight)
            # Count matches above reasonable threshold
            quality_matches = len([s for s in top_3_similarities if s > 0.2])
            quality_factor = min(quality_matches / 3.0, 1.0)
            
            # Factor 4: Similarity distribution (15% weight)
            # Prefer scenarios where top match is significantly better than others
            if len(top_3_similarities) >= 2:
                distribution = top_3_similarities[0] - top_3_similarities[1]
                distribution_factor = min(distribution, 1.0)
            else:
                distribution_factor = 0.5
            
            # Calculate weighted confidence
            confidence = (
                avg_similarity * 0.4 +
                consistency * 0.25 +
                quality_factor * 0.2 +
                distribution_factor * 0.15
            )
            
            # Apply additional sanity checks
            # Ensure confidence doesn't exceed maximum similarity by too much
            max_possible_confidence = min(top_similarities[0] * 1.2, 1.0)
            confidence = min(confidence, max_possible_confidence)
            
            # Ensure minimum confidence for reasonable matches
            if top_similarities[0] > 0.3:
                confidence = max(confidence, 0.3)
            
            return round(max(0.0, min(1.0, confidence)), 2)
            
        except Exception as e:
            # Fallback confidence calculation
            return round(min(top_similarities[0] * 0.8, 0.6), 2)
    
    def _generate_recommendations(self, specialization, severity, age, gender):
        """Generate personalized recommendations"""
        recommendations = []
        
        # Urgency-based recommendations
        if severity == 'high':
            recommendations.append('⚠️ Your symptoms suggest urgent medical attention may be needed.')
            recommendations.append('Please visit the emergency department or book an immediate consultation.')
        elif severity == 'moderate':
            recommendations.append('Your symptoms require medical attention soon.')
            recommendations.append('Please book an appointment within the next 1-2 days.')
        else:
            recommendations.append('Your symptoms can typically be managed with a routine consultation.')
            recommendations.append('Book an appointment at your convenience.')
        
        # Specialization-specific advice
        spec_advice = {
            'cardiology': 'Avoid strenuous activities and rest until you see a doctor.',
            'neurology': 'Keep a symptom diary noting frequency and triggers.',
            'orthopedics': 'Apply ice/heat as appropriate and avoid aggravating movements.',
            'dermatology': 'Avoid scratching and keep the affected area clean.',
            'gastroenterology': 'Stay hydrated and maintain a bland diet until symptoms improve.',
            'pulmonology': 'Rest, stay hydrated, and avoid smoke/pollutants.',
            'ent': 'Gargle with warm salt water and stay hydrated.',
            'ophthalmology': 'Avoid eye strain and bright lights until examined.',
            'gynecology': 'Track your symptoms and menstrual cycle.',
            'psychiatry': 'Practice stress management and maintain sleep routine.',
            'general_medicine': 'Get adequate rest and stay hydrated.'
        }
        
        if specialization in spec_advice:
            recommendations.append(spec_advice[specialization])
        
        # Age-specific recommendations
        if age:
            if age < 18:
                recommendations.append('As this is for a minor, parental/guardian presence is recommended.')
            elif age > 65:
                recommendations.append('Given your age, regular health monitoring is advisable.')
        
        return recommendations


class DoctorAllocator:
    """
    Smart doctor allocation system using load balancing and specialization matching
    Uses decision algorithm with scikit-learn principles
    """
    
    def __init__(self):
        self.specialization_weights = {
            'exact_match': 1.0,
            'related_match': 0.5,
            'general_fallback': 0.3
        }
    
    def allocate_doctor(self, patient, required_specialization, preferred_date=None):
        """
        Allocate the best-fit doctor based on multiple factors:
        - Specialization match
        - Current workload (load balancing)
        - Availability
        - Doctor rating (if available)
        
        Args:
            patient: Patient object
            required_specialization: Required medical specialization
            preferred_date: Preferred appointment date (optional)
        
        Returns:
            dict with recommended doctor and allocation score
        """
        from accounts.models import Doctor
        from appointments.models import Appointment
        
        # Get all available doctors
        available_doctors = Doctor.objects.filter(
            user__is_active=True,
            is_available=True
        )
        
        if not available_doctors.exists():
            return {
                'doctor': None,
                'score': 0,
                'reason': 'No doctors currently available'
            }
        
        # Calculate date range for workload analysis (next 7 days)
        if preferred_date:
            start_date = preferred_date
        else:
            start_date = datetime.now().date()
        
        end_date = start_date + timedelta(days=7)
        
        # Score each doctor
        doctor_scores = []
        
        for doctor in available_doctors:
            score = self._calculate_doctor_score(
                doctor,
                required_specialization,
                start_date,
                end_date
            )
            
            doctor_scores.append({
                'doctor': doctor,
                'score': score,
                'workload': self._get_doctor_workload(doctor, start_date, end_date)
            })
        
        # Sort by score (descending)
        doctor_scores.sort(key=lambda x: x['score'], reverse=True)
        
        if doctor_scores and doctor_scores[0]['score'] > 0:
            best_match = doctor_scores[0]
            return {
                'doctor': best_match['doctor'],
                'score': round(best_match['score'], 2),
                'workload': best_match['workload'],
                'reason': self._get_allocation_reason(
                    best_match['doctor'],
                    required_specialization,
                    best_match['score']
                ),
                'alternatives': [
                    {
                        'doctor': d['doctor'],
                        'score': round(d['score'], 2),
                        'workload': d['workload']
                    }
                    for d in doctor_scores[1:3]
                ]
            }
        
        return {
            'doctor': None,
            'score': 0,
            'reason': 'No suitable doctor found for the required specialization'
        }
    
    def _calculate_doctor_score(self, doctor, required_specialization, start_date, end_date):
        """Calculate multi-factor score for doctor allocation"""
        # Factor 1: Specialization match (40% weight)
        specialization_score = self._get_specialization_score(
            doctor.specialization,
            required_specialization
        )
        
        # Factor 2: Workload balance (40% weight)
        workload = self._get_doctor_workload(doctor, start_date, end_date)
        workload_score = self._get_workload_score(workload)
        
        # Factor 3: Availability (20% weight)
        availability_score = 1.0 if doctor.is_available else 0.0
        
        # Weighted total score
        total_score = (
            specialization_score * 0.4 +
            workload_score * 0.4 +
            availability_score * 0.2
        )
        
        return total_score
    
    def _get_specialization_score(self, doctor_spec, required_spec):
        """Score how well doctor's specialization matches requirement"""
        # Normalize specialization strings
        doctor_spec = doctor_spec.lower().replace(' ', '_')
        required_spec = required_spec.lower().replace(' ', '_')
        
        # Exact match
        if doctor_spec == required_spec:
            return self.specialization_weights['exact_match']
        
        # Related specializations
        related_map = {
            'cardiology': ['general_medicine', 'internal_medicine'],
            'neurology': ['general_medicine', 'internal_medicine'],
            'gastroenterology': ['general_medicine', 'internal_medicine'],
            'pulmonology': ['general_medicine', 'internal_medicine'],
            'ent': ['general_medicine'],
            'ophthalmology': ['general_medicine'],
            'orthopedics': ['general_medicine', 'sports_medicine'],
            'dermatology': ['general_medicine'],
            'psychiatry': ['psychology', 'counseling'],
        }
        
        # Check if doctor's specialization is related to required
        if required_spec in related_map:
            if doctor_spec in related_map[required_spec]:
                return self.specialization_weights['related_match']
        
        # General medicine as fallback
        if doctor_spec == 'general_medicine':
            return self.specialization_weights['general_fallback']
        
        return 0.1  # Minimal score for non-matching specialization
    
    def _get_doctor_workload(self, doctor, start_date, end_date):
        """Calculate doctor's current workload"""
        from appointments.models import Appointment
        
        # Count upcoming appointments
        upcoming_count = Appointment.objects.filter(
            doctor=doctor,
            appointment_date__gte=start_date,
            appointment_date__lte=end_date,
            status__in=['scheduled', 'confirmed']
        ).count()
        
        return upcoming_count
    
    def _get_workload_score(self, workload):
        """Convert workload to a score (lower workload = higher score)"""
        # Ideal workload: 0-5 appointments (score: 1.0)
        # Moderate: 6-10 appointments (score: 0.7)
        # High: 11-15 appointments (score: 0.4)
        # Very high: 16+ appointments (score: 0.2)
        
        if workload <= 5:
            return 1.0
        elif workload <= 10:
            return 0.7
        elif workload <= 15:
            return 0.4
        else:
            return 0.2
    
    def _get_allocation_reason(self, doctor, required_spec, score):
        """Generate human-readable reason for allocation"""
        reasons = []
        
        doctor_spec = doctor.specialization.lower().replace(' ', '_')
        required_spec = required_spec.lower().replace(' ', '_')
        
        if doctor_spec == required_spec:
            reasons.append(f"Exact specialization match ({doctor.specialization})")
        else:
            reasons.append(f"Available specialist in {doctor.specialization}")
        
        if score > 0.8:
            reasons.append("Optimal availability and low workload")
        elif score > 0.6:
            reasons.append("Good availability")
        else:
            reasons.append("Available for consultation")
        
        return " | ".join(reasons)
    
    def get_workload_analytics(self):
        """Get system-wide workload analytics for admin dashboard"""
        from accounts.models import Doctor
        from appointments.models import Appointment
        
        today = datetime.now().date()
        next_week = today + timedelta(days=7)
        
        doctors = Doctor.objects.filter(user__is_active=True)
        
        analytics = []
        for doctor in doctors:
            workload = self._get_doctor_workload(doctor, today, next_week)
            workload_status = 'Low' if workload <= 5 else 'Moderate' if workload <= 10 else 'High'
            
            analytics.append({
                'doctor': doctor,
                'workload': workload,
                'status': workload_status,
                'utilization_rate': min(workload / 15 * 100, 100)  # Assuming 15 is max capacity
            })
        
        return analytics


# Singleton instances
symptom_analyzer = SymptomAnalyzer()
doctor_allocator = DoctorAllocator()
