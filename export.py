import argparse
import shutil
from optimum.onnxruntime import ORTModelForSpeechSeq2Seq

def export_onnx(model_id, save_dir):
    model = ORTModelForSpeechSeq2Seq.from_pretrained(model_id, export=True)
    model_dir = model.model_save_dir
        
    shutil.move(model_dir, save_dir)
    print("Model exported to ONNX and saved at location", save_dir)

def main():
    parser = argparse.ArgumentParser(description="Export ONNX model")
    parser.add_argument("model_id", type=str, help="Model ID to export")
    parser.add_argument("save_dir", type=str, help="Directory to save the exported ONNX model")
    args = parser.parse_args()

    model_id = args.model_id
    save_dir = args.save_dir
    export_onnx(model_id, save_dir)

if __name__ == "__main__":
    main()
