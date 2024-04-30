number = 1551.2

# Extract the decimal part using modulo and round functions
decimal_part = abs(number) % 1  # Take the absolute value and find the modulo with 1
decimal_part = round(decimal_part, 2)  # Round the decimal part to 2 decimal places

print(decimal_part)
# Print the extracted decimal part
# print("Decimal Part:", len(decimal_part))