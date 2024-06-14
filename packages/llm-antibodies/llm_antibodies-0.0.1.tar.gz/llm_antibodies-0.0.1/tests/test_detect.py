from antibodies.detect import Detect

def test_detect_model():
    objective = "test"
    rubrics = ["criteria 1"]
    model = Detect(objective, rubrics)
    assert model(prompt="a") is True