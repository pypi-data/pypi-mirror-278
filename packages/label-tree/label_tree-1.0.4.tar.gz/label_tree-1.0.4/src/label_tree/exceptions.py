class UnknownDisease(ValueError):
    """Exception raised when an unknown disease doesn't map to any tree node."""

    def __init__(
        self,
        unknown_disease,
        message="Unknown disease does not map to any tree node",
    ):
        self.unknown_disease = unknown_disease
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: {self.unknown_disease}"
