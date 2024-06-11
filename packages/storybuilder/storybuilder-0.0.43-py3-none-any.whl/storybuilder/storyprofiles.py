CHARACTER_VOICE_PROFILES = {
    '': {
        'zh-CN': {
            'voiceName': 'zh-CN-YunxiNeural',
            'kwargs': {}
        },
        'en-US': {
            'voiceName': 'en-US-AndrewMultilingualNeural',
            'kwargs': {}
        }
    },
    'eilly': {
        'zh-CN': {
            'voiceName': 'zh-CN-XiaoxiaoNeural',
            'kwargs': {
                'style': 'affectionate',
            }
        },
        'en-US': {
            'voiceName': 'en-US-AriaNeural',
            'kwargs': {
                'style': 'cheerful',
            }
        }
    },
    'boy': {
        'zh-CN': {
            'voiceName': 'zh-CN-YunxiNeural',
            'kwargs': {
                'role': 'Boy',
                'style': 'Default',
                'prosody': {
                    'rate': '+4.00%'
                }
            }
        },
        'en-US': {
            'voiceName': 'zh-CN-YunxiNeural',
            'kwargs': {
                'role': 'Boy',
                'style': 'chat'
            }
        }
    },
    'girl': {
        'zh-CN': {
            'voiceName': 'zh-CN-XiaoshuangNeural',
            'kwargs': {
                'prosody': {
                    'rate': '+8.00%'
                }
            }
        },
        'en-US': {
            'voiceName': 'en-US-AnaNeural',
            'kwargs': {
                'style': 'chat'
            }
        }
    },
    'M': {
        'zh-CN': {
            'voiceName': 'zh-CN-YunxiNeural',
            'kwargs': {}
        },
        'en-US': {
            'voiceName': 'en-US-AndrewMultilingualNeural',
            'kwargs': {
                'style': 'e-learning'
            }
        }
    },
    'F': {
        'zh-CN': {
            'voiceName': 'zh-CN-XiaohanNeural',
            'kwargs': {}
        },
        'en-US': {
            'voiceName': 'en-US-JennyNeural',
            'kwargs': {
                'style': 'newscast'
            }
        }
    }
}

PRONUNCIATION_DICTIONARY = {
    "zh-CN": {
        '羞臊': '羞sào',
        '数数': '暑shù',
        '∠': '角',
        '°': '度',
        '<ul>': '',
        '</ul>': '',
        '<li>': '',
        '</li>': '。',
        '·': '-',
        '>': '大于',
        '<': '小于',
        '>=': '大于等于',
        '<=': '小于等于',
        'WHO': 'WH欧',
        'elif': 'L-If',
        'for': 'four',
    },
    "en-US": {
        '<ul>': '',
        '</ul>': '',
        '<li>': '',
        '</li>': '。',
    }
}

CHARACTER_FIGURE_ACCESSORY_KEYS = ['mask', 'cap']

STORY_SCENARIO_STYLES = {
    "shinkai_makoto": {
        "scenarios": {
            "cover": {"bgColor": "#C1D0BA"},
            "classroom": "475dc094-e147-478e-a1cf-770df5efa081",
            "notes": {
                "scene":"ce3ae229-7e6b-4e10-9d0a-e5e53d923d61",
                "htmlTemplate":"<h2 style=\'color:white\'><br/><ul><li></li></ul></h2>",
                "rect": [0.2, 0.2, 0.6, 0.8]
            },
            "exam": "a65ed1dc-9e27-4c3d-a5f7-090fc2af4917",
            "blackboard": {"bgColor": "#98A698"},
            "concentrak": {"index": "0bd6c33e-31eb-4083-8dd8-ee07837bc975", "bgColor": "#C1D0BA"},
        },
        "frame": "10px solid #843C0C",
        "positions": {
            "left": [0.2, 0.05],
            "right": [0.8, 0.05],
            "right-bottom": [0.85, -0.05],
        },
        "popup": 11,
        "transform": None
    },
    "close_up": {
        "scenarios": {
            "cover": "5cdab8ba-c028-45ea-87cc-b0d75dd81e10",
            "classroom": "b99b0dc2-0387-4a4f-9c61-308b362cb8f6",
            "notes": {
                "scene": "6c5c45c3-070f-439a-a6f7-a366a04c357c",
                "htmlTemplate":"<p><ul style=\'color: white\' size='5'><li></li></ul></p>",
                "rect": [0.1, 0.28, 0.7, 0.5]
            },
            "exam": "ea874992-c7a9-44c4-8bef-13cad8cee917",
            "blackboard": "e183c517-cbb7-4831-bcf6-efd310ee8790",
            "concentrak": {"index": "0bd6c33e-31eb-4083-8dd8-ee07837bc975", "bgColor": "#9BB9BF"},
        },
        "frame": "10px solid #843C0C",
        "positions": {
            "left": [0.2, -0.25],
            "right": [0.8, -0.25],
            "right-bottom": [0.8, 0.05],
        },
        "popup": 10,
        "transform": "scale(2)"
    }
}