import unittest

import os
from python_storybook.core.utils import get_type_hints, get_docs, load_story_module
from python_storybook.core import config
from typing import List, Any, Dict

config.DEBUG_MODE = True


class TestUtilsBasic(unittest.TestCase):
    def test_get_docs(self):
        def example_function():
            """I am some Docstring."""

        docs = get_docs(example_function)

        self.assertEqual(docs, "I am some Docstring.")

    def test_get_type_hints(self):
        def example_function(arg1: str, arg2: List[int]) -> Dict[str, Any]:
            return {"hi": 1}

        expected_result = {
            "arg1": "str",
            "arg2": "List[int]",
            "return": "Dict[str, Any]",
        }

        typehints = get_type_hints(example_function)

        self.assertEqual(typehints, expected_result)

    # Check the ./context/example_stories.py file
    def test_load_story_module(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_directory, "context/example_stories.py")
        expected_result = "Hi, I am a story manager."

        executed_module = load_story_module(path)
        greet_from_story_manager = executed_module.story_manager

        self.assertEqual(greet_from_story_manager, expected_result)


if __name__ == "__main__":
    unittest.main()
