import time

import lseg.data as ld
import pandas as pd
from pandas._libs import OutOfBoundsDatetime

ric_list = list(pd.read_csv("./rics.csv")["RIC"])
fields = ["TR.PriceClose"]
start_date = "2019-09-01"
end_date = "2020-09-01"
interval = "daily"

output_path = "close_prices_new.csv"

batch_size = 20  # RICs per request — smaller batches time out far less
max_retries = 5  # retry attempts per batch on timeout/transient errors
retry_backoff = 10  # seconds, multiplied by attempt number (5s, 10s, 15s...)
pause_between_batches = 5  # seconds, to avoid hammering the backend / rate limits

print(ric_list)


def chunk(seq, size):
    for i in range(0, len(seq), size):
        yield seq[i : i + size]


def get_history_with_retry(universe_chunk):
    """Call get_history for one chunk of RICs, retrying on timeout/transient errors."""
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            return ld.get_history(
                universe=universe_chunk,
                fields=fields,
                start=start_date,
                end=end_date,
                interval=interval,
            )
        except Exception as exc:  # lseg.data raises LDError / requests-style timeouts
            last_error = exc
            wait = retry_backoff * attempt
            print(
                f"  Attempt {attempt}/{max_retries} failed for {universe_chunk}: {exc}"
            )
            if attempt < max_retries:
                print(f"  Retrying in {wait}s...")
                time.sleep(wait)
    print(f"  Giving up on chunk {universe_chunk} after {max_retries} attempts.")
    raise last_error


def download(output=output_path):
    all_frames = []

    with ld.open_session():  # uses your default session config
        for batch in chunk(ric_list, batch_size):
            print(f"Fetching {len(batch)} RICs: {batch}")
            try:
                df_chunk = get_history_with_retry(batch)
            except Exception as exc:
                print(f"  Skipping chunk after repeated failures: {exc}")
                continue

            if df_chunk is not None and not df_chunk.empty:
                all_frames.append(df_chunk)

            time.sleep(pause_between_batches)

    if not all_frames:
        raise RuntimeError(
            "No data returned for any RIC — check your RIC list, date range, and session."
        )

    # get_history returns a wide dataframe indexed by date, with one column
    # per RIC (or a MultiIndex of RIC/field if you request several fields).
    # Combine all successful batches side by side, aligned on the date index.
    df = pd.concat(all_frames, axis=1)
    df = df.reset_index().rename(columns={"index": "Date"})

    df.to_csv(output, index=False)
    print(f"Saved {df.shape[0]} rows x {df.shape[1]} columns to {output}")


# use as a standalone script or as a module as well
if __name__ == "__main__":
    download()
