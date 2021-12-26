from lib.utils import find_patterns
from lib.lookups import handle_match, update_lookup_table_with_mock
import logging

logger = logging.getLogger("Ox4Shell")

DEFAULT_MAX_DEPTH = 150


def deobfuscate_patterns(payload: str) -> str:
    pattern = next(find_patterns(payload), None)
    logger.debug(f"Got deobfuscation pattern - {pattern}")

    # if no pattern was found, just return the original payload
    if not pattern:
        logger.debug(f"Pattern is empty, returning original payload")
        return payload

    # if we found a pattern, call the handle match function
    full_match, inner_group = pattern

    logger.debug(f"Found full text to replace: {full_match=}")
    logger.debug(f"Found text to lookup by: {inner_group=}")

    payload = handle_match(full_match, inner_group, payload)
    return payload


def deobfuscate(payload: str, max_depth: int = DEFAULT_MAX_DEPTH) -> str:
    update_lookup_table_with_mock()

    for i in range(max_depth):
        logger.debug(f"Entering iteration #{i}")
        logger.debug(f"Trying to deobfuscate {payload}")

        deobfuscated = deobfuscate_patterns(payload)
        logger.debug(f"Deobfuscated result is: {deobfuscated}")

        if deobfuscated == payload:
            logger.debug("Payload equals deobfuscated, exiting loop")
            return deobfuscated

        payload = deobfuscated

    raise Exception(f"deobfuscate exceeded max depth of {max_depth}")
