# based on http://protips.readthedocs.io/link-roles.html

import os
from docutils import nodes
from sphinx.transforms.post_transforms import SphinxPostTransform


class translation_link(nodes.Element):
    """Node for "link_to_translation" role."""


# Linking to translation is done at the "writing" stage to avoid issues with the info being cached between builders
def link_to_translation(name, rawtext, text, lineno, inliner, options={}, content=[]):
    node = translation_link()
    node['expr'] = (rawtext, text, options)
    return [node], []


class TranslationLinkNodeTransform(SphinxPostTransform):
    # Transform needs to happen early to ensure the new reference node is also transformed
    default_priority = 0

    def run(self, **kwargs):

        # Only output relative links if building HTML
        for node in self.document.traverse(translation_link):
            if 'html' in self.app.builder.name:
                rawtext, text, options = node['expr']
                (language, link_text) = text.split(':')
                env = self.document.settings.env
                docname = env.docname
                doc_path = env.doc2path(docname, None, None)
                current_html_dir = os.path.dirname(doc_path)
                relative_html_path = os.path.relpath(current_html_dir,start=os.path.join(env.scrdir,'html'))
                return_path = os.path.relpath(os.path(env.srcdir,'html'), start=current_html_dir)
                target_path = os.path.join(return_path, '..', language, 'html',relative_html_path, os.path.basename(doc_path))
                url = "{}.html".format(target_path)
                node.replace_self(nodes.reference(rawtext, link_text, refuri=url, **options))
            else:
                node.replace_self([])


def setup(app):
    # link to the current documentation file in specific language version
    app.add_role('link_to_translation', link_to_translation)
    app.add_node(translation_link)
    app.add_post_transform(TranslationLinkNodeTransform)

    return {'parallel_read_safe': True, 'parallel_write_safe': True, 'version': '0.5'}

