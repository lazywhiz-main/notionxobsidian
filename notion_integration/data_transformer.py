from typing import Dict, Any, List

class NotionDataTransformer:
    def __init__(self):
        pass

    def notion_blocks_to_markdown(self, blocks: List[Dict[str, Any]]) -> str:
        """Converts a list of Notion blocks to a Markdown string."""
        markdown_output = []
        for block in blocks:
            block_type = block.get("type")
            if block_type == "paragraph":
                text = self._get_rich_text_content(block["paragraph"]["rich_text"])
                if text:
                    markdown_output.append(text + "\n")
            elif block_type == "heading_1":
                text = self._get_rich_text_content(block["heading_1"]["rich_text"])
                if text:
                    markdown_output.append(f"# {text}\n")
            elif block_type == "heading_2":
                text = self._get_rich_text_content(block["heading_2"]["rich_text"])
                if text:
                    markdown_output.append(f"## {text}\n")
            elif block_type == "heading_3":
                text = self._get_rich_text_content(block["heading_3"]["rich_text"])
                if text:
                    markdown_output.append(f"### {text}\n")
            elif block_type == "bulleted_list_item":
                text = self._get_rich_text_content(block["bulleted_list_item"]["rich_text"])
                if text:
                    markdown_output.append(f"- {text}\n")
            elif block_type == "numbered_list_item":
                text = self._get_rich_text_content(block["numbered_list_item"]["rich_text"])
                if text:
                    # This needs proper numbering logic if multiple items
                    markdown_output.append(f"1. {text}\n")
            elif block_type == "to_do":
                text = self._get_rich_text_content(block["to_do"]["rich_text"])
                checked = "[x]" if block["to_do"]["checked"] else "[ ]"
                if text:
                    markdown_output.append(f"- {checked} {text}\n")
            elif block_type == "code":
                text = self._get_rich_text_content(block["code"]["rich_text"])
                language = block["code"].get("language", "plaintext")
                if text:
                    markdown_output.append(f"``` {language}\n{text}\n```\n")
            elif block_type == "quote":
                text = self._get_rich_text_content(block["quote"]["rich_text"])
                if text:
                    markdown_output.append(f"> {text}\n")
            # Add more block types as needed
            markdown_output.append("\n") # Add a newline for separation
        return "".join(markdown_output)

    def _get_rich_text_content(self, rich_text_array: List[Dict[str, Any]]) -> str:
        """Extracts plain text from a Notion rich text array."""
        return "".join([rt.get("plain_text", "") for rt in rich_text_array])

    def markdown_to_notion_blocks(self, markdown_text: str) -> List[Dict[str, Any]]:
        """Converts a Markdown string to a list of Notion block objects."""
        # This is a complex conversion and might require a more sophisticated parser
        # For simplicity, this example will just convert paragraphs
        blocks = []
        lines = markdown_text.split('\n')
        for line in lines:
            if line.strip():
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": line}}]
                    }
                })
        return blocks

    def notion_properties_to_yaml_frontmatter(self, properties: Dict[str, Any]) -> str:
        """Converts Notion page properties to YAML front matter string."""
        yaml_data = {}
        for prop_name, prop_value in properties.items():
            prop_type = prop_value.get("type")
            if prop_type == "title":
                yaml_data["title"] = self._get_rich_text_content(prop_value["title"])
            elif prop_type == "rich_text":
                yaml_data[prop_name.lower()] = self._get_rich_text_content(prop_value["rich_text"])
            elif prop_type == "select":
                if prop_value["select"]:
                    yaml_data[prop_name.lower()] = prop_value["select"]["name"]
            elif prop_type == "multi_select":
                yaml_data[prop_name.lower()] = [item["name"] for item in prop_value["multi_select"]]
            elif prop_type == "url":
                yaml_data[prop_name.lower()] = prop_value["url"]
            elif prop_type == "date":
                if prop_value["date"]:
                    yaml_data[prop_name.lower()] = prop_value["date"]["start"]
            # Add more property types as needed
        
        # Convert dict to YAML string
        import yaml
        return f"---\n{yaml.dump(yaml_data, allow_unicode=True)}---\n"

    def yaml_frontmatter_to_notion_properties(self, yaml_string: str) -> Dict[str, Any]:
        """Converts YAML front matter string to Notion page properties dictionary."""
        import yaml
        properties = {}
        try:
            # Extract YAML part
            if yaml_string.startswith("---") and "---" in yaml_string[3:]:
                _, yaml_content, _ = yaml_string.split("---", 2)
                data = yaml.safe_load(yaml_content)
                if data:
                    for key, value in data.items():
                        # Basic mapping, needs refinement based on actual Notion DB schema
                        if key == "title":
                            properties["Title"] = {"title": [{"type": "text", "text": {"content": str(value)}}]}
                        elif isinstance(value, str):
                            properties[key.capitalize()] = {"rich_text": [{"type": "text", "text": {"content": value}}]}
                        elif isinstance(value, list):
                            properties[key.capitalize()] = {"multi_select": [{"name": str(item)} for item in value]}
                        # Add more type mappings as needed
        except yaml.YAMLError as e:
            print(f"Error parsing YAML front matter: {e}")
        return properties