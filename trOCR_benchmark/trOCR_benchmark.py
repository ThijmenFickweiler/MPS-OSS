import time
import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import matplotlib.pyplot as plt
from Levenshtein import ratio  # pip install python-Levenshtein

# -------- CONFIGURATION --------
IMAGE_PATH = "sample.png"  # input image
GROUND_TRUTH = "1 euro stekker"  # expected text
NUM_THREADS_LIST = [1, 2, 4, 8]  # threads to test
NUM_BEAMS_LIST = [1, 2, 4]  # beam search values
MAX_LENGTH = 32  # max token length
NUM_RUNS = 3  # repeat predictions to average

# -------- PRELOAD MODEL --------
print("Loading processor and model...")
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
model.eval()
print("Model loaded!")

# -------- LOAD IMAGE --------
image = Image.open(IMAGE_PATH).convert("RGB")

# Optional resize for CPU speed
h = 384
w = int(image.width * h / image.height)
image = image.resize((w, h))

pixel_values = processor(images=image, return_tensors="pt").pixel_values

# -------- BENCHMARKING --------
results = []

for threads in NUM_THREADS_LIST:
    torch.set_num_threads(threads)
    for num_beams in NUM_BEAMS_LIST:
        times = []
        predictions = []

        # run prediction multiple times
        for i in range(NUM_RUNS):
            start = time.time()
            with torch.inference_mode():
                generated_ids = model.generate(pixel_values, max_length=MAX_LENGTH, num_beams=num_beams)
            t = time.time() - start
            times.append(t)

            text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            predictions.append(text)

        avg_time = sum(times) / NUM_RUNS
        pred_text = predictions[-1]  # last run

        # -------- REALISTIC ACCURACY --------
        accuracy = ratio(pred_text, GROUND_TRUTH)  # Levenshtein similarity
        bonus = 0.1 if pred_text.strip() == GROUND_TRUTH else 0
        # combine speed and accuracy into a score
        score = accuracy / (avg_time ** 0.5) + bonus

        results.append({
            "threads": threads,
            "num_beams": num_beams,
            "times": times,
            "avg_time": avg_time,
            "pred_text": pred_text,
            "accuracy": accuracy,
            "score": score
        })

        print(f"[Threads:{threads} Beams:{num_beams}] Pred: {repr(pred_text)}, "
              f"Time: {avg_time:.2f}s, Accuracy: {accuracy:.2f}, Score: {score:.2f}")

# -------- PLOTTING --------
fig, ax = plt.subplots()
for threads in NUM_THREADS_LIST:
    xs = []
    ys = []
    labels = []
    for r in results:
        if r["threads"] == threads:
            xs.append(r["num_beams"])
            ys.append(r["avg_time"])
            labels.append(f"Acc:{r['accuracy']:.2f}")
    ax.plot(xs, ys, marker='o', label=f"{threads} threads")
    for x, y, lbl in zip(xs, ys, labels):
        ax.text(x, y, lbl)
ax.set_xlabel("Num Beams")
ax.set_ylabel("Avg Time (s)")
ax.set_title(f"Inference Benchmark: {IMAGE_PATH}")
ax.legend()
plt.show()

# -------- BEST SETTINGS --------
best = max(results, key=lambda x: x["score"])
best_name = f"{IMAGE_PATH.replace('.png','')}_score_{best['score']:.2f}.txt"
with open(best_name, "w") as f:
    f.write(f"Best Settings:\n")
    f.write(f"Threads: {best['threads']}\n")
    f.write(f"Num Beams: {best['num_beams']}\n")
    f.write(f"Prediction: {best['pred_text']}\n")
    f.write(f"Accuracy (Levenshtein): {best['accuracy']:.2f}\n")
    f.write(f"Avg Time: {best['avg_time']:.2f}s\n")
    f.write(f"Score: {best['score']:.2f}\n")

print(f"Best settings saved to: {best_name}")
