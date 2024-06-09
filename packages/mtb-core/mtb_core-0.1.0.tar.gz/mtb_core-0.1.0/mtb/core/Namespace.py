class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getattr__(self, name):
        return self.__dict__.get(name, None)

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __repr__(self) -> str:
        return f"Namespace({self.__dict__})"

    def merge(self, other):
        """
        Returns a new Namespace instance that merges attributes from this
        namespace and another, with values from the other namespace taking
        precedence over those from this namespace if keys overlap.

        Args:
        - other (Namespace): The other namespace to merge with this one.

        Returns
        -------
        - Namespace: A new namespace with merged attributes.
        """
        # Create a new namespace with the current attributes
        merged = Namespace(**self.__dict__)

        # Update the new namespace with attributes from the other namespace
        for key, value in other.__dict__.items():
            setattr(merged, key, value)

        return merged
