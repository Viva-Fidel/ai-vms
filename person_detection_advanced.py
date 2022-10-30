import cv2
import numpy as np


class Person_detection_advanced:
    def __init__(self, frame):
        self.frame = frame
        self.weights = 'advanced_analytics/yolov3.weights'
        self.config = 'advanced_analytics/yolov3.cfg'
        self.classes = 'advanced_analytics/coco.names'
        self.net = cv2.dnn.readNet(self.weights, self.config)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        with open('advanced_analytics/coco.names', 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]

    def detect_person(self):

        height, width, channels = self.frame.shape

        blob = cv2.dnn.blobFromImage(self.frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)

        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                if class_id == 0:
                    confidence = scores[class_id]
                    if confidence > 0.8:
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                print(class_ids[i])
                label = str(self.classes[class_ids[i]])
                color = (0, 255, 0)
                cv2.rectangle(self.frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(self.frame, label.upper(), (x, y - 20), font, 3, color, 3)
