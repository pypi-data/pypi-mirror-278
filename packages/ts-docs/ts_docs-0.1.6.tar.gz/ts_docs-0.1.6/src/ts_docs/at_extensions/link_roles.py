import os
import logging
from docutils import nodes
from sphinx.transforms.post_transforms import SphinxPostTransform

# 设置日志记录
logging.basicConfig(filename='translation_link.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class translation_link(nodes.Element):
    """Node for "link_to_translation" role."""


def link_to_translation(name, rawtext, text, lineno, inliner, options={}, content=[]):
    node = translation_link()
    node['expr'] = (rawtext, text, options)
    return [node], []


class TranslationLinkNodeTransform(SphinxPostTransform):
    default_priority = 0

    def run(self, **kwargs):
        # Only output relative links if building HTML
        for node in self.document.traverse(translation_link):
            if 'html' in self.app.builder.name:
                rawtext, text, options = node['expr']
                (language, link_text) = text.split(':')
                env = self.document.settings.env
                docname = env.docname
                doc_path = env.doc2path(docname, False)
                return_path = '../' * doc_path.count('/')  # path back to the root from 'docname'
                # then take off 2/3 more paths for language/release/targetname and build the new URL
                if env.config.chip:
                    url = '{}.html'.format(os.path.join(return_path, '../..', language, env.config.chip, docname))
                else:
                    url = '{}.html'.format(os.path.join(return_path, '../..', language, docname))

                node.replace_self(nodes.reference(rawtext, link_text, refuri=url, **options))
            else:
                node.replace_self([])


def setup(app):
    app.add_role('link_to_translation', link_to_translation)
    app.add_node(translation_link)
    app.add_post_transform(TranslationLinkNodeTransform)
    return {'parallel_read_safe': True, 'parallel_write_safe': True, 'version': '0.5'}
