import xml.etree.ElementTree as ET
from hashlib import sha256
from pathlib import Path

import plotly.express as px
from docutils import nodes
from docutils.parsers.rst import Directive, directives


class Treemap(nodes.raw):
    def perform_replacement(self, app):
        """Performs the node replacement

        Args:
            app: Sphinx's application object to use.
            collection (TraceableCollection): Collection for which to generate the nodes.
        """
        color_map = self.build_color_map()
        all_data = {
            'name': [],
            'lines': [],
            'coverage': [],
            'coverage_range': [],
        }
        tree = ET.parse(str(self['input']))
        root = tree.getroot()

        for package in root.find('packages').findall('package'):
            self.parse_data(package, all_data)

        fig = px.treemap(
            all_data,
            path=[px.Constant(self['group_name']), 'name'],
            values='lines',
            color='coverage_range',
            color_discrete_map=color_map,
        )
        fig.update_layout(margin=dict(t=10, l=25, r=25, b=25))

        if app.builder.format == 'html':
            self['format'] = 'html'
            out_file = Path(app.outdir) / f"treemap_{self['input'].stem}.html"
            fig.write_html(str(out_file), include_plotlyjs=app.config.treemap_include_plotlyjs)
            with open(out_file, 'r') as file:
                contents = file.read()
                self.children.append(nodes.Text(contents))
            out_file.unlink()
        else:
            env = app.builder.env
            images_dir = Path(env.app.srcdir) / '_images'
            images_dir.mkdir(exist_ok=True)
            hash_value = sha256(str(all_data).encode()).hexdigest()  # create hash value based on graph parameters
            rel_file_path = Path('_images') / f'treemap-{hash_value}.png'
            if str(rel_file_path) not in env.images:
                fig.write_image(str(Path(env.app.srcdir) / rel_file_path), scale=2)
                env.images[str(rel_file_path)] = ['_images', rel_file_path.name]  # store file name in build env
            image_node = nodes.image()
            image_node['uri'] = str(rel_file_path)
            image_node['candidates'] = '*'  # look at uri value for source path, relative to the srcdir folder
            self.replace_self(image_node)

    def build_color_map(self):
        mapping = {
            '(?)': self['group_color'],
        }
        upper = 100
        for lower in reversed(sorted(self['limit_to_color_map'])):
            mapping[f'{lower}-{upper}'] = self['limit_to_color_map'][lower]
            upper = lower
        return mapping

    def parse_data(self, top_element, data):
        if isinstance(data, list):
            data = data[0]
        num_lines = 0
        misses = 0
        for line in top_element.iter('line'):
            num_lines += 1
            if not int(line.get('hits')):
                misses += 1
        try:
            coverage = round((1 - misses / num_lines) * 100, 1)
        except ZeroDivisionError:
            coverage = 100
        data.setdefault('name', []).append(f'{top_element.get("name")} ({coverage}%)')
        data.setdefault('lines', []).append(num_lines)
        data.setdefault('coverage', []).append(coverage)
        data.setdefault('coverage_range', []).append(self.coverage_to_range(coverage, self['limits']))

    @staticmethod
    def coverage_to_range(coverage, limits):
        for i, lower in enumerate(limits[:-1]):
            upper = limits[i + 1]
            msg = (f"{upper} >= {coverage} >= {lower}")
            if upper >= coverage >= lower:

                return f'{lower}-{upper}'
        raise ValueError(f'Invalid configuration for limits; got {limits} with coverage {coverage}\n{msg}')


class TreemapDirective(Directive):
    """Directive to define and configure a treemap.

    Syntax::

      .. treemap:: group_name (color)
         :input: input_file_path
         :limits: number ...
         :colors: color ...
    """
    # Required argument: group_name
    required_arguments = 1
    # Optional argument: color for group
    optional_arguments = 1
    option_spec = {
        'input': directives.path,
        'limits': directives.unchanged,
        'colors': directives.unchanged,
    }

    def run(self):
        """Processes the content of the directive"""
        env = self.state.document.settings.env
        app = env.app
        node = Treemap()
        node['document'] = env.docname
        node.line = self.lineno

        input_file_path = Path(self.options['input'].replace('<<outdir>>', str(app.outdir)))
        if not input_file_path.exists():
            raise self.error(f'Could not find input file {input_file_path} to generate a treemap')
        else:
            node['input'] = input_file_path

        default_limits = app.config.treemap_limits
        node['group_name'] = self.arguments[0]
        node['group_color'] = self.arguments[1] if len(self.arguments) > 1 else 'lightgrey'
        limits = map(int, self.options['limits'].split()) if 'limits' in self.options else default_limits.keys()
        limits = list(limits)
        colors = self.options['colors'].split() if 'colors' in self.options else list(default_limits.values())
        if len(limits) != len(colors):
            raise self.error(f'The number of limits and colors shall be the same; got {limits} and {colors}')

        node['limit_to_color_map'] = {limits[i]: colors[i] for i in range(len(limits))}
        node['limits'] = sorted(limits + [100])
        return [node]
