# Made by Isaac Joffe

from . import analyze
from . import beam
from . import number
from . import relationships
from . import yolo
import time
import argparse
from pathlib import Path

import os
import sys


current_path = os.path.dirname(os.path.abspath(__file__))
features_path = current_path + "/models/features/"
number_path = current_path + "/models/number/"
relationships_path = current_path + "/models/relationships/"


def run(image_name):
    c_time = time.time()

    print("\nExtracting image features...\n")
    image_features = yolo.run_features(image_name, features_path)
    print(f"\nDone. {time.time() - c_time} seconds.\n")
    c_time = time.time()

    print("\nReading number values...\n")
    number_model = number.create_number_model(number_path)
    if image_features:
        for i in range(len(image_features)):
            if image_features[i][-1] == 4:
                number_name = number.segment_image(image_name, image_features[i])
                number_name = number.preprocess_image(number_name)
                if number_name:
                    number_value = number.read_number(number_name, number_model)
                else:
                    number_value = 1
                image_features[i].insert(5, number_value)    # insert read value in second-to-last position
    number.clear_number_model(number_model)
    print(f"\nDone. {time.time() - c_time} seconds.\n")
    c_time = time.time()

    print("\nLoading multilayer perceptrons...\n")
    golden_bs_model = relationships.load_golden_model(relationships_path + "Beam-Support")
    golden_bl_model = relationships.load_golden_model(relationships_path + "Beam-Load")
    golden_ln_model = relationships.load_golden_model(relationships_path + "Load-Number")
    golden_gn_model = relationships.load_golden_model(relationships_path + "Length-Number")
    golden_el_model = relationships.load_golden_model(relationships_path + "Element-Length")
    golden_ls_model = relationships.load_golden_model(relationships_path + "Length-Style")
    print(f"\nDone. {time.time() - c_time} seconds.\n")
    c_time = time.time()

    print("\nConsolidating image features...\n")
    detected_beams = beam.beamify(image_features, golden_bs_model, golden_bl_model, golden_ln_model)
    print(f"\nDone. {time.time() - c_time} seconds.\n")
    c_time = time.time()

    print("\nAnalyzing resultant beam system...\n")
    save_dir = current_path + "/runs/" + (image_name.split(".")[0]).split("/")[-1]
    print(image_features)
    for i in range(len(detected_beams)):
        Path(f"{save_dir}/{i}").mkdir(parents=True, exist_ok=True)
        analyze.analyze_beam(detected_beams[i], image_features, golden_gn_model, golden_el_model, golden_ls_model, f"{save_dir}/{i}")
    print(f"\nDone. {time.time() - c_time} seconds.\n")

    print(f"\nAnalysis plots saved to directory {save_dir}.\n")
    return 


if __name__ == "__main__":
    run("data/test/IMG-8293.jpg")
