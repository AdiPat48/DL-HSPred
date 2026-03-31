# DeepHotspot-Seq

### Sequence-Only Deep Learning for Protein-Protein Interaction Hotspot Prediction

**DeepHotspot-Seq** is a computational tool designed to identify Protein-Protein Interaction (PPI) hotspots—critical residues contributing significantly to binding free energy—using only primary sequence information. By leveraging high-dimensional embeddings from pre-trained protein language models (**[ProteinBERT](https://github.com/nadavbra/protein_bert)**), this model bypasses the traditional requirement for experimental 3D structures, making hotspot prediction accessible for proteins with unknown folds.

---

## 🚀 Project Overview

Predicting hotspots from sequence alone is a significant challenge due to the lack of explicit spatial context. This project addresses this by:

1. **High-Confidence Labeling**: Generating training labels through a strict consensus of structure-based tools.
2. **Language Model Embeddings**: Using 1562-dimensional feature vectors to capture evolutionary and structural context.
3. **Deep Learning Architecture**: Implementing a custom Multi-Layer Perceptron (MLP) optimized via grid search for robust classification.

* [DeepHotspot-Seq_results.pdf](DeepHotspot-Seq_results.pdf): Detailed project presentation and methodology slides.

---

## 🛠 Methodology: The Consensus Strategy

To ensure the model learns from structure-guided hotspot data, labels were derived from a strict intersection logic:

* **Intersection Formula**: $Grahotspot \cap HotPIES \cap PredHS2$.
* **Logic**: A residue is labeled a "Hotspot" only if independently predicted by all three structural tools.
* **Data Augmentation**: This consensus pipeline was applied to the **PIMADb Dimers + Trimers** dataset, resulting in **759 high-confidence hotspots** for training.

---

## 📂 Repository Structure

* `data_processing/`: Scripts for PDB parsing and consensus dataset generation.
* `features/`: Feature extraction engine using **ProteinBERT** and dimensionality reduction (PCA, UMAP, t-SNE).
* `training/`: Core modeling scripts including the final MLP and hyperparameter grid search.
* `datasets/`: Metadata for training sets (SKEMPI V2, PPI-HotSpotDB) and the independent **BID 2018** test set.

---

## 📊 Results & Performance

### Model Benchmarking (10-fold CV)

The custom Neural Network was benchmarked against 10 baseline classifiers:

| Model | Mean CV F1-Score | Mean CV MCC |
| :--- | :---: | :---: |
| **XGBoost** | 0.82 | 0.73 |
| **Gradient Boosting** | 0.82 | 0.75 |
| **MLP (Deep Learning)** | **0.81** | **0.70** |
| **Random Forest** | 0.66 | 0.58 |

### Independent Validation (BID Dataset)

When tested on the independent **BID (2018)** dataset, the model demonstrated robust "greedy" identification of hotspots:

* **Recall**: 91% (Captured the vast majority of true hotspots).
* **F1-Score**: 58.1%.
* **Accuracy**: 46%.

---

## ⚙️ Model Architecture

The final production model is a 5-layer Multi-Layer Perceptron (MLP):
* **Input**: $(HS + NS) \times 1562$ features.
* **Layers**: 1024 → 512 → 256 → 64 → 32 → 1.
* **Activation**: Gaussian Error Linear Unit (**GELU**).
* **Optimal Tuning**: L1 Regularization (0.01) with 0.0 Dropout yielded the best internal F1-score of 0.733.

---

## 📝 Dependencies

* Python 3.8+
* TensorFlow / Keras
* Biopython (for PDB parsing)
* ProteinBERT
* Scikit-learn
* UMAP-learn / Matplotlib

## References
* Anshul Sukhwal, Ramanathan Sowdhamini, Oligomerisation status and evolutionary conservation of interfaces of protein structural domain superfamilies, Molecular BioSystems(MBS), Volume 9, Issue 7, 1 July 2013, Pages 1652–1661, https://doi.org/10.1039/C3MB25484D
* Nadav Brandes, Dan Ofer, Yam Peleg, Nadav Rappoport, Michal Linial, ProteinBERT: a universal deep-learning model of protein sequence and function, Bioinformatics, Volume 38, Issue 8, March 2022, Pages 2102–2110, https://doi.org/10.1093/bioinformatics/btac020

## Authors
* Aditi Pathak
* Vikas Tiwari
