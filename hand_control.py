import cv2
import mediapipe as mp
import serial
import time
import math

# --- SERIAL ---
arduino = serial.Serial('COM3', 9600)
time.sleep(2)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

def angle(a, b, c):
    ang = math.degrees(
        math.atan2(c.y - b.y, c.x - b.x) -
        math.atan2(a.y - b.y, a.x - b.x)
    )
    if ang < 0:
        ang += 360
    return ang

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = hands.process(rgb)

    if res.multi_hand_landmarks:
        lm = res.multi_hand_landmarks[0].landmark

        # Ángulos dedos principales
        ang_ind = angle(lm[6], lm[7], lm[8])
        ang_med = angle(lm[10], lm[11], lm[12])
        ang_anu = angle(lm[14], lm[15], lm[16])

        # Pulgar: flexión vertical
        ang_pflex = angle(lm[2], lm[3], lm[4])

        # Pulgar: giro horizontal (aproximación)
        ang_pgiro = int(abs((lm[4].x - lm[2].x) * 200))

        # Escalamos a rango 0–180 seguro
        serv_ind = max(0, min(180, int(ang_ind)))
        serv_med = max(0, min(180, int(ang_med)))
        serv_anu = max(0, min(180, int(ang_anu)))
        serv_pf  = max(0, min(180, int(ang_pflex)))
        serv_pg  = max(0, min(180, int(ang_pgiro)))

        # Enviar al Arduino
        data = f"{serv_ind},{serv_med},{serv_anu},{serv_pf},{serv_pg}\n"
        arduino.write(data.encode())
        print("ENVIADO:", data)

        mp_draw.draw_landmarks(frame, res.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Hand Control", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()
