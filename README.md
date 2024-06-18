AI Virtual Painter
Overview
The AI Virtual Painter is an interactive application that uses computer vision and machine learning to enable hand gesture-based painting on a virtual canvas. This project leverages Mediapipe for hand tracking and OpenCV for image processing and drawing. Users can draw, erase, and change colors with their fingers, creating an intuitive and immersive painting experience without the need for traditional input devices.

Key Features
Hand Gesture Recognition: Utilizes Mediapipe's advanced hand tracking to detect hand landmarks and interpret gestures in real-time.
Dynamic Drawing: Allows users to draw on a virtual canvas by moving their fingers, mimicking the use of a real brush.
Color and Brush Control: Recognizes specific gestures to change brush colors and sizes, providing a versatile painting experience.
Eraser Functionality: Offers a gesture-based eraser mode for easy correction or modification of drawings.
Interactive GUI: Displays real-time video feed from the webcam, with the virtual drawing overlaid, allowing users to see the immediate effects of their gestures.
Technology Stack
Mediapipe: Used for hand detection and tracking, capturing and processing hand landmarks to identify gestures.
OpenCV: Handles image processing, including capturing video from the webcam, drawing on the virtual canvas, and displaying the output.
How It Works
Hand Detection: Mediapipe detects and tracks the user's hand from the webcam feed, identifying key landmarks on the fingers and palm.
Gesture Interpretation: Based on the positions and movements of the detected landmarks, the application interprets different gestures (e.g., pointing, pinching, etc.).
Drawing and Erasing: OpenCV draws on the virtual canvas when a drawing gesture is detected. Switching to eraser mode allows for modifications.
Dynamic Interaction: The webcam's real-time video feed is displayed to the user, with the virtual drawing overlaid on top, providing immediate feedback.
Usage
To start painting with the AI Virtual Painter, simply run the application and position your hand in front of the webcam. Move your index finger to draw, use gestures to change colors or switch to the eraser, and watch your creations come to life on the screen.
