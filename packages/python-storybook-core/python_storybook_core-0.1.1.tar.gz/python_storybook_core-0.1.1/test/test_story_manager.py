import unittest

from python_storybook.core import StoryManager, Story
from typing import List, Any, Dict


def basic_function():
    return "hi"


def basic_void_function():
    dummy = 1
    print(dummy)


def with_typehint(arg1: str, arg2: List[str]) -> Dict[str, Any]:
    return {"string": [1, "another string"]}


def with_docs():
    """Some documentation."""
    return 1


class TestStoryManagerBasic(unittest.TestCase):
    def test_create_and_get_story(self):
        story_manager = StoryManager(title="Example")
        story_name = "any_name"

        story_manager.create_story(story_name=story_name, func=basic_void_function)

        maybe_story = story_manager.get_story(story_name=story_name)

        self.assertTrue(
            isinstance(maybe_story, Story), "maybe_story should be an instance of Story"
        )

    def test_count_created_stories(self):
        story_manager = StoryManager(title="Example")
        func_count = 4

        story_manager.create_story(func=basic_function)
        story_manager.create_story(func=basic_void_function)
        story_manager.create_story(func=with_typehint)
        story_manager.create_story(func=with_docs)

        stories = story_manager.get_stories()

        self.assertEqual(func_count, len(stories))

    def test_set_parent_name(self):
        manager_name = "Manager Name"
        story_manager = StoryManager(title=manager_name)
        story_manager.create_story(func=basic_function)

        parent_name = story_manager.get_story("basic_function").parent

        self.assertEqual(parent_name, manager_name)

    def test_get_story_full_paths(self):
        base_path = "Example/Level2"
        story_path = "StoryName"
        custom_full_path = base_path + "/" + story_path  # Example/Level2/StoryName
        auto_full_path = base_path + "/" + basic_function.__name__
        story_manager = StoryManager(title=base_path)

        # Custom Path
        story_manager.create_story(story_name=story_path, func=basic_function)
        # Auto Path
        story_manager.create_story(func=basic_function)

        full_paths = story_manager.get_story_full_paths()

        self.assertIn(custom_full_path, full_paths)
        self.assertIn(auto_full_path, full_paths)

    def test_get_story_names(self):
        story_manager = StoryManager(title="Example")
        expected_names = [
            "Custom Name",
            "basic_void_function",
            "with_typehint",
            "with_docs",
        ]

        story_manager.create_story(story_name="Custom Name", func=basic_function)
        story_manager.create_story(func=basic_void_function)
        story_manager.create_story(func=with_typehint)
        story_manager.create_story(func=with_docs)

        story_names = story_manager.get_story_names()

        for expected_name in expected_names:
            self.assertIn(expected_name, story_names)


if __name__ == "__main__":
    unittest.main()
