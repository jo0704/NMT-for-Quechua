# Low-Resource NMT for Quechua

This repository presents the code, which has been used for the Master's Thesis "Low-Resource NMT for Quechua: Different Segmentation Strategies for a Morphologically Rich Language" at the Institute for Computational Linguistics at the University of Zurich.

## Requirements

### Virtual environment 

```conda create --name new_env tensorflow-gpu=2.2.0 python=3.7 cudatoolkit=10``` \
```conda activate new_env```

### Nematus 

```git clone https://github.com/EdinburghNLP/nematus```

### Sockeye

```git clone https://github.com/awslabs/sockeye.git``` \
```cd sockeye && pip3 install --editable .```
