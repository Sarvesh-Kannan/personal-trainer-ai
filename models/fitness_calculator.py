import math

class FitnessCalculator:
    def __init__(self, age, weight, height, waist, neck, gender='male', activity_level='moderate', goal='maintenance'):
        """
        Initialize the fitness calculator with user metrics
        
        Parameters:
        - age: age in years
        - weight: weight in kg
        - height: height in cm
        - waist: waist circumference in cm
        - neck: neck circumference in cm
        - gender: 'male' or 'female'
        - activity_level: 'sedentary', 'light', 'moderate', 'active', 'very_active'
        - goal: 'lose_fat', 'maintenance', 'build_muscle'
        """
        self.age = age
        self.weight = weight
        self.height = height
        self.waist = waist
        self.neck = neck
        self.gender = gender.lower()
        self.activity_level = activity_level.lower()
        self.goal = goal.lower()
        
        # Activity level multipliers
        self.activity_multipliers = {
            'sedentary': 1.2,      # Little or no exercise
            'light': 1.375,        # Light exercise/sports 1-3 days/week
            'moderate': 1.55,      # Moderate exercise/sports 3-5 days/week
            'active': 1.725,       # Hard exercise/sports 6-7 days/week
            'very_active': 1.9     # Very hard exercise & physical job or 2x training
        }
        
        # Goal calorie adjustments
        self.goal_multipliers = {
            'lose_fat': 0.8,       # 20% calorie deficit
            'maintenance': 1.0,    # Maintain current weight
            'build_muscle': 1.1    # 10% calorie surplus
        }
    
    def calculate_bmi(self):
        """Calculate Body Mass Index (BMI)"""
        # Formula: BMI = weight(kg) / (height(m))²
        height_in_meters = self.height / 100
        bmi = self.weight / (height_in_meters ** 2)
        return round(bmi, 2)
    
    def calculate_body_fat(self):
        """Calculate body fat percentage using US Navy method"""
        # Convert cm to inches
        height_in_inches = self.height / 2.54
        waist_in_inches = self.waist / 2.54
        neck_in_inches = self.neck / 2.54
        
        if self.gender == 'male':
            # Male formula
            body_fat = 495 / (1.0324 - 0.19077 * (math.log10(waist_in_inches - neck_in_inches)) + 0.15456 * (math.log10(height_in_inches))) - 450
        else:
            # Female formula (need hip measurement, default to waist * 1.4 as approximation)
            hip_in_inches = waist_in_inches * 1.4  # Approximation
            body_fat = 495 / (1.29579 - 0.35004 * (math.log10(waist_in_inches + hip_in_inches - neck_in_inches)) + 0.22100 * (math.log10(height_in_inches))) - 450
        
        return round(body_fat, 2)
    
    def calculate_bmr(self):
        """Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor equation"""
        if self.gender == 'male':
            bmr = (10 * self.weight) + (6.25 * self.height) - (5 * self.age) + 5
        else:
            bmr = (10 * self.weight) + (6.25 * self.height) - (5 * self.age) - 161
        
        return round(bmr)
    
    def calculate_tdee(self):
        """Calculate Total Daily Energy Expenditure"""
        bmr = self.calculate_bmr()
        activity_multiplier = self.activity_multipliers.get(self.activity_level, 1.55)  # Default to moderate if not found
        tdee = bmr * activity_multiplier
        
        return round(tdee)
    
    def calculate_goal_calories(self):
        """Calculate calories based on goal (deficit, maintenance, or surplus)"""
        tdee = self.calculate_tdee()
        goal_multiplier = self.goal_multipliers.get(self.goal, 1.0)  # Default to maintenance if not found
        goal_calories = tdee * goal_multiplier
        
        return round(goal_calories)
    
    def calculate_macros(self):
        """Calculate recommended macronutrient split based on goal"""
        goal_calories = self.calculate_goal_calories()
        
        # Set protein based on body weight and goal
        if self.goal == 'lose_fat':
            # Higher protein during fat loss to preserve muscle (1g per lb of body weight)
            protein_g = self.weight * 2.2  # Convert kg to lbs
        elif self.goal == 'build_muscle':
            # Higher protein for muscle building (1.1g per lb of body weight)
            protein_g = self.weight * 2.2 * 1.1
        else:
            # Moderate protein for maintenance (0.8g per lb of body weight)
            protein_g = self.weight * 2.2 * 0.8
        
        protein_calories = protein_g * 4  # 4 calories per gram of protein
        
        # Adjust fat based on goal
        if self.goal == 'lose_fat':
            # Lower fat during cutting phase (25% of calories)
            fat_calories = goal_calories * 0.25
        else:
            # Moderate fat for other goals (30% of calories)
            fat_calories = goal_calories * 0.3
        
        fat_g = fat_calories / 9  # 9 calories per gram of fat
        
        # Remaining calories from carbs
        carb_calories = goal_calories - protein_calories - fat_calories
        carb_g = carb_calories / 4  # 4 calories per gram of carbs
        
        return {
            "protein": round(protein_g),
            "carbs": round(carb_g),
            "fat": round(fat_g)
        } 