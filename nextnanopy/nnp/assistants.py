from nextnanopy.utils.formatting import text, lines_to_text, modify_lines_in_text, paragraph, text_to_lines, preview

cbkl = "{"
cbkr = "}"
sbkl = "["
sbkr = "]"
quo = '"'
input_extension = ".in"


def sbk(init='', mid='', end=''):
    return sbkl + text(init, mid, end) + sbkr


def cbk(init='', mid='', end=''):
    return cbkl + text(init, mid, end) + cbkr


def quote(init='', mid='', end=''):
    return quo + text(init, mid, end) + quo


class InputAssistant(object):
    rc_default = {
        'indent': ' ' * 3,
        'new_line': '\n',
        'equal': ' = ',
        'block_text_init': ' ',
        'block_text_end': ' ',
        'block_init': '',
        'block_end': '',
        'comment': '# ',
        'oif': '#if ',
        'nif': '!IF',
        'when': '!WHEN ',
        'elif': '!ELIF',
        'else': '!ELSE',
        'endif': '!ENDIF',
    }

    def __init__(self):
        self.text = text
        self.sbk = sbk
        self.cbk = cbk
        self.lines = lines_to_text
        self.modify_lines = modify_lines_in_text
        self.paragraph = paragraph
        self.split_lines = text_to_lines
        self.quote = quote
        self.nline = '\n'
        self.preview = preview

    @property
    def rc(self):
        if hasattr(self, '_rc'):
            return self._rc
        else:
            return self.rc_default

    @rc.setter
    def rc(self, params):
        self._rc = rc

    # -- Basic methods
    def _indent(self, level):
        return self.get_indent_level(level)

    def get_indent_level(self, level):
        return self.rc['indent'] * level

    def equal(self, name, value):
        eq = self.rc['equal']
        return f'{name}{eq}{value}'

    def point(self, name, *values):
        vector = ', '.join([str(vi) for vi in values])
        vector = self.sbk(vector)
        return self.equal(name, vector)

    def block(self, name, content):
        bi, be = self.rc['block_init'], self.rc['block_end']
        ti, te = self.rc['block_text_init'], self.rc['block_text_end']
        return f'{name}{bi}{self.cbk(ti, content, te)}{be}'

    def add_indent(self, text, amount=1):
        return self.modify_lines(self.rc['indent'] * amount, text)

    # -- Specific methods
    def equal_lines(self, **kwargs):
        content = [self.equal(key, value) for key, value in kwargs.items()]
        return self.lines(*content)

    def equal_block(self, name, equal_kw):
        content = self.equal_lines(**equal_kw)
        content = self.add_indent(content)
        content = self.paragraph(content)
        return self.block(name, content)

    def merge_blocks(self, name, *blocks):
        content = self.lines(*blocks)
        content = self.add_indent(content)
        content = self.paragraph(content)
        return self.block(name, content)

    def comment_lines(self, text):
        return self.modify_lines(self.rc['comment'], text)

    def comment(self, text, end='\n'):
        return self.text(self.rc['comment'], text, end)

    def when_line(self, text, variable):
        init = self.rc['when'] + f"${variable} "
        return self.modify_lines(init, text)

    def if_lines(self, text, variable):
        init = self.rc['nif'] + f'${variable} '
        return self.modify_lines(init, text)

    def if_block(self, if_variable, if_content, elif_variable=None,
                 elif_content=None, else_content=None):
        content = (self.rc['nif'] + f'(${if_variable})' + self.rc['new_line']
                   + self.modify_lines(self.rc['indent'], if_content)
                   + self.rc['new_line'])
        if elif_variable is not None:
            content += (self.rc['elif'] + f'(${elif_variable})'
                        + self.rc['new_line']
                        + self.modify_lines(self.rc['indent'], elif_content)
                        + self.rc['new_line'])
        if else_content is not None:
            content += (self.rc['else'] + f'(${else_variable})'
                        + self.rc['new_line']
                        + self.modify_lines(self.rc['indent'], else_content)
                        + self.rc['new_line'])
        content += self.rc['endif']
        return content

    # - Variables
    def variables(self, **kwargs):
        content = self.equal_lines(**kwargs)
        return self.modify_lines('$', content)

    # - Global
    def global_simulate(self, dim=1):
        return self.block(f'simulate{int(dim)}D', '')

    def global_crystal(self, kind='zb', x_hkl=[1, 0, 0], y_hkl=[0, 1, 0]):
        points = [self.point(key, *value) for key, value in dict(x_hkl=x_hkl, y_hkl=y_hkl).items()]
        content = self.lines(*points)
        content = self.add_indent(content)
        content = self.paragraph(content)
        return self.block(f'crystal_{kind}', content)

    def global_substrate(self, name, alloy_x=None, alloy_y=None):
        kwargs = {'name': name}
        if alloy_x:
            kwargs['alloy_x'] = alloy_x
        if alloy_y:
            kwargs['alloy_y'] = alloy_y
        return self.equal_block('substrate', kwargs)

    def global_periodic(self, x=False, y=None, z=None):
        inputs = dict(x=x, y=y, z=z)
        kwargs = {}
        for key, value in inputs.items():
            value = str(value).lower()
            if value == 'none':
                continue
            elif value in ['true', 'yes', 'y']:
                value = 'yes'
            else:
                value = 'no'
            kwargs[key] = value
        return self.equal_block('periodic', kwargs)

    def global_temperature(self, value):
        return self.equal('temperature', value)

    def global_block(self, *blocks):
        return self.merge_blocks('global', *blocks)

    # - Grid
    def grid_line(self, pos, spacing):
        line = self.equal('pos', pos) + '\t' + self.equal('spacing', spacing)
        return self.block('line', line)

    def grid_axis(self, *pos_spacing, axis='x', min_pos=None, max_pos=None):
        content = [self.grid_line(pi, spi) for pi, spi in pos_spacing]
        for key, value in zip(['min_pos', 'max_pos'], [min_pos, max_pos]):
            if value:
                content.append(self.equal(key, value))
        content = self.lines(*content)
        return self.merge_blocks(f'{axis}grid', content)

    def grid_x(self, *pos_spacing, min_pos=None, max_pos=None):
        return self.grid_axis(*pos_spacing, min_pos=min_pos, max_pos=max_pos, axis='x')

    def grid_y(self, *pos_spacing, min_pos=None, max_pos=None):
        return self.grid_axis(*pos_spacing, min_pos=min_pos, max_pos=max_pos, axis='y')

    def grid_z(self, *pos_spacing, min_pos=None, max_pos=None):
        return self.grid_axis(*pos_spacing, min_pos=min_pos, max_pos=max_pos, axis='z')

    def grid_block(self, *blocks):
        return self.merge_blocks('grid', *blocks)

    # - Structure
    def structure_output(self, name, boxes=None):
        boxes = str(boxes).lower()
        if boxes == 'none':
            return self.block(name, '')
        if boxes in ['true', 'yes', 'y']:
            value = 'yes'
        else:
            value = 'no'
        return self.block(name, self.equal('boxes', value))

    def structure_output_region_index(self, boxes=None):
        return self.structure_output('output_region_index', boxes)

    def structure_output_material_index(self, boxes=None):
        return self.structure_output('output_material_index', boxes)

    def structure_output_contact_index(self, boxes=None):
        return self.structure_output('output_contact_index', boxes)

    def structure_output_allow_composition(self, boxes=None):
        return self.structure_output('output_allow_composition', boxes)

    def structure_output_impurities(self, boxes=None):
        return self.structure_output('output_impurities', boxes)

    def structure_output_generation(self, boxes=None):
        return self.structure_output('output_generation', boxes)

    def structure_block(self, *blocks):
        return self.merge_blocks('structure', *blocks)

    # - Region
    def region_everywhere(self):
        return self.block('everywhere', '')

    def region_contact(self, name):
        content = self.equal('name', name)
        return self.block('contact', content)

    def region_binary(self, name):
        content = self.equal('name', name)
        return self.block('binary', content)

    def region_ternary_constant(self, name, alloy_x):
        name = self.quote(name)
        return self.equal_block('ternary_constant', dict(name=name, alloy_x=alloy_x))

    def region_line(self, x):
        content = self.point('x', *x)
        return self.block('line', content)

    def region_rectangle(self, x, y):
        points = [self.point(key, *value) for key, value in dict(x=x, y=y).items()]
        content = self.lines(*points)
        content = self.add_indent(content)
        content = self.paragraph(content)
        return self.block('rectangle', content)

    def region_obelisk(self, base_x, base_y, base_z, top_x, top_y, top_z):
        kwargs = dict(
            base_x=base_x, base_y=base_y, base_z=base_z,
            top_x=top_x, top_y=top_y, top_z=top_z)
        points = [self.point(key, *value) for key, value in kwargs.items()]
        content = self.lines(*points)
        content = self.add_indent(content)
        content = self.paragraph(content)
        return self.block('obelisk', content)

    def region_cuboid(self, x, y, z):
        kwargs = dict(x=x, y=y, z=z)
        points = [self.point(key, *value) for key, value in kwargs.items()]
        content = self.lines(*points)
        content = self.add_indent(content)
        content = self.paragraph(content)
        return self.block('cuboid', content)

    def region_polygonal_prism(self, axes=['x', 'y', 'z'], vertexes=[[10.5, 14.0]], height=[0, 10]):
        point = self.point(axes[2], *height)
        blocks = [self.region_vertex(ax1=axes[0], ax2=axes[1], value1=v[0], value2=v[1]) for v in vertexes]
        return self.merge_blocks('polygonal_prism', point, *blocks)

    def region_vertex(self, ax1='x', ax2='y', value1=1.0, value2=2.0):
        kwargs = {f'{ax1}': value1, f'{ax2}': value2}
        points = [self.point(key, value) for key, value in kwargs.items()]
        content = self.lines(*points)
        content = self.add_indent(content)
        content = self.paragraph(content)
        return self.block(f'vertex', content)

    def region_doping_constant(self, name, conc):
        cblock = self.equal_block('constant', dict(name=name, conc=conc))
        return self.merge_blocks('doping', cblock)

    def region_doping_remove(self):
        cblock = self.block('remove','')
        return self.merge_blocks('doping', cblock)

    def region_integrate(self, label='', electron=False, hole=False, piezo=False, pyro=False, polarization=False):
        kwargs = {
            'electron_density': electron,
            'hole_density': hole,
            'piezo_density': piezo,
            'pyro_density': pyro,
            'polarization': polarization,
        }
        content = []
        for key, value in kwargs.items():
            if value:
                content.append(self.block(key, ''))
        if label:
            label = self.quote(label)
            content.append(self.equal('label', label))
        content = self.lines(*content)
        content = self.add_indent(content)
        content = self.paragraph(content)
        return self.block('integrate', content)

    def region_block(self, *blocks):
        return self.merge_blocks('region', *blocks)

    # - Impurities
    def impurities_donor(self, name, energy, degeneracy):
        return self.equal_block('donor', dict(name=name, energy=energy, degeneracy=degeneracy))

    def impurities_acceptor(self, name, energy, degeneracy):
        return self.equal_block('acceptor', dict(name=name, energy=energy, degeneracy=degeneracy))

    def impurities_charge(self, name, positive=True):
        kind = 'positive' if positive else 'negative'
        return self.equal_block('charge', dict(name=name, type=kind))

    def impurities_block(self, *blocks):
        return self.merge_blocks('impurities', *blocks)

    # - Contacts
    def contacts_schottky(self, name, bias, barrier,steps = 1):
        if bias == []:
            raise ValueError('bias could be a number or non-zero length list of numbers')
        if steps == 1:
            return self.equal_block('schottky', dict(name=name, bias=bias, barrier=barrier))
        else:
            return self.equal_block('schottky', dict(name=name, bias=bias, barrier=barrier,steps = steps))

    def contacts_fermi(self, name, bias,steps = 1):
        if bias == []:
            raise ValueError('bias could be a number or non-zero length list of numbers')
        return self.equal_block('fermi', dict(name=name, bias=bias,steps = steps))

    def contacts_ohmic(self, name, bias, shift=0,steps = 1):
        if bias == []:
            raise ValueError('bias could be a number or non-zero length list of numbers')
        return self.equal_block('ohmic', dict(name=name, bias=bias, shift = shift,steps = steps))

    def contacts_block(self, *blocks):
        return self.merge_blocks('contacts', *blocks)

    # - Classical
    def classical_gamma(self, output_bandedges=None):
        name = 'Gamma'
        if output_bandedges:
            return self.merge_blocks(name, output_bandedges)
        else:
            return self.block(name, '')

    def classical_hh(self, output_bandedges=None):
        name = 'HH'
        if output_bandedges:
            return self.merge_blocks(name, output_bandedges)
        else:
            return self.block(name, '')

    def classical_lh(self, output_bandedges=None):
        name = 'LH'
        if output_bandedges:
            return self.merge_blocks(name, output_bandedges)
        else:
            return self.block(name, '')

    def classical_so(self, output_bandedges=None):
        name = 'SO'
        if output_bandedges:
            return self.merge_blocks(name, output_bandedges)
        else:
            return self.block(name, '')

    def classical_bands(self):
        gamma = self.classical_gamma()
        hh = self.classical_hh()
        lh = self.classical_lh()
        so = self.classical_so()
        return self.lines(gamma, hh, lh, so)

    def classical_output_bandedges(self, averaged='yes', profiles=['Gamma', 'electron_fermi_level']):
        profiles = ' '.join(profiles)
        profiles = f'"{profiles}"'
        return self.equal_block('output_bandedges', dict(averaged=averaged, profiles=profiles))

    def classical_output_carrier_densities(self):
        return self.block('output_carrier_densities', '')

    def classical_output_intrinsic_density(self):
        return self.block('output_intrinsic_density', '')

    def classical_output_ionized_dopant_densities(self):
        return self.block('output_ionized_dopant_densities', '')

    def classical_block(self, *blocks):
        return self.merge_blocks('classical', *blocks)

    # - Poisson
    def poisson_output_potential(self):
        return self.block('output_potential', '')

    def poisson_output_electric_field(self):
        return self.block('output_electric_field', '')

    def poisson_newton_solver(self, iterations=30, search_steps=40, residual=1e-4):
        return self.equal_block('newton_solver',
                                dict(iterations=iterations, search_steps=search_steps, residual=residual))

    def poisson_debuglevel(self, value):
        return self.equal('debuglevel', value)

    def poisson_block(self, *blocks):
        return self.merge_blocks('poisson', *blocks)

    # - Currents
    def currents_output_mobilities(self):
        return self.block('output_mobilities', '')

    def currents_recombination_model(self, SRH='no', Auger='no', radiative='no', enable_generation='yes'):
        inputs = dict(SRH=SRH, Auger=Auger, radiative=radiative, enable_generation=enable_generation)
        kwargs = {}
        for key, value in inputs.items():
            if value:
                kwargs[key] = value
        return self.equal_block('recombination_model', kwargs)

    def currents_block(self, *blocks):
        return self.merge_blocks('currents', *blocks)

    # - Quantum
    def quantum_name(self, name):
        return self.equal('name', name)

    def quantum_coords(self, x, y=None, z=None):
        inputs = dict(x=x, y=y, z=z)
        kwargs = {}
        for key, value in inputs.items():
            if value:
                kwargs[key] = value
        points = [self.point(key, *value) for key, value in kwargs.items()]
        return self.lines(*points)

    def quantum_density(self, use=True):
        if use:
            value = 'no'
        else:
            value = 'yes'
        return self.equal('no_density', value)

    def quantum_boundary(self, x='neumann', y=None, z=None):
        inputs = dict(x=x, y=y, z=z)
        kwargs = {}
        for key, value in inputs.items():
            if value:
                kwargs[key] = value
        return self.equal_block('boundary', kwargs)

    def quantum_output_wavefunctions(self, max_num=5, amplitudes='no', probabilities='yes', all_k_points='yes'):
        return self.equal_block('output_wavefunctions',
                                dict(max_num=max_num, amplitudes=amplitudes, probabilities=probabilities,
                                     all_k_points=all_k_points))

    def quantum_gamma(self, num_ev=100):
        content = self.equal('num_ev', num_ev)
        return self.block('Gamma', content)

    def quantum_quantize_x(self):
        return self.block('quantize_x', '')

    def quantum_quantize_y(self):
        return self.block('quantize_y', '')

    def quantum_quantize_z(self):
        return self.block('quantize_z', '')

    def quantum_block(self, *blocks):
        region = self.merge_blocks('region', *blocks)
        return self.merge_blocks('quantum', region)

    # - Output
    def output_directory(self, path='output'):
        return self.equal('directory', path)

    def output_format(self, dim, value):
        return self.equal(f'format{dim}D', value)

    def output_section(self, name, dim=2, x=None, y=None, z=None, range_x=None, range_y=None, range_z=None):
        coords = dict(name=name, x=x, y=y, z=z)
        kwargs = {}
        for key, value in coords.items():
            if value is not None:
                kwargs[key] = value
        # dim = int(3 - (len(kwargs.keys()) - 1))

        coords = self.equal_lines(**kwargs)
        ranges = dict(range_x=range_x, range_y=range_y, range_z=range_z)
        kwargs = {}
        for key, value in kwargs.items():
            if value:
                kwargs[key] = value
        points = [self.point(key, value) for key, value in kwargs.items()]
        content = self.lines(coords, *points)
        content = self.add_indent(content)
        content = self.paragraph(content)
        return self.block(f'section{dim}D', content)

    def output_only_sections(self, value=False):
        value = str(value).lower()
        if value in ['true', 'yes', 'y']:
            value = 'yes'
        else:
            value = 'no'
        return self.equal('only_sections', value)

    def output_block(self, *blocks):
        return self.merge_blocks('output', *blocks)

    # - Run
    def run_solve_strain(self):
        return self.block('solve_strain', '')

    def run_solve_poisson(self):
        return self.block('solve_poisson', '')

    def run_solve_quantum(self):
        return self.block('solve_quantum', '')

    def run_outer_iteration(self, **kwargs):
        if not kwargs:
            return self.block('outer_iteration', '')
        else:
            return self.equal_block('outer_iteration', kwargs)

    def run_block(self, *blocks):
        return self.merge_blocks('run', *blocks)
