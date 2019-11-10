#!/usr/bin/env python3
import requests
import json
import os
import matplotlib.pyplot as plot
import seaborn
import pandas
import numpy as np

from const import *
from language_info import *


def main():
    initialze()
    all_data = []
    all_normalized_data = None
    for language_info in LANGUAGE_INFOS:
        print("start " + language_info.get_lang_name())
        lang_name = language_info.get_lang_name()

        local_data = language_info.get_lang_quolity()
        local_data = set(local_data)
        all_data.extend(local_data)

        cur_data = pandas.DataFrame(
            {"language": lang_name, "ccn": pandas.Series([x.ccn for x in local_data])}
        )
        cur_normalized_data = delete_outliner(cur_data)
        all_normalized_data = (
            cur_normalized_data
            if all_normalized_data is None
            else pandas.concat([all_normalized_data, cur_normalized_data])
        )

    print("data num :" + str(len(all_data)))
    draw_by_language(lang_name, all_normalized_data.drop_duplicates())
    draw_most_yabe(all_data)


def initialze():
    os.makedirs(Const.PROJECTS_PATH, exist_ok=True)
    os.makedirs(Const.RESULT_PATH, exist_ok=True)
    if os.path.isfile(Const.RESULT_BY_LANGUAGE):
        os.remove(Const.RESULT_BY_LANGUAGE)
    if os.path.isfile(Const.RESULT_MOST_YABE):
        os.remove(Const.RESULT_MOST_YABE)

    lang_result = open(Const.RESULT_BY_LANGUAGE, mode="a")
    lang_result.write("language" + "," + "ccn" + "\n")
    lang_result.close()

    plot.figure(figsize=(16, 10), dpi=80)
    plot.title("Density Plot of ccn by language", fontsize=22)
    plot.legend(
        title="language",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        facecolor="white",
        frameon=False,
    )


def write_by_language(lang_name, data):
    lang_result = open(Const.RESULT_BY_LANGUAGE, mode="a")
    for func_info in data:
        lang_result.write(func_info.lang + ",")
        lang_result.write(func_info.ccn + "\n")
    lang_result.close()


def write_most_yabe(all_data):
    result = sorted(all_data, key=lambda x: x.ccn, reverse=True)
    all_result = open(Const.RESULT_MOST_YABE, mode="a")
    for func_info in result[0:1000]:
        all_result.write(func_info.name + "," + func_info.ccn + "\n")
    all_result.close()


def draw_by_language(lang_name, df):
    colors = seaborn.hls_palette(24, l=0.5, s=1)

    # distribution graph
    # seaborn.kdeplot(df.loc[df['language'] == "python", "ccn"], shade=True, color=colors[0], label="python", alpha=.7)
    # seaborn.kdeplot(df.loc[df['language'] == "cpp", "ccn"], shade=True, color=colors[1], label="cpp", alpha=.7)
    # seaborn.kdeplot(df.loc[df['language'] == "java", "ccn"], shade=True, color=colors[2], label="java", alpha=.7)
    # seaborn.kdeplot(df.loc[df['language'] == "javascript", "ccn"], shade=True, color=colors[3], label="javascript", alpha=.7)
    # seaborn.kdeplot(df.loc[df['language'] == "swift", "ccn"], shade=True, color=colors[4], label="swift", alpha=.7)
    # seaborn.kdeplot(df.loc[df['language'] == "ruby", "ccn"], shade=True, color=colors[5], label="ruby", alpha=.7)
    # seaborn.kdeplot(df.loc[df['language'] == "php", "ccn"], shade=True, color=colors[6], label="php", alpha=.7)
    # seaborn.kdeplot(df.loc[df['language'] == "scala", "ccn"], shade=True, color=colors[7], label="scala", alpha=.7)
    # seaborn.kdeplot(df.loc[df['language'] == "go", "ccn"], shade=True, color=colors[8], label="go", alpha=.7)
    # seaborn.kdeplot(df.loc[df['language'] == "lua", "ccn"], shade=True, color=colors[9], label="lua", alpha=.7)

    # violin graph
    seaborn.violinplot(x="language", y="ccn", data=df, scale="width", inner="quartile")

    # violin graph
    # seaborn.boxplot(x='language', y='ccn', data=df, notch=False)

    plot.show()


def draw_most_yabe(all_data):
    all_data = sorted(set(all_data), key=lambda x: x.ccn, reverse=True)
    for x in all_data[0:100]:
        print(x)


def delete_outliner(df):
    col = df.iloc[:, 1]
    average = np.mean(col)
    sd = np.std(col)
    outlier_min = average - (sd) * 2
    outlier_max = average + (sd) * 2
    df = df[df["ccn"] >= outlier_min]
    df = df[df["ccn"] <= outlier_max]
    return df


if __name__ == "__main__":
    main()
