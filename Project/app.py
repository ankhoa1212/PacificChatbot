from flask import Flask, render_template, request
import json
import random
import pickle
import torch
import torch.nn as nn

app = Flask(__name__)

# Load classes and words
with open('classes.pkl', 'rb') as file:
    classes = pickle.load(file)

with open('words.pkl', 'rb') as file:
    words = pickle.load(file)

# Load the intents data
with open('../Dataset/University_Data.json', 'r', encoding="UTF-8") as f:
    intents = json.load(f)

# Define your NeuralNetwork class here
class NeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(NeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu1 = nn.ReLU()
        self.bn1 = nn.BatchNorm1d(hidden_size)
        self.dropout1 = nn.Dropout(0.2)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.relu2 = nn.ReLU()
        self.bn2 = nn.BatchNorm1d(hidden_size)
        self.dropout2 = nn.Dropout(0.2)
        self.fc3 = nn.Linear(hidden_size, output_size)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.bn1(x)
        x = self.dropout1(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.bn2(x)
        x = self.dropout2(x)
        x = self.fc3(x)
        output = self.softmax(x)
        return output

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return self.softmax(x)

# Function to preprocess the input sentence
def preprocess_sentence(sentence, words):
    sentence_words = sentence.lower().split()
    sentence_words = [word for word in sentence_words if word in words]
    return sentence_words

# Function to convert the preprocessed sentence into a feature vector
def sentence_to_features(sentence_words, words):
    features = [1 if word in sentence_words else 0 for word in words]
    return torch.tensor(features).float().unsqueeze(0)

# Load the PyTorch model
model_path = 'model.pth'
input_size = len(words)
hidden_size = 8
output_size = len(classes)

model = NeuralNetwork(input_size, hidden_size, output_size)
model.load_state_dict(torch.load(model_path))
model.eval()

# Function to generate a response using the trained model
def chatbot_response(user_input):
    sentence_words = preprocess_sentence(user_input, words)
    if len(sentence_words) == 0:
        return "I'm sorry, but I don't understand. Can you please rephrase or provide more information?"

    features = sentence_to_features(sentence_words, words)
    with torch.no_grad():
        outputs = model(features)

    probabilities, predicted_class = torch.max(outputs, dim=1)
    confidence = probabilities.item()
    predicted_tag = classes[predicted_class.item()]

    if confidence > 0.5:
        for intent in intents['intents']:
            if intent['tag'] == predicted_tag:
                print(intent['answer'])
                if isinstance(intent['answer'], list):
                    answers = intent['answer']
                else:
                    # Split the string into a list of answers
                    answers = intent['answer'].split('\n')
                return random.choice(answers)

    return "I'm sorry, but I'm not sure how to respond to that."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    response = chatbot_response(user_input.lower())
    return response

if __name__ == '__main__':
    app.run(debug=True)
