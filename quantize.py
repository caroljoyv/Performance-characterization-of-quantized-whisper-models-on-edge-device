import argparse
from pathlib import Path
from optimum.onnxruntime import ORTQuantizer, AutoQuantizationConfig

def quantize_arm(model_dir, save_dir):
    # Create a list of ONNX models from the directory
    onnx_models = list(Path(model_dir).glob("*.onnx"))

    # Instantiate quantizer and set quantization configuration
    quantizers = [ORTQuantizer.from_pretrained(model_dir, file_name=onnx_model) for onnx_model in onnx_models]
    qconfig = AutoQuantizationConfig.arm64(
        is_static=False,
        per_channel=False,
        nodes_to_exclude=['/conv1/Conv', '/conv2/Conv'],
        use_symmetric_activations=True,
        use_symmetric_weights=True,
        operators_to_quantize=None
    )

    for quantizer in quantizers:
        # Apply dynamic quantization and save the resulting model
        quantizer.quantize(save_dir=save_dir, quantization_config=qconfig)
        print("Quantized ", quantizer)
    
    print("Quantization complete")
    print("Model saved at location ", save_dir)

def main():
    parser = argparse.ArgumentParser(description="Quantize ONNX models for ARM deployment")
    parser.add_argument("model_dir", type=str, help="Directory containing ONNX models")
    parser.add_argument("save_dir", type=str, help="Directory to save quantized models")
    args = parser.parse_args()

    model_dir = args.model_dir
    save_dir = args.save_dir
    quantize_arm(model_dir, save_dir)

if __name__ == "__main__":
    main()
