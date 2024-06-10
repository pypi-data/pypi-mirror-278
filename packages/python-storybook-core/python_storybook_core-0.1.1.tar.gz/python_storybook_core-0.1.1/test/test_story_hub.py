import unittest
import io
import sys

from python_storybook.core import (
    StoryHub,
    StoryManager,
)


def basic_function():
    return "hi"


class TestStoryManagerBasic(unittest.TestCase):
    def setUp(self):
        StoryHub.reset()
        if False:
            self.capturedOutput = io.StringIO()
            sys.stdout = self.capturedOutput
            print("\n")

    def tearDown(self):
        if False:
            sys.stdout = sys.__stdout__
            print(self.capturedOutput.getvalue())

    def test_register(self):
        story_manager = StoryManager(title="Example")
        StoryHub.register(story_manager=story_manager)

        retrieved = StoryHub.get_manager("Example")

        self.assertEqual(retrieved, story_manager)

    def test_get_titles(self):
        titles = [
            "Any",
            "Titles",
            "Are",
            "Written",
        ]
        for title in titles:
            story_manager = StoryManager(title=title)
            StoryHub.register(story_manager=story_manager)

        retrieved = StoryHub.get_titles()

        for title in retrieved:
            self.assertIn(title, titles)

    def test_override_story_manager(self):
        def func1():
            pass

        def func2():
            pass

        story_manager = StoryManager(title="Example")
        story_manager.create_story(func=func1)
        StoryHub.register(story_manager=story_manager)

        story_manager = StoryManager(title="Example")
        story_manager.create_story(func=func2)
        StoryHub.register(story_manager=story_manager)

        retrieved = StoryHub.get_manager("Example")

        stories = retrieved.get_stories()

        self.assertEqual(1, len(stories))
        self.assertEqual(stories[0].name, "func2")

    def test_get_story(self):
        story_manager = StoryManager(title="Example")
        story_manager.create_story(func=print)
        StoryHub.register(story_manager=story_manager)
        created_story = story_manager.get_story("print")

        story = StoryHub.get_story(full_path="Example/print")

        self.assertEqual(story, created_story)


if __name__ == "__main__":
    unittest.main()
