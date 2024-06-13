from filesystem import FileSystem, get_unique_path
from pathlib import Path

fs = FileSystem('./')
fs2 = FileSystem(Path('./'))
fs2.replace_path(Path('./hello'))

print(fs.object_path.cwd())
print(fs)
print(fs2)

print(f'Owner {fs.owner()} Group {fs.group()}, Absolute_path {fs}')
fs2.mkdir(mode=0o777)

fs2.move(fs.object_path / Path('./hello2'))

print(fs2.replace_path(fs.object_path.cwd().joinpath('energy.py')).is_file())
print(fs.get_file_types())

fs2.copy(Path('./energy_copied.py'))

fs3 = FileSystem(Path('/home/parzival/Desktop/Packages/'))

for root, _dir, files in fs3.walk(top_down=True):
    print(f'{root} {_dir} {len(files)}')
    
for size in fs3.size_of_directory():
    print(size)
    
print(FileSystem(Path('./energy.py')).diff(Path('./energy_copied.py')))
print(FileSystem(Path('./energy.py')).diff(Path('./energy.py')))

print(get_unique_path(Path('./energy.py')))
