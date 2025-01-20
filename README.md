# LLM4ProteinEvolution

This repository contains the codebase for **Language Models for Text-Guided Protein Evolution**, presented at the following workshops during the **38th Conference on Neural Information Processing Systems (NeurIPS 2024)**:

- **Workshop on Foundation Models for Science**
- **Workshop on AI for New Drug Modalities**

This project explores the application of language models in guiding protein evolution through text-based inputs, enabling novel approaches in directed evolution, inverse design, and protein function prediction.

---

## Citation
If you use this codebase in your research, please consider citing our work:

```
@inproceedings{
ni2024language,
title={Language Models for Text-guided Protein Evolution},
author={Zhanghan Ni and Shengchao Liu and Hongyu Guo and Anima Anandkumar},
booktitle={NeurIPS 2024 Workshop on AI for New Drug Modalities},
year={2024},
url={https://openreview.net/forum?id=jzX3SrFSci}
}
```

---

## Features
- **Text-Guided Directed Evolution**: Leverage language models to guide the design of protein sequences based on textual descriptions.
- **Functional Annotations**: Use text inputs to predict and refine protein functionalities.
- **Applications in Drug Discovery**: Aimed at enabling advancements in new drug modalities through AI-driven protein engineering.

---

## Installation
To set up the environment, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/ZhanghanNi/LLM4ProteinEvolution.git
   cd LLM4ProteinEvolution
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage
Detailed instructions and examples can be found in the `examples/` folder. Here's a quick overview:

1. **Run Protein Evolution Experiments**:
   ```bash
   python examples/run_evolution.py --config configs/default_config.yaml
   ```

2. **Generate Functional Annotations**:
   ```bash
   python examples/generate_annotations.py --input data/protein_sequences.fasta
   ```

3. **Visualize Results**:
   Use tools in the `visualization/` folder to analyze the output.

---

## Contributions
We welcome contributions to extend this project! Please submit issues or pull requests to improve functionality or add new features.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

## Links
- [OpenReview Submission](https://openreview.net/forum?id=jzX3SrFSci)
- [NeurIPS 2024](https://neurips.cc/Conferences/2024)

---

For any inquiries or support, please contact [Zhanghan Ni](mailto:zhanghan.ni@example.com).
