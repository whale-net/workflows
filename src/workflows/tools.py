import typer

app = typer.Typer()


@app.command()
def update_helm_chart_version(commit_count: int):
    # crude but it'll do
    file_lines: list[str] = []
    with open("./charts/workflow-templates/Chart.yaml", "r") as chart:
        while True:
            line = chart.readline()
            if not line:
                break
            elif line.startswith("version:"):
                file_lines.append(f"version: 0.2.{commit_count}\n")
            else:
                file_lines.append(line)

    with open("./charts/workflow-templates/Chart.yaml", "w") as chart:
        chart.writelines(file_lines)
