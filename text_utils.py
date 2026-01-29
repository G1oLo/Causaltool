def extract_content(response):
    if hasattr(response, "messages") and response.messages:
        return response.messages[-1].content
    return getattr(response, "content", str(response))


def clean_expert_output(text):
    lines = text.splitlines()
    filtered = []
    for l in lines:
        # remove any inline or prefixed Devil's Advocate preludes and user prompts
        if (
            "Devil's Advocate" in l
            or l.strip().startswith("DA:")
            or l.strip().lower().startswith("devil")
            or l.strip().startswith("user:")
        ):
            continue
        filtered.append(l)
    return "\n".join(filtered)
