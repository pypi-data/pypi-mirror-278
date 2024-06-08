# type: ignore

from profitpulse.testrig.scenario import CLIScenario

cli = "cli"


def scenario_for(_, *args, **kwargs):
    """
    Factory for distinct scenario backends.
    """

    return CLIScenario(*args, **kwargs)
