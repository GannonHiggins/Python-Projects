


def roman_to_int(s):
    # Mapping of Roman numerals to their integer values
    roman_map = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }

    # Result integer
    total = 0
    # Value of the previous Roman digit (as we move from right to left)
    prev_value = 0

    # Iterate through the string from right to left
    for char in reversed(s):
        # Current digit's integer value
        value = roman_map[char]

        # If the current value is less than the previous one,
        # subtract it (e.g., IV -> I before V, so 4)
        if value < prev_value:
            total -= value
        else:
            # Otherwise, add it (normal additive case)
            total += value

        # Update previous value for the next iteration
        prev_value = value

    # Final converted integer value
    return total


print(roman_to_int("III"))
print(roman_to_int("IV"))
print(roman_to_int("IX"))
print(roman_to_int("LVIII"))
print(roman_to_int("MCMXCIV"))