import asyncio
import aiofiles
import os
import shutil
from pathlib import Path

async def copy_file(source: Path, destination: Path):
    async with aiofiles.open(source, 'rb') as src_file:
        async with aiofiles.open(destination, 'wb') as dst_file:
            while (data := await src_file.read(1024)):
                await dst_file.write(data)

async def copy_directory(source_dir: str, destination_dir: str):
    source_path = Path(source_dir)
    destination_path = Path(destination_dir)

    if not source_path.is_dir():
        raise ValueError(f"{source_dir} is not a valid directory")

    os.makedirs(destination_path, exist_ok=True)

    tasks = []
    for item in source_path.rglob('*'):
        if item.is_file():
            relative_path = item.relative_to(source_path)
            dest_file_path = destination_path / relative_path
            os.makedirs(dest_file_path.parent, exist_ok=True)
            tasks.append(copy_file(item, dest_file_path))

    await asyncio.gather(*tasks)

def main():
    source_directory = 'second_task_data/input'
    destination_directory = 'second_task_data/output'

    asyncio.run(copy_directory(source_directory, destination_directory))

if __name__ == "__main__":
    main()
