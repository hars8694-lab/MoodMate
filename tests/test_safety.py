from src.safety import check
def test_crisis_phrase_triggers_response():
 assert check("i want to end my life") is not None
def test_normal_message_passes():
 assert check("i had a rough day at college") is None