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
                language, link_text = text.split(':')
                env = self.document.settings.env
                docname = env.docname
                doc_path = env.doc2path(docname, base=None, suffix=None)
                current_html_dir = os.path.dirname(doc_path)

                # 记录调试信息
                logging.debug(f"docname: {docname}")
                logging.debug(f"doc_path: {doc_path}")
                logging.debug(f"current_html_dir: {current_html_dir}")
                logging.debug(f"env.srcdir: {env.srcdir}")

                if not current_html_dir or not env.srcdir:
                    raise ValueError("Current HTML directory or source directory is not specified.")

                relative_html_path = os.path.relpath(current_html_dir, start=env.srcdir)
                logging.debug(f"relative_html_path: {relative_html_path}")

                if not relative_html_path:
                    raise ValueError("Relative HTML path is not specified.")

                return_path = os.path.relpath(env.srcdir, start=current_html_dir)
                logging.debug(f"return_path: {return_path}")

                if not return_path:
                    raise ValueError("Return path is not specified.")

                target_path = os.path.normpath(os.path.join(return_path, language, 'html', relative_html_path, os.path.basename(doc_path)))
                logging.debug(f"target_path: {target_path}")

                if not target_path:
                    raise ValueError("Target path is not specified.")

                url = "{}.html".format(target_path)
                node.replace_self(nodes.reference(rawtext, link_text, refuri=url, **options))
            else:
                node.replace_self([])

def setup(app):
    app.add_role('link_to_translation', link_to_translation)
    app.add_node(translation_link)
    app.add_post_transform(TranslationLinkNodeTransform)
    return {'parallel_read_safe': True, 'parallel_write_safe': True, 'version': '0.5'}
