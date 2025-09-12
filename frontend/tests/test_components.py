def test_components_importable():
    import importlib
    importlib.import_module('components.header')
    importlib.import_module('components.sensor_panel')
    importlib.import_module('components.crop_recommendation')
    importlib.import_module('components.profit_report')
    importlib.import_module('components.digital_twin')
    importlib.import_module('components.eco_score')
    assert True
