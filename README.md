# Personalized Fitness & Diet AI App

A comprehensive web application that generates personalized fitness and nutrition plans based on user metrics, preferences, and goals.

## Features

- **Metrics Calculation**: Calculates BMI, body fat percentage, BMR, TDEE, and macronutrient recommendations
- **AI-Powered Plan Generation**: Creates personalized workout routines and meal plans using AI (Ollama)
- **PDF Generation**: Provides downloadable PDF fitness plans with all recommendations
- **Age-Appropriate Modifications**: Special considerations for users over 50
- **Educational Resources**: Informative pages about fitness metrics, nutrition, and workouts

## Tech Stack

- **Frontend**: React, Material-UI, Recharts
- **Backend**: Flask (Python), FPDF
- **AI**: Ollama (using deepseek-r1:8b model)
- **Database**: Optional integration with Supabase

## Setup Instructions

### Prerequisites

- Python 3.8+ 
- Node.js 16+
- Ollama installed and running with the `deepseek-r1:8b` model

### Backend Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate.ps1  # PowerShell
     venv\Scripts\activate.bat  # Command Prompt
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Start the Flask server:
   ```
   python -m flask --app api.app run --debug
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

### Ollama Setup

1. Make sure Ollama is installed and running
2. Pull the deepseek-r1:8b model:
   ```
   ollama pull deepseek-r1:8b
   ```

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Fill out the form with your personal details and preferences
3. Submit the form to generate your personalized fitness plan
4. View your metrics and download your personalized PDF plan

## License

MIT

## Credits

Created with ❤️ using React, Flask, and Ollama 