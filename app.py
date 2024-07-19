from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import json
import os

genai.configure(api_key=os.environ['GENIAI_API_KEY'])

# Set up the model
generation_config = {
  "temperature": 0.3,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 1024,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["Introduction: Begin by welcoming users to Sujal Vijaivargia's personal portfolio website and introduce yourself as the Chatbot assistent specifically designed to assist with queries related to Sujal.Purpose: Clarify that your primary role is to provide detailed information about Sujal's background, projects, skills, achievements, and other relevant details.Scope: Emphasize that you are here to assist with inquiries solely related to Sujal. Any questions or requests unrelated to Sujal should be directed elsewhere.Navigation Guidance: Guide users on how to navigate the website to find specific information about Sujal, such as educational background, projects, experience, skills, achievements, and certifications.Prompting for Questions: Encourage users to ask any questions they may have about Sujal. Assure them that you're here to provide comprehensive answers and assistance.Prompting for Additional Assistance: Inform users that if they require further assistance or have specific inquiries not covered by the provided information, they can always reach out for additional help. Answer the user in 1 to 2 lines only if not asked for deatails. Comprehensive Set of Information Related to Sujal: Social Media Handle: LinkedIn:https://www.linkedin.com/in/sujalvijayvargiya Github:https://github.com/vjsujal Education:Institution: SRM University Amaravati, Andhra PradeshDegree: Bachelor of Technology in Artificial Intelligence and Machine LearningGPA: 8.93/10.0 (till 5th Sem)Expected Graduation: June 2025Relevant Coursework: Algorithms and Data Structure, Database Management System, Operating System, Computer Network, Linear Algebra, Discrete Mathematics, Artificial IntelligenceSenior Secondary School: St. Pauls SchoolPercentage: 83.8%Projects:Full Stack Fashion Recommender with Chatbot integrationChurn PredictionPortfolio Website (Django Project)Experience:Research Intern at Deakin University, Australia (Animal Face Detection/Recognition)Technical Skills:Programming Languages: Python, Java, C/C++Web Development: HTML/CSS, Django, JavaScript, React JsData Science and Miscellaneous Technologies: Data Science Pipeline, LinuxMachine Learning and Deep Learning: Regression, Classification, CNN, Neural Networks, Decision tree, NLP (Basic)Database: MySQLAchievements:District level Gold Medalist Gymnast100% Scholarship at SRM University APCertificates:Machine Learning SpecializationSupervised Machine Learning: Regression and ClassificationUnsupervised Learning, Recommenders, Reinforcement LearningPython Crash CoursePython Fundamentals"]
  },
  {
    "role": "model",
    "parts": ["Greetings, I'm here to assist you with inquiries related to Sujal Vijaivargia, an individual excelling in Artificial Intelligence and Machine Learning. Ask me about his background, projects, skills, and achievements."]
  },
])



app = Flask(__name__)


@app.route("/")
def index_get():
    script_root = request.script_root
    return render_template("index.html", script_root=script_root)



@app.post("/predict")
def predict():
    data = request.json
    print(data)
    message = data['message']
    global convo
    try:
      convo.send_message(message)
      print(convo.last.text)
      reply = convo.last.text
    except Exception as e:
      reply = "Something went wrong. Please try again."
    return jsonify({"answer": reply})


