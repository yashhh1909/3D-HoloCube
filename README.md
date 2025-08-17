# 3D-HoloCube

This project combines OpenCV, MediaPipe, PyGame, and OpenGL to create an interactive 3D cube that can be controlled in real time using hand gestures detected through a webcam. The program leverages computer vision to track a single hand, extracts its landmarks, and translates natural finger movements into transformations (rotation and zoom) of the cube in 3D space.

The hand tracking is powered by MediaPipe Hands, which identifies 21 landmarks per hand. Specifically, this code focuses on the thumb tip and index fingertip to measure the distance between them. This measurement is converted into a pinch strength value (ranging from 0 to 1), where 0 means fingers are apart, and 1 means the fingers are pinched together. Pinch gestures directly control the cube’s zoom level, allowing the user to move the cube closer or farther away in 3D space.

Meanwhile, the index fingertip’s position on the screen is used to calculate movement deltas in the X and Y directions. These deltas translate into smooth rotational transformations of the cube, enabling the user to spin and tilt the cube simply by moving their index finger across the camera view.

The 3D cube itself is drawn using OpenGL. Each cube face is semi-transparent (using blending), while the edges are highlighted with cyan lines, giving it a modern wireframe-plus-surface appearance. Depth testing ensures that cube faces are rendered properly in a 3D perspective. The cube continuously updates at 60 FPS, managed by PyGame’s rendering loop.

In essence, this project is an elegant demonstration of gesture-based 3D interaction. It integrates real-time computer vision with graphics rendering, showing how intuitive gestures can replace traditional input devices like a mouse or keyboard for 3D object manipulation. This can be extended further for AR/VR applications, interactive art, or educational visualization tools.

🚀 Tech Stack

Python – Core programming language

OpenCV – Captures video frames from the webcam

MediaPipe Hands – Real-time hand tracking and landmark detection

PyGame – Game loop and window management

PyOpenGL – Rendering and transforming the 3D cube

📖 Project Description

This project integrates computer vision and 3D graphics rendering to create a cube that responds intuitively to your hand movements:

Pinch Gesture (Thumb + Index Finger) → Controls zoom in/out of the cube

Index Finger Movement → Rotates the cube along X and Y axes

Wireframe + Transparent Faces → Combines a clean wireframe outline with semi-transparent surfaces for modern visualization

The cube updates in real time at 60 FPS, creating a smooth and responsive gesture-based interface. By mapping hand landmarks to 3D transformations, this project showcases how simple finger movements can provide precise, touchless control.

🎯 Features

Real-time gesture recognition using MediaPipe

Smooth cube rotation and zooming with natural gestures

3D rendering using OpenGL with transparency and depth effects

Works on any computer with a webcam
