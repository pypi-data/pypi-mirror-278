from .main import pipeline_lcp
import warnings
import pandas as pd
warnings.filterwarnings("ignore")

data = pd.read_csv("")

pipeline = pipeline_lcp()

audio_path = ""
video_path = ""
captions1 = ""
data["summary"] = [None]*len(data)
for i,caption in enumerate(data["data"]):
    captions = "".join(caption)
    ner_words,key_words,summary = pipeline._pipeline(captions=captions)
    data["summary"][i] = summary["captions"]
    data.to_csv("Data_with_summaries.csv",index=False)