import pytest
import pandas as pd
import os
from pp_weight_estimation.core.function_test import process_pipeline

class MockLogger:
    def info(self, message):
        print(f"INFO: {message}")
    def error(self, message):
        print(f"ERROR: {message}")

logger = MockLogger()

def test_process_pipeline():
    input_csv = "tests/sample_input.csv"
    gt_csv = "tests/sample_gt.csv"
    val_color_csv = "tests/sample_val_color.csv"
    
    input_df = pd.DataFrame({
        's3_image_path': ['data/pp_images/bacon_1103.jpg', 'data/pp_images/bacon_1303.jpg', 'data/pp_images/bacon_1503.jpg'],
        'site_id': ['S001', 'S001', 'S001'],
        'taxonomy_code': ['T001', 'T001', 'T001'],
        'input_groundtruth': [400, 120, 300]
    })
    input_df.to_csv(input_csv, index=False)

    gt_df = pd.DataFrame({
        'taxonomy_code': ['T001', 'T001'],
        'reference_pixel_count': [818671, 257877],
        'groundtruth': [400, 120]
    })
    gt_df.to_csv(gt_csv, index=False)

    val_color_df = pd.DataFrame({
        'taxonomy_code': ['T001'],
        'site_id': ['S001'],
        'colors': ['[(208,170,133),(154,123,100),(81,62,43),(236,208,168),(67,52,36)]']
    })
    val_color_df.to_csv(val_color_csv, index=False)

    output_csv_path, results = process_pipeline(input_csv, gt_csv, val_color_csv, logger)

    assert os.path.exists(output_csv_path)

    output_df = pd.read_csv(output_csv_path)

    expected_columns = ['s3_image_path', 'site_id', 'taxonomy_code', 'input_groundtruth', 'mask', 'final_image', 'pixel_count', 'histogram', 'pred_w2', 'error', 'success']
    assert all([col in output_df.columns for col in expected_columns])

    assert len(results) == 3 

   
    assert all(output_df['success'])


    os.remove(input_csv)
    os.remove(gt_csv)
    os.remove(val_color_csv)
    os.remove(output_csv_path)


if __name__ == "__main__":
    pytest.main()
