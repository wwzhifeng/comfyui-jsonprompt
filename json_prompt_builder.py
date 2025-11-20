import json

def _flatten_value(v):
    parts = []
    if isinstance(v, str):
        parts.append(v)
    elif isinstance(v, (int, float, bool)):
        parts.append(str(v))
    elif isinstance(v, list):
        for item in v:
            parts.extend(_flatten_value(item))
    elif isinstance(v, dict):
        for vv in v.values():
            parts.extend(_flatten_value(vv))
    return parts


class JSONPromptBuilder:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "json_text": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "{\n  \"prompt\": \"example\"\n}",
                    },
                ),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "build"
    CATEGORY = "ZhiFeng/JSON"

    def build(self, json_text: str):
        try:
            data = json.loads(json_text)
        except Exception as e:
            return (f"JSON 解析错误: {e}",)

        parts = _flatten_value(data)

        cleaned = []
        for p in parts:
            p = str(p).strip()
            if p:
                cleaned.append(p)

        final_prompt = ", ".join(cleaned) if cleaned else "photo"
        return (final_prompt,)


NODE_CLASS_MAPPINGS = {
    "JSONPromptBuilder": JSONPromptBuilder,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JSONPromptBuilder": "JSON → Prompt Builder",
}
