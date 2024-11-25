import cv2
import numpy as np
import math

# Global variables
points = []
scale = None
labels = ["f"]  # Only measuring 'f'
current_label_index = 0
measurements = {"k": 8.0}  # k is predefined as 8 cm
calculation_steps = []  # Store steps for final summary

def click_event(event, x, y, flags, param):
    global points, scale, labels, current_label_index, measurements, calculation_steps

    if event == cv2.EVENT_LBUTTONDOWN:
        # Store clicked points
        points.append((x, y))
        print(f"Point recorded: {x}, {y}")

        # If two points are selected and scale is not set yet
        if len(points) == 2 and scale is None:
            cv2.line(img, points[0], points[1], (255, 0, 0), 2)
            cv2.imshow('Image', img)
            print("Two points selected for scale. (Make sure its 1 cm)")
            real_length_cm = 1
            pixel_distance = np.linalg.norm(np.array(points[0]) - np.array(points[1]))
            scale = real_length_cm / pixel_distance
            calculation_steps.append(f"Scale setup: real distance = {real_length_cm} cm, pixel distance = {pixel_distance:.2f} pixels, scale = {scale:.5f} cm/pixel")
            print(f"Scale set: {scale:.5f} cm per pixel")
            points = []  # Reset points for next measurements
            print(f"\nk is automatically set to {measurements['k']} cm.")
            print(f"\nNow measuring for f... click two points.")

        # If scale is set, calculate distances for labels
        elif len(points) == 2 and scale is not None:
            label = labels[current_label_index]
            print(f"Measuring for {label}...")
            cv2.line(img, points[0], points[1], (0, 255, 0), 2)
            cv2.imshow('Image', img)
            pixel_distance = np.linalg.norm(np.array(points[0]) - np.array(points[1]))
            real_distance_cm = pixel_distance * scale
            measurements[label] = real_distance_cm  # Store the distance

            # Store calculation steps
            steps = (
                f"Label: {label}\n"
                f"  - Pixel distance = {pixel_distance:.2f} pixels\n"
                f"  - Scale = {scale:.5f} cm/pixel\n"
                f"  - Real distance = pixel distance * scale = {pixel_distance:.2f} * {scale:.5f} = {real_distance_cm:.2f} cm"
            )
            calculation_steps.append(steps)
            print(f"Distance of {label}: {real_distance_cm:.2f} cm")
            points = []  # Reset points for next measurement
            current_label_index += 1

            # If all distances measured, calculate radius
            if current_label_index >= len(labels):
                print("\nAll distances measured. Calculating radius r...\n")
                k = measurements["k"]
                f_val = measurements["f"]
                r = (k**2 + f_val**2) / (math.sqrt(2) * (k - f_val))  # formula for radius of deflection

                calculation_steps.append(
                    f"Radius calculation:\n"
                    f"  - r = (k^2 + f^2) / (sqrt(2) * (k - f)) = ({k:.2f}^2 + {f_val:.2f}^2) / (sqrt(2) * ({k:.2f} - {f_val:.2f})) = {r:.2f} cm"
                )

                print(f"\nFinal radius of deflection (r):")
                print(f"r = {r:.2f} cm\n")

                # Print all steps
                print("\nCalculation steps:\n")
                for step in calculation_steps:
                    print(step)
                print("\nPress 'q' to quit at any time.")

# Load the image
image_name = input("Enter the name of the image (with extension, e.g., 'image.jpg'): ")
image_path = f"./{image_name}"  # Assuming the image is in the same directory as the script
img = cv2.imread(image_path)

if img is None:
    print(f"Error loading image '{image_name}'. Make sure the image is in the same directory as this script.")
    exit()

# Display the image
cv2.imshow('Image', img)
cv2.setMouseCallback('Image', click_event)

print("Instructions:")
print("1. Click two points to set the scale.")
print("2. Enter the real-world distance between the selected points (in cm).")
print("3. k is automatically set to 8 cm.")
print("4. Click two points to measure f.")
print("5. After measuring f, the radius (r) will be calculated and displayed.")
print("6. Press 'q' to quit the program.")

# Wait for user to quit
while True:
    key = cv2.waitKey(1)
    if key == ord('q'):
        print("Program terminated.")
        break

cv2.destroyAllWindows()
