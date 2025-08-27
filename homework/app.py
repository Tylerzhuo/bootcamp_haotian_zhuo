import io
import json
import pickle
import numpy as np
from typing import Dict, Any, List

from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

MODEL_PATH = "model/model.pkl"  # produced in Step 3


# ---------- Utilities ----------
def load_model_obj(path: str) -> Dict[str, Any]:
    with open(path, "rb") as f:
        return pickle.load(f)

def validate_and_build_array(payload: Dict[str, Any], feature_names: List[str]) -> np.ndarray:
    # check missing
    missing = [k for k in feature_names if k not in payload]
    if missing:
        raise ValueError(f"Missing features: {missing}")

    # build in correct order, type cast
    row = []
    for k in feature_names:
        v = payload[k]
        try:
            row.append(float(v))
        except Exception:
            raise ValueError(f"Feature '{k}' must be numeric, got: {type(v).__name__}")
    return np.array([row], dtype=float)


# ---------- Endpoints ----------
@app.route("/meta", methods=["GET"])
def meta():
    try:
        obj = load_model_obj(MODEL_PATH)
        meta = obj.get("metrics", {})
        out = {
            "ok": True,
            "feature_names": meta.get("feature_names", []),
            "metrics": {
                "mae": meta.get("mae", None),
                "r2": meta.get("r2", None),
                "rmse": meta.get("rmse", None),
                "n_train": meta.get("n_train", None),
                "n_test": meta.get("n_test", None),
            }
        }
        return jsonify(out)
    except FileNotFoundError:
        return jsonify({"ok": False, "error": "Model file not found."}), 500
    except Exception as e:
        return jsonify({"ok": False, "error": f"Unexpected error: {e}"}), 500


@app.route("/predict", methods=["POST"])
def predict():
    """
    POST /predict
    JSON body must contain all features listed in /meta.feature_names
    """
    try:
        obj = load_model_obj(MODEL_PATH)
        feature_names = obj["metrics"]["feature_names"]
        pipe = obj["pipeline"]

        if not request.is_json:
            return jsonify({"ok": False, "error": "Request must be application/json"}), 415
        payload = request.get_json(force=True)

        # optional: reject unknown keys to avoid silent mistakes
        unknown = [k for k in payload.keys() if k not in feature_names]
        if unknown:
            return jsonify({"ok": False, "error": f"Unknown feature keys: {unknown}"}), 400

        X = validate_and_build_array(payload, feature_names)
        yhat = float(pipe.predict(X)[0])
        return jsonify({"ok": True, "prediction": yhat, "features": payload})
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    except FileNotFoundError:
        return jsonify({"ok": False, "error": "Model file not found."}), 500
    except Exception as e:
        return jsonify({"ok": False, "error": f"Unexpected error: {e}"}), 500


@app.route("/predict/<float:x>", methods=["GET"])
def predict_one(x: float):
    """
    GET /predict/<x>
    Convenience route: fills the first feature with x and others as 0.0
    """
    try:
        obj = load_model_obj(MODEL_PATH)
        feature_names = obj["metrics"]["feature_names"]
        pipe = obj["pipeline"]
        if len(feature_names) == 0:
            return jsonify({"ok": False, "error": "Model feature list is empty."}), 500

        payload = {feature_names[0]: float(x)}
        for k in feature_names[1:]:
            payload[k] = 0.0

        X = validate_and_build_array(payload, feature_names)
        yhat = float(pipe.predict(X)[0])
        return jsonify({"ok": True, "prediction": yhat, "features": payload})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/predict/<float:x>/<float:y>", methods=["GET"])
def predict_two(x: float, y: float):
    """
    GET /predict/<x>/<y>
    Convenience route: fills first two features, others as 0.0
    """
    try:
        obj = load_model_obj(MODEL_PATH)
        feature_names = obj["metrics"]["feature_names"]
        pipe = obj["pipeline"]
        if len(feature_names) < 2:
            return jsonify({"ok": False, "error": "Model expects at least 2 features."}), 400

        payload = {feature_names[0]: float(x), feature_names[1]: float(y)}
        for k in feature_names[2:]:
            payload[k] = 0.0

        X = validate_and_build_array(payload, feature_names)
        yhat = float(pipe.predict(X)[0])
        return jsonify({"ok": True, "prediction": yhat, "features": payload})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/plot", methods=["GET"])
def plot_png():
    """Return a simple PNG image, to satisfy 'return a chart or image' requirement."""
    try:
        import matplotlib.pyplot as plt

        xs = np.linspace(-3, 3, 200)
        ys = xs ** 2
        fig, ax = plt.subplots()
        ax.plot(xs, ys, label="y=x^2")
        ax.axhline(0, linestyle="--", linewidth=1)
        ax.set_title("Sample Plot")
        ax.legend()

        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        return send_file(buf, mimetype="image/png", download_name="plot.png")
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.errorhandler(404)
def not_found(_e):
    return jsonify({"ok": False, "error": "Route not found."}), 404


if __name__ == "__main__":
    # For local development only
    app.run(host="0.0.0.0", port=8000, debug=True)
