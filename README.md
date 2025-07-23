# Multimodal large language models for information extraction from graph-structured diagrams 

This repository contains the code, data, and evaluation scripts for our research on extracting structured information from diagram images using multimodal large language models (MLLMs).

## Overview

We investigate the use of InternVL3-14B, a multimodal large language model (MLLM), for extracting structured information from graph-based diagrams (e.g., flowcharts, BPMN, etc.) using few-shot prompting and parameter-efficient fine-tuning (PEFT).  


## Repository Structure

- `data/labels/`: ground-truth JSON annotations for the diagram datasets used in our study. Note: Labels for SEM and CBD are not included due to licensing constraints.
- `evaluation/`: Evaluation scripts
- `results/`: CSV files for our results 
- `prompts/`: Text files for the prompts we used 

---

## Results 
The tables below shows F1 scores for diagram recognition across several datasets using 2-shot prompting and the PEFT model. We report performance separately for node and edge components, including subcategories like text, class, and full combinations.

### 2-Shot Prompting 

| Dataset    | Node (Text) | Node (Class) | Node (Full) | Edge (Path) | Edge (Class) | Edge (Label) | Edge (Full) |
|------------|-------------|--------------|-------------|-------------|--------------|--------------|-------------|
| FC_A       | 0.780       | 0.882        | 0.688       | 0.573       | 0.974        | 0.934        | 0.549       |
| FA         | 0.969       | 0.942        | 0.910       | 0.772       | 0.943        | 0.903        | 0.674       |
| hdBPMN     | 0.640       | 0.722        | 0.507       | 0.344       | 0.775        | 0.747        | 0.283       |
| CBD        | 0.951       | 0.988        | 0.951       | 0.822       | 0.979        | 0.960        | 0.807       |
| SEM        | 0.808       | 0.804        | 0.675       | 0.505       | 0.923        | 0.790        | 0.394       |
| SAM-UML    | 0.847       | 0.942        | 0.810       | 0.441       | 0.546        | 0.452        | 0.100       |
| SAM-BPMN   | 0.714       | 0.787        | 0.582       | 0.471       | 0.861        | 0.771        | 0.363       |

### PEFT

| Dataset  | Node (Text) | Node (Class) | Node (Full) | Edge (Path) | Edge (Class) | Edge (Label) | Edge (Full) |
| -------- | ----------- | ------------ | ----------- | ----------- | ------------ | ------------ | ----------- |
| FC\_A    | 0.869       | 0.990        | 0.865       | 0.738       | 0.992        | 0.980        | 0.722       |
| FA       | 0.981       | 0.957        | 0.947       | 0.937       | 0.978        | 0.964        | 0.922       |
| hdBPMN   | 0.680       | 0.769        | 0.633       | 0.469       | 0.793        | 0.772        | 0.441       |
| CBD      | 0.955       | 0.991        | 0.955       | 0.849       | 0.987        | 0.969        | 0.834       |
| SEM      | 0.774       | 0.669        | 0.516       | 0.445       | 0.862        | 0.673        | 0.301       |
| SAM-UML  | 0.843       | 0.289        | 0.253       | 0.377       | 0.179        | 0.508        | 0.021       |
| SAM-BPMN | 0.606       | 0.796        | 0.527       | 0.318       | 0.872        | 0.735        | 0.240       |


### SAM-UML 
The following table reports F1 scores for the SAM-UML dataset, including methods and attributes, as well as edge cardinalities.

| Method | Node (Text) | Node (Class) | Node (Methods) | Node (Attributes) | Node (Full)\* | Edge (Path) | Edge (Class) | Edge (Label) | Edge (Cardinality) | Edge (Full) |
| ------ | ----------- | ------------ | -------------- | ----------------- | ------------- | ----------- | ------------ | ------------ | ------------------ | ----------- |
| 2-Shot | 0.847       | 0.942        | 0.340          | 0.074             | 0.044         | 0.441       | 0.546        | 0.452        | 0.307              | 0.100       |
| PEFT   | 0.843       | 0.289        | 0.355          | 0.170             | 0.056         | 0.377       | 0.179        | 0.508        | 0.859              | 0.021       |

&#42; For UML-specific node recognition, a node is considered correctly matched only if its text, class, methods, and attributes all match the ground truth.

### hdBPMN and SAM-BPMN
The following table reports group recognition F1 scores for the hdBPMN and SAM-BPMN dataset. 

| Dataset  | Method | Group (Name) | Group (Class) | Group (Texts)\* | Group (Full) |
| -------- | ------ | ------------ | ------------- | ------------- | ------------ |
| SAM BPMN | 2-Shot | 0.268        | 0.371         | 0.000         | 0.000        |
|          | PEFT   | 0.378        | 0.567         | 0.142         | 0.016        |
| hdBPMN   | 2-Shot | 0.448        | 0.656         | 0.262         | 0.162        |
|          | PEFT   | 0.621        | 0.796         | 0.408         | 0.356        |

&#42; Group (Texts) refers to the nodes contained inside a group. 

### SEM 
The following table reports F1 scores for node and edge recognition on the SEM dataset using 2-shot prompting, the PEFT model, and the PEFT model with 2-shot prompting during inference.

| Dataset | Method        | Node      | Edge      |
| ------- | ------------- | --------- | --------- |
| SEM     | 2-Shot        | 0.675     | 0.394     |
|         | PEFT          | 0.516     | 0.287     |
|         | 2-Shot + PEFT | 0.635     | 0.360     |
