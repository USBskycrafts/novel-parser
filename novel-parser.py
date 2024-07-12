from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor
import sys

volume_name = r'(第*)(一|二|三|四|五|六|七|八|九|十|百|[0-9]|[\u2460-\u2473\u3251-\u325F\u32B1-\u32BF])+(卷)\s+.*'
chapter_name = r'(第*)(一|二|三|四|五|六|七|八|九|十|百|[0-9]|[\u2460-\u2473\u3251-\u325F\u32B1-\u32BF])+(章)\s+.*'

grammar = Grammar(
  fr"""
  novel = chapter_body volumes
  volumes = volume+
  volume  =  volume_name? chapter_body chapters
  chapters = chapter+
  chapter = chapter_name (chapter_body / last_body)

  chapter_name = ~r'{chapter_name}'
  volume_name = ~r'{volume_name}'
  chapter_body = ~r'[\S\s]*?(?={chapter_name}|{volume_name})'
  last_body = ~r'[\S\s]*'
  """
)


class NovelVisitor(NodeVisitor):
  def visit_novel(self, node, visited_children):
    summary, volumes = visited_children
    summary = '# ' + summary.strip() + '\n'
    novel = summary
    for volume in volumes:
      novel = novel + volume.strip() + '\n'
    return novel

  
  def visit_volume(self, node, visited_children):
    volume_name, preface, chapters = visited_children
    if volume_name != "":
      volume_name = '# ' + volume_name.strip() + '\n'
    if preface.strip() != "":
      preface = '## ' + preface.strip() + '\n'
    print(f"{volume_name} scanned, {len(chapters)} chapters in total")
    volume = volume_name + preface
    for chapter in chapters:
      volume = volume + chapter.strip() + '\n'
    return volume


  def visit_chapter(self, node, visited_children):
    chapter_name, chapter_body = visited_children
    chapter_name = '## ' + chapter_name.strip() + '\n'
    assert(len(chapter_body) == 1)
    print(f"{chapter_name} scanned")
    return chapter_name + chapter_body[0].strip()

  def generic_visit(self, node, visited_children):
    """ The generic visit method. """
    return visited_children or node.text
        

def parse(file_name):
  with open(file_name, 'r') as src, open('_out_parser_' + file_name, 'w') as dst:
    full = src.read()
    tree = grammar.parse(full)
    visitor = NovelVisitor()
    output = visitor.visit(tree)
    dst.write(str(output))


if __name__ == "__main__":
   parse(sys.argv[1]) 
