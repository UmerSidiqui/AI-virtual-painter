import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mpDraw = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set width
cap.set(4, 720)   # Set height

# Colors in BGR format
colors = {
    "Red": (0, 0, 255),
    "Green": (0, 255, 0),
    "Blue": (255, 0, 0),
    "Eraser": (0, 0, 0)  # Eraser (black but interpreted as transparent)
}

# Rectangles positions and sizes
rectangles = {
    "Red": (50, 0, 200, 100),
    "Green": (300, 0, 200, 100),
    "Blue": (550, 0, 200, 100),
    "Eraser": (800, 0, 200, 100)
}

selectedColor = None
drawColor = (255, 0, 255)  # Default drawing color
brushThickness = 15
eraserThickness = 50
xp, yp = 0, 0  # Previous points
imgCanvas = np.zeros((720, 1280, 3), np.uint8)  # Canvas to draw on

while True:
    # Read frame from webcam
    success, img = cap.read()
    if not success:
        continue

    # Flip image horizontally for natural viewing
    img = cv2.flip(img, 1)

    # Convert BGR image to RGB (Mediapipe accepts RGB images)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process image with Mediapipe Hands
    results = hands.process(imgRGB)

    # Check if hand(s) detected
    if results.multi_hand_landmarks:
        for handLandmarks in results.multi_hand_landmarks:
            # Draw hand landmarks on image
            mpDraw.draw_landmarks(img, handLandmarks, mpHands.HAND_CONNECTIONS)

            # Get landmarks for fingers
            lmList = [(int(lm.x * img.shape[1]), int(lm.y * img.shape[0])) for lm in handLandmarks.landmark]
            
            # Index finger tip and middle finger tip coordinates
            index_x, index_y = lmList[8]
            middle_x, middle_y = lmList[12]

            # Determine if both fingers are in the same rectangle
            for color, (x, y, w, h) in rectangles.items():
                if x < index_x < x + w and y < index_y < y + h and x < middle_x < x + w and y < middle_y < y + h:
                    drawColor = colors[color]
                    selectedColor = color

            # Check if the index finger is up and middle finger is down
            if lmList[8][1] < lmList[6][1] and lmList[12][1] > lmList[10][1]:
                cv2.circle(img, (index_x, index_y), brushThickness // 2, drawColor, cv2.FILLED)
                if xp == 0 and yp == 0:
                    xp, yp = index_x, index_y
                if drawColor == colors["Eraser"]:
                    cv2.line(img, (xp, yp), (index_x, index_y), drawColor, eraserThickness)
                    cv2.line(imgCanvas, (xp, yp), (index_x, index_y), drawColor, eraserThickness)
                else:
                    cv2.line(img, (xp, yp), (index_x, index_y), drawColor, brushThickness)
                    cv2.line(imgCanvas, (xp, yp), (index_x, index_y), drawColor, brushThickness)
                xp, yp = index_x, index_y
            else:
                xp, yp = 0, 0

    # Merge the canvas and the video feed
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # Draw rectangles at the top
    for color, (x, y, w, h) in rectangles.items():
        if selectedColor == color:
            cv2.rectangle(img, (x - 10, y - 10), (x + w + 10, y + h + 10), colors[color], -1)  # Enlarged rectangle
        else:
            cv2.rectangle(img, (x, y), (x + w, y + h), colors[color], -1)
        cv2.putText(img, color, (x + 40, y + 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the image
    cv2.imshow("Image", img)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
