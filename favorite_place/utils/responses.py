from favorite_place.schemas import errors


def get_responses(*args: errors.BaseError) -> dict:
    responses = {}
    for arg in args:
        responses.update(arg.to_responses())
    return responses
