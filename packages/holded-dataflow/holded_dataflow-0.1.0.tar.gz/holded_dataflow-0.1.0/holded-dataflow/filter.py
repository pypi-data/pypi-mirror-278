import holded_dataflow


def is_blacklisted(name: str, filter_type: str) -> bool:
    """
    Check if an event is blacklisted.

    Parameters:
    - name: Name of the event to check.
    - filter_type: Type of the filter to apply. Valid values are "PIPELINE" or "SSGTM".

    Returns:
    - True if the event is blacklisted for the specified filter type, False otherwise.
    """
    # Function implementation remains the same
    return holded_dataflow.is_blacklisted(name, filter_type)
