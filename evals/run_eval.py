"""Evaluates PII detection against the gold dataset: precision/recall/F1 per
entity type (exact text match, case-insensitive). No API calls — the NER model
runs locally."""

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from dataset import EXAMPLES  # noqa: E402

from pii_redaction.redactor import detect  # noqa: E402

EVALS_DIR = Path(__file__).parent


def normalize(label: str, text: str) -> tuple[str, str]:
    return label, text.strip().lower()


def evaluate() -> dict:
    counts = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0})

    for example in EXAMPLES:
        gold = {normalize(label, text) for label, text in example["gold"]}
        spans = detect(example["text"])
        predicted = {normalize(s.label, s.text) for s in spans}

        for label, text in predicted:
            if (label, text) in gold:
                counts[label]["tp"] += 1
            else:
                counts[label]["fp"] += 1
        for label, text in gold:
            if (label, text) not in predicted:
                counts[label]["fn"] += 1

    results = {}
    total_tp = total_fp = total_fn = 0
    for label, c in counts.items():
        tp, fp, fn = c["tp"], c["fp"], c["fn"]
        total_tp += tp
        total_fp += fp
        total_fn += fn
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
        results[label] = {
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "tp": tp,
            "fp": fp,
            "fn": fn,
        }

    overall_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) else 0.0
    overall_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) else 0.0
    overall_f1 = (
        2 * overall_precision * overall_recall / (overall_precision + overall_recall)
        if (overall_precision + overall_recall)
        else 0.0
    )
    results["OVERALL"] = {
        "precision": overall_precision,
        "recall": overall_recall,
        "f1": overall_f1,
        "tp": total_tp,
        "fp": total_fp,
        "fn": total_fn,
    }
    return results


def write_report(results: dict) -> None:
    lines = ["# PII Detection Evaluation Results", ""]
    lines.append(f"{len(EXAMPLES)} synthetic sentences, exact-match scoring per entity.\n")
    lines.append("| Entity type | Precision | Recall | F1 | TP | FP | FN |")
    lines.append("|---|---|---|---|---|---|---|")
    for label in ["CPF", "CNPJ", "EMAIL", "TELEFONE", "CEP", "PESSOA", "OVERALL"]:
        if label not in results:
            continue
        r = results[label]
        lines.append(
            f"| {label} | {r['precision']:.1%} | {r['recall']:.1%} | {r['f1']:.1%} | "
            f"{r['tp']} | {r['fp']} | {r['fn']} |"
        )
    (EVALS_DIR / "results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    results = evaluate()
    (EVALS_DIR / "results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    write_report(results)
    print(json.dumps(results, indent=2, ensure_ascii=False))
