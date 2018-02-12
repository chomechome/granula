import hypothesis

hypothesis.settings.register_profile(
    name='exhaustive',
    settings=hypothesis.settings(
        max_examples=100,
        perform_health_check=False,
    ),
)
hypothesis.settings.register_profile(
    name='coverage',
    settings=hypothesis.settings(
        max_examples=10,
        perform_health_check=False,
    ),
)
