# 🎯 Focus Guard

**Focus Guard** is an AI-based audio classification web application that detects and identifies specific sounds using a custom-trained machine learning model.

The project was built by first **collecting and training audio data in Google Teachable Machine**, testing the trained model, and then integrating the trained model into a **HTML, CSS, and JavaScript web application** using TensorFlow.js.

The application listens through the user's microphone, identifies the detected sound, displays the predicted class and confidence score, and then stops listening after a confident prediction.

---

## 💡 What is Focus Guard?

Focus Guard is designed to recognize different sound categories from live microphone input.

Instead of building and training a machine learning model from scratch, I used **Google Teachable Machine** to create and train a custom audio classification model.

After training the model, I connected it to my own web interface so that the trained AI model could be used directly in a browser.

### In simple terms:

**I trained the AI → exported the trained model → connected it to my website → used the microphone to give audio input → received the AI prediction → displayed the result.**

---

# 🔄 How I Built Focus Guard

The project was developed in the following stages:

```text
1. Define the sound categories
              ↓
2. Collect audio samples
              ↓
3. Create Audio Project in Teachable Machine
              ↓
4. Create classes for each sound
              ↓
5. Add/record audio samples
              ↓
6. Train the audio classification model
              ↓
7. Test the trained model
              ↓
8. Publish the trained model
              ↓
9. Get the Teachable Machine model URL
              ↓
10. Create the Focus Guard web interface
              ↓
11. Connect the model using TensorFlow.js
              ↓
12. Connect the microphone
              ↓
13. Classify live audio
              ↓
14. Display prediction and confidence
              ↓
15. Stop listening after a confident prediction