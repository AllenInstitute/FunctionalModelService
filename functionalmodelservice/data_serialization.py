import pyarrow as pa
from flask import Response, request, send_file
from cloudfiles import compression
from io import BytesIO


def after_request(response):

    accept_encoding = request.headers.get("Accept-Encoding", "")

    if "gzip" not in accept_encoding.lower():
        return response

    response.direct_passthrough = False

    if (
        response.status_code < 200
        or response.status_code >= 300
        or "Content-Encoding" in response.headers
    ):
        return response

    response.data = compression.gzip_compress(response.data)

    response.headers["Content-Encoding"] = "gzip"
    response.headers["Vary"] = "Accept-Encoding"
    response.headers["Content-Length"] = len(response.data)

    return response


def add_warnings_to_headers(headers, warnings):
    if len(warnings) > 0:
        warnings = [w.replace("\n", " ") for w in warnings]
        headers["Warning"] = warnings
    return headers


def create_df_response(
    df,
    warnings,
    arrow_format=True,
):
    accept_encoding = request.headers.get("Accept-Encoding", "")
    headers = add_warnings_to_headers({}, warnings)

    if arrow_format:
        batch = pa.RecordBatch.from_pandas(df)
        sink = pa.BufferOutputStream()
        if "lz4" in accept_encoding:
            compression = "LZ4_FRAME"
        elif "zstd" in accept_encoding:
            compression = "ZSTD"
        else:
            compression = None
        opt = pa.ipc.IpcWriteOptions(compression=compression)
        with pa.ipc.new_stream(sink, batch.schema, options=opt) as writer:
            writer.write_batch(batch)
        response = send_file(BytesIO(sink.getvalue().to_pybytes()), "data.arrow")
        response.headers.update(headers)
        return after_request(response)
    else:
        dfjson = df.to_json(orient="records")
        response = Response(dfjson, headers=headers, mimetype="application/json")
        return after_request(response)
