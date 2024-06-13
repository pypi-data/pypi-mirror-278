from transformers import T5Tokenizer, T5ForConditionalGeneration, AutoModelForTokenClassification, AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from gliner import GLiNER
import torch
import cv2
from PIL import Image
from transformers import AutoProcessor, LlavaForConditionalGeneration
import pickle
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
import re
import os
from transformers import Speech2TextProcessor, Speech2TextForConditionalGeneration
from datasets import load_dataset
import librosa
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
import json
from langdetect import detect

def get_lang_code(text,lang_code_map):
    detected_lang = detect(text)
    return lang_code_map.get(detected_lang, 'eng_Latn')


#Extract key words
def extract_keywords(inputs,model,tokenizer):
    task_prefix = "Keywords: "

    # results = []

    # for sample in inputs:
    #     input_sequences = [task_prefix + sample]
    #     input_ids = tokenizer(input_sequences, return_tensors="pt", truncation=True).to(2).input_ids
    #     output = model.generate(input_ids, no_repeat_ngram_size=3, num_beams=4)
    #     predicted = tokenizer.decode(output[0], skip_special_tokens=True)
    #     results.append((sample, predicted))
    input_sequences = [task_prefix + inputs]
    input_ids = tokenizer(input_sequences, return_tensors="pt", truncation=True).to(2).input_ids
    output = model.generate(input_ids, no_repeat_ngram_size=3, num_beams=4)
    predicted = tokenizer.decode(output[0], skip_special_tokens=True)
    return predicted


# Name Entity Recognition
def merge_entities(entities,text):
    if not entities:
        return []
    merged = []
    current = entities[0]
    for next_entity in entities[1:]:
        if next_entity['label'] == current['label'] and (next_entity['start'] == current['end'] + 1 or next_entity['start'] == current['end']):
            current['text'] = text[current['start']: next_entity['end']].strip()
            current['end'] = next_entity['end']
        else:
            merged.append(current)
            current = next_entity
    # Append the last entity
    merged.append(current)
    return merged


def perform_ner(text,labels,model):
    # NuZero requires labels to be lower-cased!
    labels = [l.lower() for l in labels]

    # text = "At the annual technology summit, the keynote address was delivered by a senior member of the Association for Computing Machinery Special Interest Group on Algorithms and Computation Theory, which recently launched an expansive initiative titled 'Quantum Computing and Algorithmic Innovations: Shaping the Future of Technology'. This initiative explores the implications of quantum mechanics on next-generation computing and algorithm design and is part of a broader effort that includes the 'Global Computational Science Advancement Project'. The latter focuses on enhancing computational methodologies across scientific disciplines, aiming to set new benchmarks in computational efficiency and accuracy."

    entities = model.predict_entities(text, labels)
    entities = merge_entities(entities,text)

    entities_text = []
    for entity in entities:
        if entity["text"] not in entities_text:
            entities_text.append(entity["text"])

    return entities_text

#Audio to text
def audio_to_text(audio_path,model,processor):    
    # Load Audio
    audio_data,sampling_rate = librosa.load(audio_path)
    sampling_rate = 16000
    
    # Process audio data
    inputs = processor(audio_data, sampling_rate=sampling_rate, return_tensors="pt").to(2)
    
    # Generate transcriptions
    print("Generating Transcription for :", audio_path)
    generated_ids = model.generate(inputs=inputs.input_features)
    print("Transcriptions Generated  for :", audio_path)

    
    # Decode the generated IDs to obtain the transcription text
    print("Decoding the generated IDs to obtain the transcription text for :", audio_path)
    transcriptions = processor.batch_decode(generated_ids, skip_special_tokens=True)
    return transcriptions[0]

#Video to text
def extract_frames(video_path, frame_path):
    video = cv2.VideoCapture(video_path)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_count = 0
    while True:
        success, frame = video.read()
        if not success:
            break
        out_path = f"{frame_path}/frame_{frame_count}.jpg"
        cv2.imwrite(out_path, frame)
        frame_count += 1
        print(f"Extracted frame {frame_count}/{total_frames}")
    video.release()

def image_text(image_list, processor1, model1):
    l = len(image_list)
    prompts = [
        "A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions and if you don't know anything related to user's question,then don't comment anything about it."
        "USER: <image>\nSummarize this in geo-political context in less than 50 words?\nASSISTANT:",
        "USER: <image>\nSummarize this in geo-political context in less than 50 words?\nASSISTANT:",
        "USER: <image>\nSummarize this in geo-political context in less than 50 words?\nASSISTANT:",
        "USER: <image>\nSummarize this in geo-political context in less than 50 words?\nASSISTANT:",
        "USER: <image>\nSummarize this in geo-political context in less than 50 words?\nASSISTANT:",
        "USER: <image>\nSummarize this in geo-political context in less than 50 words?\nASSISTANT:",
        "USER: <image>\nSummarize this in geo-political context in less than 50 words?\nASSISTANT:",
        "USER: <image>\nSummarize this in geo-political context in less than 50 words?\nASSISTANT:",
        "USER: <image>\nSummarize this in geo-political context in less than 50 words?\nASSISTANT:",
    ]
    if l == 9:
        inputs = processor1(
            prompts, image_list, return_tensors="pt", padding=True, truncation=True
        ).to(2, torch.float16)
        output = model1.generate(**inputs, max_new_tokens=500)
        return processor1.batch_decode(output, skip_special_tokens=True)
    else:
        prompts_l = prompts[:l]
        inputs = processor1(
            prompts_l,
            image_list,
            return_tensors="pt",
            padding=True,
            truncation=True,
        ).to(2, torch.float16)
        output = model1.generate(**inputs, max_new_tokens=200)
        return processor1.batch_decode(output, skip_special_tokens=True)
    
def image_extract(input_directory,processor1,model1):
    lis = []

    image_list = []
    i = 0
    for filename in os.listdir(input_directory):
        if i % 50 != 0:
            i = i + 1
            continue
        i = i + 1
        # Construct the full file path
        file_path = os.path.join(input_directory, filename)
        image = Image.open(file_path)
        image_list.append(image)
    x = 0
    while x < len(image_list):
        y = x
        x = x + 6
        if x > len(image_list):
            x = len(image_list)
        temp = image_list[y:x]
        # lis.append(temp)
        generated_text = image_text(temp,processor1,model1)
        for text in generated_text:
            lis.append(text.split("ASSISTANT:")[-1])
    return lis

def split_text(text, max_tokens=500):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    for word in words:
        word_length = len(word)
        if current_length + word_length > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(word)
        current_length += word_length + 1
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def image_to_text(image_path,model,processor):
    prompt = "<|user|>\n<image>\nIdentify the persons in the image and describe the image in terms of the geo-political context<|end|>\n"

    raw_image = Image.open(image_path).raw
    inputs = processor(prompt, raw_image, return_tensors="pt").to(0, torch.float16)

    output = model.generate(**inputs, max_new_tokens=500, do_sample=False)

    decoded_text = processor.decode(output[0][2:], skip_special_tokens=True)
    return decoded_text

def video_to_text(video_path,frames_path,model,processor):
    extract_frames(video_path,frames_path)
    lis1 = image_extract(frames_path, processor, model)
    if(len(lis1)>50):
        lis1 = lis1[:50]
    combined_text = " ".join(lis1)
    combined_text = combined_text.strip()
    combined_text = re.sub(r"[^\w\s]", "", combined_text)
    return combined_text

def summarize_with_llama(text,llm):
      output = llm(
            prompt=f"Summarize the following text:\n\n{text}\n\nSummary:",
            max_tokens=200,
            temperature=0.7,
            top_p=0.9,
            stop=["\n", "Summary:"]
      )
      summary = output["choices"][0]["text"].strip()
      return summary

def summarize_with_t5(text,model,tokenizer):
    prompt = "I have extracted caption from frames of a video and joined them in a string. can you please summarize the whole video by analysing the frame summary if i send you the frames description \n"
    prompt = prompt + text
    model_inputs = tokenizer(prompt,return_tensors="pt").to(2)
    output = model.generate(**model_inputs,max_length=2000,
        temperature=0.5,)
    summary = tokenizer.decode(output[0],skip_special_tokens=True)
    return summary

# def call_back(text):
#     if text.lsplit == "":
#         return initialize_translator
#     else:
#         return extract_keywords

def initialize_models():
    models = {}
    models["translator_model"] = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M").to(2)
    models["translator_tokenizer"] = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
    models["keywords_model"] = T5ForConditionalGeneration.from_pretrained("Voicelab/vlt5-base-keywords").to(2)
    models["keywords_tokenizer"] = T5Tokenizer.from_pretrained("Voicelab/vlt5-base-keywords")
    models["ner_model"] = GLiNER.from_pretrained("numind/NuNerZero").to(2)
    models["speechtext_model"] = Speech2TextForConditionalGeneration.from_pretrained("facebook/s2t-small-librispeech-asr").to(2)
    models["speechtext_processor"] = Speech2TextProcessor.from_pretrained("facebook/s2t-small-librispeech-asr")
    image_model_id = "xtuner/llava-phi-3-mini-hf"
    models["imagetext_model"] = LlavaForConditionalGeneration.from_pretrained(
            image_model_id,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
        ).to(2)
    models["imagetext_processor"] = AutoProcessor.from_pretrained(image_model_id)
    repo_id = "bartowski/LLaMA3-iterative-DPO-final-GGUF"
    filename = "LLaMA3-iterative-DPO-final-IQ1_M.gguf"
    model_path = hf_hub_download(repo_id=repo_id, filename=filename)
    models["Llama_summarizer"] = Llama(model_path=model_path)
    models["t5_tokenizer"] = AutoTokenizer.from_pretrained("google-t5/t5-small")
    models["t5_models"] = AutoModelForSeq2SeqLM.from_pretrained("google-t5/t5-small").to(2)
    return models



def pipeline_lcp(captions=None,audio_path=None,image_path = None,video_path=None):
    print("Initializing Models .....")
    models = initialize_models()

    text = {}
    if audio_path:
        audio_text = audio_to_text(audio_path,models["speechtext_model"],models["speechtext_processor"])
        text["audio"] = audio_text
    if image_path:
        text["image"] = image_to_text(image_path,models["imagetext_model"],models["imagetext_processor"])
    if video_path:
        video_dir = os.path.dirname(video_path)
        video_file = os.path.basename(video_path)
        video_filename = os.path.splitext(video_file)[0]
        frames_path = os.path.join(video_dir,f"{video_filename}_Frames")
        os.makedirs(frames_path, exist_ok=True)
        video_text = video_to_text(video_path,frames_path,models["imagetext_model"],models["imagetext_processor"])
        text["video"] = video_text
    
    if captions:
        text["captions"] = captions

    labels = ["Event","Location","organization","Action","Legal Terms","Infrastructure","Description of Acts","Adverse Effects"]
    
    with open('Lang_code_map.json') as f:
        lang_code_map = json.load(f)

    ner_words = {}
    key_words = {}
    summaries = {}
    for modal,modal_text in text.items():
        text_code = get_lang_code(modal_text,lang_code_map)
        translator = pipeline('translation', model=models["translator_model"], tokenizer=models["translator_tokenizer"], src_lang=text_code, tgt_lang='eng_Latn', max_length=400)
        translated_text = translator(modal_text)[0]["translation_text"]       
        print(f"Performing {modal} NER ....")
        ner_words[modal] = perform_ner(translated_text,labels,models["ner_model"])
        print(f"Performing {modal} Keyword Extraction ....")
        keywords_str = extract_keywords(translated_text,models["keywords_model"],models["keywords_tokenizer"])
        key_words[modal] = [keyword.strip() for keyword in keywords_str.split(",")]
        print(f"Performing {modal} Summarization ....")
        if modal == "video":
            summaries[modal] = summarize_with_t5(translated_text,models["t5_model"],models["t5_tokenizer"])
        else:
            summaries[modal] = summarize_with_llama(translated_text,models["Llama_summarizer"])
    return ner_words,key_words,summaries
    

if __name__ == "__main__":
    models = initialize_models()
    video_path = "/home/ml-vm/Desktop/Sambit/LCP/Vladimir Putin meets Xi Jinping in China ahead of Belt and Road Initiative forum _ AFP.mp4"
    ner_words,key_words,summary = pipeline_lcp(video_path=video_path)
    print(summary)