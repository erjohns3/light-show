


def get_multiple():
    return [2, 3]

lol = [
    1,
    *get_multiple(),
    4,
]
    

for ele in lol:
    print(f'{ele=}')