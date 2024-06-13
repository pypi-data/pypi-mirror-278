from decorator import skaff_telemetry


@skaff_telemetry(
    accelerator_name="test_python",
    version_number="0.0.1",
    project_name="xxx",
)
def example_func():
    print("hello")


example_func()
