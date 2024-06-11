# (c) 2022 DTU Wind Energy
"""
Package for validation of xarray objects
"""

from functools import wraps

from ._errors import WindClimateValidationError


def create_validator(req_vars_dict, req_dims, req_coords, checks_iterator=None):
    """
    Factory to build validation functions for xarray datasets.
    """

    def validator(wc_obj):
        errors = []
        # find missing attributes
        found_attr = []
        for attr in req_vars_dict.keys():
            if attr not in wc_obj.data_vars:
                errors.append(f"{len(errors)+1}. Missing variable: {attr}")
            else:
                found_attr.append(attr)

        # find missing dimensions
        for dim in req_dims:
            if dim not in wc_obj.dims:
                errors.append(f"{len(errors)+1}. Missing dimension: {dim}")

        # find missing coordinates
        for coord in req_coords:
            if coord not in wc_obj.coords:
                errors.append(f"{len(errors)+1}. Missing coordinate: {coord}")

        # find missing coordinates on the existing attributes
        for val in found_attr:
            for x in req_vars_dict[val]:
                if x not in wc_obj[val].dims:
                    errors.append(
                        f"{len(errors)+1}. Missing coordinate {x} on variable: {val}"
                    )

        # run extra checks
        if checks_iterator is not None:
            for f in checks_iterator:
                err_msg = f(wc_obj)
                if err_msg is not None:
                    if isinstance(err_msg, str):
                        errors.append(f"{len(errors)+1}. {err_msg}")
                    else:
                        for val in err_msg:
                            errors.append(f"{len(errors)+1}. {val}")
        if errors:
            raise WindClimateValidationError(
                f"validate found {len(errors)} errors \n" + "\n".join(errors)
            )

    def validator_wrapper(func):
        """
        Validation function for the gwc data format.

        Parameters
        ----------
        func: function
            The function that should first validate the object

        Returns
        -------
        function
            A function that first validates the dataset and then calls the initial
            function.
        """

        @wraps(func)
        def validate(*args, **kwargs):
            obj = args[0]

            # Do bwc checks
            validator(obj)  # Raises ValueError if errors exist

            result = func(*args, **kwargs)
            return result

        return validate

    return validator, validator_wrapper
