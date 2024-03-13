import os
import sys

def get_model_size(model_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(model_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    size = total_size / (1024 * 1024)  # Convert to MB
    return size

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <model_path>")
        return

    model_path = sys.argv[1]
    if not os.path.exists(model_path):
        print("Model path does not exist.")
        return

    model_size = get_model_size(model_path)
    print(f"Model size: {model_size:.2f} MB")

if __name__ == "__main__":
    main()
