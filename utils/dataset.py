#!/usr/bin/env python

import pandas as pd
import os
from tqdm import tqdm
import re
import sys

def parse_txt(filename, folder_path, ministry_name):
    with open(f"{folder_path}{filename}", "r") as f:
        lines = f.readlines()
    
    data = [list(filter(None, re.split(" |\t|\n", line)))
            for line in lines]
    
    df = pd.DataFrame(data, columns=["Day", "Time", "m1", "m2", "m3", "m4", "m5", "m6"])
    
    df["Date"] = pd.to_datetime(df["Day"] + " " + df["Time"])
    df["m1"] = df["m1"].astype(int)
    df["m2"] = df["m2"].astype(int)
    df["m3"] = df["m3"].astype(int)
    df["m4"] = df["m4"].astype(int)
    df["m5"] = df["m5"].astype(int)
    df["m6"] = df["m6"].astype(int)
    df["kWh"] = df[["m1", "m2", "m3", "m4", "m5", "m6"]].sum(axis=1)/6
    
    if ministry_name == "interieur":
        df["RAE"] = filename.split(" ")[-1][:-4]
    elif ministry_name == "education":
        df["RAE"] = filename.split("_")[0][3:]
    elif ministry_name == "justice":
        df["RAE"] = filename.split("_")[1]
    else:
        df["RAE"] = filename.split("-")[-1][:-4] # Finance
    
    return df[["RAE", "Date", "kWh"]]


def dataset_conversion(folder_path, ministry_name):
    dfs = []
    files = os.listdir(folder_path)
    for i in tqdm(range(len(files))):
        try:
            dfs.append(parse_txt(files[i], folder_path, ministry_name))
        except:
            print(f"Couldn't parse {files[i]}")

    df_final = pd.concat(dfs, ignore_index=True)
    df_final.to_csv(f"../dataset/ministeres_csv/{ministry_name}.csv", sep=';', index=False)


def dataset_merge(csv_files):
    dfs = [pd.read_csv(filename, sep=';') for filename in csv_files]

    df_merged = dfs[0]
    for i in range(1, len(dfs)):
        df_merged = df_merged.append(dfs[i], ignore_index=True)

    return df_merged


if __name__ == "main":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} [data_folder] [ministry name]")
    else:
        dataset_conversion(sys.argv[1], sys.argv[2])