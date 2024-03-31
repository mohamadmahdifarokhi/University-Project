import re


async def generate_slug(text: str) -> str:
    """
    Generate a slug from the given text.

    Args:
    - text (str): The input text to generate a slug from.

    Returns:
    - str: The generated slug.
    """
    try:
        # Convert the text to lowercase and replace spaces with hyphens
        text = text.lower().replace(" ", "-")

        # Remove special characters and keep only alphanumeric characters, Persian characters, and hyphens
        text = re.sub(r"[^a-zA-Z0-9-\u0600-\u06FF ]", "", text)

        # Replace spaces with hyphens again in case there were Persian spaces
        text = text.replace(" ", "-")

        # Remove consecutive hyphens
        text = re.sub(r"-+", "-", text)

        # Remove leading and trailing hyphens
        text = text.strip("-")

        return text

    except Exception as e:
        raise RuntimeError(f"Error during slug generation: {e}") from e
