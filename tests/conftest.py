import hypothesis

hypothesis.settings.register_profile(
    name='ci',
    settings=hypothesis.settings(
        max_examples=1000,
        perform_health_check=False,
    ),
)
