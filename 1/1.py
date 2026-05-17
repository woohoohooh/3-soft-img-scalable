# detect_bpm.py
# Usage: python detect_bpm.py
# Scans all .wav files in current directory, prints BPM and writes bpm_results.csv

import os
import librosa
import numpy as np
import pandas as pd

def estimate_bpm(path):
    y, sr = librosa.load(path, sr=None, mono=True)
    # Pre-filter: trim leading/trailing silence to improve detection
    y, _ = librosa.effects.trim(y, top_db=30)
    # Use tempo estimation (returns array of tempi for different windows)
    # aggregate by median to reduce outliers
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    if onset_env.sum() < 1e-6:
        return None
    tempi = librosa.beat.tempo(onset_envelope=onset_env, sr=sr, aggregate=None)
    if len(tempi) == 0:
        return None
    bpm_median = float(np.median(tempi))
    # Round to nearest integer (common practice)
    bpm_rounded = int(round(bpm_median))
    return bpm_rounded, float(bpm_median)

def main():
    files = [f for f in os.listdir('.') if f.lower().endswith('.wav')]
    results = []
    for f in files:
        try:
            est = estimate_bpm(f)
            if est is None:
                print(f"{f}: BPM not detected")
                results.append({'file': f, 'bpm_rounded': '', 'bpm_raw': '', 'note': 'no onsets'})
            else:
                bpm_rounded, bpm_raw = est
                print(f"{f}: {bpm_rounded} BPM (raw {bpm_raw:.2f})")
                results.append({'file': f, 'bpm_rounded': bpm_rounded, 'bpm_raw': round(bpm_raw,2), 'note': ''})
        except Exception as e:
            print(f"{f}: error {e}")
            results.append({'file': f, 'bpm_rounded': '', 'bpm_raw': '', 'note': f'error: {e}'})
    if results:
        df = pd.DataFrame(results)
        df.to_csv('bpm_results.csv', index=False)
        print("Saved bpm_results.csv")

if __name__ == '__main__':
    main()
