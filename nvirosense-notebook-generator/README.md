# nvirosense-notebook-generator

## Project Overview
The nvirosense-notebook-generator is a project designed to facilitate the analysis and processing of environmental sensor data. It includes various modules for managing device information, handling environment configurations, and processing readings from different sensors.

## Project Structure
- **src/**: Contains the core functionality of the project.
  - **devices.py**: Functions for loading and managing device information.
  - **env.py**: Manages environment variables and configurations.
  - **readings.py**: Functions for importing, exporting, and processing readings.
  - **utils.py**: Utility functions for data manipulation and formatting.

- **data/**: Contains data files used by the project.
  - **devices.json**: A JSON file listing devices with their identifiers, names, groups, and departments.

- **notebooks/**: Contains Jupyter notebooks for data analysis.
  - **willow_creek_weather.ipynb**: Analysis and processing for the "Willow Creek Weather" device.
  - **aquanet_light_sensor.ipynb**: Analysis and processing for the "Aquanet Light Sensor" device.
  - **aquanet_temp_rh.ipynb**: Analysis and processing for the "AquaNet Temp & RH" device.
  - **aquanet_wind.ipynb**: Analysis and processing for the "AquaNet Wind" device.

- **requirements.txt**: Lists the dependencies required for the project.

## Setup Instructions
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies using:
   ```
   pip install -r requirements.txt
   ```

## Usage Guidelines
- Each notebook in the `notebooks/` directory is designed to analyze data from a specific device. Open the desired notebook in Jupyter Notebook or JupyterLab to run the analysis.
- Ensure that the `data/devices.json` file is correctly populated with device information before running the notebooks.

## Notebooks Functionality
- **Willow Creek Weather**: Analyzes weather data from the Willow Creek device, including time difference calculations and data export.
- **Aquanet Light Sensor**: Replicates the analysis for the Aquanet Light Sensor device.
- **AquaNet Temp & RH**: Replicates the analysis for the AquaNet Temperature and Relative Humidity device.
- **AquaNet Wind**: Replicates the analysis for the AquaNet Wind device.

## Contribution
Contributions to the project are welcome. Please submit a pull request or open an issue for any enhancements or bug fixes.