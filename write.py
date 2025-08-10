try:
    with open("note.txt", 'r') as f:
        f.read()
finally:
    with open("note.txt", 'w') as f:
        f.write("fuck u")
        