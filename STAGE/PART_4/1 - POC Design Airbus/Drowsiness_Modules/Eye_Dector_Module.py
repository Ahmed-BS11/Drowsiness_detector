import cv2
import numpy as np
from numpy import linalg as LA
#from Drowsiness_Modules.Utils import resize
from Drowsiness_Modules.Utils import resize


class EyeDetector:

    def __init__(self, show_processing: bool = False):
        """
        Eye dector class that contains various method for eye aperture rate estimation and gaze score estimation

        Parameters
        ----------
        show_processing: bool
            If set to True, shows frame images during the processing in some steps (default is False)

        Methods
        ----------
        - show_eye_keypoints: shows eye keypoints in the frame/image
        - get_EAR: computes EAR average score for the two eyes of the face
        - get_Gaze_Score: computes the Gaze_Score (normalized euclidean distance between center of eye and pupil)
            of the eyes of the face
        """

        self.keypoints = None
        self.frame = None
        self.show_processing = show_processing
        self.eye_width = None

    def get_EAR(self, frame, landmarks):
        """
        Computes the average eye aperture rate of the face

        Parameters
        ----------
        frame: numpy array
            Frame/image in which the eyes keypoints are found
        landmarks: list
            List of 68 dlib keypoints of the face

        Returns
        -------- 
        ear_score: float
            EAR average score between the two eyes
            The EAR or Eye Aspect Ratio is computed as the eye opennes divided by the eye lenght
            Each eye has his scores and the two scores are averaged
        """

        self.keypoints = landmarks
        self.frame = frame
        pts = self.keypoints

        i = 0  # auxiliary counter
        # numpy array for storing the keypoints positions of the left eye
        eye_pts_l = np.zeros(shape=(6, 2))
        # numpy array for storing the keypoints positions of the right eye
        eye_pts_r = np.zeros(shape=(6, 2))

        for n in range(36, 42):
            point_l = pts[n]
            point_r = pts[n + 6]  # Assuming the right eye keypoints are 6 positions apart from the left eye keypoints
            eye_pts_l[i] = [point_l.x, point_l.y]
            eye_pts_r[i] = [point_r.x, point_r.y]
            i += 1

        def EAR_eye(eye_pts):
            """
            Computer the EAR score for a single eyes given it's keypoints
            :param eye_pts: numpy array of shape (6,2) containing the keypoints of an eye considering the dlib ordering
            :return: ear_eye
                EAR of the eye
            """
            ear_eye = (LA.norm(eye_pts[1] - eye_pts[5]) + LA.norm(
                eye_pts[2] - eye_pts[4])) / (2 * LA.norm(eye_pts[0] - eye_pts[3]))
            '''
            EAR is computed as the mean of two measures of eye opening (see dlib face keypoints for the eye)
            divided by the eye lenght
            '''
            return ear_eye

        ear_left = EAR_eye(eye_pts_l)  # computing the left eye EAR score
        ear_right = EAR_eye(eye_pts_r)  # computing the right eye EAR score

        # computing the average EAR score
        ear_avg = (ear_left + ear_right) / 2

        return ear_avg

    def show_eye_keypoints(self, color_frame, landmarks):
        """
        Shows eyes keypoints found in the face, drawing red circles in their position in the frame/image

        Parameters
        ----------
        color_frame: numpy array
            Frame/image in which the eyes keypoints are found
        landmarks: list
            List of 68 dlib keypoints of the face
        """

    
        self.keypoints = landmarks

        for n in range(36, 48):
            keypoint = self.keypoints[n]
            x = keypoint[0]
            y = keypoint[1]
            cv2.circle(color_frame, (x, y), radius=1, color=(0, 0, 255), thickness=-1)
        return
    def detect_face_landmarks(self,frame, face_detector, landmark_predictor):
        self.frame=frame
        self.face_detector=face_detector
        self.landmark_predictor=landmark_predictor
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector(gray_frame)
        
        landmarks_list = []
        for face in faces:
            landmarks = landmark_predictor(gray_frame, face)
            landmarks_points = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(68)]
            landmarks_list.append(landmarks_points)
        
        return landmarks_list

    def get_eye_state(self, frame, landmarks,eye_state_model):
        self.keypoints = landmarks
        self.frame = frame
        pts = self.keypoints

        def preprocess(frame,img_size=100):
        # Read the image in grayscale
            img_array = cv2.imread(frame, cv2.IMREAD_GRAYSCALE)

            # Resize the image while maintaining the aspect ratio
            desired_size = (img_size, img_size)
            height, width = img_array.shape
            aspect_ratio = width / height

            if aspect_ratio >= 1:
                new_width = desired_size[0]
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = desired_size[1]
                new_width = int(new_height * aspect_ratio)

            resized_image = cv2.resize(img_array, (new_width, new_height))

            # Pad the resized image to make it square (img_size x img_size)
            pad_width = (desired_size[1] - new_height) // 2
            pad_height = (desired_size[0] - new_width) // 2
            padded_image = np.pad(resized_image, ((pad_width, pad_width), (pad_height, pad_height)), mode='constant', constant_values=0)


            # Convert the grayscale image to RGB
            rgb_image = cv2.cvtColor(padded_image, cv2.COLOR_GRAY2RGB)
            #rgb_image = apply_data_augmentation(rgb_image)
            return rgb_image
        
        
        def extract_eyes_from_landmarks(frame, landmarks):
            #if len(landmarks) != 68:
            #   raise ValueError("Facial landmarks should contain 68 points.")

            # Define the indices for the left and right eyes based on facial landmarks.
            left_eye_indices = [i for i in range(36, 42)]
            right_eye_indices = [i for i in range(42, 48)]

            # Extract left and right eye regions from the frame.
            left_eye_coords = np.array([landmarks[i] for i in left_eye_indices], dtype=np.int32)
            right_eye_coords = np.array([landmarks[i] for i in right_eye_indices], dtype=np.int32)

            # Calculate the bounding boxes for the left and right eye regions.
            left_eye_x = np.min(left_eye_coords[:, 0])
            left_eye_y = np.min(left_eye_coords[:, 1])
            left_eye_w = np.max(left_eye_coords[:, 0]) - left_eye_x
            left_eye_h = np.max(left_eye_coords[:, 1]) - left_eye_y

            right_eye_x = np.min(right_eye_coords[:, 0])
            right_eye_y = np.min(right_eye_coords[:, 1])
            right_eye_w = np.max(right_eye_coords[:, 0]) - right_eye_x
            right_eye_h = np.max(right_eye_coords[:, 1]) - right_eye_y

            # Extend the cropping region to include the eyebrow area
            extended_eye_crop = 10
            left_eye_x -= extended_eye_crop
            left_eye_y -= extended_eye_crop
            left_eye_w += 2 * extended_eye_crop
            left_eye_h += 2 * extended_eye_crop

            right_eye_x -= extended_eye_crop
            right_eye_y -= extended_eye_crop
            right_eye_w += 2 * extended_eye_crop
            right_eye_h += 2 * extended_eye_crop

            # Crop the eye regions from the frame.
            left_eye_region = frame[left_eye_y:left_eye_y+left_eye_h, left_eye_x:left_eye_x+left_eye_w]
            right_eye_region = frame[right_eye_y:right_eye_y+right_eye_h, right_eye_x:right_eye_x+right_eye_w]

            # Convert the eye regions to grayscale.
            left_eye_gray = cv2.cvtColor(left_eye_region, cv2.COLOR_BGR2GRAY)
            right_eye_gray = cv2.cvtColor(right_eye_region, cv2.COLOR_BGR2GRAY)

            return [left_eye_gray, right_eye_gray]




        eyes = extract_eyes_from_landmarks(frame, landmarks)  # Considering the first detected face
        left_eye_roi, right_eye_roi = eyes[0], eyes[1]
        preprocessed_left_eye_roi = preprocess(left_eye_roi,img_size=100)
        preprocessed_right_eye_roi = preprocess(right_eye_roi,img_size=100)

        # Make predictions using your pre-trained model
        left_eye_prediction = eye_state_model.predict(preprocessed_left_eye_roi)
        right_eye_prediction = eye_state_model.predict(preprocessed_right_eye_roi)

        # Interpret predictions to determine eye state
        if left_eye_prediction > 0.5 and right_eye_prediction > 0.5:
            eye_state = 'open'
        else:
            eye_state = 'closed'

        return eye_state,[left_eye_prediction,right_eye_prediction]
         
    
    def get_Gaze_Score(self, frame, landmarks):
        """
        Computes the average Gaze Score for the eyes
        The Gaze Score is the mean of the l2 norm (euclidean distance) between the center point of the Eye ROI
        (eye bounding box) and the center of the eye-pupil

        Parameters
        ----------
        frame: numpy array
            Frame/image in which the eyes keypoints are found
        landmarks: list
            List of 68 dlib keypoints of the face

        Returns
        -------- 
        avg_gaze_score: float
            If successful, returns the float gaze score
            If unsuccessful, returns None

        """
        self.keypoints = landmarks
        self.frame = frame

        def get_ROI(left_corner_keypoint_num: int):
            """
            Get the ROI bounding box of the eye given one of it's dlib keypoint found in the face

            :param left_corner_keypoint_num: most left dlib keypoint of the eye
            :return: eye_roi
                Sub-frame of the eye region of the opencv frame/image
            """

            kp_num = left_corner_keypoint_num

            eye_array = np.array(
                [(self.keypoints.part(kp_num).x, self.keypoints.part(kp_num).y),
                 (self.keypoints.part(kp_num+1).x,
                  self.keypoints.part(kp_num+1).y),
                 (self.keypoints.part(kp_num+2).x,
                  self.keypoints.part(kp_num+2).y),
                 (self.keypoints.part(kp_num+3).x,
                  self.keypoints.part(kp_num+3).y),
                 (self.keypoints.part(kp_num+4).x,
                  self.keypoints.part(kp_num+4).y),
                 (self.keypoints.part(kp_num+5).x, self.keypoints.part(kp_num+5).y)], np.int32)

            min_x = np.min(eye_array[:, 0])
            max_x = np.max(eye_array[:, 0])
            min_y = np.min(eye_array[:, 1])
            max_y = np.max(eye_array[:, 1])

            eye_roi = self.frame[min_y-2:max_y+2, min_x-2:max_x+2]

            return eye_roi

        def get_gaze(eye_roi):
            """
            Computes the L2 norm between the center point of the Eye ROI
            (eye bounding box) and the center of the eye pupil
            :param eye_roi: float
            :return: (gaze_score, eye_roi): tuple
                tuple
            """

            eye_center = np.array(
                [(eye_roi.shape[1] // 2), (eye_roi.shape[0] // 2)])  # eye ROI center position
            gaze_score = None
            circles = None

            # a bilateral filter is applied for reducing noise and keeping eye details
            eye_roi = cv2.bilateralFilter(eye_roi, 4, 40, 40)

            circles = cv2.HoughCircles(eye_roi, cv2.HOUGH_GRADIENT, 1, 10,
                                       param1=90, param2=6, minRadius=1, maxRadius=9)
            # a Hough Transform is used to find the iris circle and his center (the pupil) on the grayscale eye_roi image with the contours drawn in white

            if circles is not None and len(circles) > 0:
                circles = np.uint16(np.around(circles))
                circle = circles[0][0, :]

                cv2.circle(
                    eye_roi, (circle[0], circle[1]), circle[2], (255, 255, 255), 1)
                cv2.circle(
                    eye_roi, (circle[0], circle[1]), 1, (255, 255, 255), -1)

                # pupil position is the first circle center found with the Hough Transform
                pupil_position = np.array([int(circle[0]), int(circle[1])])

                cv2.line(eye_roi, (eye_center[0], eye_center[1]), (
                    pupil_position[0], pupil_position[1]), (255, 255, 255), 1)

                gaze_score = LA.norm(
                    pupil_position - eye_center) / eye_center[0]
                # computes the L2 distance between the eye_center and the pupil position

            cv2.circle(eye_roi, (eye_center[0],
                                 eye_center[1]), 1, (0, 0, 0), -1)

            if gaze_score is not None:
                return gaze_score, eye_roi
            else:
                return None, None

        left_eye_ROI = get_ROI(36)  # computes the ROI for the left eye
        right_eye_ROI = get_ROI(42)  # computes the ROI for the right eye

        # computes the gaze scores for the eyes
        gaze_eye_left, left_eye = get_gaze(left_eye_ROI)
        gaze_eye_right, right_eye = get_gaze(right_eye_ROI)

        # if show_processing is True, shows the eyes ROI, eye center, pupil center and line distance
        if self.show_processing and (left_eye is not None) and (right_eye is not None):
            left_eye = resize(left_eye, 1000)
            right_eye = resize(right_eye, 1000)
            cv2.imshow("left eye", left_eye)
            cv2.imshow("right eye", right_eye)

        if gaze_eye_left and gaze_eye_right:

            # computes the average gaze score for the 2 eyes
            avg_gaze_score = (gaze_eye_left + gaze_eye_left) / 2
            return avg_gaze_score

        else:
            return None
