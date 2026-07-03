"""
Developed by Jules GILLY in November 2022 for a personal use
This file forms the class to transform the data from the user
    This files works with the class 'FEM - Beam Element'

BeamInfo (dictionary) needs to contain:
    - L: length of the beam
    - b: width of the beam
    - h: height of the beam
    - E: Young's modulus  
    - supports: Dictionary (keys: type and position)
                supports = { 1: {'Type': type1, 'Position': x1},
                             2: {'Type': type2, 'Position': x2}, And so on }
                where the type is one of the following: "Simply supported", "Roller", "Free", "Fixed"
    - distributedLoads: Dictionary (keys: type of loads, positions (xmin and xmax), values (pmin and pmax))
             dloads = { 1: {'Type': type1, 'xmin': xmin1, 'xmax': xmax1, 'pmin': pmin1, 'pmax': pmax1},
                        2: {'Type': type2, 'xmin': xmin2, 'xmax': xmax2, 'pmin': pmin2, 'pmax': pmax2}, And so on }
             where the type is one of the following: "Uniform", "Linear", "Trapezoidal"
    - pointLoads: Dictionary (keys: type of loads, position and value)
             ploads = { 1: {'Type': type1, 'Position': x1, 'P': P1},
                        2: {'Type': type2, 'Position': x2, 'P': P2}, And so on }
             where the type is one of the following: "Horizontal", "Vertical", "Moment"

Warning: sign convention!!
for distributed loads, positive value means down
for point loads, positive value means up for vertical load and counter clockwise for moment
"""
class element(object):
    def __init__(self, BeamInfo, nom_fichier):
        self.extractInfo(BeamInfo)
        self.nom_fichier = nom_fichier
        self.main()

    def extractInfo(self, BeamInfo):
        self.Length = BeamInfo["length"]
        self.b = BeamInfo["width"]
        self.h = BeamInfo["height"]
        self.E_modulus = BeamInfo["Young's Modulus"]
        self.supports = BeamInfo["supports"]
        self.p = BeamInfo["distributedLoads"]
        self.P = BeamInfo["pointLoads"]

    def main(self):
        import numpy as np

        # Pas FE
        maille = 0.01

        # number of nodes
        nnodes = int(self.Length / maille) + 1

        # number of elements
        nele = nnodes - 1

        # Area: list of the areas for each element of the beam
        A = [self.b*self.h]*nele

        # Young's Modulus: list of the Es for each element of the beam
        E = [self.E_modulus]*nele

        # Inertia: list of the inertias for each element of the beam
        I = [self.b*self.h**3/12]*nele

        # FE data
        nDOFs = 3 # number of DOFs per node
        x = np.zeros(nnodes) # position of nodes
        nodeDOFs = np.zeros((nnodes,3)) # DOFs associated at each nodes
        for i in range(nnodes):
            x[i] = i*maille
            nodeDOFs[i,:] = np.array([[i*3, i*3+1, i*3+2]])

        eleNumb = np.zeros((nele, 2), dtype = 'int32') # numbering of elements
        for i in range(nele):
            eleNumb[i,0] = int(i+1)
            eleNumb[i,1] = int(i+2)

        # fixity
        # Create empty fixity array
        fixity = np.array([['nan', 'nan', 'nan']]*nnodes)
        # Loop over the number of support 
        for _, info in self.supports.items():
            # Get the supported node number
            index, = np.where(x == float(info['Position']))
            # If statement to determine the type of support
            if info['Type'].lower() == "simply supported":
                # Modify the fixity array for fixed DOFs
                fixity[int(index),:] = np.array([[0, 0, 'nan']])
            elif info['Type'].lower() == "fixed":
                # Modify the fixity array for fixed DOFs
                fixity[int(index),:] = np.array([[0, 0, 0]])
            elif info['Type'].lower() == "roller":
                # Modify the fixity array for fixed DOFs
                fixity[int(index),:] = np.array([['nan', 0, 'nan']])
        
        # distributed loads p = self.p
        p = np.zeros((len(self.p), 5), dtype = object)
        for id, info in self.p.items():
            p[id - 1, :] = np.array(list([info['Type'], info['xmin'], info['xmax'], info['pmin'], info['pmax']]))

        # support loads: P = pointLoads
        P = np.zeros((len(self.P), 2))
        # Loop over the number of point loads
        for id, info in self.P.items():
            # Get the number of the node to which the load i is applied
            index,=np.where(x == float(info['Position']))
            # If statement to determine the type of point load
            if info['Type'].lower() == "horizontal":
                # Get the DOF associated with the type of load and the node
                dof = int(nodeDOFs[int(index),0])
                # Construct line i of the P array
                P[id - 1,:] = np.array([[dof, info['P']]])
            elif info['Type'].lower() == "vertical":
                # Get the DOF associated with the type of load and the node
                dof = int(nodeDOFs[int(index),1])
                # Construct line i of the P array
                P[id - 1,:] = np.array([[dof, info['P']]])
            elif info['Type'].lower() == "moment":
                # Get the DOF associated with the type of load and the node
                dof = int(nodeDOFs[int(index),2])
                # Construct line i of the P array
                P[id - 1,:] = np.array([[dof, info['P']]])
        
        # Dictionaries
        self.elementInfo = {'length': self.Length,
                       'Area': A,
                       'Young Modulus': E,
                       'Inertia': I,
                       'fixity': fixity,
                       'name': self.nom_fichier}
        self.problemData = {'loading': p,
                            'support loads': P
        }
        self.FEData = {'DOFs per node': nDOFs,
                  'number of nodes': nnodes,
                  'position of nodes': x,
                  'number of elements': nele,
                  'element numbering': eleNumb,
                  'DOFs numbering': nodeDOFs}
        
        