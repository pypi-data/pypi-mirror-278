import os, json

from dataclasses import dataclass, field
from typing import Dict, Set, Optional

from pathlib import Path

from watchdog.observers import Observer, BaseObserverSubclassCallable
from watchdog.events import FileSystemEventHandler

class manifest_manager:
    __manifest_contents = {}
    
    def __init__(self, name : str, root_path : Path):
        '''
        
        '''
        self.name = name
        if name in self.__manifest_contents:
            self.state = self.__manifest_contents[name]
        else:
            self.state = manifest_state(root_path, calculate_manifest(root_path))
            self.__manifest_contents[name] = self.state
    
    def update_manifest(self, record : Path):
        '''
        Update the manifest with the new record. Expected to be called after the record has been uploaded.
        The record should be a path of the dataset (where all the files are synchronised within)
        '''
        keys = record.path.split('/')
        
        manifest = self.state.current_manifest
        for key in keys:
            manifest = manifest.defaultdict(key, {})
        # this time should be fetched at upload time
        manifest[keys[-1]] = os.stat(record).st_mtime

        self.state.update_queue.pop(record)
        
        manifest_json = json.dumps(self.state.current_manifest)
        # dao_sync_source.update_manifest(self.name, manifest_json)
    
    def get_new_records(self) -> Optional[Path]:
        if self.state.update_queue:
            # return last item
            return list(self.state.update_queue.keys())[-1]
        return None

@dataclass
class manifest_state:
    root_path: Path
    current_manifest: dict
    update_queue: Dict[Path, float] = field(default_factory=dict)
    file_watcher: Optional[BaseObserverSubclassCallable] = None
    
    def __post_init__(self):
        self.file_watcher = get_observer(self.root_path, self.update_queue)
        new_manifest = calculate_manifest(self.root_path)
        self.update_queue = diff_manifest(self.current_manifest, new_manifest) + self.update_queue

def get_observer(directory, update_queue) -> BaseObserverSubclassCallable:
    observer = Observer()
    observer.schedule(file_watcher(update_queue), directory, recursive=True)
    observer.start()
    return observer

class file_watcher(FileSystemEventHandler):
    def __init__(self, update_queue : Set[Path]):
        super().__init__()
        self.update_queue = update_queue
    
    def on_created(self, event):
        if event.src_path.endswith('.DS_Store'):
            return
        self.update_queue[Path(event.src_path)] = os.stat(event.src_path).st_mtime
    
    def on_modified(self, event):
        if event.src_path.endswith('.DS_Store'):
            return
        self.update_queue[Path(event.src_path)] = os.stat(event.src_path).st_mtime
        
    def on_moved(self, event):
        if event.src_path.endswith('.DS_Store'):
            return
        self.update_queue[Path(event.src_path)] = os.stat(event.src_path).st_mtime


def calculate_manifest(directory)-> Dict[str, "dict|float"]:
    main_path = Path(directory)

    manifest = {}
    for root, _, files in os.walk(directory):
        for file in files:
            dirs = os.path.relpath(root, start=main_path).split('/')
            if dirs[0] == '.':
                continue
            mod_time = os.stat(f"{root}/{file}").st_mtime

            assignment_key = manifest
            for d in dirs:
                assignment_key = assignment_key.setdefault(d, {})
            assignment_key[file] = mod_time

    return manifest

def diff_manifest(manifest_old, manifest_new, initial_key : str = "") -> Dict[Path, float]:
    differences = {}
    for key in manifest_new.keys():
        if isinstance(manifest_new[key], dict):
            if key in manifest_old:
                differences += diff_manifest(manifest_old[key], manifest_new[key], f"{initial_key}{key}/")
            else:
                differences += diff_manifest({}, manifest_new[key], f"{initial_key}{key}/")
        else:
            if key in manifest_old and manifest_old[key] == manifest_new[key]:
                continue
            differences[Path(f"{initial_key}{key}")] = manifest_new[key]

    if initial_key == "":
        # sort file order by modification time
        differences = dict(sorted(differences.items(), key=lambda item: item[1]))
    return differences
