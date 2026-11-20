# Online Shopper Purchase Prediction

Streamlit frontend for the frontend milestone. It runs independently of the backend.

## Run

On Windows, extract the ZIP directly into the desired project folder and double-click `Start-Shop.cmd`. The first run creates a virtual environment and installs the dependencies.

To start manually from the same folder:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open http://localhost:8501 if Streamlit does not open it automatically.

## Demo

- **Overview** links to the two workflows.
- **Data Explorer** starts with 12 fictional sessions. Download and extract the [UCI dataset](https://archive.ics.uci.edu/dataset/468/online), then upload `online_shoppers_intention.csv` to explore the actual sessions. The explorer requires `VisitorType`, `Weekend`, and `Revenue`.
- **Prediction** previews four inputs using UCI column names. The page shows a pending state for model output. Agree on the final feature set with the model team before connecting the API.

To integrate with the full template later, place these files in its `frontend` folder. The original API client and secondary views remain available for the backend milestone.
