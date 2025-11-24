import os
import openai
import base64
import time

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
BASE_URL = os.environ.get("BASE_URL", "https://api.ai.it.ufl.edu")
IMAGE_MODEL_DEPLOYMENT = os.environ.get("IMAGE_MODEL_DEPLOYMENT", "flux.1-dev")

client = openai.OpenAI(api_key=OPENAI_API_KEY, base_url=BASE_URL)

def flyer_prompt(title, subtitle, desc, date, time, location, icon_desc,
                 bg="Orange, White, Blue (UF Themed)",
                 style="Technology, Futuristic",
                 font="Simple font, san-serif"):
    return (
        f"Generate an 8.5 x 11 flyer with: "
        f"Title: {title} "
        f"Subtitle: {subtitle} "
        f"Description: {desc} "
        f"Date: {date} "
        f"Time: {time} "
        f"Location: {location} "
        f"Background: {bg} "
        f"Style: {style} "
        f"Font: {font} "
        f"Icon Description: {icon_desc}"
    )

def generate_flyer_image(title, subtitle, desc, date, time, location, icon_desc,
                       bg="Orange, White, Blue (UF Themed)",
                       style="Technology, Futuristic",
                       font="Simple font, san-serif",
                       image_output_path="flyer.png"):
    try:
        prompt = flyer_prompt(title, subtitle, desc, date, time, location, icon_desc, bg, style, font)
        response = client.responses.create(
            model=IMAGE_MODEL_DEPLOYMENT,  # use the stable deployment name
            input=[
                {"role": "user", "content": [{"type": "input_text", "text": prompt}]}
            ],
            tools=[{"type": "image_generation"}],
        )
        image_generation_calls = [
            item for item in response.output
            if getattr(item, "type", None) == "image_generation_call"
        ]
        if image_generation_calls:
            image_base64 = image_generation_calls[0].result
            if image_base64:
                with open(image_output_path, "wb") as f:
                    f.write(base64.b64decode(image_base64))
                return image_output_path
        return None
    except Exception:
        import traceback
        traceback.print_exc()
        return None

# Example usage
generate_flyer_image("Testing", "Test Function", "Testing Cody's Function",
                   "Right Now", "Right Now", "Bed", "Bed")