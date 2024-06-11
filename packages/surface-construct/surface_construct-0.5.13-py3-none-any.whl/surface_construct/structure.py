import itertools
from hashlib import md5

import ase
import networkx as nx
import numpy as np

from surface_construct.atoms import adj_matrix, topo_identity, topodist_matrix, coordnum_adj, bondlist, get_sub_matrix


# TODO: 使用 adj 的 eigvalsh 代替 dist？
# TODO：使用 scipy 的 eigvalsh 代替 np？ 与 networkx.linalg.spectrum 一致
# TODO：cus 的保存：{array_id: [{'array':[], 'atoms':[], 'site_idx':[], 'topo_id':''}]}
# TODO: 只有当 array_id 相同的时候才计算 topo_id, 如果 topo_id 不相同则保存


class Structure:
    def __init__(self, atoms=None, bulk_cn=None):
        """
        TODO: bridge hollow 位点；
        :param atoms: ase.Atoms
        :param bulk_cn: int, list or dict.
        """
        self._hollow_topo_dict = None
        self._bridge_topo_dict = None
        self._hollow_site_idx = None
        self._hollow_topo_array = None
        self._hollow_topo_id = None
        self._bridge_site_idx = None
        self._bridge_topo_array = None
        self._bridge_topo_id = None
        atoms_type = sorted([i for i in set(atoms.numbers)])  # 默认原子顺序是从小到大
        self.atoms_type = atoms_type
        self._type_permutation = list(itertools.product(atoms_type, atoms_type))  # 原子类型组合
        self._type_combination = [(i, i) for i in atoms_type] \
                                 + list(itertools.combinations(atoms_type, 2))  # 原子类型组合
        self.natoms = len(atoms)
        self._atoms = atoms
        self._graph = None

        self._adj_matrix = None
        self._topodist_matrix = None
        self._topo_id = None
        self._all_cn = None
        self._cus_cn = None
        self._cus_idx = None
        self._cus_topo_id = None
        self._cus_topo_array = None
        self._cus_topo_dict = None
        self._cus_graph = None
        self._cus_site_idx = None
        self._site_topo_dict = None
        self.bulk_cn = bulk_cn  # 体相原子的配位数，可能是 int 或者 list
        self._locality = None  # 默认局域原子考虑第二层紧邻原子

        self._site_idx = None  # 用来临时存放 site_idx
        self.gcn = None  # TODO: GCN

    @property
    def atoms(self):
        if self._atoms is None:
            pass  # 重构 atoms
        return self._atoms

    @atoms.deleter  # 删除的主要目的是为了节省空间，在 JSON 构造之前进行删除，构造一个 JSON 化的atoms
    def atoms(self):
        self._atoms = None

    @property
    def locality(self):
        if self._locality is None:
            self._locality = 2
        return self._locality

    @locality.setter
    def locality(self, v):
        if self._locality != v:
            self._locality = v
            # 重新计算 cus_topo_id 相关项
            self._cus_topo_id = None
            self._cus_topo_array = None
            self._cus_topo_dict = None
        else:
            pass

    @property
    def adj_matrix(self):
        if self._adj_matrix is None:
            self._adj_matrix = adj_matrix(self.atoms)
        return self._adj_matrix

    @property
    def topodist_matrix(self):
        if self._topodist_matrix is None:
            self._topodist_matrix = topodist_matrix(self.adj_matrix)
        return self._topodist_matrix

    @property
    def topo_id(self):
        if self._topo_id is None:
            self._topo_id = topo_identity(self.topodist_matrix)

        return self._topo_id

    @property
    def bulk_cn(self):
        """
        Now use the common value for fcc or hcp crystal.
        TODO: 改成更通用的函数，加入各种元素的默认配位数
        参考体相的配位数
        :return: dict, {(atom_number1, atom_number2): CN}
        """
        if self._bulk_cn is None:
            self._bulk_cn = [{j: 12 for j in self._type_permutation}] * self.natoms

        return self._bulk_cn

    @bulk_cn.setter
    def bulk_cn(self, v):
        if type(v) in (int,):
            self._bulk_cn = [{j: v for j in self._type_permutation}] * self.natoms
        elif type(v) in (dict,):
            # 如果找不到对应的 key，反转顺序试试，如果还没有，使用默认值，并给出警告
            new_v = v.copy()
            for t in self._type_permutation:
                if t not in v:
                    if (t[1], t[0]) in v:
                        new_v[t] = v[(t[1], t[0])]
                    else:
                        new_v[t] = 12  # 使用默认值
                        print("Warning: Not set CN for", t, ", use default value 12.")
            for i in range(self.natoms):
                self._bulk_cn = [{j: new_v[j] for j in self._type_permutation}] * self.natoms
        else:
            raise "Wrong input of bulk_cn!"

    @property
    def all_cn(self):
        if self._all_cn is None:
            self._all_cn = coordnum_adj(self.adj_matrix)
        return self._all_cn

    @property
    def cus_idx(self):
        """
        配位不饱和原子的序号。配位不饱和是相对于一个给定值，或者一个对应的列表.
        :return:
        """
        if self._cus_idx is None:
            cus_cn = [{bcn[t] - icn[t] for t in self._type_permutation}
                      for bcn, icn in zip(self.bulk_cn, self.all_cn)]
            # 不需要保存 cus_cn，调用 self.all_cn[idx] 就可以。没有发现其他地方要用 cus_cn
            # 找到 any 不为 0 的 idx
            self._cus_idx = [i for i, v in enumerate(cus_cn) if any(v)]
        return self._cus_idx

    @property
    def cus_topo_id(self):
        """
        TODO: 求解过程写成重复可用的函数
        TODO: 使用第一近邻的 topo_id 不一定能保证 结构的唯一性。可能要考虑当 topo_id 相同时，比较 topo_array 是否相同。
              如果不相同，则使用 topo_array 生成的 id。
              使用双 id？

        CUS 的 topo_id。也是 top 位点的 id
        :return: list, 所有 CUS 的 topo_id
        """
        if self._cus_topo_id is None:
            self._cus_topo_id = []
            self._cus_topo_array = []
            self._cus_site_idx = []
            for idx in self.cus_idx:
                topo_id, topo_array, site_idx = self.get_site_array([idx])
                self._cus_topo_array.append(topo_array)
                self._cus_topo_id.append(topo_id)
                if self.natoms == 1:
                    self._cus_site_idx.append([idx])
                else:
                    self._cus_site_idx.append(list(site_idx) + [idx])

        return self._cus_topo_id

    @property
    def cus_topo_array(self):
        if self._cus_topo_array is None:
            _ = self.cus_topo_id

        return self._cus_topo_array

    @property
    def cus_site_idx(self):
        if self._cus_site_idx is None:
            _ = self.cus_topo_id

        return self._cus_site_idx

    @property
    def cus_topo_dict(self):
        if self._cus_topo_dict is None:
            self._cus_topo_dict = {i: {'array': j, 'site_idx': k, 'atoms': self.atoms[k]} for i, j, k in
                                   zip(self.cus_topo_id, self.cus_topo_array, self.cus_site_idx)}

        return self._cus_topo_dict

    @property
    def cus_graph(self):
        """
        构建 cus 原子的 Graph
        :return:
        """
        if self._cus_graph is None:
            self._cus_graph = self.graph.subgraph(self.cus_idx)
        return self._cus_graph

    @property
    def graph(self):
        if self._graph is None:
            bond_list = bondlist(self.adj_matrix)
            self._graph = nx.Graph()
            self._graph.add_nodes_from(range(self.natoms))
            self._graph.add_edges_from(bond_list)
        return self._graph

    @property
    def bridge_topo_id(self):
        """
        得到 bridge site array 和 topo_id。根据cus原子的图，找到所有的边，即是bridge site。
        组合的方法：直接加和，这样得到的与top 长度相同，不过会损失一些信息。第二种，堆叠，这样要对其进行排序。
        :return: {topo_id: array}
        """
        if self._bridge_topo_id is None:
            self._bridge_topo_id = []
            self._bridge_topo_array = []
            self._bridge_site_idx = []
            for idx in self.cus_graph.edges:
                topo_id, topo_array, site_idx = self.get_site_array(idx)
                self._bridge_topo_array.append(topo_array)
                self._bridge_topo_id.append(topo_id)
                self._bridge_site_idx.append(list(site_idx) + [i for i in idx])

        return self._bridge_topo_id

    @property
    def bridge_topo_array(self):
        if self._bridge_topo_array is None:
            _ = self.bridge_topo_id

        return self._bridge_topo_array

    @property
    def bridge_site_idx(self):
        if self._bridge_site_idx is None:
            _ = self.bridge_topo_id

        return self._bridge_site_idx

    @property
    def bridge_topo_dict(self):
        if self._bridge_topo_dict is None:
            self._bridge_topo_dict = {i: {'array': j, 'site_idx': k, 'atoms': self.atoms[k]} for i, j, k in
                                      zip(self.bridge_topo_id, self.bridge_topo_array, self.bridge_site_idx)}

        return self._bridge_topo_dict

    @property
    def hollow_topo_id(self):
        """
        TODO: 使用 nx.minimum_cycle_basis 得不到所有的 hollow 位点，是否能得到所有的类型也并没有经过细致的验证

        :return:
        """
        if self._hollow_topo_id is None:
            self._hollow_topo_id = []
            self._hollow_topo_array = []
            self._hollow_site_idx = []
            for idx in nx.minimum_cycle_basis(self.cus_graph):
                topo_id, topo_array, site_idx = self.get_site_array(idx)
                self._hollow_topo_array.append(topo_array)
                self._hollow_topo_id.append(topo_id)
                self._hollow_site_idx.append(list(site_idx) + [i for i in idx])

        return self._hollow_topo_id

    @property
    def hollow_topo_array(self):
        if self._hollow_topo_array is None:
            _ = self.hollow_topo_id

        return self._hollow_topo_array

    @property
    def hollow_site_idx(self):
        if self._hollow_site_idx is None:
            _ = self.hollow_topo_id

        return self._hollow_site_idx

    @property
    def hollow_topo_dict(self):
        if self._hollow_topo_dict is None:
            self._hollow_topo_dict = {i: {'array': j, 'site_idx': k, 'atoms': self.atoms[k]} for i, j, k in
                                      zip(self.hollow_topo_id, self.hollow_topo_array, self.hollow_site_idx)}

        return self._hollow_topo_dict

    @property
    def site_topo_dict(self):
        """
        包含 top, bridge, hollow 位
        :return:
        """
        if self._site_topo_dict is None:
            self._site_topo_dict = self.cus_topo_dict.copy()
            self._site_topo_dict.update(self.bridge_topo_dict)
            self._site_topo_dict.update(self.hollow_topo_dict)

        return self._site_topo_dict

    def get_site_array(self, idx_list):
        """
        从 adj_matrix 得到位点的向量。其中的id 包含两个，一个第一近邻层原子配位 array_id，另一个为 topo_id
        :param idx_list: list, 位点的序号
        :return:
        """

        # 第一层：各个元素的数目
        atomnumber_lst = [self.atoms[idx].number for idx in idx_list]
        atomnumber_count = [atomnumber_lst.count(a) for a in self.atoms_type]

        site_array = atomnumber_count
        nodes = idx_list
        idx_set = set(idx_list)
        site_idx = []
        for layer in range(self.locality):
            # 第一近邻原子各个元素的数目
            nodes = set([j for i in nodes for j in self.graph.neighbors(i)])
            if layer == 0 and len(nodes) > 0:  # 仅仅保存第一近邻原子位点
                site_idx = set.difference(nodes, idx_set)  # 存入临时位点, 需要剔除 idx，否则会重复
            atomnumber_lst = [self.atoms[idx].number for idx in nodes]
            atomnumber_count = [atomnumber_lst.count(a) for a in self.atoms_type]
            site_array += atomnumber_count

            # 第一近邻原子各个化学键的统计
            subgraph = self.graph.subgraph(nodes).to_directed()  # 转化成有向图，用来统计所有的 uv 组合
            bond_lst = [(self.atoms[u].number, self.atoms[v].number) for u, v in subgraph.edges()]
            bond_count = [bond_lst.count(b) for b in self._type_combination]
            # (i,i) 被统计多了一倍，要除掉
            for i in range(len(self.atoms_type)):
                bond_count[i] = int(bond_count[i] / 2)
            site_array += bond_count

        # 得到 topo_id
        # 首先取出相应的 topo_dist_matrix
        dm = get_sub_matrix(self.topodist_matrix, site_idx)
        topo_id = topo_identity(dm)
        # 双 id
        content = ' '.join(map(str, site_array))
        array_id = md5(content.encode('utf-8')).hexdigest()
        site_id = (topo_id, array_id)
        return site_id, site_array, site_idx

    def todict(self):
        """
        TODO:
        需要被保存的量，主要用于节省计算时间和内存。
        atoms, adj_matrix, topo_id, cus_idx, cus_topo_id
        :return: 一个字典，用于 JSON 化
        """
        dct = {
            'atoms': self.atoms.todict(),
            'adj_matrix': self.adj_matrix,
            'topo_id': self.topo_id,
            'cus_idx': self.cus_idx,
            'cus_topo_id': self.cus_topo_id,
            'cus_topo_array': self.cus_topo_array,
            'cus_topo_dict': self.cus_topo_dict,
            'bulk_cn': self.bulk_cn,
            'all_cn': self.all_cn,
        }
        return dct

    @classmethod
    def fromdict(cls, dct):
        """
        从 json 中重构当前 object. 会覆盖掉现有的所有属性
        :return:
        """
        atoms = ase.Atoms.fromdict(dct['atoms'])
        struct = cls(atoms=atoms, bulk_cn=dct['bulk_cn'])
        struct._adj_matrix = dct['adj_matrix']
        struct._topo_id = dct['topo_id']
        struct._cus_idx = dct['cus_idx']
        struct._cus_topo_id = dct['cus_topo_id']
        struct._cus_topo_array = dct['cus_topo_array']
        struct._cus_topo_dict = dct['cus_topo_dict']
        struct._all_cn = dct['all_cn']

        return struct

    def copy(self):
        """
        Copy 一个新的结构，相当于从 fromdict 创建一个新的，节省时间
        :return:
        """
        dct = self.todict()
        return self.__class__.fromdict(dct)

    def delete(self, idx):
        """
        删除 idx 相应的原子
        :param idx: int 或者 list
        :return: 新的 obj
        """
        atoms = self.atoms.copy()
        del atoms[idx]
        # 把对应的 adj_matrix idx 删除
        adj = self.adj_matrix.copy()
        adj = np.delete(adj, idx, 0)
        adj = np.delete(adj, idx, 1)

        struct = self.__class__(atoms, self.bulk_cn)
        struct._adj_matrix = adj

        return struct

    def sub_structure(self, idx_lst):
        """
        从 idx list 构建新的 object
        :param idx_lst:
        :return:
        """
        atoms = self.atoms[idx_lst]
        adj = get_sub_matrix(self.adj_matrix, idx_lst)

        struct = self.__class__(atoms, self.bulk_cn)
        struct._adj_matrix = adj

        return struct


class TopoSite:
    """
    位点类，包含位点的结构，array_id，topo_id，以及 tag。
    tag定义：0 是吸附位点，1 是第一近邻原子，以此类推
    """

    def __init__(self, atoms, neighbor_list, adsorbate=None):
        """

        :param atoms: ase.Atoms
        :param neighbor_list: list in list, 近邻原子的序号，根据配位层数依次排列
        """
        self._topodist_matrix = None
        self._adj_matrix = None
        self.atoms = atoms
        self.neighbor_list = neighbor_list
        if adsorbate is None:
            self.adsorbate = 'X'
        tags = [(nei, idx) for idx, neighbors in enumerate(neighbor_list) for nei in neighbors]
        tags = [t[1] for t in sorted(tags, key=lambda x: x[0])]
        self.atoms.set_tags(tags)  # 为了显示
        self._topo_id = None
        self._array_id = None

    @property
    def adj_matrix(self):
        if self._adj_matrix is None:
            self._adj_matrix = adj_matrix(self.atoms)
        return self._adj_matrix

    @adj_matrix.setter
    def adj_matrix(self, v):
        self._adj_matrix = v

    @property
    def topodist_matrix(self):
        if self._topodist_matrix is None:
            self._topodist_matrix = topodist_matrix(self.adj_matrix)
        return self._topodist_matrix

    @topodist_matrix.setter
    def topodist_matrix(self, v):
        self._topodist_matrix = v

    @property
    def topo_id(self):
        if self._topo_id is None:
            self._topo_id = topo_identity(self.topodist_matrix)
        return self._topo_id

    @topo_id.setter
    def topo_id(self, v):
        self._topo_id = v


class SurfaceSite:
    def __init__(self,
                 surface=None,
                 adsorbate=None,
                 vector=None,
                 xyz=None,
                 properties=None,
                 calc=None,
                 construct_para=None,
                 energy_ref=None,
                 ):
        pass

    def todict(self):
        """
        Export site to dict
        :return: dict
        TODO: dict structure
            {
                "MD5": "ABCDEF1231341234123123123", NO
                "MD5short": "ABCDEF", NO
                "vector": [0.0, 0.0, 0.0],  NO
                "property": {  NO
                    "energy": 0.0,  NO
                    "trans-state": 0  NO
                },
                "adsorbate": {},  YES
                "element": [1, 2],  NO
                "construct_para": {  NO
                    "method": "MLAT",
                    "radius": 1.0,
                    "r_type": "VDW",
                    "r_scale": 1.0
                },
                "surface": {},  NO
                "xyz": [0.0, 0.0, 0.0],  NO
                "calc_para": {},  NO
                "energy_ref": 0.0  NO
            }
        """
        pass
