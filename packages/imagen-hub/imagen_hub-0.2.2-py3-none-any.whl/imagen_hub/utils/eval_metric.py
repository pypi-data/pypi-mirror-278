import os
import csv
import sys
import traceback
import json
from PIL import Image
import os
import pandas as pd
import numpy as np
import math 
from functools import partial
from scipy.stats import spearmanr
from .math_helper import sigfig
from imagen_hub.metrics import MetricImageReward, MetricCLIP_I, MetricDINO, MetricDreamSim, MetricLPIPS
from .eval_human import get_one_model_dict

class QualityEvaluator():
    def __init__(self, device="cuda") -> None:
        self.dino_model = MetricDINO(device)
        self.clipi_model = MetricCLIP_I(device)
        self.dreamsim_model = MetricDreamSim(device)
        self.lpips_model = MetricLPIPS(device)

        self.report_dict = {}
        
    def evaluate_all(self, list_real_images, list_generated_images):
        try:
            dino_score = [self.dino_model.evaluate(x, y) for (x,y) in zip(list_real_images, list_generated_images)]
            print("====> Dino | Avg: ", sigfig(sum(dino_score) / len(dino_score)))
            self.report_dict['dino'] = dino_score
        except Exception as e:
            tb = traceback.format_exc()
            print(f"Dino | Error: {e}\n{tb}")
            pass

        try:
            clipi_score = [self.clipi_model.evaluate(x, y) for (x,y) in zip(list_real_images, list_generated_images)]
            print("====> CLIP-I | Avg: ", sigfig(sum(clipi_score) / len(clipi_score)))
            self.report_dict['clip-i'] = clipi_score
        except Exception as e:
            tb = traceback.format_exc()
            print(f"CLIP-I | Error: {e}\n{tb}")
            pass

        try:
            dreamsim_score = [self.dreamsim_model.evaluate(x, y) for (x,y) in zip(list_real_images, list_generated_images)]
            avg_dreamsim_score = sum(dreamsim_score) / len(dreamsim_score)
            print("====> DreamSim | Avg: ", sigfig(avg_dreamsim_score))
            self.report_dict['dreamsim'] = dreamsim_score
        except Exception as e:
            tb = traceback.format_exc()
            print(f"DreamSim | Error: {e}\n{tb}")
            pass

        try:
            lpips_score = [self.lpips_model.evaluate(x, y) for (x,y) in zip(list_real_images, list_generated_images)]
            avg_lpips_score = sum(lpips_score) / len(lpips_score)
            print("====> LPIPS | Avg: ", sigfig(avg_lpips_score))
            self.report_dict['lpips'] = lpips_score
        except Exception as e: 
            tb = traceback.format_exc()
            print(f"LPIPS | Error: {e}\n{tb}")
            pass

        return self.report_dict

def grab_images(root_dir):
    results_dict = {}
    subdirectories = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]
    for subdir in subdirectories:
        subdir_path = os.path.join(root_dir, subdir)
        for root, _, files in os.walk(subdir_path):
            try:
                from natsort import natsorted
                results_dict[subdir] = [os.path.join(root_dir, subdir, path) for path in natsorted(files)]
                print(f"{subdir} | sort with natsorted | No. of files: {len(files)}")
            except:
                results_dict[subdir] = [os.path.join(root_dir, subdir, path) for path in sorted(files)]
                print(f"{subdir} | No. of files: {len(files)}")
    return results_dict

def grab_images_by_lookup(root_dir, lookup_csv=None):
    results_dict = {}
    subdirectories = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]
    lookup_csv = os.path.join(root_dir, "dataset_lookup.csv") if lookup_csv == None else lookup_csv
    #lookup_json = os.path.join(root_dir, "dataset_lookup.json") if lookup_json == None else lookup_json
    # Open the CSV file and read its contents into the list
    with open(lookup_csv, 'r', newline='') as file:
        data_list = []
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data_list.append(row[0])  # Assuming you want to extract the first (and only) column
        data_list = data_list[1:] # dropping first row
        
    for subdir in subdirectories:
        subdir_path = os.path.join(root_dir, subdir)
        try:
            from natsort import natsorted
            results_dict[subdir] = [os.path.join(root_dir, subdir, path) for path in natsorted(data_list)]
            #print(f"{subdir} | sort with natsorted | No. of files: {len(data_list)}")
        except:
            results_dict[subdir] = [os.path.join(root_dir, subdir, path) for path in sorted(data_list)]
            #print(f"{subdir} | No. of files: {len(data_list)}")
    return results_dict

def fetch_attribute(filebasename, root_dir, lookup_json=None, fetch_attr="prompt"):
    lookup_json = os.path.join(root_dir, "dataset_lookup.json") if lookup_json == None else lookup_json
    with open(lookup_json, 'r') as json_file:
        data = json.load(json_file)
    if filebasename in data:
        fetched_attr = data[filebasename][fetch_attr]
        return fetched_attr
    else:
        print("Image name", filebasename, "not found in", lookup_json)
        raise KeyError(filebasename)

def infer_quality_metric(model_eval, root_dir, compare_to_attr="input", lookup_csv=None):
    result_dict = grab_images_by_lookup(root_dir, lookup_csv)
    for k in result_dict.keys():
        result_dict[k] = [Image.open(img_path).convert("RGB") for img_path in result_dict[k]]
    for k in sorted(result_dict.keys()):
        if k != "input" and k != "token" and k != "mask" and k != "GroundTruth":
            print(f"{k} | Inferencing")
            model_eval.evaluate_all(result_dict[compare_to_attr], result_dict[k])

def infer_quality_metric_corr(model_eval, root_dir, task_name, grab_human_dir="/mnt/tjena/maxku/max_projects/DreamAquarium/eval/simple_human_eval_results", lookup_csv=None):
    result_dict = grab_images_by_lookup(root_dir, lookup_csv)
    for k in result_dict.keys():
        result_dict[k] = [Image.open(img_path).convert("RGB") for img_path in result_dict[k]]
    for k in sorted(result_dict.keys()):
        if k != "input" and k != "token" and k != "mask" and k != "GroundTruth":
            print(f"{k} | Inferencing")
            model_eval.evaluate_all(result_dict["input"], result_dict[k])
            human_dict = get_one_model_dict(grab_human_dir, task_name, k)
            for metric_name in model_eval.report_dict.keys():
                print(f"==> PR | {metric_name}", spearmanr(model_eval.report_dict[metric_name], human_dict['PR'])[0])

def infer_clip_metric(model_clip, root_dir, attr_as_prompt, preprocess_prompt=None, lookup_csv=None):
    result_dict = grab_images_by_lookup(root_dir, lookup_csv)
    for k in sorted(result_dict.keys()):
        result_dict[k] = [
                            [Image.open(img_path).convert("RGB") for img_path in result_dict[k]], 
                            [os.path.basename(img_path) for img_path in result_dict[k]]
                         ]
        # fetch the prompts using the file basename
        temp_basenames = result_dict[k][1]
        if preprocess_prompt is not None:
            result_dict[k][1] = [preprocess_prompt(fetch_attribute(p, root_dir, None, attr_as_prompt)) for p in result_dict[k][1]]
        else:
            result_dict[k][1] = [fetch_attribute(p, root_dir, None, attr_as_prompt) for p in result_dict[k][1]]

    for k in sorted(result_dict.keys()):
        if k != "input" and k != "mask" and k != "token" and k != "GroundTruth":
            print(f"{k} | Inferencing")
            list_images = result_dict[k][0]
            prompts = result_dict[k][1]
            clip_score = [model_clip.evaluate(y,p) for (y,p) in zip(list_images, prompts)]
            #print(clip_score)
            avg_score = sum(clip_score) / len(clip_score)
            print("====> CLIPScore | Avg: ", sigfig(avg_score))
            return clip_score
        
def infer_clip_metric_corr(model_clip, root_dir, attr_as_prompt, preprocess_prompt=None, task_name=None, grab_human_dir="/mnt/tjena/maxku/max_projects/DreamAquarium/eval/simple_human_eval_results"):
    result_dict = grab_images_by_lookup(root_dir)
    for k in sorted(result_dict.keys()):
        result_dict[k] = [
                            [Image.open(img_path).convert("RGB") for img_path in result_dict[k]], 
                            [os.path.basename(img_path) for img_path in result_dict[k]]
                         ]
        # fetch the prompts using the file basename
        temp_basenames = result_dict[k][1]
        if preprocess_prompt is not None:
            result_dict[k][1] = [preprocess_prompt(fetch_attribute(p, root_dir, None, attr_as_prompt)) for p in result_dict[k][1]]
        else:
            result_dict[k][1] = [fetch_attribute(p, root_dir, None, attr_as_prompt) for p in result_dict[k][1]]

    corr_list = []
    for k in sorted(result_dict.keys()):
        if k != "input" and k != "mask" and k != "token" and k != "GroundTruth":
            human_dict = get_one_model_dict(grab_human_dir, task_name, k)
            list_images = result_dict[k][0]
            prompts = result_dict[k][1]
            clip_score = [model_clip.evaluate(y,p) for (y,p) in zip(list_images, prompts)]
            corr_list.append(spearmanr(clip_score, human_dict['SC'])[0])
    print(sum(corr_list)/len(corr_list))