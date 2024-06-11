import snowflake.core._internal.telemetry


def pytest_configure(config):
    snowflake.core._internal.telemetry._called_from_test = True
