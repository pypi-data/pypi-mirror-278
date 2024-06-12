import eenhoorntje_llm_lib.llm
import eenhoorntje_llm_lib.language_codes
import copy

TRANSLATION_REFUSAL = "Ø"


def create_prompt(source, source_lang, target_lang, model):
    source_language_name = eenhoorntje_llm_lib.language_codes.get_language_name(source_lang)
    target_language_name = eenhoorntje_llm_lib.language_codes.get_language_name(target_lang)

    messages = [
        {"role": "user",
         "content": f"Translate the following from {source_language_name} to {target_language_name}: '{source}'. Make the translation sound as natural as possible. Write only the translation, do not write anything else."}
    ]

    if "openai/gpt" in model:
        system_message = {
            "role": "system",
            "content": f"Please translate the user message from {source_language_name} "
                       f"to {target_language_name}. "
                       f"Make the translation sound as natural as possible."
        }
        user_message = {
            "role": "user",
            "content": source
        }
        messages = [system_message, user_message]

    if "anthropic/claude" in model:
        pass

    return messages


def translate(source, source_lang, target_lang, engine, custom_prompt=None):
    model = engine

    messages = create_prompt(source, source_lang, target_lang, model)

    if custom_prompt:
        messages = copy.deepcopy(custom_prompt)
        for i in range(len(messages)):
            messages[i]["content"] = messages[i]["content"].replace("{source_content}", source)
            messages[i]["content"] = messages[i]["content"].replace("{source_language}",
                                                                    eenhoorntje_llm_lib.language_codes.get_language_name(
                                                                        source_lang))
            messages[i]["content"] = messages[i]["content"].replace("{target_language}",
                                                                    eenhoorntje_llm_lib.language_codes.get_language_name(
                                                                        target_lang))

    translation = eenhoorntje_llm_lib.llm.call_llm(messages, model, max_tokens=min(2048, len(source) * 4))

    if translation is None:
        return TRANSLATION_REFUSAL

    return translation
