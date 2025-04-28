import os
def extract_number(filename):
    try:
        return int(os.path.splitext(filename)[0])
    except ValueError:
        return float('inf')