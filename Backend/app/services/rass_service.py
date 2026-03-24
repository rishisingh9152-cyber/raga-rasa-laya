from app.models.rass_model.predict import predict


class RassService:

    @staticmethod
    def classify_song(file_path: str):

        try:
            result = predict(file_path)

            print("🔥 RASS RAW OUTPUT:", result)

            # ----------------------------
            # ✅ EXPECTED: tuple output
            # (rass, prediction, confidence)
            # ----------------------------
            if isinstance(result, (list, tuple)):

                rass = result[0] if len(result) > 0 else "unknown"
                prediction = result[1] if len(result) > 1 else []
                confidence = result[2] if len(result) > 2 else 0

                return {
                    "rass": rass,
                    "prediction": prediction,
                    "confidence": confidence
                }

            # ----------------------------
            # ✅ DICT FORMAT (fallback)
            # ----------------------------
            elif isinstance(result, dict):

                return {
                    "rass": result.get("rass", "unknown"),
                    "prediction": result.get("prediction", []),
                    "confidence": result.get("confidence", 0),
                    "message": result.get("error", "")
                }

            # ----------------------------
            # ❌ UNKNOWN FORMAT
            # ----------------------------
            else:
                return {
                    "rass": "unknown",
                    "prediction": [],
                    "confidence": 0,
                    "message": "Invalid model output"
                }

        except Exception as e:
            return {
                "rass": "unknown",
                "prediction": [],
                "confidence": 0,
                "message": str(e)
            }