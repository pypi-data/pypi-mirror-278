import os
from typing import List, Any, Optional, Callable, Dict
from .utils import get_source_safe, get_docs, get_type_hints
from python_storybook.core import Story


class StoryManager:
    def __init__(self, title: str):
        self.title = title
        self.meta: Any = ""
        self.stories: Dict[str, Story] = {}
        self.path: str = os.path.abspath(__file__)

    def create_story(
        self,
        func: Callable[[Any], str],
        meta: Optional[Dict[str, Any]] = None,
        story_name: Optional[str] = None,
        kwargs: Optional[Dict[str, str]] = None,
    ) -> None:
        if story_name is None:
            story_name = func.__name__
        story = Story(
            name=story_name,
            meta=meta,
            parent=self.title,
            full_path=f"{self.title}/{story_name}",
            docs=get_docs(func),
            source=get_source_safe(func),
            typehints=get_type_hints(func),
            kwargs=kwargs,
        )
        self.stories[story_name] = story

    def get_story(self, story_name: str) -> Story:
        if story_name in self.stories.keys():
            return self.stories[story_name]
        raise f"There is no story named {story_name}"

    def get_story_names(self) -> List[str]:
        return list(self.stories.keys())

    def get_story_full_paths(self) -> List[str]:
        return [story.full_path for story in self.stories.values()]

    def get_stories(self):
        return list(self.stories.values())
