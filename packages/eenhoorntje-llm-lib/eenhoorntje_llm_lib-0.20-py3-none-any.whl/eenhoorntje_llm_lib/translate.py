import eenhoorntje_llm_lib.language_codes
import eenhoorntje_llm_lib
import eenhoorntje_llm_lib.deepl
import eenhoorntje_llm_lib.translate_llm
import eenhoorntje_llm_lib.gemini
import eenhoorntje_llm_lib.google
TRANSLATION_REFUSAL = "Ø"


def translate(source, source_lang, target_lang, engine="anthropic/claude-3-opus", custom_prompt=None, tags=False, formality="default"):
    if source_lang == target_lang:
        return source
    if engine == "DeepL":
        return eenhoorntje_llm_lib.deepl.translate_with_deepl(source, source_lang, target_lang, tags, formality)
    if engine == "Google":
        return eenhoorntje_llm_lib.google.translate_with_google(source, source_lang, target_lang)
    if engine == "Gemini":
        return eenhoorntje_llm_lib.gemini.translate_with_gemini(source, source_lang, target_lang, custom_prompt)
    return eenhoorntje_llm_lib.translate_llm.translate(source, source_lang, target_lang, engine, custom_prompt)


if __name__ == "__main__":
    res = translate("hoi goe gaat het met jouw?", "ru", "en")
    print(res)
    # translate_corpus()
