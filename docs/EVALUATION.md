# Evaluation

AiDetection is intentionally evaluation-first. A detector should not be described as universally accurate without a held-out benchmark.

## Dataset manifest

Create a CSV with these columns:

```text
path,label,modality,source,generator,compression
samples/real.jpg,real,image,camera,none,original
samples/synthetic.jpg,synthetic,image,generator-name,model-family,jpeg
```

Keep private or licensed media outside the repository. Do not commit sensitive uploads or copyrighted datasets without permission.

## Metrics

For binary labels, report:
- precision, recall, F1
- ROC-AUC and PR-AUC where probabilities are available
- false-positive rate and false-negative rate
- calibration/error by confidence bucket
- performance by modality
- performance by generator/source
- robustness after resizing, recompression, transcoding, and common edits

## Reproducibility

Record:
- detector model ID and revision
- package/runtime versions
- dataset version or immutable manifest hash
- preprocessing settings
- decision threshold
- random seed where applicable

Never tune a threshold on the same held-out set used for the final score.

## Interpretation

A benchmark measures performance on its evaluation population. It does not establish authorship or provenance for an individual file. Report uncertainty, dataset limitations, and failure cases alongside aggregate metrics.
