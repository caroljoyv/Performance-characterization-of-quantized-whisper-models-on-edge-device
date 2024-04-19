# Performance Characterization of Quantized Whisper Models on Edge Device


## Abstract:

The pre-trained speech recognition model Whisper, is one of
the best performing models available. Even though the Whisper releases
show superior performance on devices with the necessary resources, these
models fail to deliver the same level of performance on edge devices
when deployed completely offline, especially when it comes to latency.
Quantization is a thoroughly studied model compression technique in
the premise of Deep Neural Networks, which reduces the model size by
using smaller integer representations for weights and activations. In this
work, quantization is applied to the Whisper releases which are then
deployed on an edge device, Raspberry Pi with ARM processor and the
performance of the models is studied. For reference, the quantized models
are also deployed on an Intel x86 processor. The work presented here
is one of the initial attempts to study the performance of quantized
Whisper models on edge devices.


## Usage:

1. **export.py**: Use this script to export the trained Whisper model to the ONNX format.

2. **quantize.py**: Utilize this script to apply dynamic quantization techniques and optimize the Whisper model for deployment on edge devices.

3. **compute.py**: Execute this script to run the Whisper model on your audio dataset and generate transcripts for evaluation.

4. **accuracy.py**: Run this script after obtaining model predictions and ground truth transcripts to compute accuracy metrics such as WER, CER, etc.

5. **model-size.py**: Run this script to calculate the model size of the Whisper model.






## Requirements:

To install the required dependencies, use `pip install -r requirements.txt`.


