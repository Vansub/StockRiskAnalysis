AD project: MoneyPort
Machine Learning  and Risk Assessment



Componenets: 
1. Flask Backend (Moneyport-ML, app.py)
2. Spring Boot Backend(StockAssessment)
3. Reactjs Frontend (Moneyport/frontend)


Risk Assessment and Stock Recommendation 
This project is Flask-based web application that assess and investor’s risk profile and recommends stocks based on that assessment.

Project Structure:

traindataGenerator.py :  to generate the features for training 
risk_assessment_traintest.py:   train-test using Decision Tree 
app.py :  Main Flask Application
models:
1. Risk_assessment_model.pk1 :  Pickled machine learning model  for risk assessment
2. Label_encoder.pk1 : Picked label encoder for risk levels
   
Populate_Stock_db.py: Script to populate the MYSQL database with stock data

Setup
Part 1:
Run traindataGenerator for generating the csv file (investment_risk_assessment.csv
)
Run risk_assessment_traintest to train the model using Decision Tree 
Models will be created in a model folder: 
1.	risk_assessment_model.pkl
2.	label_encoder.pkl

Part 2:
1.install MySQL database :
 CREATE  TABLE  stocks(
Id INT AUTO_INCREMENT PRIMARY KEY,
symbol VARCHAR(10) NOT NULL,	
name VARCHAR(100) NOT NULL,
risk_level ENUM(‘R1’,’R2’,’R3’) NOT NULL,
sector VARCHAR(50),
UNIQUE (symbol)
);
Postman: the table features and query result
 
Browser:
 
2. Update the db_config in both app.py and populate_stock_db.py with MySQL credentials
3. Run ‘populate_stock_db.py’ to populate the database with sample stock data
4. Ensure ‘risk_assessment_model.pkl’ and  ‘label_encoder.pkl’ are on the same directory as     
   app.py
Running the application
1.	Run Flask application (app.py)
   
3.	The application will start running on ‘http://localhost:8080’
Postman test result given below:
API endpoint
/predict_and_recommend (POST)

Input : JSON        
{
  "investmentGoal": 1,
  "timeHorizon": 2,
  "riskTolerance": 1,
  "income": 2,
  "investmentExperience": 3,
  "lossReaction": 2,
  "age": 3
}
Output: JSON with risk_level and recommended_stocks




Test using postman 
POST
http://localhost:8080/predict_and_recommend
Body
Raw
Json

{
    "investment_goal": 3,
    "time_horizon": 2,
    "risk_tolerance": 4,
    "income": 2,
    "investment_experience": 3,
    "loss_reaction": 3,
    "age": 2
}

Result:[ will get 10 results ]
{
    "recommended_stocks": [
        {
            "current_price": 223.96,
            "name": "Apple Inc.",
            "sector": "Technology",
            "symbol": "AAPL"
        },
Part 3:
StockAssessment 
Springboot backend will handle API requests from react frontend and interacts with the Flask backend for predictions and recommendations
server.port = 8082 (should be different from flask (8080))
API endpoint: 
Post
/predict_and_recommend

Part 4:
React frontend

running the applicaton together with all above components
1. Start  FlaskBackend in vscode
   cd Moneyport_ML/flask_backend
   python app.py
2. Start SpringBoot backend in 
   run the springboot
3. split vscode terminal if required to run the react frontend
   cd Moneyport/frontend
   npm start
Testig:
Postman
http://localhost:8080 in postman
http://localhost:8082 in postman
http://localhost:3000 in browser

 
