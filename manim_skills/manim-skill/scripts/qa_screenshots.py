#!/usr/bin/env python3
"""
qa_screenshots.py
-----------------
Extract QA frames from a rendered Manim video.
Run after every render iteration.

Usage:
    python scripts/qa_screenshots.py <video_path> [--extra-times 3.5,7.2]

Output:
    qa_frames/ directory with labeled PNG files
    qa_report.txt with basic metadata
"""

import subprocess
import sys
import os
import argparse
from pathlib import Path


def get_duration(video_path: str) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", video_path],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())


def extract_frame(video_path: str, timestamp: float, output_path: str):
    subprocess.run(
        ["ffmpeg", "-ss", str(timestamp), "-i", video_path,
         "-vframes", "1", output_path, "-y"],
        capture_output=True
    )


def run_qa(video_path: str, extra_times: list[float] = None):
    if not os.path.exists(video_path):
        print(f"ERROR: Video not found at {video_path}")
        sys.exit(1)

    output_dir = Path("qa_frames")
    output_dir.mkdir(exist_ok=True)

    duration = get_duration(video_path)
    print(f"Video duration: {duration:.2f}s")

    # Standard 5-point QA timestamps
    pcts = [0, 25, 50, 75, 100]
    timestamps = [duration * p / 100 for p in pcts]

    # Add extra timestamps if requested
    if extra_times:
        for t in extra_times:
            if 0 <= t <= duration:
                timestamps.append(t)

    timestamps = sorted(set(timestamps))

    extracted = []
    for ts in timestamps:
        label = f"{ts:.1f}s"
        out = str(output_dir / f"frame_{label.replace('.', '_')}.png")
        extract_frame(video_path, ts, out)
        extracted.append((label, out))
        print(f"  Extracted frame at {label} → {out}")

    # Write QA report
    report_path = "qa_report.txt"
    with open(report_path, "w") as f:
        f.write(f"QA Report\n")
        f.write(f"Video: {video_path}\n")
        f.write(f"Duration: {duration:.2f}s\n")
        f.write(f"Frames extracted: {len(extracted)}\n\n")
        f.write("INSPECTION CHECKLIST\n")
        f.write("=" * 40 + "\n")
        checklist = [
            "LAYOUT: No object outside safe zone x∈[-6.5,6.5] y∈[-3.6,3.6]",
            "LAYOUT: No two objects overlapping",
            "LAYOUT: Frame occupancy 50-75% (not empty, not cluttered)",
            "LAYOUT: One clear primary focus per frame",
            "READABILITY: All text ≥32px equivalent",
            "READABILITY: Sufficient contrast vs background",
            "READABILITY: Equations render correctly",
            "READABILITY: Labels don't overlap what they label",
            "NARRATIVE: Visual matches expected narration moment",
            "NARRATIVE: No concept shown before introduced",
            "NARRATIVE: Scene order matches transcript",
            "COLOR: PALETTE used consistently",
            "COLOR: Same color = same semantic meaning throughout",
            "AESTHETICS: Visual hierarchy clear per frame",
            "AESTHETICS: No decoration-only animations",
            "AESTHETICS: Transitions feel smooth",
        ]
        for item in checklist:
            f.write(f"  [ ] {item}\n")
        f.write("\nFAILURES DETECTED:\n")
        f.write("  (fill in manually after inspection)\n")

    print(f"\nQA report written to {report_path}")
    print(f"Open qa_frames/ to inspect extracted frames.")
    print(f"Fill out checklist in {report_path} before proceeding.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract QA frames from Manim video")
    parser.add_argument("video_path", help="Path to rendered .mp4 file")
    parser.add_argument("--extra-times", help="Comma-separated extra timestamps in seconds",
                        default="")
    args = parser.parse_args()

    extra = []
    if args.extra_times:
        extra = [float(t) for t in args.extra_times.split(",")]

    run_qa(args.video_path, extra)
