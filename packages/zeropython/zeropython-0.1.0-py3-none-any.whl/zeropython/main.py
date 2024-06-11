import pathlib

import typer

import zeropython.ast_cleaner
import zeropython.ast_detector
import zeropython.report

app = typer.Typer(pretty_exceptions_enable=False)


@app.command()
def main(file: pathlib.Path):
    report = zeropython.report.Report()
    try:
        cleaned_code, report = zeropython.ast_detector.ast_detect(
            file.read_text(encoding="utf-8"), report
        )
    except UnicodeDecodeError as e:
        raise ValueError(f"{file.stem} is not a valid python file") from e
    print(report)


if __name__ == "__main__":
    app()
