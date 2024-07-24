from flask import Flask, request, jsonify
import pandas as pd
import pickle
import yfinance as yf
import mysql.connector
from waitress import serve
from mysql.connector import Error
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Global variables for model and label encoder
model = None
le = None

# Load the pre-trained model and label encoder
try:
    model_path = r"C:\Users\Vani\Desktop\AD project- Portfolio Visualiser\Moneyport_ML\models\risk_assessment_model.pkl"
    le_path = r"C:\Users\Vani\Desktop\AD project- Portfolio Visualiser\Moneyport_ML\models\label_encoder.pkl"
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    with open(le_path, 'rb') as f:
        le = pickle.load(f)
    
    print("Model and label encoder loaded successfully")
except FileNotFoundError as fnf_error:
    print(f"FileNotFoundError: {str(fnf_error)}")
except pickle.UnpicklingError as pkl_error:
    print(f"PickleError: {str(pkl_error)}")
except Exception as e:
    print(f"Error loading model or label encoder: {str(e)}")

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'dhushdiya2024',
    'database': 'stocks'
}

# Get DB connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def get_stocks_for_risk_level(risk_level):
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to database")
        return []
    
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT symbol, name, sector FROM stocks WHERE risk_level = %s"
        cursor.execute(query, (risk_level,))
        stocks = cursor.fetchall()
        print(f"Fetched {len(stocks)} stocks for risk level {risk_level}")
        return stocks
    except Error as e:
        print(f"Error fetching stocks for risk level {risk_level}: {e}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def fetch_stock_data(stocks):
    stock_data = []
    for stock in stocks:
        try:
            ticker = yf.Ticker(stock['symbol'])
            info = ticker.info
            stock_data.append({
                'symbol': stock['symbol'],
                'name': stock['name'],
                'sector': stock['sector'],
                'current_price': info.get('currentPrice', 0)
            })
            print(f"Successfully fetched data for {stock['symbol']}")
        except Exception as e:
            print(f"Error fetching data for {stock['symbol']}: {e}")
    return stock_data

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "API is working"}), 200

@app.route('/predict_and_recommend', methods=['POST'])
def predict_and_recommend():
    global model, le
    if model is None or le is None:
        return jsonify({'error': 'Model or label encoder not loaded'}), 500

    try:
        data = request.json
        print("Received data:", data)
        
        # Ensure all expected keys are present
        expected_keys = ['investmentGoal', 'timeHorizon', 'riskTolerance', 'income', 'investmentExperience', 'lossReaction', 'age']
        for key in expected_keys:
            if key not in data:
                raise ValueError(f"Missing key in received data: {key}")
        
        answers = [
            data['investmentGoal'],
            data['timeHorizon'],
            data['riskTolerance'],
            data['income'],
            data['investmentExperience'],
            data['lossReaction'],
            data['age']
        ]
        
        print("Answers:", answers)

        # Convert answers to a DataFrame
        input_data = pd.DataFrame([answers], columns=[
            'investmentGoal', 'timeHorizon', 'riskTolerance', 'income',
            'investmentExperience', 'lossReaction', 'age'
        ])
        print("Input data for model:", input_data)
        
        # Predict risk level
        prediction = model.predict(input_data)
        risk_level = le.inverse_transform(prediction)[0]
        print("Predicted risk level:", risk_level)
        
        # Fetch recommended stocks
        stocks = get_stocks_for_risk_level(risk_level)
        stock_data = fetch_stock_data(stocks)

        return jsonify({
            'risk_level': risk_level,
            'recommended_stocks': stock_data
        })
    except ValueError as ve:
        print(f"ValueError in predict_and_recommend: {str(ve)}")
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        print(f"Error in predict_and_recommend: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
