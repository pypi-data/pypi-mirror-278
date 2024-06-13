from pathlib import Path
from typing import Self
from collections import Counter

import shutil

type Path_Location = [Path, str]
type Path_Components = [Path_Location, tuple[str]]
type File_Contents = [bytes, str]
type Creation_Error = [bool, str]

# Could return bool and log errors!!! -> Later
class FileSystem:
    @staticmethod
    def does_exist(path) -> bool:
        if path.exists():
            return True
        
        return False
        
    def __init__(self, object_location: Path_Location):
        self.object_path = self.load_path(object_location)
    
    def load_path(self, object_location: Path_Location) -> Path_Location:
        try:
            if isinstance(object_location, Path):
                return object_location
            elif isinstance(object_location, str):
                return Path(object_location)
            else:
                raise Exception(f'The following isnt of type Path_Location: {object_location}')
        except Exception as e:
            raise Exception(f'{object_location} raised the following exception: {e}')
            
    def move(self, other_path: Path_Location) -> Self:
        other_path = self.load_path(other_path)
        
        '''
            if not self.does_exist(other_path):
                self.copy(other_path)
            else:
                with other_path.open(mode="xb") as writer:
                    writer.write(self.object_path.read_bytes())
                    
            self.object_path.unlink()
            
            # Change class variable to point to the new location
            self.object_path = other_path
        '''
        self.object_path = shutil.move(str(self.object_path.absolute()), str(other_path.absolute()))
        
        return self
        
    def copy(self, other_path: Path):
        other_path = self.load_path(other_path)
        
        shutil.copy(self.object_path, other_path)
        
    def is_file(self) -> bool:
        return self.object_path.is_file()
        
    def group(self):
        return self.object_path.group()
        
    def owner(self):
        return self.object_path.owner()
        
    def diff(self, other_path: Path_Location) -> bool:
        other_path = self.load_path(other_path)

        return self.object_path.samefile(other_path)
        
    def mkdir(self, mode: int, parents: bool = False, exist_ok: bool = False) -> Creation_Error:
        try:
            return self.object_path.mkdir(mode=mode, parents=parents, exist_ok=exist_ok)
        except Exception as e:
            return e 
            
    def get_absolute_path(self) -> str:
        return self.object_path.absolute()
        
    def replace_path(self, new_location: Path_Location) -> Self:
        self.object_path = self.load_path(new_location)

        return self
        
    # top_down = True allows modification to prune search
    ## Not sure if you can delete/prune when passed to client interfaces???
    def walk(self, top_down: bool = False):
        for root, dirs, files in self.object_path.walk(top_down=top_down):
            yield (root, dirs, files)
        
    # yields level sizes if True
    def size_of_directory(self, get_level_sizes: bool = False):
        if not self.is_file():
            total_size = 0
            
            for root, dirs, files in self.walk():
                size_of_files = sum((root / filename).stat().st_size for filename in files)
                if get_level_sizes:
                    num_of_files = len(files)
                    
                    yield f'{root} consumes {size_of_files} bytes in {num_of_files} non-directory files'
                    
                total_size += size_of_files
                
            yield f'{self.object_path} contains {total_size} bytes'
            
    def get_file_types(self):
        return Counter([entry.suffix for entry in self.object_path.iterdir()
                                           if entry.is_file() and len(set(entry.suffix)) != 1])
   
    def get_component(self, option: str) -> str:
        match option:
            case 'parent':
                return self.object_path.parent
            case 'stem':
                return self.object_path.stem
            case _:
                return self.object_path.suffix
        
    def exists(self) -> bool:
        return self.object_path.exists()
        
    def __str__(self) -> str:
        return str(self.get_absolute_path())
        
    # Following isn't tested for now!!!
    #####
    # Could do over the wire with this as a PoC!!!
    #####
    # st_mode, st_size, st_atime, st_mtime, AND st_ctime is either g, ge, l, le, e, OR mask... doesn't use both mask and conditional 
    # attributes = {'st_mode': ['e', 0o343] OR ['mask', 0o111], 'st_ino': 12003032, 'st_dev': 12342, 'st_nlink': 1332, 'st_uid': 501, 'st_gid': 501, 'st_size': 264, 'st_atime': ['ge', 1297230295], 'st_mtime': ['ge', 1297230027}] 'st_ctime': ['e', 1297230027]}
    def attribute_comparison(self, value: int, boundary: int, option: str) -> bool:
        if option == 'l':
            return value < boundary
        elif option == 'le':
            return value <= boundary
        elif option in ['e', 'mask']:
            return value == boundary
        elif option == 'g':
            return value > boundary
        else:
            return value >= boundary
        
    def parse_attributes(path: Path_Location, attributes: dict) -> bool:
        file_metadata = path.stat()
        
        for key, values in attributes.items():
            value = file_metadata[key]
            
            if key in ['st_mode', 'st_size', 'st_atime', 'st_mtime', 'st_ctime']:
                option = values[0]
                boundary = values[1]
            else:
                option = 'mask'
                boundary = values
                
            if not self.attribute_comparison(value, boundary, option):
                return False
                
        return True
        
    def get_search_result(search_generator, attributes):
        # return (path for path in search_generator if self.parse_attributes(path, attributes))
        # Above isn't legible
        
        for path in search_generator:
            if self.parse_attributes(path, attributes):
                yield path
        
    def search(self, pattern: str, recursive: bool = False, attributes: dict = {}):
        if recursive:
            return self.get_search_result(self.object_path.rglob(pattern), attributes)
        return self.get_search_result(self.object_path.glob(pattern), attributes)
                                           
def get_unique_path(path_location: Path_Location) -> Path_Location:
    tmp_path = FileSystem(path_location)
    
    parent_dir = tmp_path.get_component('parent')
    base_filename = tmp_path.get_component('stem')
    extension = tmp_path.get_component('suffix')
    
    counter = 0
            
    while tmp_path.exists():
        counter += 1
                
        tmp_path.replace_path(parent_dir / f'{base_filename}{counter}{extension}')
    
    return tmp_path
