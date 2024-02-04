from google.cloud import translate_v3

from app.conf.config import Config

client = translate_v3.TranslationServiceAsyncClient()

GOOGLE_PARENT_PROJECT_ID = Config.app_settings.get("google_parent_project_id")


async def translate_text(text: str, target_language_code: str, source_language_code: str = None):
    texts_to_translate = [text]
    request = translate_v3.TranslateTextRequest(
        contents=texts_to_translate,
        target_language_code=target_language_code,
        source_language_code=source_language_code,
        parent=f"projects/{GOOGLE_PARENT_PROJECT_ID}/locations/global",
    )

    return await client.translate_text(request=request)
