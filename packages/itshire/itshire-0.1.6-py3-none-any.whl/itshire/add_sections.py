import logging
import pathlib
import sys

import mistletoe


def extract_headers(file_path):
    with open(file_path, "r") as file:
        markdown_content = file.read()
    parsed_markdown = mistletoe.Document(markdown_content)
    headers = []

    def _traverse(node):
        if isinstance(node, mistletoe.block_token.Heading):
            header_text = "".join(_extract_text(child) for child in node.children)
            headers.append(header_text.strip())
        for child in getattr(node, "children", []):
            _traverse(child)

    def _extract_text(node):
        if isinstance(node, mistletoe.span_token.RawText):
            return node.content
        elif isinstance(node, mistletoe.span_token.InlineCode):
            return node.children[0].content
        else:
            return "".join(_extract_text(child) for child in node.children)

    _traverse(parsed_markdown)
    return headers


def add_sections(file_path, section_names):
    with open(file_path, "r") as file:
        markdown_content = file.read()

    original_content = markdown_content

    for section_name in section_names:
        if section_name not in markdown_content:
            markdown_content += f"\n## [[{section_name}]]\n- [x] shopping\n"

    if markdown_content != original_content:
        with open(file_path, "w") as file:
            file.write(markdown_content)


def main():
    file_paths = [line.strip() for line in sys.stdin if line.strip()]
    file_paths = [pathlib.Path(s) for s in file_paths]
    logging.debug(file_paths)
    stores = [
        "Central Co-op",
        "Hau Hau Market",
        "M2M",
        "PCC",
        "QFC",
        "Safeway",
        "Trader Joes",
        "Uwajimaya",
    ]

    for file_path in file_paths:
        logging.info(f"file path: {file_path.absolute()}")
        existing_headers = extract_headers(file_path)
        missing_sections = [
            store_name for store_name in stores if store_name not in existing_headers
        ]
        if missing_sections:
            add_sections(file_path, missing_sections)

    print("Sections added successfully.")


if __name__ == "__main__":
    main()
