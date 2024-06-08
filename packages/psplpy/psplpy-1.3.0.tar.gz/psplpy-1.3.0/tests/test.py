if __name__ == '__main__':
    import test_middleware_utils
    import test_serialization_utils
    import test_concurrency_utils
    import test_network_utils
    import test_file_utils
    import test_image_utils
    import test_other_utils
    import test_dynamic_compose
else:
    from . import test_middleware_utils
    from . import test_serialization_utils
    from . import test_concurrency_utils
    from . import test_network_utils
    from . import test_file_utils
    from . import test_image_utils
    from . import test_other_utils
    from . import test_dynamic_compose


def global_test():
    test_middleware_utils.tests()
    test_serialization_utils.tests()
    test_concurrency_utils.tests()
    test_network_utils.tests()
    test_file_utils.tests()
    test_image_utils.tests()
    test_other_utils.tests()
    test_dynamic_compose.tests()


if __name__ == '__main__':
    global_test()
