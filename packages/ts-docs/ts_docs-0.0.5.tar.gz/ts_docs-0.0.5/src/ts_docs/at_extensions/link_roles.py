import os
import logging
from docutils import nodes
from sphinx.transforms.post_transforms import SphinxPostTransform

# 设置日志记录
logging.basicConfig(filename='translation_link.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class translation_link(nodes.Element):
    """Node for "link_to_translation" role."""

def link_to_translation(name, rawtext, text, lineno, inliner, options={}, content=[]):
    node = translation_link()
    node['expr'] = (rawtext, text, options)
    return [node], []

class TranslationLinkNodeTransform(SphinxPostTransform):
    default_priority = 0

    def run(self, **kwargs):
        for node in self.document.traverse(translation_link):
            if 'html' in self.app.builder.name:
                rawtext, text, options = node['expr']
                target_language, link_text = text.split(':')
                env = self.document.settings.env
                docname = env.docname
                current_language = 'en' if 'en' in env.srcdir else 'zh_CN'

                logging.debug(f"docname: {docname}")
                logging.debug(f"current_language: {current_language}")
                logging.debug(f"target_language: {target_language}")
                logging.debug(f"env.srcdir: {env.srcdir}")

                # 获取相对于 srcdir 的文档路径
                doc_relative_path = os.path.relpath(env.doc2path(docname, base=None, suffix=''), start=env.srcdir)
                logging.debug(f"doc_relative_path: {doc_relative_path}")

                # 替换语言部分
                new_doc_path = doc_relative_path.replace(current_language, target_language)
                logging.debug(f"new_doc_path: {new_doc_path}")

                # 去掉 .rst 后缀并生成新的 URL
                if new_doc_path.endswith('.rst'):
                    new_doc_path = new_doc_path[:-4]
                logging.debug(f"new_doc_path after removing .rst: {new_doc_path}")

                # 生成新的 URL
                url = os.path.join("/", target_language, "html", new_doc_path) + ".html"
                logging.debug(f"url: {url}")

                node.replace_self(nodes.reference(rawtext, link_text, refuri=url, **options))
            else:
                node.replace_self([])

def setup(app):
    app.add_role('link_to_translation', link_to_translation)
    app.add_node(translation_link)
    app.add_post_transform(TranslationLinkNodeTransform)
    return {'parallel_read_safe': True, 'parallel_write_safe': True, 'version': '0.5'}
