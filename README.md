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

# Stage 5:Data Storage

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

# Stage 6: Data Preprocessing — Cleaning Strategy

## Functions
- `drop_missing(df, thresh=None)`: Drop rows with <70% non-missing by default (configurable via `thresh`).
- `fill_missing_median(df, cols=None)`: Median-impute numeric columns.
- `normalize_data(df, cols=None)`: Min–max normalize numeric columns to [0,1].

## Pipeline
1. Load raw CSV from `data/raw/`.
2. `drop_missing` → `fill_missing_median` → `normalize_data`.
3. Save cleaned dataset to `data/processed/` as timestamped CSV (and Parquet if available).

## Assumptions & Notes
- Operates on numeric columns; categoricals/text are left unchanged.
- Parquet export is optional (`pyarrow` or `fastparquet` recommended).
- Reproducible, function-based pipeline; all paths managed under `data/`.
