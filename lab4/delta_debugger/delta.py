import math

from typing import Tuple

from delta_debugger import run_target

EMPTY_STRING = b""


def delta_debug(target: str, input: bytes) -> bytes:
    """
    Delta-Debugging algorithm

    TODO: Implement your algorithm for delta-debugging.

    Hint: It may be helpful to use an auxilary function that
    takes as input a target, input string, n and
    returns the next input and n to try.

    :param target: target program
    :param input: crashing input to be minimized
    :return: 1-minimal crashing input.
    """

    # Split input into two items
    left_input = input[:math.ceil(len(input) / 2)]
    right_input = input[math.ceil(len(input) / 2):]

    # Run target with left input
    left_return_code = run_target(target, left_input)
    # Run target with right input
    right_return_code = run_target(target, right_input)

    # If left input crashes, return left input
    if left_return_code != 0:
        return delta_debug(target, left_input)
    # If right input crashes, return right input
    elif right_return_code != 0:
        return delta_debug(target, right_input)
    
    # If both inputs do not crash, go to phase 2
    return delta_debug_phase_2(target, input)

def delta_debug_phase_2(target: str, input: bytes) -> bytes:
    # Remove one character from input
    while True:
        errorlevel = 0
        for i in range(len(input)):
            # Remove character at index i
            new_input = input[:i] + input[i+1:]
            # Run target with new input
            new_return_code = run_target(target, new_input)
            # If target crashes, set input to new input and break
            if new_return_code != 0:
                input = new_input
                errorlevel = 1
                break
        if errorlevel == 0:
            break
    # If no input crashes, return input
    return input