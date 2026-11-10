import alchemy

print(alchemy.create_air())

try:
    print(alchemy.create_earth())
except AttributeError as e:
    print(f"Error as expected: {e}")
