import inspect


def handle_ui_error(screenshot_file_name=""):
    def decorator(cls):
        for name, method in vars(cls).items():
            if (
                callable(method)
                and not inspect.isclass(method)
                and not name.startswith("__")
                # NOTE: can not support method with fixture decorator
                and not hasattr(method, "_pytestfixturefunction")
            ):
                setattr(
                    cls,
                    name,
                    handle_ui_errors(method, screenshot_file_name, cls.__name__),
                )

        return cls

    return decorator


def handle_ui_errors(method, screenshot_file_name, class_name):
    def wrapper(*args, **kwargs):
        try:
            result = method(*args, **kwargs)
            return result
        except Exception as e:
            file_name = f"{class_name}_{method.__name__}_error.png"

            if screenshot_file_name:
                file_name = screenshot_file_name
            test_instance = args[0]
            test_instance.screenshot(file_name)
            test_instance.logger.info(f"{file_name} saved")

            raise e

    return wrapper
