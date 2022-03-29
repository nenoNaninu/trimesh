"""
Check things related to STL files
"""
try:
    from . import generic as g
except BaseException:
    import generic as g


class STLTests(g.unittest.TestCase):

    def test_header(self):
        m = g.get_mesh('featuretype.STL')
        # make sure we have the right mesh
        assert g.np.isclose(m.volume, 11.627733431196749, atol=1e-6)

        # should have saved the header from the STL file
        assert len(m.metadata['header']) > 0

        # should have saved the STL face attributes
        assert len(m.face_attributes['stl']) == len(m.faces)
        assert len(m.faces) > 1000
        # add a non-correlated face attribute, which should be ignored
        m.face_attributes['nah'] = 10

        # remove all faces except three random ones
        m.update_faces([1, 3, 4])
        # faces and face attributes should be untouched
        assert len(m.faces) == 3
        assert len(m.face_attributes['stl']) == 3
        # attribute that wasn't len(m.faces) shouldn't have been touched
        assert m.face_attributes['nah'] == 10

    def test_attrib(self):
        m = g.get_mesh('featuretype.STL')

        len_vertices = len(m.vertices)
        # assign some random vertex attributes
        random = g.np.random.random(len(m.vertices))
        m.vertex_attributes['random'] = random
        m.vertex_attributes['nah'] = 20

        # should have saved the STL face attributes
        assert len(m.face_attributes['stl']) == len(m.faces)
        assert len(m.faces) > 1000
        # add a non-correlated face attribute, which should be ignored
        m.face_attributes['nah'] = 10

        # remove all faces except three random ones
        m.update_faces([1, 3, 4])
        # faces and face attributes should be untouched
        assert len(m.faces) == 3
        assert len(m.face_attributes['stl']) == 3
        # attribute that wasn't len(m.faces) shouldn't have been touched
        assert m.face_attributes['nah'] == 10

        # check all vertices are still in place
        assert m.vertex_attributes['nah'] == 20
        assert g.np.allclose(random, m.vertex_attributes['random'])
        assert len(m.vertices) == len_vertices

        # remove all vertices except four
        v_mask = [0, 1, 2, 3]
        m.update_vertices(v_mask)
        # make sure things are still correct
        assert m.vertex_attributes['nah'] == 20
        assert g.np.allclose(m.vertex_attributes['random'], random[v_mask])
        assert len(m.vertices) == len(v_mask)

    def test_ascii_multibody(self):
        s = g.get_mesh('multibody.stl')
        assert len(s.geometry) == 2

    def test_empty(self):
        # demo files to check
        empty_files = ['stl_empty_ascii.stl',
                       'stl_empty_bin.stl']

        for empty_file in empty_files:
            e = g.get_mesh('emptyIO/' + empty_file)

            # result should be an empty scene without vertices
            assert isinstance(e, g.trimesh.Scene)
            assert not hasattr(e, 'vertices')

            # create export
            try:
                e.export(file_type='ply')
            except BaseException:
                return
            raise ValueError("Shouldn't export empty scenes!")


if __name__ == '__main__':
    g.trimesh.util.attach_to_log()
    g.unittest.main()
