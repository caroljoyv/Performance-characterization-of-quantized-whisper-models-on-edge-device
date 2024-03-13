import sys
import os
import librosa
import time
from transformers import WhisperProcessor, AutoConfig
from optimum.onnxruntime import ORTModelForSpeechSeq2Seq

def compute(model_name, file_name):
    total_rtf = 0
    transcriptions = []

    # specify complete model path
    model_path = os.path.join("/home/carol/mp/quantize", model_name)
    
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
    audio_files.pop() # remove the empy element from the list

    print()
    count = 0   
    print("Staring transcription")
    for audio_file in audio_files:
        
        count += 1
        print(count, end=", ")
        audio_path = os.path.join("/home/carol/mp/quantize/sampled/dev-clean-sampled", audio_file) 
        
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
    
        # Decode the predicted IDs -- trans
        decoding_start_time = time.time()
        trans = processor.decode(predicted_ids, skip_special_tokens=True)
        decoding_time = time.time() - decoding_start_time
        
        # Calculate RTF
        read_time = time.time() - start_time
        total_utterance_duration = len(audio_data) / sample_rate
        rtf = (read_time + inference_time + decoding_time) / total_utterance_duration

        print(trans)
        # append transcription to the list ans sum rtf
        transcriptions.append(trans)
        total_rtf += rtf

    average_rtf = total_rtf / len(audio_files)
    
    # Write transcriptions to file
    output_file = "/home/carol/mp/quantize/transcriptions/tiny/transcription.txt"
    with open(output_file, "w") as f:
        f.write(str(transcriptions))

    print("Average RTF for the dataset:", average_rtf)

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py model_name file_name")
        sys.exit(1)
    
    model_name = sys.argv[1]
    file_name = sys.argv[2]
    compute(model_name, file_name)

if __name__ == "__main__":
    main()