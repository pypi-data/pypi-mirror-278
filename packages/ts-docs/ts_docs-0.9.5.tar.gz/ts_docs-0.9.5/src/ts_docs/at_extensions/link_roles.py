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
                # 获取当前文档路径
                doc_path = env.doc2path(docname, base=None, suffix=None)
                current_html_dir = os.path.dirname(doc_path)

                # 调试信息
                print(f"docname: {docname}")
                print(f"doc_path: {doc_path}")
                print(f"current_html_dir: {current_html_dir}")
                print(f"env.srcdir: {env.srcdir}")

                # 确保 current_html_dir 和 env.srcdir 非空
                if not current_html_dir or not env.srcdir:
                    raise ValueError("Current HTML directory or source directory is not specified.")

                # 获取当前路径相对于html目录的相对路径
                relative_html_path = os.path.relpath(current_html_dir, start=os.path.join(env.srcdir, 'html'))

                # 调试信息
                print(f"relative_html_path: {relative_html_path}")

                # 确保 relative_html_path 非空
                if not relative_html_path:
                    raise ValueError("Relative HTML path is not specified.")

                # 构建返回根目录的相对路径
                return_path = os.path.relpath(os.path.join(env.srcdir, 'html'), start=current_html_dir)

                # 调试信息
                print(f"return_path: {return_path}")

                # 确保 return_path 非空
                if not return_path:
                    raise ValueError("Return path is not specified.")

                # 生成目标语言的文档路径
                target_path = os.path.join(return_path, '..', language, 'html', relative_html_path, os.path.basename(doc_path))

                # 调试信息
                print(f"target_path: {target_path}")

                # 确保 target_path 非空
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
