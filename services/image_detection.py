from ultralytics import YOLO

model = YOLO("./models/best.pt")

def detect_ingredients_from_image(image_path):
    results = model(image_path)
    labels = set()

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0].item())
            label = r.names[cls_id]
            labels.add(label)

    return list(labels)
