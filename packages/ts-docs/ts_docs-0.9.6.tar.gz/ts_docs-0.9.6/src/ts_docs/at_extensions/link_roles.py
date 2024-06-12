import os
from docutils import nodes
from sphinx.transforms.post_transforms import SphinxPostTransform


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
                # 获取当前文档的目录
                doc_dir = os.path.dirname(env.doc2path(docname))

                # 确保当前文档目录和源目录存在
                if not doc_dir or not env.srcdir:
                    raise ValueError("Current document directory or source directory is not specified.")

                # 生成目标语言的文档路径
                target_doc_dir = doc_dir.replace('en/html', f'{language}/html')

                # 生成完整的URL
                target_doc_path = os.path.join(target_doc_dir, os.path.basename(docname) + '.html')

                url = os.path.normpath(target_doc_path)

                node.replace_self(nodes.reference(rawtext, link_text, refuri=url, **options))
            else:
                node.replace_self([])


def setup(app):
    app.add_role('link_to_translation', link_to_translation)
    app.add_node(translation_link)
    app.add_post_transform(TranslationLinkNodeTransform)
    return {'parallel_read_safe': True, 'parallel_write_safe': True, 'version': '0.5'}
