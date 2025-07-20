# Multimodal large language models for information extraction from graph-structured diagrams

This repository contains the code, data, and evaluation scripts for our research on extracting structured information from diagram images using multimodal large language models (MLLMs).

## Overview

We investigate the use of InternVL3-14B, a multimodal large language model (MLLM), for extracting structured information from graph-based diagrams (e.g., flowcharts, BPMN, etc.).  
This project explores both prompting-based and PEFT-finetuned strategies.

## Repository Structure

- `data/labels/`: ground-truth JSON annotations for the diagram datasets used in our study
- `data/predictions/`: JSON extractions for the diagram datasets from the MLLM
- `evaluation/`: Evaluation scripts 

---
