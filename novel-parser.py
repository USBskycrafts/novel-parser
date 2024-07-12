from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor
import sys

chapter_name = r'(第*)(一|二|三|四|五|六|七|八|九|十|百|[0-9]|[\u2460-\u2473\u3251-\u325F\u32B1-\u32BF])+(章)\s+.*'
role_name = r'(第*)(一|二|三|四|五|六|七|八|九|十|百|[0-9]|[\u2460-\u2473\u3251-\u325F\u32B1-\u32BF])+(卷)\s+.*'

grammar = Grammar(
  fr"""
  novel = chapter_body roles
  roles = role+
  role  =  role_name chapter_body chapters
  chapters = chapter+
  chapter = chapter_name (chapter_body / last_body)

  chapter_name = ~r'{chapter_name}'
  role_name = ~r'{role_name}'
  chapter_body = ~r'[\S\s]*?(?={chapter_name}|{role_name})'
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

  
  def visit_role(self, node, visited_children):
    role_name, preface, chapters = visited_children
    role_name = '# ' + role_name.strip() + '\n'
    if preface.strip() != "":
      preface = '## ' + preface.strip() + '\n'
    print(f"{role_name} scanned, {len(chapters)} chapters in total")
    volume = role_name + preface
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
