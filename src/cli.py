from time import sleep
import typer
from src.trials_runner import TrailsRunner, TrailsRunnerParameters
from src.utils.helper import read_yaml_file

        

app = typer.Typer()

@app.callback()
def main() -> None:
    """easier-poc CLI.

    Proof-of-Concept for the Easier Gates Projects
    """
    print("Welcome to the search-algorithms CLI")

@app.command()
def run():
    """Run the search-algorithms."""
    configs = read_yaml_file("src/config.yaml")
    print(configs)
    parameters = TrailsRunnerParameters(**configs)

    trails_runner = TrailsRunner(parameters)
    sleep(5)
    trails_runner.run()

