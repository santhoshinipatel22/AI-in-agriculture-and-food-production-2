"""
24/7 AI Chatbot for Smart Farming
Powered by NLP and Knowledge Base
"""

import json
from datetime import datetime
import re

class FarmingChatbot:
    """
    Intelligent chatbot for farming queries with knowledge base
    """
    
    def __init__(self):
        self.knowledge_base = self._initialize_knowledge_base()
        self.conversation_history = []
        self.user_context = {}
    
    def _initialize_knowledge_base(self):
        """Initialize knowledge base with farming information"""
        return {
            'crops': {
                'rice': {
                    'season': 'Monsoon (June-September)',
                    'water_requirement': '200-300 mm/month',
                    'best_soil': 'Clay loam, pH 6.0-7.0',
                    'maturity': '120-150 days',
                    'yield': '4000-6000 kg/ha',
                    'common_diseases': ['Blast', 'Brown spot', 'Leaf scald'],
                },
                'wheat': {
                    'season': 'Winter (October-March)',
                    'water_requirement': '400-500 mm',
                    'best_soil': 'Loam, pH 6.0-7.5',
                    'maturity': '120-140 days',
                    'yield': '4000-5500 kg/ha',
                    'common_diseases': ['Powdery mildew', 'Rust', 'Blight'],
                },
                'corn': {
                    'season': 'Spring/Summer (March-July)',
                    'water_requirement': '500-800 mm',
                    'best_soil': 'Well-drained loam',
                    'maturity': '90-120 days',
                    'yield': '5000-8000 kg/ha',
                    'common_diseases': ['Leaf blight', 'Stalk rot', 'Anthracnose'],
                },
            },
            'diseases': {
                'leaf_rust': {
                    'crops': ['Wheat', 'Barley', 'Corn'],
                    'symptoms': 'Reddish-brown pustules on leaves',
                    'cause': 'Fungal infection',
                    'treatment_organic': 'Sulfur dust, Neem oil',
                    'treatment_chemical': 'Mancozeb, Tebuconazole',
                    'prevention': 'Resistant varieties, Crop rotation',
                },
                'powdery_mildew': {
                    'crops': ['Wheat', 'Barley', 'Cucumber', 'Melon'],
                    'symptoms': 'White powder on leaves',
                    'cause': 'Fungal infection',
                    'treatment_organic': 'Sulfur, Potassium bicarbonate',
                    'treatment_chemical': 'Triazoles, Sulfites',
                    'prevention': 'Good air circulation, Remove infected parts',
                },
            },
            'practices': {
                'intercropping': 'Growing two or more crops on same field to maximize yield',
                'mulching': 'Covering soil to retain moisture and prevent weeds',
                'crop_rotation': 'Alternating crops to maintain soil fertility',
                'drip_irrigation': 'Water-efficient targeted irrigation method',
                'organic_farming': 'Using natural methods without synthetic chemicals',
            },
            'fertilizers': {
                'neem': 'Natural pesticide, controls many insects, organic approved',
                'urea': '46% nitrogen, most common nitrogen fertilizer',
                'superphosphate': 'Phosphorus source for plant development',
                'muriate_potash': 'Potassium source for plant growth',
                'cow_dung': 'Organic manure, improves soil structure',
            },
        }
    
    def process_query(self, user_input):
        """
        Process user query and generate response
        """
        user_input = user_input.lower().strip()
        
        # Log conversation
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user': user_input,
        })
        
        # Detect query type
        if 'crop' in user_input or 'plant' in user_input:
            response = self._handle_crop_query(user_input)
        elif 'disease' in user_input or 'pest' in user_input or 'infection' in user_input:
            response = self._handle_disease_query(user_input)
        elif 'water' in user_input or 'irrigat' in user_input:
            response = self._handle_irrigation_query(user_input)
        elif 'price' in user_input or 'market' in user_input or 'sell' in user_input:
            response = self._handle_price_query(user_input)
        elif 'weather' in user_input or 'rain' in user_input or 'temperature' in user_input:
            response = self._handle_weather_query(user_input)
        elif 'subsidy' in user_input or 'scheme' in user_input or 'loan' in user_input:
            response = self._handle_subsidy_query(user_input)
        else:
            response = self._handle_general_query(user_input)
        
        self.conversation_history[-1]['bot'] = response
        return response
    
    def _handle_crop_query(self, query):
        """Handle crop-related queries"""
        response = {}
        
        for crop, info in self.knowledge_base['crops'].items():
            if crop in query:
                response = {
                    'type': 'crop_info',
                    'crop': crop.capitalize(),
                    'information': info,
                    'message': f"Here's information about {crop.capitalize()}:\n" +
                                f"Season: {info['season']}\n" +
                                f"Water Requirement: {info['water_requirement']}\n" +
                                f"Best Soil: {info['best_soil']}\n" +
                                f"Maturity Period: {info['maturity']}\n" +
                                f"Expected Yield: {info['yield']}"
                }
                break
        
        if not response:
            response = {
                'type': 'crop_list',
                'message': f"Available crops: {', '.join(self.knowledge_base['crops'].keys())}\n" +
                           "Ask me about any of these crops for detailed information."
            }
        
        return response
    
    def _handle_disease_query(self, query):
        """Handle disease-related queries"""
        for disease, info in self.knowledge_base['diseases'].items():
            if disease.replace('_', ' ') in query or disease.replace('_', '') in query:
                return {
                    'type': 'disease_info',
                    'disease': disease.replace('_', ' ').title(),
                    'information': info,
                    'message': f"Information about {disease.replace('_', ' ').title()}:\n" +
                                f"Affects: {', '.join(info['crops'])}\n" +
                                f"Symptoms: {info['symptoms']}\n" +
                                f"Organic Treatment: {info['treatment_organic']}\n" +
                                f"Chemical Treatment: {info['treatment_chemical']}\n" +
                                f"Prevention: {info['prevention']}"
                }
        
        return {
            'type': 'general',
            'message': "For disease identification, please upload a photo of the affected leaf. " +
                      "Or describe the symptoms in detail."
        }
    
    def _handle_irrigation_query(self, query):
        """Handle irrigation-related queries"""
        return {
            'type': 'irrigation_advisory',
            'message': "Irrigation advice:\n" +
                      "- Check soil moisture before irrigating\n" +
                      "- Best time: Early morning or late evening\n" +
                      "- Drip irrigation: Most water-efficient\n" +
                      "- Avoid irrigation during heavy rain\n" +
                      "- Water requirement varies by crop and season"
        }
    
    def _handle_price_query(self, query):
        """Handle market price queries"""
        return {
            'type': 'price_info',
            'message': "Market price information:\n" +
                      "- Check daily prices on AGMARKNET website\n" +
                      "- Current rates may vary by location\n" +
                      "- Best to sell when prices are high\n" +
                      "- Use AI prediction for optimal selling time\n" +
                      "- Storage can help sell at better prices later"
        }
    
    def _handle_weather_query(self, query):
        """Handle weather-related queries"""
        return {
            'type': 'weather_guidance',
            'message': "Weather guidance:\n" +
                      "- Monitor 10-day forecast for planning\n" +
                      "- Delay planting if heavy rain expected\n" +
                      "- Increase irrigation in high temperature\n" +
                      "- Spray fungicides during humid weather\n" +
                      "- Use weather-based alerts for better decisions"
        }
    
    def _handle_subsidy_query(self, query):
        """Handle government scheme queries"""
        return {
            'type': 'subsidy_info',
            'message': "Government Schemes:\n" +
                      "- PM-KISAN: Rs. 6000/year for all farmers\n" +
                      "- Soil Health Card: Free soil testing\n" +
                      "- Crop Insurance: Risk protection\n" +
                      "- Infrastructure Development: Subsidized equipment\n" +
                      "Check eligibility and apply through government portals or banks"
        }
    
    def _handle_general_query(self, query):
        """Handle general queries"""
        return {
            'type': 'general',
            'message': "I can help you with:\n" +
                      "- Crop information and recommendations\n" +
                      "- Disease identification and treatment\n" +
                      "- Irrigation and water management\n" +
                      "- Market prices and trends\n" +
                      "- Weather forecasts and advisories\n" +
                      "- Government schemes and subsidies\n" +
                      "What would you like to know?"
        }
    
    def get_recommendation(self, context):
        """
        Get farming recommendation based on context
        context: {
            'crop': str,
            'season': str,
            'soil_condition': dict,
            'weather': dict,
        }
        """
        crop = context.get('crop', '').lower()
        
        recommendations = []
        
        if crop in self.knowledge_base['crops']:
            crop_info = self.knowledge_base['crops'][crop]
            recommendations.append(f"Best season for {crop}: {crop_info['season']}")
            recommendations.append(f"Expected yield: {crop_info['yield']}")
        
        return {
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat(),
        }


if __name__ == '__main__':
    chatbot = FarmingChatbot()
    
    # Test conversations
    test_queries = [
        "Tell me about rice farming",
        "How to prevent leaf rust?",
        "When should I irrigate my crops?",
        "What are current vegetable prices?",
    ]
    
    for query in test_queries:
        response = chatbot.process_query(query)
        print(f"User: {query}")
        print(f"Bot: {response['message']}\n")
