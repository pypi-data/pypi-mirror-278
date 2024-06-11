import os
from typing import List
from python_storybook.core import StoryManager, Story
import importlib.util
from pathlib import Path


class StoryHub:
    _all_managers = {}

    @staticmethod
    def register(story_manager: StoryManager) -> None:
        StoryHub._all_managers[story_manager.title] = story_manager

    @staticmethod
    def get_manager(title: str) -> StoryManager:
        for manager_title, manager in StoryHub._all_managers.items():
            if title == manager_title:
                return manager
        raise f"There is no StoryManager with the title: {title}."

    @staticmethod
    def get_titles() -> List[str]:
        titles = list(StoryHub._all_managers.keys())
        return titles

    @staticmethod
    def get_all_story_full_paths() -> List[str]:
        paths = []
        for manager in StoryHub._all_managers.values():
            paths.extend(manager.get_story_full_paths())
        return paths

    @staticmethod
    def get_story(full_path: str) -> Story:
        split = full_path.split("/")
        title = "/".join(split[:-1])
        story_name = split[-1]
        story_manager = StoryHub.get_manager(title)
        story = story_manager.get_story(story_name=story_name)
        return story

    @staticmethod
    def reset():
        StoryHub._all_managers.clear()

    @staticmethod
    def import_and_register(path):
        # Create a module name based on file path
        module_name = os.path.splitext(os.path.basename(path))[0]
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, 'story_manager'):
            # Assuming StoryHub has a method 'register' that can register a story manager
            StoryHub.register(story_manager=module.story_manager)
        else:
            print(f"No 'story_manager' found in {path}")

    @staticmethod
    def register_story_managers(directory=None):
        if directory is None:
            directory = Path(__file__).parent

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('_stories.py'):
                    file_path = os.path.join(root, file)
                    StoryHub.import_and_register(file_path)
