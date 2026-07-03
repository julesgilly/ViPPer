"""
Developed by Jules GILLY in September 2022 for a personal use
This file forms the finite element model of a uniform beam system and solves it
    This files works with the class 'Elements'

Inputs variables:
    Material and dimensions data:
        E: Beam's Young's modulus
        A: Beam's cross-sectional area
        I: Beam's inertia
        Length: Beam's length
        fixity:  prescribed displacements for node i's 3 d.o.f.
                 Note: A free d.o.f. will have a value of NaN
                       Example: a = float("nan")
                                print(math.isnan(a)) returns True
                 fixity(i,1) = prescribed disp. in global X direction
                 fixity(i,2) = prescribed disp. in global Y direction
                 fixity(i,3) = prescribed rotation about global Z axis
        orientation: orientation of the beam's elements
        
    Problem data:
        distributedLoad: Array (size: numberOfloads x 5) containing, for every loads, the type of load, x_min and x_max, p_min and p_max
                         distributedLoad = ['type', x_min, x_max, p_min, p_max  (Load 1)
                                            And so on]
        supportLoad: Array (size: numberOfloads x 2) containing, for every loads, the number of the DOFs at which P is applied, value: P
                         nodalLoad = [ #DOF, P  (Load 1)
                                      And so on]
        p_min, p_max: maximum and minimum value of a load (minimum value is defined as the value of the load closest to the 'beginning' of the beam)
        x_min, x_max: maximum and minimum location of maximum and minimum load on element
    
    Finite element data:
        nele: number of elements
        nnodes: number of nodes
        nodeNumb: vector of nodes numbers
        nDOFs: number of DOfs per node ( = 3 in this case)
        eleNumb: array containing the numbers of the nodes for each element
                 eleNumb = [1 2   (Element 1)
                            3 4   (Element 2)
                            5 6]  And so on
        nodeDOFs: numbering of the nodes' DOFs
                  nodeDOFs = [1 2 3   (node 1's DOFs)
                              4 5 6    (node 2's DOFs)
                              7 8 9]   And so on 
        x: vector of nodes' horizontal position
        y: vector of nodes' vertical position
        h: vector of element's lengths
    

Output variables:
    Finite element data:
        K_i: Element stiffness matrix
        K: (Global) stiffness matrix
        f_i: Element load vector
        f: (Global) load vector
        uHat: FE displacement approximation at all nodes x_i
        
Limitations:
    - Only works for elements with a Young's modulus E and an Inertia I constant over the element
    - Beam must not be oriented
    - Only cnsidering linearly and uniformly distributed loads

Improvement:
     - Create functions to write a document showing the results using ReportLab
""" 
import numpy as np 

class BeamFEM(object):
    def __init__(self, elementInfo, problemData, FEData):
        self.extractData(elementInfo, problemData, FEData)
        self.main()
        self.plot(elementInfo)
        self.end_Data()
    
    def extractData(self, elementInfo, problemData, FEData):
        # Extract miscellaneous variables:
        # Variables related to the element
        try:
            self.A = elementInfo['Area']
            self.E = elementInfo['Young Modulus']
            self.I = elementInfo['Inertia']
            self.fixity = elementInfo['fixity']
            
            # Variables related to the problem
            self.p = problemData['loading']
            self.P = problemData['support loads']
            
            # Variables related to the Finite Element method
            self.nDOFs = FEData['DOFs per node']
            self.nnodes = FEData['number of nodes']
            self.x = FEData['position of nodes']
            self.nele = FEData['number of elements']
            self.eleNumb = FEData['element numbering']
            self.nodeDOFs = FEData['DOFs numbering']
        except KeyError as e:
            raise ValueError(f"Missing key in input data : {e}")
        
        self.positionEle = self.positionElement(self.nele, self.x, self.eleNumb)
        self.freeNodeNumb, self.supportNodeNumb, self.vertSupportNodeNumb, self.displacedNodeNumb, self.delta_fn = self.nodeNumbering(self.fixity, self.nodeDOFs)
    
    def main(self):
        # import modules
        import time
        
        t1 = time.time()
        
        # Create variables for computation
        K = np.zeros((self.nnodes*self.nDOFs, self.nnodes*self.nDOFs))
        f = np.zeros((self.nnodes*self.nDOFs, 1))
        displacement = np.zeros((self.nnodes*self.nDOFs, 1))
        
        # To get more precise results, increase this value to at least 500
        # To get faster results, decrease this value but no lower than 100
        # To get good results and good computation time, use a value between 250-350
        numberOfIntegrationPoint = 250
        
        # Loop over the number of elements
        for i in range(self.nele):
            # For each element:
                
            # Extract the value of the area
            Area  = self.A[i]
            
            # Extract the value for the element's Young's modulus
            E_modulus =self.E[i]
            
            # Extract the value of the elemtn's inertia
            Inertia = self.I[i]
            
            # Compute the position of the start node and end node
            x_i = self.positionEle[i,0]
            x_ip1 = self.positionEle[i,1]
            
            # Compute the element stiffness matrix
            K_i = self.elementStiffnessMatrix(x_i, x_ip1, numberOfIntegrationPoint, E_modulus, Area, Inertia)
            
            # Compute the element load vector
            f_i = self.elementLoadVector(x_i, x_ip1, self.p, numberOfIntegrationPoint)
            
            # Assemble the global stiffness matrix
            K[self.eleNumb[i,0]*3-3:self.eleNumb[i,1]*3, self.eleNumb[i,0]*3-3:self.eleNumb[i,1]*3] += K_i
            
            # Assemble the global load vector
            f[self.eleNumb[i,0]*3-3:self.eleNumb[i,1]*3] += f_i
            
        # Extract from the global matrices, the reduced matrices (at free DOFs)
        reducedK, reducedf= self.reducedGlobalMatrices(K, f, self.freeNodeNumb)
        F = self.sollicitationSupport(self.P, self.nnodes, self.nDOFs)
        reducedf -= F[self.freeNodeNumb]
        # Extract the free-displaced stiffness matrix
        Kfn = K[np.ix_(self.freeNodeNumb, self.displacedNodeNumb)]

        # Compute the displacements at the free DOFs
        uhat = np.linalg.inv(reducedK).dot(-reducedf-Kfn.dot(self.delta_fn))
        
        # Construct the vector of total displacements
        displacement[np.ix_(self.freeNodeNumb)] = uhat
        displacement[np.ix_(self.displacedNodeNumb)] = self.delta_fn
        
        # Construct vectors of the different types of displacement
        verticalDisplacement = displacement[1:displacement.shape[0]:3]
        pente = displacement[2:displacement.shape[0]:3]
        verticalReaction = K.dot(displacement)[self.vertSupportNodeNumb]
        
        # Compute Moment and Shear Force
        
        # Modify the displacement vector to get a matrix for which the columns 
        # are the displacements for each element
        beamDOFsDisplacements = np.reshape(displacement, (self.nDOFs, self.nnodes), order = 'F')
        rollBeamDOFsDisplacements = np.roll(beamDOFsDisplacements, -1)
        beamDOFsDisplacements = np.delete(np.insert(beamDOFsDisplacements, self.nDOFs, rollBeamDOFsDisplacements, axis = 0), [0,3], axis = 0)
        beamDOFsDisplacements = np.delete(beamDOFsDisplacements, -1, axis = 1)
        
        # Create an empty array to store the values of the moment
        moment = np.zeros((self.nele, 2))
        shearForce = np.zeros((self.nele, 2))
        
        # Loop over the number of elements
        for i in range(self.nele):
            # For each element:
            
            # Extract the value for the element's Young's modulus
            E_modulus = self.E[i]
            
            # Extract the value of the elemtn's inertia
            Inertia = self.I[i]
            
            # Compute the position of the start node and end node
            x_i = self.positionEle[i,0]
            x_ip1 = self.positionEle[i,1]
            
            # Compute the B matrix at xi and xip1
            B_i = self.derivativesShapeFunctionsVector(x_i, x_i, x_ip1)
            B_ip1 = self.derivativesShapeFunctionsVector(x_ip1, x_i, x_ip1)
            
            # Compute the derivative of the B-matrix
            C = self.thirdDerivativesShapeFunctionsVector(x_i, x_ip1)
            
            # Compute the moments at the nodes of the element
            m_i = E_modulus * Inertia * B_i.dot(beamDOFsDisplacements[:,i])
            m_ip1 = E_modulus * Inertia * B_ip1.dot(beamDOFsDisplacements[:,i])
            
            # Compute the shear force at the nodes of the element
            v_i = E_modulus * Inertia * C.dot(beamDOFsDisplacements[:,i])
            
            # Store these values in an array
            moment[i,:] = np.array([[m_i, m_ip1]])
            if i !=0:
                shearForce[i,0], shearForce[i,1]= shearForce[i-1,1], -v_i
            else:
                shearForce[i,0], shearForce[i,1] = -v_i, -v_i
        
        # Store
        self.displacement = displacement
        self.verticalDisplacement = verticalDisplacement
        self.moment = moment
        self.shearForce = shearForce
        self.verticalreaction = verticalReaction

    
    def plot(self, elementInfo):
        # import modules
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        import os
        
        # Plots
        # Set figure size used to save the figures and use them in the final report
        plt.figure(figsize=(20,10))

        # Placing the plots in the plane        
        plot1 = plt.subplot2grid((16,4), (0,0), rowspan = 4, colspan = 4) # Deformed shape
        plot1.set_xlabel('Longueur du VPP (en m)')
        plot1.set_ylabel('Déformée (en m)')

        plot2 = plt.subplot2grid((16,4), (6,0), rowspan = 4, colspan = 4) # Bending Moment
        plot2.set_xlabel('Longueur du VPP (en m)')
        plot2.set_ylabel('Moment fléchissant (en MN.m)')

        plot3 = plt.subplot2grid((16,4), (12,0), rowspan = 4, colspan = 4) # Shear Force
        plot3.set_xlabel('Longueur du VPP (en m)')
        plot3.set_ylabel('Effort Tranchant (en MN)')
        
        # Plot the deformed shape
        self.subplot(plot1, self.x, self.verticalDisplacement)
        plot1.set_title("Deformed Shape")
        plot1.grid()
        
        # Plot the bending moment 
        self.subplot(plot2, self.positionEle.flatten(), self.moment.flatten())
        plot2.set_title("Bending Moment")
        plot2.grid()
        
        # Plot the shear force 
        self.subplot(plot3, self.positionEle.flatten(), self.shearForce.flatten())
        plot3.set_title("Shear Force")
        plot3.grid()
        
        # Packing all the plots and displaying them
        plt.tight_layout()

         # Sauvegarder les figures en PNG
        directory = 'ViPPer/Documents/Figures/'
        plt.savefig(os.path.join(directory, f"sollicitations_{elementInfo['name']}.jpeg"), dpi=300)
        
        # plt.show()
        # print(f"Min. displacement: {np.min(self.verticalDisplacement): 0.5f} m, Max. displacement: {np.max(self.verticalDisplacement): 0.5f} m")
        # print(f"Min. moment: {np.min(self.moment):0.5f} MN.m, Max. moment: {np.max(self.moment):0.5f} MN.m")
        # print(f"Min. shear force: {np.min(self.shearForce):0.5f} MN, Max. shear force: {np.max(self.shearForce):0.5f} MN")
        
    def subplot(self, plot_xy, x, y):
        # import modules
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches

        # Plot 
        plot_xy.plot(x, y, color = 'fuchsia')

        # Affichage des valeurs min et max sur le graphique

        # Calcul des valeurs min et max 
        x_min, x_max = np.min(x), np.max(x)
        y_min, y_max = np.min(y), np.max(y)

        # Définir la taille des rectangles d'affichage en fonction de l'échelle du graphique
        # Récupérer la valeur de l'échelle du graphique
        x_range = plot_xy.get_xlim()[1] - plot_xy.get_xlim()[0]
        y_range = plot_xy.get_ylim()[1] - plot_xy.get_ylim()[0]

        # Taille relative pour les rectangles
        rectangle_width = 0.008 * x_range  # 0.8% de la largeur de l'axe x
        rectangle_height = 0.05 * y_range   # 5% de la hauteur de l'axe y

        # Création des rectangles autour des valeurs min et max
        # Création du recatngle avec les bonnes dimensions
        min_rect = patches.Rectangle((x[np.argmin(y)] - rectangle_width / 2, y_min - rectangle_height / 2), rectangle_width, rectangle_height, linewidth=1.5, edgecolor='red', facecolor='none', label='Min')
        # Ajout du rectangle sur le graphique
        plot_xy.add_patch(min_rect) 
        # Ajout et Placement du texte
        plot_xy.text(x[np.argmin(y)] + rectangle_width, y_min + rectangle_height, f'Min: ({x[np.argmin(y)]:.3f}, {y_min:.3f}) ', fontsize=10, verticalalignment='bottom', horizontalalignment='left', color='red')

        # Création du recatngle avec les bonnes dimensions
        max_rect = patches.Rectangle((x[np.argmax(y)] - rectangle_width / 2, y_max - rectangle_height / 2), rectangle_width, rectangle_height, linewidth=1.5, edgecolor='green', facecolor='none', label='Max')
        # Ajout du rectangle sur le graphique
        plot_xy.add_patch(max_rect) 
        # Ajout etPlacement du texte
        plot_xy.text(x[np.argmax(y)] - rectangle_width, y_max - rectangle_height, f'Max: ({x[np.argmax(y)]:.3f}, {y_max:.3f}) ', fontsize=10, verticalalignment='top', horizontalalignment='right', color='green')

    def shapeFunctionsVector(self, x, x_i, x_ip1):
        """ Compute the shape functions vector for a beam element
        DOFs are: vertical translations and rotations at nodes
        Assuming no axial deformations """
        h_e = x_ip1 - x_i
        N1 = (x - x_ip1)*(2*x**2 - x_ip1*x - 3*x_i*x - x_ip1*(x_ip1 - 3*x_i))/h_e**3
        N2 = (x - x_i)*(x - x_ip1)**2/h_e**2
        N3 = (x - x_i)*(-2*x**2 + x_i*x + 3*x_ip1*x + x_i*(x_i - 3*x_ip1))/h_e**3
        N4 = (x - x_ip1)*(x - x_i)**2/h_e**2
        N = np.array([N1, N2, N3, N4])
        return N

    def derivativesShapeFunctionsVector(self, x, x_i, x_ip1):
        """ Compute the B-matrix, i.e: the derivatives of the shape functions vector
        In this case, we need the second derivatives with respect to x """
        h_e = x_ip1 - x_i 
        B1 = 1/h_e**3*(12*x - 6*x_i - 6*x_ip1)
        B2 = 1/h_e**2*(6*x - 2*x_i - 4*x_ip1)
        B3 = 1/h_e**3*(-12*x + 6*x_i + 6*x_ip1)
        B4 = 1/h_e**2*(6*x - 4*x_i - 2*x_ip1)
        B = np.array([B1, B2, B3, B4])
        return B
    
    def thirdDerivativesShapeFunctionsVector(self, x_i, x_ip1):
        """ Compute the derivatives of the B-matrix """
        h_e = x_ip1 - x_i
        C1 = 12/h_e**3
        C2 = 6/h_e**2
        C3 = -12/h_e**3
        C4 = 6/h_e**2
        C = np.array([C1, C2, C3, C4])
        return C

    def flexureStiffnessMatrix(self, x_i, x_ip1, numberOfIntegrationPoints, E, I):
        """ Compute the flexural part of the element Stiffness matrix """
        # Create variables for computation
        x = np.linspace(x_i, x_ip1, numberOfIntegrationPoints)
        fx = 0
        # Loop over the position x on the element
        for i in range(len(x)):
            # Add the product to the numerical integration sum
            fx += np.transpose([self.derivativesShapeFunctionsVector(x[i], x_i, x_ip1)]).dot([self.derivativesShapeFunctionsVector(x[i], x_i, x_ip1)])
        # Compute the integration
        area = fx*(x_ip1-x_i)/numberOfIntegrationPoints
        # Compute the element stiffness matrix
        K = E*I*area
        return K
    
    def axialStiffnessmatrix(self, x_i, x_ip1, E, A):
        """ Compute the axial part of the element stiffness matrix """
        h_e = x_ip1 - x_i
        K = np.array([[E*A/h_e, -E*A/h_e], [-E*A/h_e, E*A/h_e]])
        return K
    
    def orientationMatrix(self, x_i, x_ip1, y_i, y_ip1):
        """ In general, an element of a curved beam can be in any orientation
            This function allows to compute the orientation matrix to go from
            local to global coordinates """
        # Not working at this point
        h_e = ((x_ip1 - x_i)**2 + (y_ip1 - y_i)**2)**0.5
        l = (x_ip1 - x_i)/h_e
        m = (y_ip1 - y_i)/h_e
        subGamma = np.array([[l, m], [-m, l]])
        Gamma = np.eye(6)
        Gamma[np.ix_([0,1], [0,1])] = subGamma
        Gamma[np.ix_([3,4], [3,4])] = subGamma
        return Gamma
    
    def elementStiffnessMatrix(self, x_i, x_ip1, numberOfIntegrationPoints, E, A, I):
        K = np.zeros((6,6))
        K1 = self.flexureStiffnessMatrix(x_i, x_ip1, numberOfIntegrationPoints, E, I)
        K2 = self.axialStiffnessmatrix(x_i, x_ip1, E, A)
        # Affect each term of submatrices to the right term of K
        K[np.ix_([0, 3], [0, 3])] = K2
        K[np.ix_([1, 2, 4, 5], [1, 2, 4, 5])] = K1
        return K
    
    def loadVector(self, x_i, x_ip1, distributedLoad, numberOfIntegrationPoints):
        """ Create an array for the load used for the integration of the element load vector
        Limiation: only works for linear loads """
        # Create variable
        x = np.linspace(x_i, x_ip1, numberOfIntegrationPoints)
        f = np.zeros((1, numberOfIntegrationPoints))
        # Loop over the number of loads
        for i in range(distributedLoad.shape[0]):
            # Define variable to make code easier to read
            x_min, x_max = float(distributedLoad[i,1]), float(distributedLoad[i,2])
            p_min, p_max = float(distributedLoad[i,3]), float(distributedLoad[i,4])
            # Loop over the position x on the element
            for j in range(len(x)):
                # Test to find if the element is subjectetd to load i
                if x[j]>=x_min and x[j]<x_max:
                    if distributedLoad[i,0] == 'linear' or distributedLoad[i,0] == 'uniform':
                        # Change value of vector f at location x[i]
                        f[0,j] += (p_max - p_min)/(x_max - x_min)*(x[j] - x_min) + p_min 
                    # elif distributedLoad[i,0] == 'other type' (example 'exponential'):
                        # Complete this code
        return f

    def elementLoadVector(self, x_i, x_ip1, distributedLoad, numberOfIntegrationPoints):
        """Compute the element load vector using numerical integration """
        # Create variables for computation
        x = np.linspace(x_i, x_ip1, numberOfIntegrationPoints)
        fx = 0
        f = np.zeros((6,1))
        # Call previous function to get the vector of loads for every integration points
        p = self.loadVector(x_i, x_ip1, distributedLoad, numberOfIntegrationPoints)
        # Loop over the position x on the element
        for i in range(len(x)):
            # Add the product to the numerical integration sum
            fx += p[0,i] * np.transpose([self.shapeFunctionsVector(x[i], x_i, x_ip1)])
        # Compute the element load vector
        f[np.ix_([1,2,4,5])] = fx * (x_ip1-x_i)/numberOfIntegrationPoints
        return f

    def nodeNumbering(self, fixity, nodeDOFs):
        """ Create an array containing the number of the free DOFs"""
        import math
        # Create variables for computation
        freeNodeNumb, supportNodeNumb, vertSupportNodeNumb, displacedNodeNumb = [], [], [], []
        # list containing the value of the displacement of the displaced nodes 
        delta_fn = []
        # loop over the number of nodes
        for i in range(fixity.shape[0]):
            for j in range(fixity.shape[1]):
                # If a "NaN" is encountered: add the number of the DOF in list of free DOFs
                if math.isnan(float(fixity[i,j])) == True:
                    freeNodeNumb.append(nodeDOFs[i,j])
                # If a '0' is encountered: add the number of the DOF in list of supported DOFs
                elif float(fixity[i,j]) == 0:
                    supportNodeNumb.append(nodeDOFs[i,j])
                    # Append the DOFs associated with the vertical component
                    if j == fixity.shape[1] - 2:
                        vertSupportNodeNumb.append(nodeDOFs[i,j])
                # If a non-zero value is encountered: add the number of the DOF in list of displaced DOFs
                else:
                    displacedNodeNumb.append(nodeDOFs[i,j])
                    delta_fn.append(float(fixity[i,j]))
        # Transform lists into arrays for later use
        freeNodeNumb = np.array(freeNodeNumb, dtype = 'int32')
        supportNodeNumb = np.array(supportNodeNumb, dtype = 'int32')
        vertSupportNodeNumb = np.array(vertSupportNodeNumb, dtype = 'int32')
        displacedNodeNumb = np.array(displacedNodeNumb, dtype = 'int32')
        delta_fn = np.transpose([np.array(delta_fn)])
        return freeNodeNumb, supportNodeNumb, vertSupportNodeNumb, displacedNodeNumb, delta_fn

    def reducedGlobalMatrices(self, K, f, freeNodeNumb):
        """ From the global matrices, extract the matrices at free degrees of freedom """
        reducedK = K[np.ix_(freeNodeNumb,freeNodeNumb)]
        reducedf = f[freeNodeNumb]
        return reducedK, reducedf
    
    def positionElement(self, nele, x, eleNumb):
        """ For each element, extract from the position array, the global position of 
            start and end of element"""
        positionEle = np.zeros((nele,2))
        for i in range(nele):
            positionEle[i,0] = x[i]
            positionEle[i,1] = x[i+1]
        return positionEle
    
    def sollicitationSupport(self, supportLoad, nnodes, nDOFs):
        F = np.zeros((nnodes*nDOFs, 1))
        # Check if supportLoad not empty (np.array([]) = empty)
        if len(supportLoad):
            for i in range(len(supportLoad)):
                numberOfDOF = int(supportLoad[i,0])
                F[numberOfDOF] += supportLoad[i,1]
        return F
    
    def end_Data(self):

        # Get the min and max value of the moment 
        minMoment, maxMoment = abs(np.min(self.moment.flatten())), abs(np.max(self.moment.flatten()))

        # Get the min and max value of the shear force
        minShear, maxShear = abs(np.min(self.shearForce.flatten())), abs(np.max(self.shearForce.flatten()))

        self.endDict = {"Moment MIN": minMoment,
                   "Moment MAX": maxMoment,
                   "Tranchant MIN": minShear,
                   "Tranchant MAX": maxShear,
                   "Reactions": self.verticalreaction}