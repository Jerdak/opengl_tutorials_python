#! /usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes

class PackedVertex(object):
    libc_name = ctypes.util.find_library("c")
    libc = ctypes.CDLL(libc_name)
    
    libc.memcmp.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t)
    def __init__(self,pos,uv,norm):
        self.position = pos
        self.uv = uv
        self.normal = norm

    def __hash__(self):
        return hash((tuple(self.position),tuple(self.uv),tuple(self.normal)))

    def __eq__(self,other):
        """ Compare PackedVertex objects at the byte level

            ctype arrays don't allow direct comparisons ([1]) so instead
            do a memory comparison ([2]), similar to what was done in the original
            .cpp tutorials.  

            The main difference is that std::map defines equality as a 
            reflexive comparison because std::map's are ordered,
            unlike Python dict.  That means instead of looking for values
            >0 like in the original vboindexer.cpp you need to look for
            values == 0 which denote memory block equality.

            refs:
                [1] - http://stackoverflow.com/questions/25159248/compare-ctypes-arrays-without-additional-memory
                [2] - http://www.cplusplus.com/reference/cstring/memcmp/
        """
        a = self.libc.memcmp(self.position, other.position, ctypes.sizeof(self.position))
        b = self.libc.memcmp(self.normal, other.normal, ctypes.sizeof(self.normal))
        c = self.libc.memcmp(self.uv, other.uv, ctypes.sizeof(self.uv))
        return (a==0 and b == 0 and c == 0)


def getSimilarVertexIndex_fast(packed,vertex_to_out_index):
    if packed not in vertex_to_out_index:
        return False,None
    else:
        return True,vertex_to_out_index[packed]

def indexVBO(vertices,uvs,normals):
    vertex_to_out_index = {}

    out_verts = []
    out_uvs = []
    out_normals = []
    out_indices = []

    found_count = 0
    for i,vertex in enumerate(vertices):
        packed = PackedVertex(vertices[i],uvs[i],normals[i])
        found,index = getSimilarVertexIndex_fast(packed,vertex_to_out_index)


        if found:
            out_indices.append(index)
            found_count += 1
        else:
            out_verts.append(vertices[i])
            out_uvs.append(uvs[i])
            out_normals.append(normals[i])
            new_index = len(out_verts)-1
            out_indices.append(new_index)

            vertex_to_out_index[packed] = new_index

    print("Found %d duplicate vertices creating the VBO"%(found_count))
    return out_verts,out_uvs,out_normals,out_indices



if __name__ == "__main__":
    p1 = PackedVertex([1,2,3],[4,5,6],[7,8,9])
    p2 = PackedVertex([1,2,3],[4,5,6],[7,8,9])
    p3 = PackedVertex([1,2,3],[4,5,6],[7,8,10])

        
    d = {}
    d[p1] = 0
    assert(d[p1] == 0)
    assert(d[PackedVertex([1,2,3],[4,5,6],[7,8,9])] == 0)
    assert(p1 in d)
    assert(p2 in d)

    assert(p3 not in d)
    d[p3] = 1
    assert(p3 in d)

    del d[p1]
    assert(p1 not in d)

    del d[p3]
    assert(p3 not in d)