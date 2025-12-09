import argparse
import csv
import re
import sys
from pathlib import Path
from typing import List, Sequence

try:
    import PyPDF2
except ImportError:
    print("ERROR: PyPDF2 not installed. Activate your venv and run: pip install PyPDF2", file=sys.stderr)
    sys.exit(1)


# --------------------------
# Extraction helpers
# --------------------------
def extract_text_from_pdf(pdf_path: Path) -> str:
    with pdf_path.open('rb') as f:
        reader = PyPDF2.PdfReader(f)
        texts: List[str] = []
        for page in reader.pages:
            try:
                txt = page.extract_text() or ""
            except Exception:
                txt = ""
            texts.append(txt)
        return "\n".join(texts)


# --------------------------
# Cleaning helpers
# --------------------------
COMMON_FIXES = {
    r"Micr osoft": "Microsoft",
    r"Azur e": "Azure",
    r"resour ce": "resource",
    r"Resour ce": "Resource",
    r"subscr iption": "subscription",
    r"Subscr iption": "Subscription",
    r"Administr ator": "Administrator",
    r"configur e": "configure",
    r"deplo y": "deploy",
    r"envir onment": "environment",
    r"manag e": "manage",
    r"identit ies": "identities",
    r"Identit ies": "Identities",
}


def clean_text(content: str) -> str:
    text = content.replace("\r", "").replace("\u00a0", " ")
    for pattern, replacement in COMMON_FIXES.items():
        text = re.sub(pattern, replacement, text)

    text = re.sub(r"[ \t]+", " ", text)  # collapse runs of spaces
    text = re.sub(r"\n{3,}", "\n\n", text)  # collapse excess blank lines
    text = re.sub(r" ?([,:;.!?])", r"\1", text)  # trim space before punctuation
    return text.strip()


def clean_file(in_path: Path, out_path: Path) -> None:
    raw = in_path.read_text()
    cleaned = clean_text(raw)
    out_path.write_text(cleaned)


# --------------------------
# Parsing helpers (best effort for Tutorial Dojo / Whizlabs dumps)
# --------------------------
QUESTION_SPLIT = re.compile(r"\n(\d+)\.\s+QUESTION", re.IGNORECASE)


def split_questions(text: str) -> List[tuple[int, str]]:
    positions = list(QUESTION_SPLIT.finditer(text))
    results: List[tuple[int, str]] = []
    for idx, match in enumerate(positions):
        start = match.start()
        end = positions[idx + 1].start() if idx + 1 < len(positions) else len(text)
        block = text[start:end].strip()
        try:
            number = int(match.group(1))
        except ValueError:
            number = idx + 1
        results.append((number, block))
    return results


OPTION_RE = re.compile(r"^[A-E][).]", re.IGNORECASE)


def extract_fields(block: str) -> dict:
    category_match = re.search(r"Categor\s*y:\s*(.+)", block, re.IGNORECASE)
    category = category_match.group(1).strip() if category_match else ""

    lines = block.splitlines()
    options: List[str] = []
    option_start = None
    for i, line in enumerate(lines):
        if OPTION_RE.match(line.strip()):
            option_start = i
            break
    question_text = ""
    if option_start is not None:
        question_text = " ".join(l.strip() for l in lines[:option_start] if l.strip())
        for line in lines[option_start:]:
            if OPTION_RE.match(line.strip()):
                options.append(line.strip())
    else:
        question_text = " ".join(l.strip() for l in lines if l.strip())

    answer = ""
    answer_match = re.search(r"Correct Answer[s]*:\s*(.+)", block, re.IGNORECASE)
    if answer_match:
        answer = answer_match.group(1).strip()
    else:
        inline = re.search(r"Correct\s*[:\-]\s*(.+)", block, re.IGNORECASE)
        answer = inline.group(1).strip() if inline else ""

    explanation = ""
    exp_match = re.search(r"Explanation:\s*(.+)", block, re.IGNORECASE | re.DOTALL)
    if exp_match:
        explanation = exp_match.group(1).strip()

    return {
        "category": category,
        "question": question_text,
        "options": " | ".join(options),
        "answer": answer,
        "explanation": explanation,
        "raw": block,
    }


def parse_to_csv(in_path: Path, out_path: Path) -> None:
    text = in_path.read_text()
    questions = split_questions(text)
    with out_path.open("w", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["number", "category", "question", "options", "answer", "explanation", "raw"],
        )
        writer.writeheader()
        for number, block in questions:
            fields = extract_fields(block)
            writer.writerow({"number": number, **fields})


# --------------------------
# CLI
# --------------------------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract, clean, and parse Whizlabs / Tutorials Dojo PDF or text dumps."
    )
    sub = parser.add_subparsers(dest="cmd")

    pdf_cmd = sub.add_parser("pdf", help="Extract text from PDF(s)")
    pdf_cmd.add_argument("pdfs", nargs="+", help="PDF file(s) to extract")
    pdf_cmd.add_argument("--out-dir", type=Path, help="Optional output directory for .txt")

    clean_cmd = sub.add_parser("clean", help="Clean spacing/artifacts in a text file")
    clean_cmd.add_argument("input", type=Path, help="Input text file")
    clean_cmd.add_argument("--output", type=Path, help="Output text file (default: <input>.clean.txt)")

    parse_cmd = sub.add_parser("parse", help="Parse cleaned text into CSV (best effort)")
    parse_cmd.add_argument("input", type=Path, help="Input text file (cleaned preferred)")
    parse_cmd.add_argument("--output", type=Path, help="Output CSV file (default: <input>.csv)")

    return parser


def run_pdf(args: argparse.Namespace) -> None:
    out_dir: Path | None = args.out_dir
    for pdf in args.pdfs:
        p = Path(pdf)
        if not p.exists():
            print(f"WARN: File not found: {p}", file=sys.stderr)
            continue
        text = extract_text_from_pdf(p)
        target = (out_dir / p.name).with_suffix(".txt") if out_dir else p.with_suffix(".txt")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
        print(f"Extracted: {p.name} -> {target}")


def run_clean(args: argparse.Namespace) -> Path:
    in_path: Path = args.input
    out_path: Path = args.output or in_path.with_suffix(".clean.txt")
    clean_file(in_path, out_path)
    print(f"Cleaned: {in_path} -> {out_path}")
    return out_path


def run_parse(args: argparse.Namespace) -> None:
    in_path: Path = args.input
    out_path: Path = args.output or in_path.with_suffix(".csv")
    parse_to_csv(in_path, out_path)
    print(f"Parsed questions -> {out_path}")


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    # Backward compatibility: if no subcommand and first arg looks like a PDF, treat as pdf extraction.
    if args.cmd is None and len(sys.argv) > 1 and sys.argv[1].lower().endswith(".pdf"):
        args.cmd = "pdf"
        args.pdfs = sys.argv[1:]
        args.out_dir = None

    if args.cmd == "pdf":
        run_pdf(args)
    elif args.cmd == "clean":
        run_clean(args)
    elif args.cmd == "parse":
        run_parse(args)
    else:
        parser.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()