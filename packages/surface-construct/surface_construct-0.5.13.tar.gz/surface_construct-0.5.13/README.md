# 基于分层采样策略的催化剂表面位点全局分析

A Method with Stratified Sampling Strategy for Comprehensive Analysis of Catalyst Surface Composed of Multiple Sites



![表面位点全局分析](docs/surface_distribution_3d.jpg)



## 程序流程图  Program Workflow



![flowchart](docs/flowchart2.jpg)

## 重要的概念 Glossary

* 表面格点 Grid：以范德华或者共价键长等值面进行离散化得到，表现为 (xi, yi, zi) 三维坐标。

  ![Ru Grid](docs/Ru0001_grid.jpg)

* 表面向量 Vector：用来表征格点局部化学环境的向量表示方法，表现形式为 N 维的向量。

  * 本方法中我们使用正则化的距离向量表达，其中距离是与N个最近邻原子之间的距离。
  * 正则化是为了保证不同化学环境格点的区分度尽量大。我们这里使用距离的倒数作为正则化方法，即距离越远对化学环境的描述贡献越小。
  * 为了减小计算量，在进行向量操作之前要对向量进行降维。降维的标准是保证保留尽可能多的信息，默认信息丢失不超过 5%。

* 向量化 Vectorization:  将格点转化为向量的过程

  * 当前我们使用多点定位 Multilateration 进行向量化

    ![multilateration](docs/multilateration.jpg)

* 分层采样 Stratified sampling。根据“相似结构具有相似性质”的原理采样分层采样的策略对表面位点进行采样，降低计算量。

  ![stratified sampling](docs/stratified_sampling.jpg)

* 吸附结构

  ![adsorption structure](docs/adsorption_structure.jpg)

## 安装

`pip install -U surface-construct`

## 发布新版本 （only for 管理员）

python -m build
twine upload --verbose dist/*

## 使用方法 Manual

### 所需文件 Required Files

* `surface_reaction_sample.py`: 主流程文件

* `parameter.py`: 参数定义文件

* `POSCAR.0`: 表面结构文件

  * 注意：名字可以修改，与 `parameter.py` 设置一致
  * 设置需要固定的原子

* bsub 文件。在公司集群上提交，以下面的为例

  ```Bash
  #/bin/bash
  #BSUB -J Sampling
  #BSUB -q short
  #BSUB -n 28
  #BSUB -o out.%J.txt
  #BSUB -e error.%J.txt
  #BSUB -R span[ptile=28]
  module load old/intel18u4
  export OMP_NUM_THREADS=1
  export I_MPI_ADJUST_REDUCE=3
  workdir=`pwd`
  date
  
  export PATH="/export/home/renpengju/miniconda3/bin:$PATH"
  export VASP_PP_PATH=$HOME/vasp/mypps
  export VASP_SCRIPT=$workdir/run_vasp.py
  
  cat > run_vasp.py << EOF
  import os
  exitcode = os.system('mpirun -PSM2 /export/soft_old/vasp541/vasp.5.4.1/bin/vasp_gam')
  EOF
  
  python surface_reaction_sample.py > surface_reaction_sample.py.log
  
  date
  ```

### 参数设置 

注意：所有的参数均在 `parameter.py` 进行设置

```python
from ase.calculators.vasp import Vasp
import numpy as np

# 用户参数，以下参数必须设定，没有默认值
poscar = 'ru_0001_POSCAR'
atomnum = [7, 7]  # 吸附的原子序号， 第一个原子靠近表面
bondlength = 1.65  # 初始的键长
angle = [np.pi / 2, 0.0]  # 分子吸附的角度，[theta, phi_x]: [与 z 轴的角度，绕 z 轴的旋转角度(相对于x)]

# 以下参数可选，具有默认值
calc = Vasp(
    xc='PBE',
    gga='PE',
    kpts=(1, 1, 1),
    encut=400,
    setups='recommended',
    ncore=4,
    gamma=True,
    nelm=200,
    algo='fast',
    ismear=0,
    sigma=0.05,
    ibrion=-1,  # 不使用 vasp 自身的优化，必须是 -1
    ediff=1e-4,
    prec='normal',
    nsw=0,  # 不使用 vasp 优化，必须是 0
    lreal='Auto',
    lwave=True,  # 保存 WAVECAR 可以加速
    lcharg=False,
    ispin=1)

scan_type = 'transition_state'  # 扫描类型：'optimization'，'transition_state'
grid_interval = 0.1  # angstrom, 格点的间距
Nsample = 5  # 第一次采样的点
Niter = 3  # 最大迭代次数
fmax = 0.1  # 结构优化 force 的收敛标准
max_error = 0.01  # 表面采样的收敛标准
radii_type = 'covalent_radii'  # 半径选项：'vdw_radii'，'covalent_radii'
radii_factor = 1.1  # 原子半径系数
sampleproperty = {'phi_x': np.linspace(0, np.pi/3, 2, endpoint=False)}
```

### 手动添加格点能量信息

通过脚本 `append_sample.py`实现，打开之后，修改以下信息

```python
pkl_filename = 'surface_grid.pkl'
keep_old_sample = True  # 判断是否保留原有的采样的点
results = [
    '0_opt.traj',  # 支持 ase.traj, vasprun.xml 文件，仅读取最后优化后的结果
    '1_opt.traj',
    '2_opt.traj',
    '3_opt.traj',
    '4_opt.traj',
    '5_opt.traj',
    '6_opt.traj',
    '7_opt.traj',
    '8_opt.traj',
    '9_opt.traj',
]
```

运行: `python append_sample.py`

注意：文件夹下必须有 `parameter.py` 和相应的表面结构文件

注意：为了避免失误，再运行前对 `surface_grid.pkl` 进行备份



### [其他 ASE 优化算法](https://wiki.fysik.dtu.dk/ase/ase/optimize.html)

* BFGS, BFGSLineSearch, LBFGS, LBFGSLineSearch
* GPMin
* MDMin
* FIRE

各种优化算法的对比，参考[链接](https://wiki.fysik.dtu.dk/gpaw/devel/ase_optimize/ase_optimize.html)

**使用方法**

修改 `surface_reaction_sample.py` 其中的一行 

```
from ase.optimize import BFGS
```

改为

```
from ase.optimize import XXX as BFGS
```

注意：目前这只是权宜之计，后面会把相应的设置加入到 `parameter.py`

### Gaussian Process Regression 方法

高斯过程回归 GPR 的优点：

* 不仅可以返回回归函数，可以给出拟合的置信度。根据置信度，可以进行进一步差点，迭代进行可以系统地降低整个拟合误差。
* 可以灵活地选择 kernel 函数来适用于不同的场景。

GPR 最重要的参数是kernel的选择。根据格点向量的特点，我们使用添加噪音的 (RBF) (aka Gassian kernel, Squared Exponetial Kernel) kernel 函数：
$$
k(x_i,x_j)=\sigma^2 \exp(-{d(x_i,x_j)^2\over 2l^2}) + {noise\_level}
$$


其中 $l$ 代表 length scale, $\sigma ^2$ 是 output variance。 使用 scikit-learn 中的类进行构造，
$$
\text{Kernel = ConstantKernel}\times \text{RBF} + \text{WhiteKernel}
$$
其中 ConstantKernel 代表 output variance  $\sigma^2$, 因为 scikit-learn 内置的 RBF kernel 不包含这一项，WhiteKernel 将 noise_level 考虑进去，RBF 是 Radial Basis Function kernel。

**重要的参数**

* RBF kernel
  * Length Scale $l$：determines the length of the 'wiggles' in your function.  In general, you won't be able to extrapolate more than ℓ units away from your data. [^Duvenaud] 
  
    参考 [^BASC] 文献，此处我们设置实空间的 $l_{grid}=1 \text{\AA}$ ，变化范围[0.5, 2.0]，转化为向量空间的长度[^向量空间转化]。根据实际情况，我们使用非对称 anisotropic 的 RBF。
* Constant kernel

  * GPR 在训练之前将 y 数值进行正则化，因而此处设置为 1.0，且训练过程中不变化。

* White kernel

  * noise level 是一个经验的参数。根据 DFT 吸附和过渡态的常见误差的量级为 0.1 eV，将此数值绝对值定为 0.1。设置时需要根据 y 正则化的系数进行缩放。在拟合过程中，keep fixed。

* GPR

  * $\alpha$：参数用于防止过拟合，根据经验设置为 $10^{-5}$。 
  * n_restarts_optimizer：9，经验选择。
  * 其他数值使用默认值。




## 路线图 Roadmap

* v 0.4.1: 单原子和双原子分子表面吸附
* v 0.4.2: 双原子过渡态计算，扫描 phi 角度
* v 0.5: 多种表面采样方法
* v 0.6: 表面位点数据库
* v 0.7: 颗粒体系表面格点构造
* v 0.8: 多原子体系（内坐标受限体系）
* v 0.9: 完善用户界面、例子、教程
* v 1.0: 发布第一个正式版
* v 1.1: 孔材料体系格点构造
* v 1.2: 多原子体系（复杂内坐标体系）
* v 1.3: 团簇体系



## Reference

[^Duvenaud]: [The Kernel Cookbook: Advice on Covariance functions](https://www.cs.toronto.edu/~duvenaud/)]
[^BASC]: Shane Carr, Roman Garnett, Cynthia LoBASC: Applying Bayesian Optimization to the Search for Global Minima on Potential Energy Surfaces.
[^向量空间转化]: 计算实空间和向量空间的相邻格点距离的映射系数，根据此系数将实空间的距离转化为向量空间距离。

