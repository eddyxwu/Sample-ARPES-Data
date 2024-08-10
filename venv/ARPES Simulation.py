import numpy as np
import chinook.build_lib as build_lib
import chinook.operator_library as operators
from chinook.ARPES_lib import experiment

a,c = 5.0,5.0
avec = np.array([[np.sqrt(0.5)*a,np.sqrt(0.5)*a,0],
[np.sqrt(0.5)*a,-np.sqrt(0.5)*a,0],
[0,0,c]])

kpoints = np.array([[0.5,0.5,0.0],[0.0,0.0,0.0],[0.5,-0.5,0.0]])
labels = np.array(['$M_x$','$\\Gamma$','$M_y$'])



kdict = {'type':'F',
'avec':avec,
'pts':kpoints,
'grain':200,
'labels':labels}

k_object = build_lib.gen_K(kdict)

spin = {'bool':True,  #include spin-degree of freedom: double the orbital basis
'soc':True,    #include atomic spin-orbit coupling in the calculation of the Hamiltonian
'lam':{0:0.5}} #spin-orbit coupling strength in eV, require a value for each unique species in our basis

Sb1 = np.array([0.0,0.0,0.0])
Sb2 = np.array([np.sqrt(0.5)*a,0,0])

basis = {'atoms':[0,0], #two equivalent atoms in the basis, both labelled as species #0
'Z':{0:51},     #We only have one atomic species, which is antimony #51 in the periodic table.
'orbs':[['51x','51y','51z'],['51x','51y','51z']], #each atom includes a full 5p basis in this model, written in n-l-xx format
'pos':[Sb1,Sb2], #positions of the atoms, in units of Angstrom
'spin':spin} #spin arguments.

basis_object = build_lib.gen_basis(basis)

Ep = 0.7
Vpps = 0.25
Vppp = -1.0
VSK = {'051':Ep,'005511S':Vpps,'005511P':Vppp}
cutoff = 0.72*a

V1 = {'051':Ep,'005511S':Vpps,'005511P':Vppp}
V2 = {'005511S':Vpps/a,'005511P':Vppp/a}
VSK = [V1,V2]

cutoff = [0.8*a,1.1*a]

hamiltonian = {'type':'SK',     #Slater-Koster type Hamiltonian
      'V':VSK,          #dictionary (or list of dictionaries) of onsite and hopping potentials
       'avec':avec,     #lattice geometry
      'cutoff':cutoff,  #(cutoff or list of cutoffs) maximum length-scale for each hoppings specified by VSK
      'renorm':1.0,     #renormalize bandwidth of Hamiltonian
       'offset':0.0,    #offset the Fermi level
      'tol':1e-4,       #minimum amplitude for matrix element to be included in model.
      'spin':spin}      #spin arguments, as defined above

TB = build_lib.gen_TB(basis_object,hamiltonian,k_object)

TB.Kobj = k_object
TB.solve_H()
TB.plotting()

px = operators.fatbs(proj=[0,3,6,9],TB=TB,Elims=(-5,5),degen=True)
py = operators.fatbs(proj=[1,4,7,10],TB=TB,Elims=(-5,5),degen=True)
pz = operators.fatbs(proj=[2,5,8,11],TB=TB,Elims=(-5,5),degen=True)
#The degen flag averages over degenerate states. All states are at least two-fold degenerate,
#so this flag should certainly be on here.

LdS_matrix = operators.LSmat(TB)
LdS = operators.O_path(LdS_matrix,TB,degen=True)

arpes = {'cube':{'X':[-0.628,0.628,300],'Y':[-0.628,0.628,300],'E':[-0.05,0.05,50],'kz':0.0}, #domain of interest
'hv':100,                          #photon energy, in eV
'T':10,                           #temperature, in K
'pol':np.array([1,0,-1]),           #polarization vector
'SE':['constant',0.02],            #self-energy, assume for now to be a constant 20 meV for simplicity
'resolution':{'E':0.02,'k':0.02}}  #resolution

arpes_experiment = experiment(TB,arpes) #initialize experiment object
arpes_experiment.datacube() #execute calculation of matrix elements

I,Ig,ax = arpes_experiment.spectral(slice_select=('w',0.0))



