import numpy as np
import mediapipe as mp
from mediapipe.python.solutions.drawing_utils import _normalized_to_pixel_coordinates
import cv2
POSE = mp.solutions.pose
mp_face_mesh = mp.solutions.face_mesh
FACE_MESH = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5)


def get_face_mesh_landmarks(frame, face_mesh):
    frame.flags.writeable = False
    results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    ls_single_face = results.multi_face_landmarks[0].landmark
    image_rows, image_cols, _ = frame.shape
    mesh_pts = []
    for idx in ls_single_face:
        mesh_pts.append(np.array(_normalized_to_pixel_coordinates(idx.x, idx.y, image_cols, image_rows)))

    mesh_pts = np.array(mesh_pts, dtype=object)
    return mesh_pts
