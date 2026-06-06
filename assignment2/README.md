# Assignment 2 — Legacy Code Modernization / CNN MNIST

**Mahmudul Hasan (4125999049)** · Xi'an Jiaotong University · 2026  
**Course:** AI-Augmented Software Engineering · **Weight:** 20% · **Due:** Week 8

---

## Deliverables

| File | Description |
|------|-------------|
| [MAHMUDUL_HASAN_4125999049_Assignment_2.pdf](MAHMUDUL_HASAN_4125999049_Assignment_2.pdf) | Full assignment report (PDF) |
| [cnn_mnist/](cnn_mnist/) | Modernized CNN for MNIST digit classification |

---

## Project: CNN for MNIST

PyTorch CNN (`DigitCNN`) for handwritten digit recognition — training, evaluation, confusion matrix, and demo predictions.

<p align="center">
  <img src="cnn_mnist/demo_results.png" alt="MNIST demo predictions" width="45%" />
  <img src="cnn_mnist/confusion_matrix.png" alt="Confusion matrix" width="45%" />
</p>

### Code

| File | Purpose |
|------|---------|
| [cnn_mnist/model.py](cnn_mnist/model.py) | `DigitCNN` architecture |
| [cnn_mnist/mnist_cnn.py](cnn_mnist/mnist_cnn.py) | Train, test, demo CLI |
| [cnn_mnist/mnist_cnn_model.pth](cnn_mnist/mnist_cnn_model.pth) | Pre-trained weights (~812 KB) |
| [cnn_mnist/requirements-cpu.txt](cnn_mnist/requirements-cpu.txt) | **Recommended** — CPU PyTorch (~200 MB, not 2.7 GB) |
| [cnn_mnist/requirements.txt](cnn_mnist/requirements.txt) | Default (may pull GPU/CUDA wheels) |

---

## Quick start

**Important:** Plain `pip install torch` pulls **CUDA/GPU packages (~2 GB+)**. For this CPU-only MNIST demo, use the CPU wheels (~200 MB):

```bash
cd assignment2/cnn_mnist

# Recommended: CPU-only install (~200 MB, one command)
python3 -m pip install -r requirements-cpu.txt

# Or manual CPU install:
# python3 -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
# python3 -m pip install matplotlib numpy scikit-learn Pillow

# Demo with pre-trained weights (downloads MNIST ~12–65 MB on first run)
python3 mnist_cnn.py --mode demo

# Train from scratch (optional)
python3 mnist_cnn.py --mode train

# Evaluate + confusion matrix
python3 mnist_cnn.py --mode eval
```

If you already started a GPU install, press **Ctrl+C**, then run the CPU commands above.

**Note:** MNIST data (~65 MB) is **not** stored in git. PyTorch downloads it to `cnn_mnist/data/MNIST/` on first run. Weights are already in git as `mnist_cnn_model.pth` (~812 KB).

---

## Related course work

| Assignment | Folder |
|------------|--------|
| Assignment 1 — Reasoning Log | [assignment1/](../assignment1/) |
| Assignment 2 | **this folder** |
| Assignment 3 — Swiss Cheese Test Suite | [assignment3/](../assignment3/) |
| Assignment 4 — Final Capstone | [assignment4/](../assignment4/) + [app/](../app/) |

---

## Related

| Resource | Link |
|----------|------|
| Main repository | [README](../README.md) |
| Weekly labs (Week 4 refactoring) | [lab_reports/Week4_SessionA_Report.pdf](../lab_reports/Week4_SessionA_Report.pdf) |
