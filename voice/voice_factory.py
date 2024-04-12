"""
voice factory
"""

def create_voice(voice_type):
    """
    create a voice instance
    :param voice_type: voice type code
    :return: voice instance
    """
    if voice_type == 'baidu':
        from voice.baidu.baidu_voice import BaiduVoice
        return BaiduVoice()
    elif voice_type == 'google':
        from voice.google.google_voice import GoogleVoice
        return GoogleVoice()
    elif voice_type == 'openai':
        from voice.openai.openai_voice import OpenaiVoice
        return OpenaiVoice()
    elif voice_type == 'pytts':
        from voice.pytts.pytts_voice import PyttsVoice
        return PyttsVoice()
    raise RuntimeError
