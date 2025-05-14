import os
from PyQt6.QtWidgets import QFileDialog
from services.missing_service import MissingService
from funcs.def_bins import get_default_bin_count
import pandas as pd

class DataLoaderService:
    @staticmethod
    def select_file(window):
        path, _ = QFileDialog.getOpenFileName(
            window,
            'Select the File',
            '',
            'All Supported Files (*.txt *.csv *.xlsx *.xls);;'
            'Text Files (*.txt);;CSV Files (*.csv);;'
            'Excel Files (*.xlsx *.xls);;All Files (*)'
        )
        return path if path else None

    @staticmethod
    def load_data(path):
        try:
            file_extension = os.path.splitext(path)[1].lower()

            if file_extension in ['.xlsx', '.xls']:
                df = pd.read_excel(path)
            elif file_extension == '.csv':
                df = pd.read_csv(path, decimal=',')
            elif file_extension == '.txt':
                with open(path, 'r') as file:
                    lines = [line.strip().replace(',', '.') for line in file]
                    valid_data = []
                    for x in lines:
                        if not x:
                            continue
                        try:
                            if ',' in x:
                                x = x.split(',')[1]
                            valid_data.append(float(x))
                        except ValueError:
                            print(f"Skipping invalid value: {x}")
                    if not valid_data:
                        print("No valid data found in file")
                        return None
                    return pd.Series(valid_data)
            else:
                print(f"Unsupported file type: {file_extension}")
                return None

            if len(df.columns) > 1:
                df = df.iloc[:, -1]

            df = pd.to_numeric(df, errors='coerce')
            if df.empty:
                print("No valid numerical data found in file")
                return None

            return df

        except FileNotFoundError:
            print("File not found")
            return None
        except PermissionError:
            print("Permission denied when accessing file")
            return None
        except Exception as e:
            print(f"Error loading file: {str(e)}")
            return None

    @staticmethod
    def postprocess_loaded_data(window, data):
        missing_info = MissingService.detect_missing(data)
        has_missing = missing_info['total_missing'] > 0

        window.graph_panel.bins_spinbox.setEnabled(True)
        window.data_version_combo.setEnabled(True)

        window.standardize_button.setEnabled(not has_missing)
        window.log_button.setEnabled(not has_missing)
        window.shift_spinbox.setEnabled(not has_missing)
        window.shift_button.setEnabled(not has_missing)

        window.normal_anomaly_button.setEnabled(not has_missing)
        window.asymmetry_anomaly_button.setEnabled(not has_missing)
        window.confidence_anomaly_button.setEnabled(not has_missing)
        window.anomaly_gamma_spinbox.setEnabled(not has_missing)

        window.impute_mean_button.setEnabled(has_missing)
        window.impute_median_button.setEnabled(has_missing)
        window.interpolate_linear_button.setEnabled(has_missing)
        window.drop_missing_button.setEnabled(has_missing)

        window.data_version_controller.update_data_versions()
        window.missing_controller.update_data_reference(data)

        bin_count = get_default_bin_count(data)
        window.graph_panel.bins_spinbox.setValue(bin_count)

        if has_missing:
            window.show_info_message(
                "Missing Values Detected",
                f"Found {missing_info['total_missing']} missing values "
                f"({missing_info['missing_percentage']:.2f}%).\n"
                "Please handle missing values before performing data operations."
            )
            
            window.graph_panel.clear()
            window.graph_panel.data = None
            window.gof_tab.clear_tests()
            window.stat_controller.clear()
        else:
            window.graph_controller.set_data(window.data_model.series)
            window.stat_controller.update_statistics_table()
            window.gof_tab.evaluate_tests()

        window.state_controller.update_state_for_data(data)
        window.state_controller.update_transformation_label()
        window.state_controller.update_navigation_buttons()
