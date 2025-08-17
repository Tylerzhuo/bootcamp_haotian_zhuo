# bootcamp_haotian_zhuo
## Folder Structure
- **homework/** → All homework contributions will be submitted here.
- **project/** → All project contributions will be submitted here.
- **class_materials/** → Local storage for class materials. Never pushed to
GitHub.

## Homework Folder Rules
- Each homework will be in its own subfolder (`homework0`, `homework1`, etc.)
- Include all required files for grading.
## Project Folder Rules
- Keep project files organized and clearly named.

# Data Storage

## Directory Structure

* **`data/raw/`**
  Stores raw, unmodified data in CSV format.

* **`data/processed/`**
  Stores cleaned and structured data in Parquet format for efficient reloading and downstream usage.

* **Environment-driven paths**
  Both directories are configurable via environment variables (e.g., `DATA_RAW_PATH`, `DATA_PROCESSED_PATH`), making the workflow portable across different machines.

## File Naming

* All data files are saved with **timestamped filenames** (e.g., `dataset_2025-08-16_1200.csv`).
* This enables reproducibility and traceability of intermediate artifacts.

## Supported Formats

* **CSV**: Human-readable, widely supported, but less efficient for large-scale analytics.
* **Parquet**: Optimized for analytics workloads, preserves schema and dtypes, and provides faster I/O.
* If the Parquet engine is missing, the system falls back gracefully and notifies the user.

## Utility Functions

* `detect_format(path)`: Infers storage format based on file suffix.
* `write_df(df, path)`: Saves a DataFrame to CSV or Parquet, automatically creating parent directories.
* `read_df(path)`: Loads data back, with user-friendly errors for unsupported formats.

These abstractions reduce boilerplate and enforce consistent data handling.

## Validation Checks

* **Shape Consistency**: Reloaded DataFrame must match original dimensions.
* **Key Dtypes**: Critical columns are checked for dtype consistency between saved and reloaded versions.
* **Error Handling**:

  * Fallback if Parquet engine is unavailable.
  * Informative messages if unsupported suffixes are encountered.

## Assumptions

* Environment variables for data paths are correctly set.
* User has basic familiarity with pandas DataFrames.
* Data volume fits comfortably in memory for this project stage.
