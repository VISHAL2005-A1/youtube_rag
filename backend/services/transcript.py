import re


TAG_PATTERN = re.compile(r"<[^>]+>")
WHITESPACE_PATTERN = re.compile(r"\s+")


def parse_timestamp(timestamp: str) -> float:

    parts = timestamp.split(":")

    if len(parts) == 3:

        hours = float(parts[0])
        minutes = float(parts[1])
        seconds = float(parts[2])

        return hours * 3600 + minutes * 60 + seconds

    elif len(parts) == 2:

        minutes = float(parts[0])
        seconds = float(parts[1])

        return minutes * 60 + seconds

    raise ValueError(f"Invalid timestamp: {timestamp}")


def clean_text(text: str) -> str:

    text = TAG_PATTERN.sub("", text)

    text = WHITESPACE_PATTERN.sub(" ", text)

    return text.strip()


def parse_vtt(file_path: str):
    """
    Read VTT file line-by-line.

    Does NOT load the complete file into memory.

    Yields:
        {
            "text": "...",
            "start": 12.34
        }
    """

    current_timestamp = None
    current_text = []

    previous_text = ""

    with open(file_path, "r", encoding="utf-8") as file:

        for line in file:

            line = line.strip()

            # End of a VTT cue
            if not line:

                if current_timestamp and current_text:

                    text = clean_text(
                        " ".join(current_text)
                    )

                    if text and text != previous_text:

                        try:

                            start_seconds = parse_timestamp(
                                current_timestamp
                            )

                            yield {
                                "text": text,
                                "start": round(start_seconds, 3)
                            }

                            previous_text = text

                        except ValueError:
                            pass

                current_timestamp = None
                current_text = []

                continue

            # Header
            if line.startswith("WEBVTT"):
                continue

            # Notes
            if line.startswith("NOTE"):
                continue

            # Timestamp line
            if "-->" in line:

                current_timestamp = (
                    line
                    .split("-->")[0]
                    .strip()
                    .split()[0]
                )

                current_text = []

                continue

            # Cue number
            if line.isdigit():
                continue

            # Caption text
            if current_timestamp:

                current_text.append(line)

    # Handle last cue if file doesn't end with blank line
    if current_timestamp and current_text:

        text = clean_text(
            " ".join(current_text)
        )

        if text and text != previous_text:

            try:

                start_seconds = parse_timestamp(
                    current_timestamp
                )

                yield {
                    "text": text,
                    "start": round(start_seconds, 3)
                }

            except ValueError:
                pass


def create_chunks(
    transcript,
    video_id,
    video_title,
    playlist_id,
    chunk_size=700
):
    """
    Create chunks incrementally.

    `transcript` is a generator from parse_vtt().

    Yields one chunk at a time.
    """

    current_text = []
    current_start = None
    current_length = 0

    for item in transcript:

        text = item["text"].strip()

        if not text:
            continue

        if current_start is None:

            current_start = item["start"]

        current_text.append(text)

        current_length += len(text)

        if current_length >= chunk_size:

            yield {
                "text": " ".join(current_text),
                "video_id": video_id,
                "video_title": video_title,
                "playlist_id": playlist_id,
                "start_time": current_start
            }

            # Reset current chunk
            current_text = []
            current_start = None
            current_length = 0

    # Remaining text
    if current_text:

        yield {
            "text": " ".join(current_text),
            "video_id": video_id,
            "video_title": video_title,
            "playlist_id": playlist_id,
            "start_time": current_start
        }