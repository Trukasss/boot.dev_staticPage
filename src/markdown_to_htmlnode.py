from textnode import markdown_to_blocks
from textblock import block_to_block_type, 

def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)