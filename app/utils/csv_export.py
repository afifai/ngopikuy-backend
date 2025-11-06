import io
import pandas as pd
from flask import Response

def df_to_csv_response(df: pd.DataFrame, filename: str) -> Response:
    csv_buf = io.StringIO()
    df.to_csv(csv_buf, index=False)
    csv_buf.seek(0)
    return Response(
        csv_buf.read(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
