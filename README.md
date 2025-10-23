# CTOVSR: A Chinese Traditional Opera Video Super-Resolution Dataset

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-blue.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Dataset Size](https://img.shields.io/badge/Dataset%20Size-XX%20GB-orange.svg)](https://your-science-data-bank-link.com)
[![Paper](https://img.shields.io/badge/Paper-Link%20to%20be%20added-brightgreen.svg)](https://your-paper-link.com)

**CTOVSR** is a large-scale, high-quality dataset designed for the super-resolution of aged Chinese Traditional Opera videos. This project addresses the urgent need to digitally preserve and restore invaluable cultural heritage, much of which suffers from severe degradation due to aging, storage, and dissemination.

## 🌟 Introduction

Traditional opera is a crystallization of human civilization, with many genres inscribed on the UNESCO Intangible Cultural Heritage List. However, historical video recordings of these performances are often of low quality, marred by artifacts like blur, noise, and compression errors. The **CTOVSR** dataset was created to facilitate the development of advanced Video Super-Resolution (VSR) models capable of restoring these precious archives.

Our key innovation is the **"Real-world+"** data construction methodology, which fuses authentically degraded video pairs with targeted synthetic degradations. This hybrid approach ensures that the dataset not only reflects the entire, complex lifecycle of real-world video degradation but also covers a diverse range of scenarios, enabling models to achieve superior generalization and restoration performance.

## ✨ Dataset Highlights

*   **Authentic Degradation**: Features "Real-world+" pairs derived from professionally restored films and their corresponding, naturally degraded online versions, capturing the complete degradation pipeline.
*   **High Diversity**: Comprises 900 video sequences from 45 distinct operas, covering a wide variety of scenes, costumes, lighting conditions, and camera work.
*   **Strict Alignment**: All LR-HR pairs are meticulously aligned both spatially and temporally through a rigorous manual and algorithmic verification process.
*   **Hybrid Data Strategy**: Augments authentic data with synthetically degraded sequences (second-order and compression) to enhance model robustness.
*   **Benchmark Ready**: Includes clearly defined training and testing sets for standardized evaluation.

## 📊 Dataset Composition

| Attribute             | Details                                                      |
| --------------------- | ------------------------------------------------------------ |
| **Total Sequences**   | 900 LR-HR pairs                                              |
| **Sequence Length**   | 100 consecutive frames per sequence                          |
| **Frame Format**      | 8-bit PNG                                                    |
| **Color Space**       | sRGB                                                         |
| **Resolution (HR)**   | 1920×1080                                                    |
| **Resolution (LR)**   | 480×270 (for 4× super-resolution)                            |
| **Training Set**      | 800 pairs                                                    |
| **Testing Set**       | 100 pairs (`CTOVSR_test`)                                    |
| **Real-world Test**   | Additional LR-only videos for real-world generalization testing (`REAL_test`) |
| **Degradation Types** | Real-world ("Real-world+"), Second-Order Synthetic, Compression Synthetic |

## 📁 File Structure

The dataset is organized into training and testing sets with a clear directory structure:

```
├── CTOVSR/
│   ├── gt/
│   │   ├── 000/
│   │   │   ├── 00000000.png
│   │   │   └── ... (100 frames)
│   │   └── ... (sequences 000 to 799 for training)
│   └── lq/
│       ├── 000/
│       │   ├── 00000000.png
│       │   └── ... (100 frames)
│       └── ... (sequences 000 to 799 for training)
│
├── CTOVSR_test/
│   ├── gt/
│   │   ├── 000/
│   │   │   └── ... (100 frames)
│   │   └── ... (sequences 000 to 099 for testing)
│   └── lq/
│       ├── 000/
│       │   └── ... (100 frames)
│       └── ... (sequences 000 to 099 for testing)
│
└── metadata.csv
```

The metadata.csv file provides detailed information for each sequence, including the **source video/opera title**  and the specific **type of degradation** applied.

## 📜 Citation

If you use the CTOVSR dataset in your research, please cite our paper:

```
@article{your_citation_key,
  title={A Chinese Traditional Opera Video Super-Resolution Dataset Based on the "Real-world+" Degradation Fusion},
  author={Wang, Xi and Qin, Bingxin and Zhang, Yichi and Yang, Xinyu},
  journal={Scientific Data (To be submitted)},
  year={2024},
  % Add more details once published
}
```

