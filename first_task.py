import asyncio
from typing import Callable
import aiofiles
from os import listdir
from os.path import isfile, join

class InvalidFile(Exception):
    pass

class InvalidAction(Exception):
    pass

class InvalidNumbers(Exception):
    pass

async def process_file(filename: str) -> float:
    actions: list[Callable[[float, float], float]] = [
        lambda a, b: a + b,
        lambda a, b: a * b,
        lambda a, b: a / b,
        lambda a, b: a ** 0.5 + b ** 0.5,
        lambda a, b: a ** 2 + b ** 2
    ]

    async with aiofiles.open(filename, 'r') as file:
        rows = await file.readlines()

        if len(rows) != 2:
            raise InvalidFile('input file should contain 2 rows')

        action, numbers = int(rows[0]), list(map(float, rows[1].split()))

        if not (1 <= action <= 5):
            raise InvalidAction('action should be integer between 1 and 5')

        if len(numbers) != 2:
            raise InvalidNumbers('in numbers row you should specify strictly 2 numbers')

        result = actions[action](*numbers)

        return result

async def execute(input_path: str, output_path: str):
    files = [f for f in listdir(input_path) if isfile(join(input_path, f))]

    results = await asyncio.gather(*(process_file(file) for file in files))

    async with aiofiles.open(f"{output_path}/out.dat", "w") as out_file:
        await out_file.write('\n'.join(map(str, results)))

def main():
    path = 'first_task_data'
    input_path = f'{path}/input'
    output_path = f'{path}/output'

    asyncio.run(execute(input_path, output_path))

if __name__ == "__main__":
    main()
