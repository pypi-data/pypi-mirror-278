from python_storybook.core import config
import inspect
import typing
import importlib.util
import os


def get_docs(func):
    return inspect.getdoc(func)


def get_type_hints(func):
    type_hints = typing.get_type_hints(func)
    output = {}
    for key, value in type_hints.items():
        if isinstance(value, type):
            output[key] = value.__name__
        elif isinstance(value, typing._GenericAlias):
            output[key] = str(value).replace('typing.', '')
        else:
            if config.DEBUG_MODE:
                raise 'Not covered type!'
            else:
                output[key] = value.__name__
    return output


def load_story_module(story_path):
    module_name = os.path.splitext(os.path.basename(story_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, story_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_source_safe(func):
    try:
        return inspect.getsource(func)
    except Exception as e:
        print(f"Failed to get source. The function might be from outer. Error Message: {e}")


def _get_type_hints_inspect(func):

    signature = inspect.signature(func)
    type_hints = {
        name: param.annotation for name, param in signature.parameters.items()
    }
    type_hints["return"] = signature.return_annotation
    return type_hints


def _get_type_hints_typing(func):
    type_hints = typing.get_type_hints(func)
    return type_hints
