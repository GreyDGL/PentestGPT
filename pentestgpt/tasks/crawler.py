import json

import requests
from bs4 import BeautifulSoup


def crawl_dotCMS_description_page(
    url="https://www.dotcms.com/docs/latest/container-api", output_dir="outputs"
):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Extract the title of the page
    title = soup.find("h1").get_text()

    # Extract the subtitles and their descriptions and code chunks
    subtitles = soup.find_all("h2")
    parsed_subtitles = []
    for subtitle in subtitles:
        subtitle_title = subtitle.get_text()
        subtitle_contents = subtitle.find_next_siblings(["p", "pre"])
        subtitle_parsed_contents = []
        description = ""
        for content in subtitle_contents:
            # Check if the content is a code block
            if content.name == "pre" and content.code:
                code = content.get_text()
                # Add the previous description and code chunk to the list
                if len(description) != 0:  # If there is no description, don't add it
                    parsed_description = description.strip().replace("\n", " ")
                    parsed_code = code.strip().replace("\n", " ")
                    subtitle_parsed_contents.append([parsed_description, parsed_code])

            else:
                # Concatenate the non-code content into a single description string
                description += (
                    "\n" + content.get_text() if description else content.get_text()
                )
        parsed_subtitles.append([subtitle_title, subtitle_parsed_contents])

    # Save the results as a structured JSON object
    title = title.strip().replace(" ", "_").lower()
    output = {"title": title}
    for parsed_subtitle in parsed_subtitles:
        output[parsed_subtitle[0]] = parsed_subtitle[1]

    with open(f"{output_dir}/{title}.json", "w") as f:
        json.dump(output, f)
    return output


def crawl_strapi_documentation(url, output_dir="outputs"):
    pass


if __name__ == "__main__":
    output_dir = "outputs"
