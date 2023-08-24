from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtCore import Qt,QThread,pyqtSignal,QTimer

import time
import cv2
import dlib
import numpy as np
from Drowsiness_Modules.Utils import get_face_area
from Drowsiness_Modules.Eye_Dector_Module import EyeDetector as EyeDet
from Drowsiness_Modules.Attention_Scorer_Module import AttentionScorer as AttScorer
from Drowsiness_Modules.Pose_Estimation_Module import HeadPoseEstimator as HeadPoseEst
from imutils import face_utils
from keras.models import load_model  # Assuming you trained your model using TensorFlow

eye_state_model = load_model('STAGE\PART_2\my_model.keras', compile=False)
eye_state_model.compile(loss="binary_crossentropy", optimizer = "adam", metrics = ["accuracy"])
class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def __init__(self):
        super().__init__()
        self.counter_closed=0
        self.counter_open=0
        self.isAsleep = False
        self.yawning=0


    def calculate_mar(self,mouth_points):
        A = np.linalg.norm(mouth_points[1] - mouth_points[7])
        B = np.linalg.norm(mouth_points[2] - mouth_points[6])
        C = np.linalg.norm(mouth_points[3] - mouth_points[5])
        D = np.linalg.norm(mouth_points[0] - mouth_points[2])
        mar = (A + B + C) / (2.0*D)
        return mar


    def Drowsiness(self, frame, Predictor, Eye_det, Scorer, Detector, Head_pose):
        frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #gray = cv2.bilateralFilter(gray, 5, 10, 10)
        gray=frame
        faces = Detector(gray)
        if len(faces) > 0:  # process the frame only if at least a face is found

            for face in faces:
                # Determine the facial landmarks for the face region
                shape = Predictor(gray, face)
                shape = face_utils.shape_to_np(shape)

                # Extract the mouth landmarks using the FACIAL_LANDMARKS_68_IDXS dictionary
                (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS['mouth']
                mouth_points = shape[60:69]

                # Calculate the mouth aspect ratio (MAR)
                mar = self.calculate_mar(mouth_points)

                # Draw the landmarks and MAR value on the frame
                cv2.drawContours(frame, [mouth_points], 0, (0, 255, 0), 2)
                for (x, y) in mouth_points:
                    cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)

                cv2.putText(frame, "MAR: {:.2f}".format(mar), (5, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (50, 173, 176), 1, cv2.LINE_AA)

            if (mar > 1.1):
                self.yawning+=1
                if self.yawning > 10:
                    cv2.putText(frame, "Yawning!", (5, 200), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
            else :
                self.yawning=0

            # take only the bounding box of the biggest face
            faces = sorted(faces, key=get_face_area, reverse=True)
            driver_face = faces[0]

            # predict the 68 facial keypoints position
            landmarks = Predictor(gray, driver_face)
            # shows the eye keypoints (can be commented)
            Eye_det.show_eye_keypoints(
                color_frame=frame, landmarks=landmarks)

            # compute the EAR score of the eyes
            ear = Eye_det.get_EAR(frame=gray, landmarks=landmarks)
            state=EyeDet.get_eye_state(self, frame, landmarks,eye_state_model)[0]
            r_p=EyeDet.get_eye_state(self, frame, landmarks,eye_state_model)[1][0]
            l_p=EyeDet.get_eye_state(self, frame, landmarks,eye_state_model)[1][1]
            # compute the PERCLOS score and state of tiredness
            _, perclos_score = Scorer.get_PERCLOS(ear)

            frame_det, roll, pitch, yaw = Head_pose.get_pose(frame=frame, landmarks=landmarks)
            if roll<0 or abs(pitch)>35 or abs(yaw)>25:
                distracted = True
            else:
                distracted = False
            #_, _, distracted = Scorer.eval_scores(ear, 0, roll, pitch, yaw)
            if distracted :
                cv2.putText(frame, "Distracted!", (5, 160), cv2.FONT_HERSHEY_DUPLEX, 0.5, (222,111,20), 1, cv2.LINE_AA)

            # if the head pose estimation is successful, show the results
            if frame_det is not None:
                frame = frame_det

            # show the real-time EAR score
            if ear is not None:
                left_text = "Left Eye Probabilities:"
                cv2.putText(frame, left_text, (5, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (50, 173, 176), 1, cv2.LINE_AA)

                for i, prob in enumerate(l_p):
                    text = f"Class {i}: {prob:.3f}"
                    y_pos = 40 + i * 20
                    cv2.putText(frame, text, (5, y_pos), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (50, 173, 176), 1, cv2.LINE_AA)

                # Display right eye probabilities
                right_text = "Right Eye Probabilities:"
                cv2.putText(frame, right_text, (5, 100), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (50, 173, 176), 1, cv2.LINE_AA)

                for i, prob in enumerate(r_p):
                    text = f"Class {i}: {prob:.3f}"
                    y_pos = 120 + i * 20
                    cv2.putText(frame, text, (5, y_pos), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (50, 173, 176), 1, cv2.LINE_AA)   
            if (state=='closed'):
                self.counter_closed+=1
                self.counter_open=0
                if self.counter_closed > 50 :
                    cv2.putText(frame, "Asleep!", (5, 220), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
                    self.isAsleep = True
            else:
                self.counter_open+=1
                if self.counter_open < 30 and self.isAsleep:
                    cv2.putText(frame, "Asleep!", (5, 220), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
                if self.counter_open > 40 : 
                    self.counter_closed = 0
                    self.counter_open=0
                    self.isAsleep = False

            # show the real-time PERCLOS score
            cv2.putText(frame, "PERCLOS:" + str(round(perclos_score, 3)), (5, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (50, 173, 176), 1, cv2.LINE_AA)

            if perclos_score > 0.09 :
                cv2.putText(frame, "Fatigue!", (5, 180), cv2.FONT_HERSHEY_DUPLEX, 0.5, (236,232,26), 1, cv2.LINE_AA)
            frame = cv2.resize(frame, (0,0), fx=2, fy=2)
        return frame



    def run(self):
        self.ThreadActive = True
        Predictor = dlib.shape_predictor(r"STAGE\PART_4\1 - POC Design Airbus\Face_Landmarks.dat")
        # visualisation parameters
        show_eye_proc = False
        show_axis = True
        verbose = False

        # Attention Scorer parameters (EAR, Gaze Score, Pose)
        ear_tresh = 0.12
        ear_time_tresh = 2
        gaze_tresh = 0.2
        gaze_time_tresh = 2
        pitch_tresh = 30
        yaw_tresh = 30
        pose_time_tresh = 3.0
        fps_lim = 20

        Eye_det = EyeDet(show_processing=show_eye_proc)
        Scorer = AttScorer(fps_lim, ear_tresh=ear_tresh, ear_time_tresh=ear_time_tresh, gaze_tresh=gaze_tresh,
                   gaze_time_tresh=gaze_time_tresh, pitch_tresh=pitch_tresh, yaw_tresh=yaw_tresh, pose_time_tresh=pose_time_tresh, verbose=verbose)
        Detector = dlib.get_frontal_face_detector()
        Head_pose = HeadPoseEst(show_axis=show_axis)
        Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                FlippedImage = self.Drowsiness(FlippedImage, Predictor, Eye_det, Scorer, Detector, Head_pose)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(540, 384, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
    def stop(self):
        self.ThreadActive = False
        self.quit()