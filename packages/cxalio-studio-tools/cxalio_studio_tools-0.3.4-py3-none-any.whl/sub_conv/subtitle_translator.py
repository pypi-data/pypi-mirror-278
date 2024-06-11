import time

import translators
from xpinyin import Pinyin as pinYin

from cx_subtitle import Subtitle, SubtitleProcessor
from .env import env


class SubtitleTranslator(SubtitleProcessor):
    MAX_SEQUENCE = 120
    SLEEP_SECOND = 15

    def __init__(self, target_lang='en'):
        super(SubtitleTranslator, self).__init__()
        env.debug('初始化翻译器')
        self.target_lang = target_lang
        self.ts = translators
        self._count = 0
        self._pin_yin = None

    def _fallback_translate(self, s: str):
        if not self._pin_yin:
            self._pin_yin = pinYin()
        return self._pin_yin.get_pinyin(s, ' ')

    def __call__(self, s: Subtitle):
        translated_content = s.content
        for i in range(10):
            if env.wanna_quit:
                break
            try:
                translated_content = str(self.ts.translate_text(s.content, to_language=self.target_lang))
                env.debug(f'翻译文本 "{s.content}" 为 "{translated_content}" ')
                break
            except KeyboardInterrupt:
                env.error(f'用户终止服务')
                break
            except Exception as e:
                env.error(f'ERROR {i}: [red]{e}[/red]')
                time.sleep(2)
        if translated_content == s.content:
            env.debug(f'[yellow]{translated_content}[/yellow]，在线翻译失败，将启动备用方案')
            translated_content = self._fallback_translate(translated_content)

        self._count += 1
        if self._count >= SubtitleTranslator.MAX_SEQUENCE:
            env.info('[cyan]达到连续最大请求数，正在等待……[/cyan]')
            time.sleep(SubtitleTranslator.SLEEP_SECOND)
            self._count = 0

        return s.with_content(translated_content)
