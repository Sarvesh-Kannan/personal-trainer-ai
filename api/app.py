import os
import json
import requests
import time
from fpdf import FPDF
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from models.fitness_calculator import FitnessCalculator
from database.supabase_client import SupabaseClient
from utils.config import Config

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Supabase client
supabase_client = SupabaseClient()

PLANS_DIR = os.path.join(os.path.dirname(__file__), '../plans')
os.makedirs(PLANS_DIR, exist_ok=True)

def generate_with_ollama(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "deepseek-r1:8b",
            "prompt": prompt,
            "stream": False
        }
    )
    response.raise_for_status()
    return response.json()["response"]

def generate_pdf(content, user_name, metrics, age):
    """Generate a PDF file with the fitness plan"""
    timestamp = int(time.time())
    filename = f"fitness_plan_{timestamp}.pdf"
    filepath = os.path.join(PLANS_DIR, filename)
    
    # Function to clean text of problematic Unicode characters
    def clean_text(text):
        # Replace curly apostrophes and quotes with straight ones
        text = text.replace('\u2018', "'").replace('\u2019', "'")
        text = text.replace('\u201c', '"').replace('\u201d', '"')
        # Replace other problematic characters
        text = text.replace('\u2013', '-').replace('\u2014', '-')
        text = text.replace('\u2022', '*')  # Replace bullet points
        return text
    
    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Personalized Fitness Plan for {clean_text(user_name)}", ln=True, align="C")
    pdf.ln(5)
    
    # Metrics Summary
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Your Health Metrics:", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 8, f"BMI: {metrics.get('bmi', 'N/A')}", ln=True)
    pdf.cell(0, 8, f"Body Fat: {metrics.get('bodyFatPercentage', 'N/A')}%", ln=True)
    pdf.cell(0, 8, f"BMR: {metrics.get('bmr', 'N/A')} calories/day", ln=True)
    pdf.cell(0, 8, f"TDEE: {metrics.get('tdee', 'N/A')} calories/day", ln=True)
    pdf.cell(0, 8, f"Goal Calories: {metrics.get('goalCalories', 'N/A')} calories/day", ln=True)
    
    macros = metrics.get('macros', {})
    pdf.cell(0, 8, f"Macros: Protein: {macros.get('protein', 'N/A')}g | Carbs: {macros.get('carbs', 'N/A')}g | Fat: {macros.get('fat', 'N/A')}g", ln=True)
    pdf.ln(5)
    
    # Content
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Your Personalized Plan:", ln=True)
    pdf.set_font("Arial", "", 10)
    
    # Clean the content
    content = clean_text(content)
    
    # Split content by lines and add to PDF
    lines = content.split('\n')
    for line in lines:
        # Skip empty lines
        if not line.strip():
            pdf.ln(3)
            continue
            
        # Check if line is a section header (e.g., "WORKOUT PLAN", "MEAL PLAN")
        if line.strip().upper() == line.strip() and len(line.strip()) > 0 and not line.startswith(' '):
            pdf.ln(5)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, line, ln=True)
            pdf.set_font("Arial", "", 10)
        else:
            # For regular text, wrap long lines
            pdf.multi_cell(0, 5, line)
    
    # Age disclaimer for users over 50
    if age and int(age) >= 50:
        pdf.ln(10)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Important Note for Seniors:", ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 5, "Since you are 50 or older, please consider the following:")
        pdf.multi_cell(0, 5, "- Always consult with your healthcare provider before starting any new exercise program.")
        pdf.multi_cell(0, 5, "- Begin each workout with a longer warm-up (10-15 minutes) to properly prepare your joints and muscles.")
        pdf.multi_cell(0, 5, "- Focus on proper form rather than intensity or weight.")
        pdf.multi_cell(0, 5, "- Consider aquatic exercises which are lower impact on joints.")
        pdf.multi_cell(0, 5, "- Listen to your body and rest when needed. Recovery may take longer as we age.")
        pdf.multi_cell(0, 5, "- If you feel pain (not just muscle fatigue), stop the exercise immediately.")
    
    # Footer
    pdf.ln(10)
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 10, f"Generated on {time.strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
    
    # Save PDF
    try:
        pdf.output(filepath)
        return filename
    except Exception as e:
        print(f"Error generating PDF: {e}")
        # Fallback to text file if PDF generation fails
        txt_filename = f"fitness_plan_{timestamp}.txt"
        txt_filepath = os.path.join(PLANS_DIR, txt_filename)
        with open(txt_filepath, 'w', encoding='utf-8') as f:
            f.write(f"Personalized Fitness Plan for {user_name}\n\n")
            f.write("Your Health Metrics:\n")
            f.write(f"BMI: {metrics.get('bmi', 'N/A')}\n")
            f.write(f"Body Fat: {metrics.get('bodyFatPercentage', 'N/A')}%\n")
            f.write(f"BMR: {metrics.get('bmr', 'N/A')} calories/day\n")
            f.write(f"TDEE: {metrics.get('tdee', 'N/A')} calories/day\n")
            f.write(f"Goal Calories: {metrics.get('goalCalories', 'N/A')} calories/day\n")
            f.write(f"Macros: Protein: {macros.get('protein', 'N/A')}g | Carbs: {macros.get('carbs', 'N/A')}g | Fat: {macros.get('fat', 'N/A')}g\n\n")
            f.write(content)
            
            if age and int(age) >= 50:
                f.write("\n\nImportant Note for Seniors:\n")
                f.write("Since you are 50 or older, please consider the following:\n")
                f.write("- Always consult with your healthcare provider before starting any new exercise program.\n")
                f.write("- Begin each workout with a longer warm-up (10-15 minutes) to properly prepare your joints and muscles.\n")
                f.write("- Focus on proper form rather than intensity or weight.\n")
                f.write("- Consider aquatic exercises which are lower impact on joints.\n")
                f.write("- Listen to your body and rest when needed. Recovery may take longer as we age.\n")
                f.write("- If you feel pain (not just muscle fatigue), stop the exercise immediately.\n")
        
        return txt_filename

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "API is running"}), 200

@app.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        
        # Extract user data
        age = data.get('age')
        weight = data.get('weight')  # in kg
        height = data.get('height')  # in cm
        waist = data.get('waist')    # in cm
        neck = data.get('neck')      # in cm
        gender = data.get('gender', 'male')
        activity_level = data.get('activityLevel', 'moderate')
        goal = data.get('goal', 'maintenance')
        
        # Validate required fields
        if not all([age, weight, height, waist, neck]):
            return jsonify({"error": "Missing required fields"}), 400
            
        # Create calculator instance
        calculator = FitnessCalculator(
            age=age,
            weight=weight,
            height=height,
            waist=waist,
            neck=neck,
            gender=gender,
            activity_level=activity_level,
            goal=goal
        )
        
        # Calculate all metrics
        results = {
            "bmi": calculator.calculate_bmi(),
            "bodyFatPercentage": calculator.calculate_body_fat(),
            "bmr": calculator.calculate_bmr(),
            "tdee": calculator.calculate_tdee(),
            "goalCalories": calculator.calculate_goal_calories(),
            "macros": calculator.calculate_macros()
        }
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate-plan', methods=['POST'])
def generate_plan():
    try:
        data = request.json
        metrics = data.get('metrics', {})
        preferences = data.get('preferences', {})
        medical_conditions = data.get('medicalConditions', [])
        goal = data.get('goal', 'maintenance').lower()
        user_name = data.get('name', 'User')
        age = data.get('age')

        # Macros calculation remains as is
        macros = metrics.get('macros', {})

        # Determine workout plan days based on goal
        if 'muscle' in goal:
            workout_days = 6
        else:
            workout_days = 3

        # Fat loss: add explicit calorie deficit instruction
        fat_loss_instruction = ''
        if 'fat' in goal or 'loss' in goal or 'weight' in goal:
            fat_loss_instruction = 'The meal plan MUST be in a calorie deficit based on the user\'s TDEE and goal calories. Meals should be filling, high in protein, and support fat loss.'

        # Add age-specific considerations for older adults
        age_instructions = ''
        if age and int(age) >= 50:
            age_instructions = """
Since the user is 50 or older, include these IMPORTANT exercise modifications:
- Reduce high-impact exercises (like jumping, running on hard surfaces)
- Include more joint-friendly activities (swimming, cycling, elliptical)
- Focus on mobility and flexibility exercises
- Decrease weight/resistance but maintain proper form
- Include more comprehensive warm-ups and cool-downs
- Suggest longer recovery periods between training days
- Emphasize proper hydration and nutrition for recovery
- Recommend using perceived exertion rather than maximum effort
"""

        # Build prompt for Ollama (plain text, not JSON)
        prompt = f"""
You are a professional fitness and nutrition coach creating a personalized plan for {user_name}, age {age}. Based on the following data, generate a detailed, readable plan in plain text:

User metrics:
- BMI: {metrics.get('bmi', 'Not provided')}
- Body Fat %: {metrics.get('bodyFatPercentage', 'Not provided')}%
- BMR: {metrics.get('bmr', 'Not provided')} calories
- TDEE: {metrics.get('tdee', 'Not provided')} calories
- Goal calories: {metrics.get('goalCalories', 'Not provided')} calories
- Macros: Protein: {macros.get('protein', 'Not provided')}g, Carbs: {macros.get('carbs', 'Not provided')}g, Fat: {macros.get('fat', 'Not provided')}g

Preferences:
- Cuisine: {preferences.get('cuisine', 'Not provided')}
- Restrictions: {preferences.get('restrictions', 'None')}
- Medical conditions: {', '.join(medical_conditions) if medical_conditions else 'None'}
- Primary goal: {goal}

{fat_loss_instruction}
{age_instructions}

Please provide:
1. A {workout_days}-day workout plan, with each day described in detail.
2. A 3-day meal plan, with each meal (breakfast, lunch, dinner, snacks) described in detail.
3. Rest day activities and recommendations.
4. Morning and evening routine suggestions for optimal health.
5. A general suggestion or opinion based on the user's metrics and calculated values, regardless of their goal.

Format the output as readable sections with clear headings for each part. Use ALL CAPS for main section headings. Do not use JSON or markdown. Make it personalized for {user_name} directly, using their name throughout the plan.
"""
        
        # Generate the response using Ollama
        response_text = generate_with_ollama(prompt)

        # Generate PDF with the response
        pdf_filename = generate_pdf(response_text, user_name, metrics, age)

        # Return macros and download link for the PDF
        return jsonify({
            "macros": macros,
            "planFile": pdf_filename
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/plan-file/<filename>', methods=['GET'])
def download_plan_file(filename):
    return send_from_directory(PLANS_DIR, filename, as_attachment=True)

@app.route('/api/user', methods=['POST'])
def create_user():
    try:
        data = request.json
        result = supabase_client.create_user(data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/user/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        result = supabase_client.get_user(user_id)
        if result:
            return jsonify(result), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.json
        result = supabase_client.update_user(user_id, data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/plan/<user_id>', methods=['POST'])
def save_plan(user_id):
    try:
        data = request.json
        result = supabase_client.save_plan(user_id, data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/plan/<user_id>', methods=['GET'])
def get_plan(user_id):
    try:
        result = supabase_client.get_plan(user_id)
        if result:
            return jsonify(result), 200
        return jsonify({"error": "Plan not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 