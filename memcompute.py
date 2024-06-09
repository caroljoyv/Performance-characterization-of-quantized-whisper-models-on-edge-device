import sys
import os
import librosa
import time
import numpy as np
import matplotlib.pyplot as plt
import psutil
from transformers import WhisperProcessor, AutoConfig
from optimum.onnxruntime import ORTModelForSpeechSeq2Seq
from memory_profiler import memory_usage


def monitor_resources(interval=1.0):
    cpu_loads = []
    memory_usages = []
    
    def collect():
        while True:
            cpu_loads.append(psutil.cpu_percent(interval=None))
            memory_usages.append(psutil.virtual_memory().used / (1024 ** 2))  # Convert to MB
            time.sleep(interval)

    return cpu_loads, memory_usages, collect


def compute(model_name, file_name, output_file_name):
    total_rtf = 0
    rtf_values = []
    transcriptions = []

    # specify complete model path
    model_path = os.path.join("/home/carol/whisper-quantized", model_name)
    
    # Load the model and processor
    processor = WhisperProcessor.from_pretrained(model_name)
    model_config = AutoConfig.from_pretrained(model_name)
    sessions = ORTModelForSpeechSeq2Seq.load_model(
                os.path.join(model_path, 'encoder_model.onnx'),
                os.path.join(model_path, 'decoder_model.onnx'),
                os.path.join(model_path, 'decoder_with_past_model.onnx'))
    model = ORTModelForSpeechSeq2Seq(sessions[0], sessions[1], model_config, model_path, sessions[2])
    
    # Read filenames from the file to a list
    with open(file_name, "r") as file:
        audio_files = file.read().splitlines()
    audio_files.pop()  # remove the empty element from the list

    print()
    count = 0   
    print("Starting transcription")
    for audio_file in audio_files:
        
        count += 1
        print(count, end=", ")
        audio_path = os.path.join("/home/carol/whisper-quantized/dataset/dev-clean-sampled", audio_file) 
        #/home/carol/mp/quantize/sampled/dev-clean-sampled
        # Load the audio file
        audio_data, sample_rate = librosa.load(audio_path, sr=16000, mono=True)
    
        # Preprocess the audio
        start_time = time.time()
        input_features = processor(audio_data, sampling_rate=sample_rate, return_tensors="pt").input_features
        
        # Get forced decoder prompt IDs
        forced_decoder_ids = processor.get_decoder_prompt_ids(language="english", task="translate")
    
        # Perform model inference
        inference_start_time = time.time()
        predicted_ids = model.generate(input_features, forced_decoder_ids=forced_decoder_ids)[0]
        inference_time = time.time() - inference_start_time
    
        # Decode the predicted IDs
        decoding_start_time = time.time()
        trans = processor.decode(predicted_ids, skip_special_tokens=True)
        decoding_time = time.time() - decoding_start_time
        
        # Calculate RTF
        read_time = time.time() - start_time
        total_utterance_duration = len(audio_data) / sample_rate
        rtf = (read_time + inference_time + decoding_time) / total_utterance_duration
        
        # Append transcription and rtf to the lists
        transcriptions.append(trans)
        rtf_values.append(rtf)
        
        # Print the transcription
        print(trans)
    
    # Calculate statistics
    average_rtf = np.mean(rtf_values)
    mean_rtf = np.mean(rtf_values)
    p75_rtf = np.percentile(rtf_values, 75)
    p90_rtf = np.percentile(rtf_values, 90)
    
    # Write transcriptions to file
    with open(output_file_name, "w") as f:
        f.write(str(transcriptions))

    # Print statistics
    print("\nStatistics:")
    print("Average RTF for the dataset:", average_rtf)
    print("Mean RTF for the dataset:", mean_rtf)
    print("P75 RTF for the dataset:", p75_rtf)
    print("P90 RTF for the dataset:", p90_rtf)


def main():
    if len(sys.argv) != 4:
        print("Usage: python compute.py model_name file_name output_file_name")
        sys.exit(1)
    
    model_name = sys.argv[1]
    file_name = sys.argv[2]
    output_file_name = sys.argv[3]

    # Start resource monitoring
    cpu_loads, memory_usages, collect = monitor_resources()
    
    from threading import Thread
    monitor_thread = Thread(target=collect)
    monitor_thread.daemon = True
    monitor_thread.start()
    
    # Profile memory usage and run compute
    mem_usage = memory_usage((compute, (model_name, file_name, output_file_name)), interval=1)
    
    # Save the profiling data
    with open(f'{model_name}_memory_usage.txt', 'w') as f:
        for mem in mem_usage:
            f.write(f"{mem}\n")

    with open(f'{model_name}_cpu_loads.txt', 'w') as f:
        for cpu in cpu_loads:
            f.write(f"{cpu}\n")

    # Plot memory and CPU usage
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(mem_usage, label='Memory Usage (MB)')
    plt.xlabel('Time (s)')
    plt.ylabel('Memory Usage (MB)')
    plt.title(f'{model_name} Memory Usage Over Time')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(cpu_loads, label='CPU Load (%)')
    plt.xlabel('Time (s)')
    plt.ylabel('CPU Load (%)')
    plt.title(f'{model_name} CPU Load Over Time')
    plt.legend()

    plt.tight_layout()
    plt.savefig(f'{model_name}_resource_usage.png')
    plt.show()

if __name__ == "__main__":
    main()