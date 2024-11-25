import cv2
import numpy as np

# global variables
points = []
scale = None
labels = ["k", "g", "f", "a", "c", "d", "b"]  # predefined labels to measure
current_label_index = 0
measurements = {}  # store measured values
calculation_steps = []  # store steps for final summary

def click_event(event, x, y, flags, param):
    global points, scale, labels, current_label_index, measurements, calculation_steps

    if event == cv2.EVENT_LBUTTONDOWN:
        # store clicked points
        points.append((x, y))
        print(f"point recorded: {x}, {y}")

        # if two points are selected and scale is not set yet
        if len(points) == 2 and scale is None:
            cv2.line(img, points[0], points[1], (255, 0, 0), 2)
            cv2.imshow('Image', img)
            print("two points selected for scale.")
            real_length_cm = float(input("enter the real-world distance between these points (in cm): "))
            pixel_distance = np.linalg.norm(np.array(points[0]) - np.array(points[1]))
            scale = real_length_cm / pixel_distance
            calculation_steps.append(f"scale setup: real distance = {real_length_cm} cm, pixel distance = {pixel_distance:.2f} pixels, scale = {scale:.5f} cm/pixel")
            print(f"scale set: {scale} cm per pixel")
            points = []  # reset points for next measurements
            print(f"\nnow measuring for {labels[current_label_index]}... click two points.")

        # if scale is set, calculate distances for labels
        elif len(points) == 2 and scale is not None:
            label = labels[current_label_index]
            print(f"measuring for {label}...")
            cv2.line(img, points[0], points[1], (0, 255, 0), 2)
            cv2.imshow('Image', img)
            pixel_distance = np.linalg.norm(np.array(points[0]) - np.array(points[1]))
            real_distance_cm = pixel_distance * scale
            measurements[label] = real_distance_cm  # store the distance

            # store calculation steps
            steps = (
                f"label: {label}\n"
                f"  - pixel distance = {pixel_distance:.2f} pixels\n"
                f"  - scale = {scale:.5f} cm/pixel\n"
                f"  - real distance = pixel distance * scale = {pixel_distance:.2f} * {scale:.5f} = {real_distance_cm:.2f} cm"
            )
            calculation_steps.append(steps)
            print(f"distance of {label}: {real_distance_cm:.2f} cm")
            points = []  # reset points for next measurement
            current_label_index += 1

            # if not all labels are measured, prompt for next label
            if current_label_index < len(labels):
                print(f"\nnow measuring for {labels[current_label_index]}... click two points.")

            # if all distances measured, calculate radius
            if current_label_index >= len(labels):
                print("\nall distances measured. calculating radius r...\n")
                k = measurements["k"]
                f = measurements["f"]
                a = measurements["a"]
                c_squared = k**2 + f**2
                r = (c_squared + a**2) / (2 * a)  # radius of deflection
                
                calculation_steps.append(
                    f"radius calculation:\n"
                    f"  - c^2 = k^2 + f^2 = {k:.2f}^2 + {f:.2f}^2 = {c_squared:.2f}\n"
                    f"  - r = (c^2 + a^2) / (2a) = ({c_squared:.2f} + {a:.2f}^2) / (2 * {a:.2f}) = {r:.2f} cm"
                )
                print("\nfinal radius of deflection (r):")
                print(f"r = {r:.2f} cm\n")

                # print all steps
                print("\ncalculation steps:\n")
                for step in calculation_steps:
                    print(step)
                print("\npress 'q' to quit at any time.")

# load the image
image_name = input("enter the name of the image (with extension, e.g., 'image.jpg'): ")
image_path = f"./{image_name}"  # assuming the image is in the same directory as the script
img = cv2.imread(image_path)

if img is None:
    print(f"error loading image '{image_name}'. make sure the image is in the same directory as this script.")
    exit()

# display the image
cv2.imshow('Image', img)
cv2.setMouseCallback('Image', click_event)

print("instructions:")
print("1. click two points to set the scale.")
print("2. enter the real-world distance between the selected points (in cm).")
print("3. click two points for each of the predefined labels (k, g, f, a, c, d, b) as prompted.")
print("4. after all distances are measured, the radius (r) will be calculated and displayed.")
print("5. press 'q' to quit the program.")

# wait for user to quit
while True:
    key = cv2.waitKey(1)
    if key == ord('q'):
        print("program terminated.")
        break

cv2.destroyAllWindows()
