# -*- coding: utf-8 -*-
"""
Created on Wed May 26 11:21:26 2021

@author: jules
"""
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as li
import math as m
import classes_projet as cl
import time

pas=0.001

#Unités: MN, MPa, m, cm²

#Combinaison
Coeff_ELU_G=1.35
Coeff_ELU_Q=1.5

#Béton
#(fck, fctm, Ecm, epscu1, epsc1, epscu2, epsc2,n)
Caract_beton_flexion=[(12,1.6,27,3.5,1.8,3.5,2,2),(16,1.9,29,3.5,1.9,3.5,2,2),(20,2.2,30,3.5,2,3.5,2,2),(25,2.6,31,3.5,2.1,3.5,2,2),(30,2.9,33,3.5,2.2,3.5,2,2),(35,3.2,34,3.5,2.25,3.5,2,2),(40,3.5,35,3.5,2.3,3.5,2,2),(45,3.8,36,3.5,2.4,3.5,2,2),(50,4.1,37,3.5,2.45,3.5,2,2),(55,4.2,38,3.2,2.5,3.1,2.2,1.75),(60,4.4,39,3,2.6,2.9,2.3,1.6),(70,4.6,41,2.8,2.7,2.7,2.4,1.45),(80,4.8,42,2.8,2.8,2.6,2.5,1.4),(90,5,44,2.8,2.8,2.6,2.6,1.4)]
E=10000 #MPa
rho_beton=0.025 #MN/m3
classe_exposition_defaut="XC" #ou "XS", "XF", "XD", "XA", "X0"
classe_exposition_complete="XC2"

#Acier
Es=200000 #MPa
sigma_acier=435 #MPa
palier_acier_defaut="Horizontal" #ou "Incliné"
classe_acier_defaut="B" #ou "A", "C"

#Géométrie
presence_dallage=True
voute_decharge=False
fck_dallage=25 #MPa
ep_dallage=0.2 #m mini
p_dallage=0.5 #MN/ml
L_dallage=5 #m distance entre poteau
a_dallage=0.5 #m Largeur des poteaux
enrobage_dallage=0.05 #m

#Charpente
Em=210000 #MPa
G=80770 #MPa
lamine_defaut=True
fy_flexion=355 #MPa

#Section
c=0.03 #Enrobage
I=((0.30)**3)/12 #m4

# Coefficients 
Coeff_beton=1.5  #Sécurité béton
Coeff_acier=1.15 #Sécurité acier
n=15 # Coefficient d'équivalence acier béton pour les sections homogènes

#Cuvelage
cuvelage_defaut=False #ou "Impermeabilisation", "Etanche", "Etancheite"
niveau_eau_defaut="EE" #ou "EB", "EH"
precaution=False
Duree_ouverture="Longue" #ou "Courte"
psy_2=0.3

#Liernes
Type_lierne="Béton dans l'épaisseur" #"Béton en surépaisseur intérieure", "Béton en surépaisseur extérieure", "Métallique"

#Butons
alpha_T=1.2*10**-5 #K-1
fy_compression=235 #MPa

#Bois
Classe_service_defaut=3
Duree_action_defaut="Moyen" #ou "Instantanée", "Permanent", "Long", "Court"
Gamma_M=1.3 #car bois massif
Liste_diametre_defaut=[0.2,0.25,0.3,0.35,0.4]
beta=0.2 #car bois massif

#Platines métallique
Liste_chevilles=[cl.M8, cl.M10, cl.M12, cl.M16, cl.M20, cl.M24]

#Fondation
Gamma_R_d=1.1
Gamma_R_h=1.1
Type_fondation="Coulée pleine fouille" #ou "Préfabriquée"
Gamma_r_v=2.3
Gamma_r_v_d=1.2
Gamma_r_v_elu=1.4
Type_interface="Frottante" # "Frottante" ou "Adhérente"
qnet_defaut=0.144
Butee=False
###############################################################################

####################### Fonctions auxiliaires #################################

def creation_liste_vide(nb_points):
    Liste=[]
    while len(Liste)<nb_points:
        Liste.append(0)
    return Liste

def creation_liste_abscisse(pas, debut, fin):
    longueur=fin-debut
    nb_points=int(longueur/pas)
    Liste=[debut]
    for i in range(1, nb_points+1):
        Liste.append(Liste[i-1]+pas)
    return Liste

def graphique(X, L, legende): #couleur=k NOIR, b=BLEU, g=VERT, r=ROUGE, c=CYAN, y=JAUNE, ...
    O=creation_liste_vide(len(X))
    plt.plot(X,O,color='k', linewidth=0.5)
    plt.plot(X, L, linewidth=1, label=str(legende))
    plt.legend()
    plt.grid()
    plt.axvline(color='c', linewidth=1)
    plt.show()


def integrale(X, Y):
    res=0
    for i in range(len(X)-1):
        res+=((Y[i+1]+Y[i])*(X[i+1]-X[i]))/2
    return res

def copie_liste(Liste):
    Liste_copie=[]
    for i in range(len(Liste)):
        Liste_copie.append(Liste[i])
    return Liste_copie

def copie_liste_double(Liste):
    Liste_copie=[]
    for i in range(len(Liste)):
        Liste_i=[]
        for j in range(len(Liste[i])):
            Liste_i.append(Liste[i][j])
        Liste_copie.append(Liste_i)
    return Liste_copie

def copie_inverse_liste(Liste):
    res=creation_liste_vide(len(Liste))
    for i in range(len(Liste)):
        res[i]=Liste[len(Liste)-1-i]
    return res

def liste_multiple_vers_simple(Liste):
    res=[]
    for i in range(len(Liste)):
        for j in range(len(Liste[i])):
            res.append(Liste[i][j])
    return res

def liste_entier(Liste):
    for i in range(len(Liste)):
        Liste[i]=int(Liste[i])
    return Liste

### Fonctions de calculs

######################### Combinaison #########################################

def ELU(P, Q, Coeff_ELU_G, Coeff_ELU_Q): #MAJ
    return Coeff_ELU_G*P+Coeff_ELU_Q*Q

def ELS_QP(P, Q, psy_2):   #MAJ
    return P+psy_2*Q

def ELS_C(P, Q):   #MAJ
    return P+Q

def ELU_STR_portance(G, Q):   #MAJ
    #Si V augmente c'est défavorable donc les actions positives sont défavorables
    if G>=0:
        gamma_g=1.35
    else:
        gamma_g=1
    if Q>0:
        gamma_q=1.5
    else: 
        gamma_q=0
    return gamma_g*G+gamma_q*Q

def ELU_STR_glissement_V(G, Q):   #MAJ
    #Si V augmente cela devient favorbale donc les actions positives verticales sont favorable
    if G>=0:
        gamma_g=1
    else:
        gamma_g=1.35
    if Q>0:
        gamma_q=0
    else: 
        gamma_q=1.35
    return gamma_g*G+gamma_q*Q

def ELU_STR_glissement_H(G, Q):   #MAJ
    #Si H augmente c'est défavorable donc les actions positives sont défavorables
    if G>=0:
        gamma_g=1.35
    else:
        gamma_g=1
    if Q>0:
        gamma_q=1.5
    else: 
        gamma_q=0
    return gamma_g*G+gamma_q*Q
###############################################################################

######################### Béton ###############################################

def f_ctm(fck):  #MAJ
    if fck<=50:
        fctm=0.3*(fck**(2/3))
    else:
        fctm=2.12*m.ln(1+(fck+8)/10)
    return fctm

def fct_eff(fck):   #MAJ
    if fck<=50:
        f=0.3*fck**(2/3)
    else:
        f=2.12*m.ln(1+(fck+8)/10)
    return f

###############################################################################

######################### Calculs des sollicitations ##########################

def schema_statique(Liste_cote_appuis, hauteur_voile):
    #retournera un dessin
    methode=0
    if len(Liste_cote_appuis)<2:
        methode=0
    elif len(Liste_cote_appuis)==2:
        methode=1
    else:
        methode=2
    return methode

def console_gauche(Liste_chargement, Liste_sollicitations, pas, debut, fin):  #MAJ
    X=creation_liste_abscisse(pas, debut, fin)
    M=creation_liste_vide(len(X))
    T=creation_liste_vide(len(X))
    for i in range(len(Liste_chargement)):
        zmin,zmax,pmin,pmax=Liste_chargement[i][0],Liste_chargement[i][1],Liste_chargement[i][2],Liste_chargement[i][3]
        for j in range(len(X)):
           if X[j]>zmin and X[j]<=zmax:
                px=pmin+(pmax-pmin)*(X[j]-zmin)/(abs(zmax-zmin))
                if px>=pmin:
                    zi=X[j]-(px+2*pmin)*(X[j]-zmin)/(3*(px+pmin))
                else:
                    zi=zmin+(pmin+2*px)*(X[j]-zmin)/(3*(px+pmin))
                M[j]-=(pmin+px)*(X[j]-zmin)/2*(X[j]-zi)
                T[j]-=(pmin+px)*(X[j]-zmin)/2
            
           if X[j]>zmax and zmin!=zmax:
               if pmax>=pmin:
                   zi=zmax-(pmax+2*pmin)*abs(zmax-zmin)/(3*(pmax+pmin))
               else:
                   zi=zmin+(pmin+2*pmax)*abs(zmax-zmin)/(3*(pmax+pmin))
               M[j]-=(pmin+pmax)*abs(zmax-zmin)/2*(X[j]-zi)
               T[j]-=(pmin+pmax)*abs(zmax-zmin)/2
            
           if X[j]>zmax and zmin==zmax:
               M[j]-=max(pmin, pmax)*(X[j]-zmax)
               T[j]-=max(pmin, pmax)

    for i in range(len(M)):
        M[i]-=Liste_sollicitations[0][1]

    return X, M, T

def console_droite(Liste_chargement, Liste_sollicitations, pas, debut, fin):  #MAJ
    X=creation_liste_abscisse(-pas, fin, debut)
    M=creation_liste_vide(len(X))
    T=creation_liste_vide(len(X))
    for i in range(len(Liste_chargement)):
        zmin,zmax,pmin,pmax=Liste_chargement[i][0],Liste_chargement[i][1],Liste_chargement[i][2],Liste_chargement[i][3]
        for j in range(len(X)):
           if X[j]>zmin and X[j]<=zmax:
                px=pmin+(pmax-pmin)*(X[j]-zmin)/(abs(zmax-zmin))
                if px>=pmax:
                    zi=X[j]+(px+2*pmax)*abs(X[j]-zmax)/(3*(px+pmax))
                else:
                    zi=zmax-(pmax+2*px)*abs(X[j]-zmax)/(3*(px+pmax))
                M[j]-=(pmax+px)*abs(X[j]-zmax)/2*abs(X[j]-zi)
                T[j]-=(pmax+px)*abs(X[j]-zmax)/2
            
           if X[j]<zmin and zmin!=zmax:
               if pmax>=pmin:
                   zi=zmax-(pmax+2*pmin)*abs(zmax-zmin)/(3*(pmax+pmin))
               else:
                   zi=zmin+(pmin+2*pmax)*abs(zmax-zmin)/(3*(pmax+pmin))
               M[j]-=(pmin+pmax)*abs(zmax-zmin)/2*abs(X[j]-zi)
               T[j]-=(pmin+pmax)*abs(zmax-zmin)/2
            
           if X[j]<zmin and zmin==zmax:
               M[j]-=max(pmin, pmax)*abs(X[j]-zmax)
               T[j]-=max(pmin, pmax)
    T_=copie_inverse_liste(T)
    M_=copie_inverse_liste(M)
    for i in range(len(M)):
        T_[i]=-T_[i]
        M_[i]+=Liste_sollicitations[-1][1]

    return X, M_, T_
    
def methode_coupure(Liste_cote_appuis, Liste_chargement, Liste_sollicitations, pas, debut, fin):  #MAJ
    #1-Déterminer les efforts ponctuels equivalents et leurs positions
    Liste_charges_eq=[]
    for i in range(len(Liste_chargement)):
        zmin,zmax,pmin,pmax=Liste_chargement[i][0],Liste_chargement[i][1],Liste_chargement[i][2],Liste_chargement[i][3]
        if zmin==zmax:
            Feq=max(pmin, pmax)
        else:
            Feq=(pmin+pmax)*abs(zmax-zmin)/2
        
        if pmin>pmax:
            zeq=zmin+(2*pmax+pmin)*abs(zmax-zmin)/(3*(pmin+pmax))
        else:
            zeq=zmax-(pmax+2*pmin)*(zmax-zmin)/(3*(pmin+pmax))
        Liste_charges_eq.append((Feq,zeq))
    
    #2-Détermination des réactions d'appuis
    V=[] #Liste définissant les réactions d'appuis
    for i in range(len(Liste_cote_appuis)):
        V.append(0)
    else:
        A=np.zeros((len(V),len(V)))        
    A[0,0]=A[0,len(V)-1]=1
    for i in range(len(V)):
        A[1,i]=Liste_cote_appuis[i]
    
    B=np.zeros((len(V),1))
    Ftot, Mtot=0, -sum(Liste_sollicitations[i][1] for i in range(len(Liste_sollicitations)))
    for i in range(len(Liste_charges_eq)):
        Ftot+=Liste_charges_eq[i][0]
        Mtot+=Liste_charges_eq[i][0]*Liste_charges_eq[i][1]
    B[0,0], B[1,0]=Ftot, Mtot
    
    res=li.solve(A,B)
    for i in range(len(res)):
        V[i]=(Liste_cote_appuis[i],res[i,0])
    #3-Détermination du moment fléchissant
    X=creation_liste_abscisse(pas, debut, fin)
    M_chargement, M_reaction, M_tot=creation_liste_vide(len(X)), creation_liste_vide(len(X)), creation_liste_vide(len(X))
    T_chargement, T_reaction, T_tot=creation_liste_vide(len(X)),creation_liste_vide(len(X)),creation_liste_vide(len(X))
    for i in range(len(Liste_chargement)):
        zmin,zmax,pmin,pmax=Liste_chargement[i][0],Liste_chargement[i][1],Liste_chargement[i][2],Liste_chargement[i][3]
        for j in range(len(X)):
            if X[j]>zmin and X[j]<=zmax:
                px=pmin+(pmax-pmin)*(X[j]-zmin)/(abs(zmax-zmin))
                if px>=pmin:
                    zi=X[j]-(px+2*pmin)*(X[j]-zmin)/(3*(px+pmin))
                else:
                    zi=zmin+(pmin+2*px)*(X[j]-zmin)/(3*(px+pmin))
                M_chargement[j]+=(pmin+px)*(X[j]-zmin)/2*(X[j]-zi)
                T_chargement[j]+=(pmin+px)*(X[j]-zmin)/2
            
            if X[j]>zmax and zmin!=zmax:
                if pmax>=pmin:
                    zi=zmax-(pmax+2*pmin)*abs(zmax-zmin)/(3*(pmax+pmin))
                else:
                    zi=zmin+(pmin+2*pmax)*abs(zmax-zmin)/(3*(pmax+pmin))
                M_chargement[j]+=(pmin+pmax)*abs(zmax-zmin)/2*(X[j]-zi)
                T_chargement[j]+=(pmin+pmax)*abs(zmax-zmin)/2
            
            if X[j]>zmax and zmin==zmax:
                M_chargement[j]+=max(pmin, pmax)*(X[j]-zmax)
                T_chargement[j]+=max(pmin, pmax)
    
                
    for i in range(len(V)):
        for j in range(len(X)):
            if X[j]>=V[i][0]:
                M_reaction[j]+=V[i][1]*(X[j]-V[i][0])
                T_reaction[j]+=V[i][1]

    for i in range(len(M_tot)):
        M_tot[i]=-M_chargement[i]+M_reaction[i]-Liste_sollicitations[0][1]
        for k in range(len(Liste_sollicitations)):
            if X[i]>=Liste_sollicitations[k][0]:
                M_tot[i]+=-Liste_sollicitations[k][1]
    for i in range(len(T_tot)):
        T_tot[i]=T_reaction[i]-T_chargement[i]

    return X, M_tot, T_tot

def methode_3moments(Liste_appuis, Liste_chargement, Liste_sollicitations, E, I, pas, debut, fin):   #MAJ
    L_poutre=[]
    Console_debut=False
    Console_fin=False
    L_travee=[]
    if debut!=Liste_appuis[0]:
        L_poutre.append((debut, Liste_appuis[0]))
        Console_debut=True
    for i in range(len(Liste_appuis)-1):
        L_poutre.append((Liste_appuis[i], Liste_appuis[i+1]))
        L_travee.append(Liste_appuis[i+1]-Liste_appuis[i])
    if fin!=Liste_appuis[-1]:
        L_poutre.append((Liste_appuis[-1], fin))
        Console_fin=True
 
    X=[]
    X_=[]
    for i in range(len(L_poutre)):
        X_i=creation_liste_abscisse(pas, L_poutre[i][0],L_poutre[i][1])
        X_j=creation_liste_abscisse(pas, 0, L_poutre[i][1]-L_poutre[i][0])
        X.append(X_i)
        X_.append(X_j)
    #### Calcul des moments isostatiques
    M_iso, T_iso=[],[]                                            
    for i in range(len(L_poutre)): 
        L_i,L_j=L_poutre[i][0], L_poutre[i][1]
        L_chargement_i=[]
        for j in range(len(Liste_chargement)):
            zmin,zmax,pmin,pmax=Liste_chargement[j][0],Liste_chargement[j][1],Liste_chargement[j][2],Liste_chargement[j][3]
            if zmin>=L_i and zmax<=L_j:
                L_chargement_i.append((zmin,zmax,pmin,pmax))
            if L_i<=zmin<=L_j and zmax>L_j:
                L_chargement_i.append((zmin, L_j, pmin, pmin+(pmax-pmin)*(L_j-zmin)/(zmax-zmin)))
            if L_i<=zmax<=L_j and zmin<L_i:
                L_chargement_i.append((L_i, zmax, pmin+(pmax-pmin)*(L_i-zmin)/(zmax-zmin), pmax))
            if zmin<L_i and zmax>L_j:
                L_chargement_i.append((L_i, L_j, pmin+(pmax-pmin)*(L_i-zmin)/(zmax-zmin), pmin+(pmax-pmin)*(L_j-zmin)/(zmax-zmin)))
        if L_i in Liste_appuis and L_j in Liste_appuis:
            L_soll=[(0,0)]
            if len(Liste_sollicitations)>=3:
                for i in range(1,len(Liste_sollicitations)-1):
                    if L_i<=Liste_sollicitations[i][0]<=L_j:
                        L_soll.append((Liste_sollicitations[i][0], Liste_sollicitations[i][1]))
            L_soll.append((0,0))
            M_iso.append(methode_coupure([L_i,L_j], L_chargement_i, L_soll, pas, L_i, L_j)[1])
            T_iso.append(methode_coupure([L_i,L_j], L_chargement_i, L_soll, pas, L_i, L_j)[2])
        if L_i not in Liste_appuis:
            m=console_gauche(L_chargement_i, [(Liste_sollicitations[0][0], Liste_sollicitations[0][1])], pas, L_i, L_j)[1]
            t=console_gauche(L_chargement_i, [(Liste_sollicitations[0][0], Liste_sollicitations[0][1])], pas, L_i, L_j)[2]
            M_iso.append(m)
            T_iso.append(t)
            Liste_sollicitations[0]=(Liste_sollicitations[0][0], -m[-1])
        if L_j not in Liste_appuis:
            m=console_droite(L_chargement_i, [(Liste_sollicitations[-1][0], Liste_sollicitations[-1][1])], pas, L_i, L_j)[1]
            t=console_droite(L_chargement_i, [(Liste_sollicitations[-1][0], Liste_sollicitations[-1][1])], pas, L_i, L_j)[2]
            M_iso.append(m)
            T_iso.append(t)
            Liste_sollicitations[-1]=(Liste_sollicitations[-1][0], m[0])
    #####Calcul des rotations
    W=[]
    M_o, M_e=copie_liste_double(M_iso), copie_liste_double(M_iso)
        
    for i in range(len(X_)):
        for j in range(len(X_[i])):
            L_i,L_j=L_poutre[i][0], L_poutre[i][1]
            if L_i in Liste_appuis and L_j in Liste_appuis:
                M_o[i][j]=M_o[i][j]*(1-X_[i][j]/abs(L_poutre[i][1]-L_poutre[i][0]))/(E*I)
                M_e[i][j]=M_e[i][j]*(X_[i][j]/abs(L_poutre[i][1]-L_poutre[i][0]))/(E*I)
            else:
                M_o[i][j]=0
                M_e[i][j]=0
        w_o=(-1)*integrale(X_[i], M_o[i])
        w_e=integrale(X_[i], M_e[i])
        W.append((w_o, w_e))
        W_=[]
    for i in range(len(W)):
        if W[i]!=(0,0):
            W_.append(W[i])
    
    #Résolution de l'équation des 3 moments
    A=np.zeros((len(Liste_appuis), len(Liste_appuis)))
    A[0,0]=A[len(Liste_appuis)-1, len(Liste_appuis)-1]=1
    for i in range(len(Liste_appuis)-2):
        A[i+1,i]=L_travee[i]
        A[i+1,i+1]=2*(L_travee[i]+L_travee[i+1])
        A[i+1,i+2]=L_travee[i+1]
    
    B=np.zeros((len(Liste_appuis),1))
    B[0,0]=-Liste_sollicitations[0][1]
    B[len(Liste_appuis)-1,0]=Liste_sollicitations[-1][1]
    for i in range(1,len(Liste_appuis)-1):
        B[i,0]=-6*E*I*(W_[i-1][1]-W_[i][0])
    
    M_appuis=[]
    if Console_debut==True:
        M_appuis.append(M_iso[0][0])
    res=li.solve(A,B)
    for i in range(len(res)):
        M_appuis.append(res[i,0])
    if Console_fin==True:
        M_appuis.append(M_iso[-1][-1])
    #Moment hyperstatique
    M_hyper=[]
    T_hyper=[]
    for i in range(len(X_)):
        M_hyper_i=[]
        if Console_debut==False and Console_fin==False:
            for j in range(len(X_[i])):
                M_hyper_i.append(M_appuis[i]+(M_appuis[i+1]-M_appuis[i])*X_[i][j]/(max(X_[i])-min(X_[i])))
        else:
            if Console_debut==True and i==0:
                for j in range(len(X_[0])):
                    M_hyper_i.append(0)
            elif Console_fin==True and i==len(X_)-1:
                for j in range(len(X_[-1])):
                    M_hyper_i.append(0)
            else:
                for j in range(len(X_[i])):
                    M_hyper_i.append(M_appuis[i]+(M_appuis[i+1]-M_appuis[i])*X_[i][j]/(max(X_[i])-min(X_[i])))
        M_hyper.append(M_hyper_i)

    for i in range(len(M_hyper)):
        for j in range(len(M_hyper[i])):
            M_hyper[i][j]+=M_iso[i][j]
            
    for i in range(len(T_iso)):
        T_hyper_i=[]
        for j in range(len(T_iso[i])):
            if Console_debut==True and i==0:
                T_hyper_i.append(T_iso[i][j])
            elif Console_fin==True and i==len(T_iso)-1:
                T_hyper_i.append(T_iso[i][j])
            else:
                if T_iso[i][j]>0:
                    T_hyper_i.append(T_iso[i][j]+(M_appuis[i+1]-M_appuis[i])/(L_poutre[i][1]-L_poutre[i][0]))
                elif T_iso[i][j]<0:
                    T_hyper_i.append(T_iso[i][j]+(M_appuis[i+1]-M_appuis[i])/(L_poutre[i][1]-L_poutre[i][0]))
                elif T_iso[i][j]==0:
                    T_hyper_i.append(0)
        T_hyper.append(T_hyper_i)
        
    Xu=liste_multiple_vers_simple(X)
    #T_isou=liste_multiple_vers_simple(T_iso)
    M_isou=liste_multiple_vers_simple(M_iso)
    T_hyper_u=liste_multiple_vers_simple(T_hyper)
    M_hyper_u=liste_multiple_vers_simple(M_hyper)
    graphique(Xu, M_hyper_u, "Moment (MN.m)")
    #graphique(Xu, T_hyper_u, "Tranchant")
    
    #Calcul des reactions d'appuis
    R=[]
    for i in range(len(T_hyper)+1):
        if i==0:
            R.append(T_hyper[0][0])
        elif i!=0 and i!=len(T_hyper):
            R.append(T_hyper[i][0]-T_hyper[i-1][-2])
        elif i==len(T_hyper):
            R.append(T_hyper[len(T_hyper)-1][-1])    
    return X, M_hyper, T_hyper, R
###############################################################################

######################## Déformée RDM par différences finies ##################

def diff_finies(X, M, E, I, pas):   #MAJ
    Y=[]  
    nb_points=int(len(X))
    A=np.zeros((nb_points, nb_points))
    A[0,0]=A[nb_points-1, nb_points-1]=1/pas**2
    for i in range(1, nb_points-1):
        A[i,i-1]=1/pas**2
        A[i,i+1]=1/pas**2
        A[i,i]=-2/pas**2
    B=np.zeros((nb_points, 1))
    B[0,0]=B[nb_points-1, 0]=0
    for i in range(1, nb_points-1):
        B[i,0]=-M[i]/(E*I)
    res=li.solve(A,B)
    for i in range(len(res)):
        Y.append(-res[i,0])
    return Y

def diff_finies_avant(X, M, E, I, pas, y_1, y_2):   #MAJ
    Y=[]
    nb_points=int(len(X))
    A=np.zeros((nb_points, nb_points))
    for i in range(nb_points):
        A[i,i]=1/pas**2
    for i in range(nb_points-1):
        A[i,i+1]=-2/pas**2
    for i in range(nb_points-2):
        A[i,i+2]=1/pas**2
        A[-2,-2], A[-2,-1], A[-2,-3]=1,0,0
    B=np.zeros((nb_points, 1))
    for i in range(nb_points-2):
        B[i,0]=-M[i]/(E*I)
    B[nb_points-1, 0]=-M[-1]/(E*I)+(2*y_1-y_2)/pas**2
    B[nb_points-2,0]=-y_1
    res=li.solve(A,B)
    for i in range(len(res)):
        Y.append(-res[i,0])
    return Y

def diff_finies_apres(X, M, E, I, pas, y_1, y_2):   #MAJ
    Y=[]
    nb_points=int(len(X))
    A=np.zeros((nb_points, nb_points))
    for i in range(nb_points):
        A[i,i]=1/pas**2
    for i in range(1,nb_points):
        A[i,i-1]=-2/pas**2
    for i in range(2,nb_points):
        A[i,i-2]=1/pas**2
    A[1,1], A[1,0], A[1,2]=1,0,0
    B=np.zeros((nb_points, 1))
    for i in range(2,nb_points):
        B[i,0]=-M[i]/(E*I)
    B[0, 0]=-M[0]/(E*I)+(2*y_1-y_2)/pas**2
    B[1,0]=-y_1
    res=li.solve(A,B)
    for i in range(len(res)):
        Y.append(-res[i,0])
    return Y

def deformee(X, M, Liste_appuis, E, I, pas, debut, fin):   #MAJ
    Y=creation_liste_vide(len(X))
    Console_debut=False
    Console_fin=False 
    if m.isclose(debut,Liste_appuis[0])==False:
        Console_debut=True
    if m.isclose(fin,Liste_appuis[-1])==False:
        Console_fin=True
    for i in range(len(X)):
        Y_i=[]
        if (i==0 and Console_debut==True):
            pass
        elif (i==len(X)-1 and Console_fin==True):
            pass
        else: 
            Y_i=diff_finies(X[i], M[i], E, I, pas)
        Y[i]=Y_i
    if Console_debut==True:
        Y[0]=diff_finies_avant(X[0],M[0], E, I, pas, Y[1][0], Y[1][1])
        
    if Console_fin==True:
        Y[-1]=diff_finies_apres(X[-1], M[-1], E, I, pas, Y[-2][-1], Y[-2][-2])
    
    Y_=liste_multiple_vers_simple(Y)
    X_=liste_multiple_vers_simple(X)
    for i in range(len(Y_)):
            Y_[i]=-Y_[i]*100
            
    #plt.plot(Y_, X_, linewidth=0.75)
    #plt.xlabel("Déformée (en cm)")
    #plt.ylabel("Profondeur du voile en cote relative (en m)")
    #plt.grid()
    #ax=plt.gca()
    #ax.invert_yaxis()
    #plt.show()
    return Y

def ep_mini_deformee(f_max, X, M, Liste_appuis, b, pas, debut, fin):
    h_=0.01
    I_=b*h_**3/12
    Y=deformee(X, M, Liste_appuis, E, I_, pas, debut, fin)
    Y=liste_multiple_vers_simple(Y)
    maxi, mini= abs(max(Y)), abs(min(Y))
    while maxi>f_max or mini>f_max:
        h_+=0.01
        Y=deformee(X, M, Liste_appuis, E, b*h_**3/12, pas, debut, fin)
        Y=liste_multiple_vers_simple(Y)
        maxi, mini= abs(max(Y)), abs(min(Y))
    return round(h_,2)
    
######################## Calculs des sections d'acier #########################

def contrainte_acier(cuvelage, alpha_u, fyk, palier_acier, classe_acier, niveau_eau, coeff_secu_acier, Es):  # MAJ
    if cuvelage==False:
        eps_s1=3.5/1000*(1-alpha_u)/alpha_u
        if palier_acier=="Horizontal":
                if eps_s1<=fyk/(coeff_secu_acier*Es):
                    sigma_s1=Es*eps_s1
                else:
                    sigma_s1=fyk/coeff_secu_acier
        else:
            if eps_s1<=fyk/(coeff_secu_acier*Es):
                sigma_s1=Es*eps_s1
            else:
                if classe_acier=="A":
                    sigma_s1=min(432.37+952.38*eps_s1, 454)
                elif classe_acier=="B":
                    sigma_s1=min(433.2+727.27*eps_s1,466)
                else:
                    sigma_s1=min(432.84+895.52*eps_s1,494)
    else:
        if cuvelage=="Imperméabilisation":
            sigma_s1=min(2/3*fyk, 240)
        elif cuvelage=="Etanche" or cuvelage=="Etancheite":
            if niveau_eau=="EB":
                sigma_s1=min(2/3*fyk, 200)
            elif niveau_eau=="EH":
                sigma_s1=min(2/3*fyk, 300)
            elif niveau_eau=="EE":
                sigma_s1=min(2/3*fyk,400)   
    return sigma_s1
         
def flexion_simple_rect(M_elu,M_els,largeur,d,h,fck,fyk,classe_exposition,classe_acier,palier_acier, coeff_secu_beton, coeff_secu_acier, cuvelage, niveau_eau, Es):   # MAJ
    # M en MN.m; b,d,d_ en m; fck,fyk en MPa
    #Données:
    d_=h-d
        
    #Calcul de mu_lim ###################################################################
    alpha_e=15
    gamma=M_elu/M_els
    if classe_exposition=="XD" or classe_exposition=="XS" or classe_exposition=="XF":
        if fck<=30:
            if palier_acier=="Horizontal":
                mu_lim=(2740*gamma+60*fck-3100)*10**-4
            else:
                mu_lim=(2800*gamma+37*fck-2605)*10**-4
        else:
            if palier_acier=="Horizontal":
                A=71.2*fck+108
                B=-5.2*fck+874.4
                C=0.03*fck-12.5
                K=(A+B*alpha_e+C*(alpha_e**2))*10**-4
                mu_lim=(fck*K)/((4.69-1.70*gamma)*fck+(159.90-76.20*gamma))
            else:
                A=75.3*fck-189.8
                B=-5.6*fck+874.5
                C=0.04*fck-13
                K=(A+B*alpha_e+C*(alpha_e**2))*10**-4
                mu_lim=(fck*K)/((4.62-1.66*gamma)*fck+(165.69-79.62*gamma))
    else:
        mu_lim=0.372
    ####################################################################################
    
    # Calcul de mu_lu
    mu_lu=abs(M_elu)/(largeur*d**2*fck/1.5)
    
    #Calcul de As1 et As2
    delta=d_/d
    
    if fck<=50:
        lambda_=0.8
    elif fck>50 and fck<90:
        lambda_= 0.8-(fck-50)/400
       
    if mu_lu<=mu_lim:
        alpha_u=(1/lambda_)*(1-(1-2*mu_lu)**0.5)
        z=d*(1-0.5*lambda_*alpha_u)
        sigma_s1=contrainte_acier(cuvelage, alpha_u,fyk, palier_acier, classe_acier, niveau_eau, coeff_secu_acier, Es)
        As1=abs(M_elu)/(z*sigma_s1)
        As2=0
        
    else:
        alpha_u=(1/lambda_)*(1-(1-2*mu_lim)**0.5)
        z=d*(1-0.5*lambda_*alpha_u)
        sigma_s1=contrainte_acier(cuvelage, alpha_u,fyk, palier_acier, classe_acier, niveau_eau, coeff_secu_acier, Es)
        M_lu=mu_lim*largeur*d**2*fck/coeff_secu_beton
        if palier_acier=="Horizontal":
            a=0.5/alpha_e+13
            b=6517/alpha_e+1
        else:
            a=-5/alpha_e+13
            b=6855/alpha_e-9
        sigma_s2e=0.6*alpha_e*gamma*fck-delta*(a*fck+b)
        sigma_s1e=(a*fck+b)-0.6*alpha_e*gamma*fck
        As2=(abs(M_elu)-M_lu)/((d-d_)*sigma_s2e)
        As1=M_lu/(z*sigma_s1)+As2*sigma_s2e/sigma_s1e
    print(largeur, d, h, fck, fyk, coeff_secu_acier, cuvelage, precaution, M_elu, 0)
    As_min=section_min(largeur, d, h, fck, fyk, coeff_secu_acier, cuvelage, precaution, M_elu, 0)
    As_retenu=max(As1*10**4, As_min)
    return mu_lim, mu_lu, alpha_u, z, sigma_s1, As1*10**4, As_min, As_retenu, As2*10**4

def flexion_simple_T(M_elu,M_els,b,d,h, hf, bf, fck,fyk,classe_exposition,classe_acier,palier_acier, coeff_secu_beton, coeff_secu_acier, cuvelage, niveau_eau, Es):  # MAJ
    M_tu=(bf*hf*fck/coeff_secu_beton)*(d-hf/2)
    
    if M_tu>=abs(M_elu):
        mu_lim, mu_lu, alpha_u, z, sigma_s1, As1, As_min, As_retenu, As2=flexion_simple_rect(M_elu,M_els,bf,d,h,fck,fyk,classe_exposition,classe_acier,palier_acier, coeff_secu_beton, coeff_secu_acier, cuvelage, niveau_eau, Es)
        
    else: 
        M_2=((bf-b)*hf*fck/coeff_secu_beton)*(d-hf/2)
        M_1=abs(M_elu)-M_2
        mu_lu=abs(M_1)/(b*d**2*fck/coeff_secu_beton)
        d_=h-d
        alpha_e=15
        gamma=M_elu/M_els
        if classe_exposition=="XD" or classe_exposition=="XS" or classe_exposition=="XF":
            if fck<=30:
                if palier_acier=="Horizontal":
                    mu_lim=(2740*gamma+60*fck-3100)*10**-4
                else:
                    mu_lim=(2800*gamma+37*fck-2605)*10**-4
            else:
                if palier_acier=="Horizontal":
                    A=71.2*fck+108
                    B=-5.2*fck+874.4
                    C=0.03*fck-12.5
                    K=(A+B*alpha_e+C*(alpha_e**2))*10**-4
                    mu_lim=(fck*K)/((4.69-1.70*gamma)*fck+(159.90-76.20*gamma))
                else:
                    A=75.3*fck-189.8
                    B=-5.6*fck+874.5
                    C=0.04*fck-13
                    K=(A+B*alpha_e+C*(alpha_e**2))*10**-4
                    mu_lim=(fck*K)/((4.62-1.66*gamma)*fck+(165.69-79.62*gamma))
        else:
            mu_lim=0.372
        ##################################################################################
        
        if fck<=50:
            lambda_=0.8
        elif fck>50 and fck<90:
            lambda_= 0.8-(fck-50)/400
        
        if mu_lu<=mu_lim:
            alpha_u=(1/lambda_)*(1-(1-2*mu_lu)**0.5)
            z=d*(1-0.5*lambda_*alpha_u)
            sigma_s1=contrainte_acier(cuvelage, alpha_u,fyk, palier_acier, classe_acier, niveau_eau, coeff_secu_acier, Es)
            As2=0
        else:
            alpha_u=(1/lambda_)*(1-(1-2*mu_lim)**0.5)
            z=d*(1-0.5*lambda_*alpha_u)
            sigma_s1=contrainte_acier(cuvelage, alpha_u,fyk, palier_acier, classe_acier, niveau_eau, coeff_secu_acier, Es)
            As2=(bf-b)*hf*fck/coeff_secu_beton/sigma_s1*10**4
        
        As1=abs(M_1)/(z*sigma_s1)*10**4

    As_min=section_min(b, d, h, fck, fyk, coeff_secu_acier, cuvelage, precaution, M_elu, 0)
    As_retenu=max(As1, As_min)
    return mu_lim, mu_lu, alpha_u, z, sigma_s1, As1, As_min, As_retenu, As2
        
###################### Contraintes ############################################

def K_a(nb_couche, Liste_phi):   #MAJ
    Liste_Ka=[]
    for i in range(nb_couche):
        Liste_Ka.append((m.tan(m.pi/4-Liste_phi[i]*m.pi/180/2))**2)
    return Liste_Ka

def sigma_verticale_tot(X, nb_couche, Liste_cote, Liste_gamma):   #MAJ
    sigma=[] 
    for i in range(nb_couche):
        Liste_i=[]
        if i==0:
            for j in range(len(X[0])):
                Liste_i.append(Liste_gamma[0]*(X[0][0]-X[0][j]))
        else:
            for j in range(len(X[i])):
                Liste_i.append(sigma[i-1][-1]+Liste_gamma[i]*(X[i][0]-X[i][j]))
        sigma.append(Liste_i)
    return sigma

def pression_hydrostatique(X, nb_couche, eau, Niveau_eau):   #MAJ
    u=[]
    for i in range(nb_couche):
        u_i=[]
        for j in range(len(X[i])):
            if eau==True and X[i][j]<=Niveau_eau:
                u_i.append(0.010*(Niveau_eau-X[i][j]))
            else:
                u_i.append(0)
        u.append(u_i)
    return u

def sigma_verticale(sigma_v_tot, u):   #MAJ
    sigma=[]
    for i in range(len(sigma_v_tot)):
        Liste_i=[]
        for j in range(len(sigma_v_tot[i])):
            Liste_i.append(sigma_v_tot[i][j]-u[i][j])
        sigma.append(Liste_i)
    return sigma

def sigma_horizontale(X, nb_couche, sigma_v, Liste_Ka, Liste_c):   #MAJ
    sigma=[]
    for i in range(nb_couche):
        Liste_i=[]
        for j in range(len(X[i])):
            Liste_i.append(Liste_Ka[i]*sigma_v[i][j]-2*Liste_c[i]*(Liste_Ka[i])**0.5)
        sigma.append(Liste_i)
    return sigma 

def sigma_horizontale_tot(sigma_h, u):   #MAJ
    sigma=[]
    for i in range(len(sigma_h)):
        Liste_i=[]
        for j in range(len(sigma_h[i])):
            if sigma_h[i][j]+u[i][j]<0:
                Liste_i.append(0)
            else:
                Liste_i.append(sigma_h[i][j]+u[i][j])
        sigma.append(Liste_i)
    return sigma 

def contraintes_sol(nb_couche, Liste_cote, Liste_phi, Liste_c, Liste_gamma, eau, Niveau_eau):   #MAJ
    X=[]
    for i in range(nb_couche):
        X_i=creation_liste_abscisse(-0.001, Liste_cote[i][0], Liste_cote[i][1])
        X.append(X_i)

    Liste_Ka=K_a(nb_couche, Liste_phi)
    sigma_v_tot=sigma_verticale_tot(X, nb_couche, Liste_cote, Liste_gamma)

    u=pression_hydrostatique(X, nb_couche, eau, Niveau_eau)
    sigma_v=sigma_verticale(sigma_v_tot, u)
    sigma_h=sigma_horizontale(X, nb_couche, sigma_v, Liste_Ka, Liste_c)
    sigma_h_tot=sigma_horizontale_tot(sigma_h, u)
        
    return X, sigma_h_tot

def butee(nb_couche, Liste_cote, Liste_phi, Liste_c, Liste_gamma, eau, Niveau_eau):   #MAJ
    X=[]
    for i in range(nb_couche):
        X_i=creation_liste_abscisse(-0.001, Liste_cote[i][0], Liste_cote[i][1])
        X.append(X_i)
    Liste_Ka=K_a(nb_couche, Liste_phi)
    Liste_Kp=[]
    for i in range(len(Liste_Ka)):
        Liste_Kp.append(1/Liste_Ka[i])
    sigma_v_tot=sigma_verticale_tot(X, nb_couche, Liste_cote, Liste_gamma)

    u=pression_hydrostatique(X, nb_couche, eau, Niveau_eau)
    sigma_v=sigma_verticale(sigma_v_tot, u)
    sigma_h=sigma_horizontale(X, nb_couche, sigma_v, Liste_Kp, Liste_c)
    sigma_h_tot=sigma_horizontale_tot(sigma_h, u)
    
    for i in range(len(X)):
        plt.plot(sigma_h_tot[i], X[i])
    
    return sigma_h_tot[-1][-1]/2

###############################################################################

############################## Calculs des surcharges #########################

def moyenne_angle_frottement(nb_couche, Liste_cote, Liste_phi):  #MAJ
    res=0
    somme=0
    for i in range(nb_couche):
        res+=Liste_phi[i]*(Liste_cote[i][0]-Liste_cote[i][1])
        somme+=(Liste_cote[i][0]-Liste_cote[i][1])
    res=res/somme
    return res 

def pl_uniforme_d(q,d,nb_couche, moy_phi, Niveau_inf, Niveau_sup):  #MAJ
    X=creation_liste_abscisse(-pas, Niveau_inf, Niveau_sup)
    sigma=[]
    Ka=(m.tan(m.pi/4-moy_phi*m.pi/180/2))**2
    z_1=d*m.tan(moy_phi*m.pi/180)
    z_2=d*m.tan(m.pi/4+moy_phi*m.pi/180/2)
    for i in range(len(X)):
        if (X[0]-X[i])<z_1:
            sigma.append(0)
        elif (X[0]-X[i])>=z_1 and (X[0]-X[i])<z_2:
            sigma.append(q*Ka*(X[0]-X[i]-z_1)/(z_2-z_1))
        else: 
            sigma.append(q*Ka)
    return X, sigma
            
def pl_lineique_d(Q,d,nb_couche, moy_phi, Niveau_inf, Niveau_sup):   #MAJ
    X=creation_liste_abscisse(-pas, Niveau_inf, Niveau_sup)
    sigma=[]
    Ka=(m.tan(m.pi/4-moy_phi*m.pi/180/2))**2
    z_1=d*m.tan(moy_phi*m.pi/180)
    z_2=d*m.tan(m.pi/4+moy_phi*m.pi/180/2)
    p_max=2*Q*(Ka)**0.5/(z_2-z_1)
    for i in range(len(X)):
        if (X[0]-X[i])<z_1 or (X[0]-X[i])>=z_2:
            sigma.append(0)
        elif (X[0]-X[i])==z_1:
            sigma.append(p_max)
        else:
            sigma.append(-p_max*((X[0]-X[i])-z_1)/(z_2-z_1)+p_max)

    return X, sigma

def pl_uniforme_limitee(q, d, B, nb_couche, moy_phi, Niveau_sup, Niveau_inf):   #MAJ
    X=creation_liste_abscisse(-pas, Niveau_sup, Niveau_inf)
    sigma=[]
    distribution=""
    Ka=(m.tan(m.pi/4-moy_phi*m.pi/180/2))**2
    sigma_lim=q*Ka
    z_1=d*m.tan(moy_phi*m.pi/180)
    z_2=d*m.tan(m.pi/4+moy_phi*m.pi/180/2)
    z_3=(B+d)*m.tan(moy_phi*m.pi/180)
    z_4=(B+d)*m.tan(m.pi/4+moy_phi*m.pi/180/2)
    z_3_=0
    if z_2<z_3:
        distribution="Trapézoïdale"
    else:
        distribution="Triangulaire"
    if distribution=="Trapézoïdale":
        sigma_max=2*B*q*m.tan(m.pi/4+moy_phi*m.pi/180/2)/((z_3+z_4)-(z_1+z_2))
        if sigma_max>sigma_lim:
            sigma_max=sigma_lim
        z_3_=2*B*m.tan(m.pi/4+moy_phi*m.pi/180/2)/Ka+z_1+z_3-z_4
    elif distribution=="Triangulaire":
        sigma_max=2*B*q*m.tan(m.pi/4+moy_phi*m.pi/180/2)/(z_4-z_1)
        if sigma_max>sigma_lim:
            sigma_max=sigma_lim
        z_3_=2*B*m.tan(m.pi/4+moy_phi*m.pi/180/2)/Ka+z_1+z_2-z_4
    if z_2<z_3 and sigma_max<sigma_lim:
        for i in range(len(X)):
            if (X[0]-X[i])<z_1 or (X[0]-X[i])>z_4:
                sigma.append(0)
            elif (X[0]-X[i])>=z_1 and (X[0]-X[i])<z_2:
                sigma.append(sigma_max*((X[0]-X[i])-z_1)/(z_2-z_1))
            elif (X[0]-X[i])>=z_2 and (X[0]-X[i])<z_3:
                sigma.append(sigma_max)
            elif (X[0]-X[i])>=z_3 and (X[0]-X[i])<=z_4:
                sigma.append(-sigma_max*((X[0]-X[i])-z_4)/(z_4-z_3))
    elif z_2>z_3 and sigma_max<sigma_lim:
        for i in range(len(X)):
            if (X[0]-X[i])<z_1 or (X[0]-X[i])>z_4:
                sigma.append(0)
            elif (X[0]-X[i])>=z_1 and (X[0]-X[i])<z_3:
                sigma.append(sigma_max*((X[0]-X[i])-z_1)/(z_3-z_1))
            elif (X[0]-X[i])>=z_3 and (X[0]-X[i])<=z_4:
                sigma.append(-sigma_max*((X[0]-X[i])-z_4)/(z_4-z_3))
    elif z_2<z_3 and sigma_max==sigma_lim:
        for i in range(len(X)):
            if (X[0]-X[i])<z_1 or (X[0]-X[i])>z_4:
                sigma.append(0)
            elif (X[0]-X[i])>=z_1 and (X[0]-X[i])<z_2:
                sigma.append(sigma_max*((X[0]-X[i])-z_1)/(z_2-z_1))
            elif (X[0]-X[i])>=z_2 and (X[0]-X[i])<z_3_:
                sigma.append(sigma_max)
            elif (X[0]-X[i])>=z_3_ and (X[0]-X[i])<=z_4:
                sigma.append(-sigma_max*((X[0]-X[i])-z_4)/(z_4-z_3_))
    elif z_2>z_3 and sigma_max==sigma_lim:
        for i in range(len(X)):
            if (X[0]-X[i])<z_1 or (X[0]-X[i])>z_4:
                sigma.append(0)
            elif (X[0]-X[i])>=z_1 and (X[0]-X[i])<z_3:
                sigma.append(sigma_max*((X[0]-X[i])-z_1)/(z_3-z_1))
            elif (X[0]-X[i])>=z_3 and (X[0]-X[i])<z_3_:
                sigma.append(sigma_max)
            elif (X[0]-X[i])>=z_3_ and (X[0]-X[i])<=z_4:
                sigma.append(-sigma_max*((X[0]-X[i])-z_4)/(z_4-z_3_))
    return X, sigma

def pression_contigue(q, nb_couche, Liste_cote, Liste_phi):   #MAJ
    X=[]
    for i in range(nb_couche):
        X_i=creation_liste_abscisse(-0.001, Liste_cote[i][0], Liste_cote[i][1])
        X.append(X_i)
    sigma=[]
    Ka=K_a(nb_couche, Liste_phi)
    for i in range(len(X)):
        Q=q*Ka[i]
        sigma_i=[]
        for j in range(len(X[i])):
            sigma_i.append(Q)
        sigma.append(sigma_i)
    X_=liste_multiple_vers_simple(X)
    sigma_=liste_multiple_vers_simple(sigma)
    return X_, sigma_

def pression_contigue_limitee(q, B, nb_couche, moy_phi, Niveau_inf, Niveau_sup):   #MAJ
    X=creation_liste_abscisse(-pas, Niveau_inf, Niveau_sup)
    sigma=[]
    Ka=(m.tan(m.pi/4-moy_phi*m.pi/180/2))**2
    z_1=B*m.tan(m.pi/4+moy_phi*m.pi/180/2)
    sigma_max=q*Ka
    for i in range(len(X)):
        if (X[0]-X[i])>z_1:
            sigma.append(0)
        else:
            sigma.append(sigma_max)
    return X, sigma 

def pl_uniforme_aire(q,d,B,L,nb_couche, moy_phi, Niveau_inf, Niveau_sup):   #MAJ
    #L=Longueur du chargement dans le cas rectangulaire
    #L=diamètre dans le cas d'un chargement circulaire
    L_p=L+d
    K_p=L_p/(L_p+d)
    X=pl_uniforme_limitee(K_p*q, d, B, nb_couche, moy_phi, Niveau_inf, Niveau_sup)[0]
    sigma=pl_uniforme_limitee(K_p*q, d, B, nb_couche, moy_phi, Niveau_inf, Niveau_sup)[1]
    return X, sigma

def el_lineique(Q,d,alpha, nb_couche, moy_phi, Niveau_inf, Niveau_sup):   #MAJ
    X=creation_liste_abscisse(-pas, Niveau_inf, Niveau_sup)
    sigma=[]
    Z=[]
    for i in range(len(X)):
        Z.append(X[0]-X[i])
    #lambda_=(d+2)/(d+1)
    lambda_=1.5
    for i in range(len(Z)):
        sigma.append(lambda_*2*Q/m.pi*(Z[i]*m.cos(alpha*m.pi/180)-d*m.sin(alpha*m.pi/180))*d**2/(d**2+Z[i]**2))
    return X, sigma

def risberme(dimensions, gamma, phi, c, Niveau_inf):   #MAJ
    #gmma, phi, c: caractéristiques sol risberme
    H, d, alpha=dimensions[0], dimensions[1], dimensions[2]
    L_r=d+H/m.tan(alpha*m.pi/180)
    W=(L_r+d)*H*gamma/2
    B_max=W*m.tan(phi*m.phi/180)+c*L_r
    pos=Niveau_inf+H/3
    return pos, B_max

def talus(d, dimensions, nb_couche, moy_phi, gamma, Niveau_inf, Niveau_sup):   #MAJ
    H, d_, alpha=dimensions[0], dimensions[1], dimensions[2]
    X=creation_liste_abscisse(-pas, Niveau_inf, Niveau_sup)
    sigma=[]
    Ka=(m.tan(m.pi/4-moy_phi*m.pi/180/2))**2
    sigma_max=Ka*gamma*H
    z_1=d*m.tan(moy_phi*m.pi/180)
    z_2=d_*m.tan(moy_phi*m.pi/180)+d*m.tan(m.pi/4+moy_phi*m.pi/180/2)
    for i in range(len(X)):
        if (X[0]-X[i])<z_1:
            sigma.append(0)
        elif (X[0]-X[i])>=z_1 and (X[0]-X[i])<z_2:
            sigma.append(sigma_max*((X[0]-X[i])-z_1)/(z_2-z_1))
        elif (X[0]-X[i])>=z_2:
            sigma.append(sigma_max)
    return X, sigma

###############################################################################

########################### Calculs des sections d'acier ######################
def verification_flambement(N_elu, b, h, fck, Liste_appuis, coeff_secu_beton):
    #Liste_appui de la forme [Appui_1, Appui_2, ..., Appui_semelle]
    A, B, C=0.7, 1.1, 0.7
    A_c, I_c= b*h, b*h**3/12
    n=N_elu/(A_c*fck/coeff_secu_beton)
    i_=(A_c/I_c)**0.5
    lambda_lim=20*A*B*C/(n**0.5)
    hauteur=[]
    for i in range(len(Liste_appuis)-1):
        hauteur.append(abs(Liste_appuis[i+1]-Liste_appuis[i]))
    hauteur_max=max(hauteur)
    l_o=hauteur_max
    lambda_=l_o/i_
    if lambda_>lambda_lim:
        return False
    else:
        return True    

def flexion_composee_voile(N_elu, N_els, M_elu, M_els, b, h, d, fck, fyk, classe_exposition, classe_acier, palier_acier, cuvelage, n, coeff_secu_acier, coeff_secu_beton, niveau_eau, Es, precaution):
    #Données
    d_=h-d
    e=M_elu/N_elu
    res, verif="", ""
    #flambement faire une fonction à part 
    e_els,e_elu,etat=etat_section(N_elu, N_els, M_elu, M_els, b, h, d, fck, fyk, classe_exposition, classe_acier, palier_acier, coeff_secu_beton)
    
    #Section partiellement tendue 
    if etat=="Partiellement tendue": 
        m_ua, mu_lim, mu_cu, alpha_u, z, sigma_s1, As1, As2=flexion_partiellement_(N_elu, M_elu, M_els, b, h, d, fck, fyk, classe_exposition, classe_acier, palier_acier, coeff_secu_beton, coeff_secu_acier, cuvelage, niveau_eau, Es)
        As_min=section_min(b, d, h, fck, fyk, coeff_secu_acier, cuvelage, precaution, M_elu, N_elu) 
        As1_retenu=max(As1, As_min)
        As2_retenu=As2
        
    #Section partiellement comprimée
    elif etat=="Partiellement comprimée":
        m_ua, mu_lim, mu_cu, alpha_u, z, sigma_s1, As1, As2=flexion_partiellement_(N_elu, M_elu, M_els, b, h, d, fck, fyk, classe_exposition, classe_acier, palier_acier, coeff_secu_beton, coeff_secu_acier, cuvelage, niveau_eau, Es)
        As_min=section_min(b, d, h, fck, fyk, coeff_secu_acier, cuvelage, precaution, M_elu, N_elu) 
        As1_retenu=max(As1, As_min)
        As2_retenu=As2
        
    #Section totalement tendue
    elif etat=="Totalement tendue":
        As1_retenu=flexion_totalement_tendue(N_elu, N_els, M_elu, M_els, b, h, d, fck, fyk, classe_exposition, classe_acier, palier_acier, coeff_secu_beton, coeff_secu_acier, cuvelage, niveau_eau, Es)[0]
        As2_retenu=flexion_totalement_tendue(N_elu, N_els, M_elu, M_els, b, h, d, fck, fyk, classe_exposition, classe_acier, palier_acier, coeff_secu_beton, coeff_secu_acier, cuvelage, niveau_eau, Es)[1]
        
    #Section totalement comprimée
    elif etat=="Totalement comprimée":
        As_min=max(0.1*N_elu/(fyk/coeff_secu_acier)*10**4, section_min(b, d, h, fck, fyk, coeff_secu_acier, cuvelage, precaution, M_elu, N_elu))
        As_max=0.08*b*h*10**4
        As1=As_min
        As2=As_min #Demander le ferraillage à l'utilisateur
        res=verif_section_diagramme_interaction(As1, As2, M_elu, N_elu, b, h, d, fck, fyk, classe_acier)[0]
        if res!="La section d'acier choisie convient ! ":
            res="Pas de section convenable trouvée !"
            As1=0
            As2=0
        else:
            res="La section minimale convient !"
        
        As1_retenu=As1
        As2_retenu=As2
        A, Ih, _= inertie_homogene(As1_retenu, As2_retenu, b, d, h, n)
        sigma_cmax=N_els/A+N_els*e_els*h/2/Ih
        if sigma_cmax>0.6*fck:
            verif="Contraintes à l'ELS non vérifiées !"
        else:
            verif="La vérification à l'ELS est satisfaite !"
    return "Section "+etat, As1_retenu, As2_retenu, res, verif

def etat_section(N_elu, N_els, M_elu, M_els, b, h, d, fck, fyk, classe_exposition, classe_acier, palier_acier, coeff_secu_beton):
    e_u=M_elu/N_elu
    e_ser=M_els/N_els
    d_=h-d
    etat=""
    
    if M_elu>=0 and N_elu>=0:
        e_elu=abs(e_u)-h/2+d
    elif M_elu>=0 and N_elu<0:
        e_elu=abs(e_u)+h/2-d
    elif M_elu<0 and N_elu>=0:
        e_elu=abs(e_u)-h/2+d
    elif M_elu<0 and N_elu<0:
        e_elu=abs(e_u)+h/2-d
    M_ua=abs(N_elu)*e_elu
    mu_u=abs(M_ua)/(b*d**2*fck/coeff_secu_beton)
    
    if M_els>=0 and N_els>=0:
        e_els=abs(e_ser)-h/2+d
    elif M_els>=0 and N_els<0:
        e_els=abs(e_ser)+h/2-d
    elif M_els<0 and N_els>=0:
        e_els=abs(e_ser)-h/2+d
    elif M_els<0 and N_els<0:
        e_els=abs(e_ser)+h/2-d

    if (abs(e_elu)>h/2-d_ and N_elu<0) and (abs(e_els)>h/2-d_ and N_els<0):
        etat="Partiellement tendue"
    elif (abs(e_elu)<=h/2-d_ and N_elu<0) and (abs(e_els)>h/2-d_ and N_els<0):
        etat="Totalement tendue"
    elif (abs(e_elu)>h/2-d_ and N_elu<0) and (abs(e_els)<=h/2-d_ and N_els<0):
        etat="Totalement tendue"
    elif (abs(e_elu)<=h/2-d_ and N_elu<0) and (abs(e_els)<=h/2-d_ and N_els<0):
        etat="Totalement tendue"
    elif (N_elu>0 and mu_u<=0.493) and (N_els>0 and abs(e_ser)>h/6):
        etat="Partiellement comprimée"
    elif (N_elu>0 and mu_u<=0.493) and (N_els>0 and abs(e_ser)<=h/6):
        etat="Totalement comprimée"
    elif (N_elu>0 and mu_u>0.493) and (N_els>0 and abs(e_ser)>h/6):
        etat="Totalement comprimée"
    elif (N_elu>0 and mu_u>0.493) and (N_els>0 and abs(e_ser)<=h/6):
        etat="Totalement comprimée"
        
    return e_els, e_elu, etat
        
def flexion_partiellement_(N_elu, M_elu, M_els, b, h, d, fck, fyk, classe_exposition, classe_acier, palier_acier, coeff_secu_beton, coeff_secu_acier, cuvelage, niveau_eau, Es):
    d_=h-d
    e=M_elu/N_elu
    delta=d_/d
    #section rectangulaire
    if M_elu>0 and N_elu>0:
        e_=abs(e)-h/2+d
    elif M_elu>0 and N_elu<0:
        e_=abs(e)+h/2-d
    elif M_elu<0 and N_elu>0:
        e_=abs(e)-h/2+d
    elif M_elu<0 and N_elu<0:
        e_=abs(e)+h/2-d
    M_ua=abs(N_elu)*e_
    
    #Calcul du moment limite ##################################################
    alpha_e=15
    gamma=M_elu/M_els
    if classe_exposition=="XD" or classe_exposition=="XS" or classe_exposition=="XF":
        if fck<=30:
            if palier_acier=="Horizontal":
                mu_lim=(2740*gamma+60*fck-3100)*10**-4
            else:
                mu_lim=(2800*gamma+37*fck-2605)*10**-4
        else:
            if palier_acier=="Horizontal":
                A=71.2*fck+108
                B=-5.2*fck+874.4
                C=0.03*fck-12.5
                K=(A+B*alpha_e+C*(alpha_e**2))*10**-4
                mu_lim=(fck*K)/((4.69-1.70*gamma)*fck+(159.90-76.20*gamma))
            else:
                A=75.3*fck-189.8
                B=-5.6*fck+874.5
                C=0.04*fck-13
                K=(A+B*alpha_e+C*(alpha_e**2))*10**-4
                mu_lim=(fck*K)/((4.62-1.66*gamma)*fck+(165.69-79.62*gamma))
    else:
        mu_lim=0.372
    ###########################################################################
    
    #Calcul de la section d'acier #############################################
    
    mu_cu=abs(M_ua)/(b*d**2*fck/coeff_secu_beton)
    
    if fck<=50:
        lambda_=0.8
    elif fck>50 and fck<90:
        lambda_= 0.8-(fck-50)/400
        
    if mu_cu<=mu_lim:
        alpha_u=(1/lambda_)*(1-(1-2*mu_cu)**0.5)
        z=d*(1-0.5*lambda_*alpha_u)
        sigma_s1=contrainte_acier(cuvelage, alpha_u,fyk, palier_acier, classe_acier, niveau_eau, coeff_secu_acier, Es)
        As1=abs(M_elu)/(z*sigma_s1)-N_elu/sigma_s1
        As2=0
        
    else:
        alpha_u=(1/lambda_)*(1-(1-2*mu_lim)**0.5)
        z=d*(1-0.5*lambda_*alpha_u)
        sigma_s1=contrainte_acier(cuvelage, alpha_u,fyk, palier_acier, classe_acier, niveau_eau, coeff_secu_acier, Es)
        M_lu=mu_lim*b*d**2*fck/coeff_secu_beton
        if palier_acier=="Horizontal":
            a=0.5/alpha_e+13
            b=6517/alpha_e+1
        else:
            a=-5/alpha_e+13
            b=6855/alpha_e-9
        sigma_s2e=0.6*alpha_e*gamma*fck-delta*(a*fck+b)
        sigma_s1e=(a*fck+b)-0.6*alpha_e*gamma*fck
        As2=(abs(M_ua)-M_lu)/((d-d_)*sigma_s2e)
        As1=M_lu/(z*sigma_s1)+As2*sigma_s2e/sigma_s1e-N_elu/sigma_s1
    
    return M_ua, mu_lim, mu_cu, alpha_u, z, sigma_s1, As1*10**4, As2*10**4

def flexion_totalement_tendue(N_elu, N_els, M_elu, M_els, b, h, d, fck, fyk, classe_exposition, classe_acier, palier_acier, coeff_secu_beton, coeff_secu_acier, cuvelage, niveau_eau, Es):
    #efforts en MN
    d_=h-d
    e=M_elu/N_elu
    fctm=f_ctm(fck)
    #################################
    if fck<=50:
        lambda_=0.8
    elif fck>50 and fck<90:
        lambda_= 0.8-(fck-50)/400
    alpha_u= (1/lambda_)*(1-(1-2*(M_elu/(b*d**2*fck/coeff_secu_beton)))**0.5)
    #################################
    sigma_s1=contrainte_acier(cuvelage, alpha_u, fyk, palier_acier, classe_acier, niveau_eau, coeff_secu_acier, Es)
    #As1=section acier inférieure
    #As2=section acier supérieure
    
    if M_elu>=0:
        e1=-abs(e)+h/2-d_
        e2=abs(e)+h/2-d_
        
    else: 
        e1=abs(e)+h/2-d_
        e2=-abs(e)+h/2-d_
    
    As1=abs(N_elu)*e2/((e1+e2)*sigma_s1)
    As2=abs(N_elu)*e1/((e1+e2)*sigma_s1)
    
    Nf=(h/2)/(3*(e-h/6))*(b*d*fctm)
    As_min1=abs(Nf)*e2/((e1+e2)*fyk)
    As_min2=abs(Nf)*e1/((e1+e2)*fyk) #Cuvelage!!!!!!!!!
    
    sigma_1=(N_els*e2)/((e1+e2)*As1)
    sigma_2=(N_els*e1)/((e1+e2)*As2)
    sigma=max(sigma_1, sigma_2)
    if sigma>0.8*fyk:
        verif="Contraintes à l'ELS non vérifiées !"
    else:
        verif="La vérification à l'ELS est satisfaite !"
    
    As1_retenu=max(As1, As_min1)
    As2_retenu=max(As2, As_min2)
    
    return As1_retenu*10**4, As2_retenu*10**4, verif

def verification_contrainte_partiellement_(N_els, M_els, As1, As2, fck, fyk, n, b, h, d, e_ser): #Si cuvelage sinon pas besoin
    d_=h-d
    c=d-e_ser
    p=-3*c**2-6*n*As2*(c-d_)/b+6*n*As1*(d-c)/b
    q=-2*c**3-6*n*As2*(c-d_)**2/b+6*n*As1*(d-c)**2/b
    poly=np.polynomial.polynomial.Polynomial([q, p,0,1])
    res=poly.roots()
    xc=max(res)
    x1=xc+c
    If=inertie_fissuree(n,As1, As2, b, h, d)
    sigma_c=N_els*xc*x1/If
    sigma_s1=n*N_els*xc*(d-x1)/If
    sigma_s2=n*N_els*xc*(x1-d_)/If
    if sigma_c>fck or sigma_s1>0.8*fyk or sigma_s2>0.8*fyk:
        return "La vérification à l'ELS à échouer !"
    else:
        return "La vérification à l'ELS est satisfaite !"
    
def diagramme_interaction(As_inf, As_sup, M_elu, N_elu, b, h, d, fck, fyk, classe_acier):
    d_=h-d
    for i in range(len(Caract_beton_flexion)):
        if Caract_beton_flexion[i][0]==fck:
            fctm, Ecm, epscu1, epsc1, epscu2, epsc2,n=Caract_beton_flexion[i][1], Caract_beton_flexion[i][2],Caract_beton_flexion[i][3],Caract_beton_flexion[i][4],Caract_beton_flexion[i][5],Caract_beton_flexion[i][6],Caract_beton_flexion[i][7]
    if classe_acier=="A":
        eps_uk=25 #pour mille
        k=1.05
    elif classe_acier=="B":
        eps_uk=50
        k=1.08
    else:
        eps_uk=75
        k=1.15
    
    
    N_A, M_A=pivot_A(b,h,d,fck,fyk,epsc2,n, eps_uk, k, As_inf, As_sup)
    N_A_B, M_A_B=pivot_A_B(b,h,d,fck,fyk,epsc2, n, eps_uk, k, As_inf, As_sup)
    N_B,M_B=pivot_B(b,h,d,fck,fyk,epsc2, n, eps_uk, k, As_inf, As_sup)
    N_B_C, M_B_C=pivot_B_C(b,h,d,fck,fyk,epsc2,n,eps_uk, k, As_inf, As_sup)
    N_C, M_C=pivot_C(b,h,d,fck,fyk, epsc2,n, eps_uk, k, As_inf, As_sup)
    
    N=[N_A, [N_A_B], N_B, N_B_C, N_C]
    M=[M_A, [M_A_B], M_B, M_B_C, M_C]
    N_=liste_multiple_vers_simple(N)
    M_=liste_multiple_vers_simple(M)
    
    N_milieu=(N_[0]+N_[-1])/2
    M_milieu=(M_[0]+M_[-1])/2
    
    N_2=[]
    M_2=[]
    for i in range(len(N_)):    
        N_2.append((N_milieu-N_[i])*2+N_[i])
        M_2.append((M_milieu-M_[i])*2+M_[i])
    
    
    return N_, N_2, M_, M_2

def pivot_A(b,h,d, fck, fyk, epsc2, n, eps_uk,k, As_inf, As_sup):
    d_=h-d
    N_sup=[0]*5+[0,0.6,1.2,1.8,2.4,2.6]
    eps_sup=[-50,-32,-25,-18,-12]+[0]*6
    eps_inf=[-50]*11
    N_inf=[0]*11
    Axe_neutre=[0]*11
    Coeff_remp=[0]*11
    Coeff_grav=[0]*11
    Effort_beton=[0]*11
    sigma_sup=[0]*11
    sigma_inf=[0]*11
    Effort_sup=[0]*11
    Effort_inf=[0]*11
    N_tot=[0]*11
    M_tot=[0]*11
    
    for i in range(5):
        N_sup[i]=eps_sup[i]-((eps_sup[i]-eps_inf[i])/(d_-d))*d_
        N_inf[i]=((eps_sup[i]-eps_inf[i])/(d_-d))*h+(eps_sup[i]-((eps_sup[i]-eps_inf[i])/(d_-d))*d_)
    for i in range(5,11):
        eps_sup[i]=(-(N_sup[i]-eps_inf[i])/d)*d_+N_sup[i]
        N_inf[i]=(-(N_sup[i]-eps_inf[i])/d)*h+N_sup[i]    
    for i in range(11):
        y=N_sup[i]*h/(abs(N_sup[i])+abs(N_inf[i]))
        if y>=0:
            Axe_neutre[i]=y
    for i in range(11):
        if Axe_neutre[i]==0:
            Coeff_remp[i]=0
            Coeff_grav[i]=0
        elif N_sup[i]<epsc2 and N_sup[i]!=0:
            Coeff_remp[i]=1+(((1-(N_sup[i])/epsc2)**(1+n))-1)/((1+n)*abs(N_sup[i])/epsc2)
            Coeff_grav[i]=-((abs(N_sup[i])/epsc2)**2*n**2-2*(abs(N_sup[i])/epsc2)**2*(1-(abs(N_sup[i])/epsc2))**n+3*(abs(N_sup[i])/epsc2)**2*n+2*(abs(N_sup[i])/epsc2)**2+4*(abs(N_sup[i])/epsc2)*(1-(abs(N_sup[i])/epsc2))**n-2*(1-(abs(N_sup[i])/epsc2))**n-2*(abs(N_sup[i])/epsc2)*n-4*(abs(N_sup[i])/epsc2)+2)/(2*(abs(N_sup[i])/epsc2)*(n+2)*((abs(N_sup[i])/epsc2)*(1-(abs(N_sup[i])/epsc2))**n-(1-(abs(N_sup[i])/epsc2))**n-(abs(N_sup[i])/epsc2)*n+1-(abs(N_sup[i])/epsc2)))
        elif N_sup[i]==0:
            Coeff_remp[i]=0
            Coeff_grav[i]=0
        else:
            Coeff_remp[i]=1-1/(abs(N_sup[i])/epsc2*(1+n))
            Coeff_grav[i]=((n/(n+1))*((abs(N_sup[i])/epsc2)-1+(n+1)/(2*n+4))+0.5*((abs(N_sup[i])/epsc2)-1)**2)/((abs(N_sup[i])/epsc2)*((n/(n+1))+((abs(N_sup[i])/epsc2)-1)))
    for i in range(11):
        if Axe_neutre[i]!=0:
            Effort_beton[i]=Coeff_remp[i]*Axe_neutre[i]*b*fck/1.5
    for i in range(11):
        if abs(eps_sup[i])<2.17:
            sigma_sup[i]=eps_sup[i]*Es/1000 
            sigma_inf[i]=eps_inf[i]*Es/1000 
        else:
            sigma_sup[i]=fyk/1.15*((1+((k-1)*(abs(eps_sup[i])/1000-fyk/1.15/Es))/(eps_uk/1000-fyk/1.15/Es)))*abs(eps_sup[i])/eps_sup[i]
            sigma_inf[i]=fyk/1.15*((1+((k-1)*(abs(eps_inf[i])/1000-fyk/1.15/Es))/(eps_uk/1000-fyk/1.15/Es)))*abs(eps_inf[i])/eps_inf[i]
    for i in range(11):
        Effort_sup[i]=sigma_sup[i]*As_sup*10**-4
        Effort_inf[i]=sigma_inf[i]*As_inf*10**-4
        
    for i in range(11):
        N_tot[i]=Effort_beton[i]+Effort_sup[i]+Effort_inf[i]
        if Axe_neutre[i]==0:
            M_tot[i]=Effort_inf[i]*(h/2-d)-Effort_sup[i]*(d_-h/2)
        else:
            M_tot[i]=Effort_beton[i]*(h/2-Coeff_grav[i]*Axe_neutre[i])+Effort_inf[i]*(h/2-d)-Effort_sup[i]*(d_-h/2)
    return N_tot, M_tot
        
def pivot_A_B(b,h,d,fck,fyk,epsc2, n, eps_uk, k, As_inf, As_sup):
    d_=h-d
    N_sup=3.5
    eps_inf=-50
    eps_sup=(-(N_sup-eps_inf)/d)*d_+N_sup
    N_inf=(-(N_sup-eps_inf)/d)*h+N_sup
    y=N_sup*h/(abs(N_sup)+abs(N_inf))
    Axe_neutre=0
    if y>=0:
        Axe_neutre=y
    Coeff_remp=1-1/(abs(N_sup)/epsc2*(1+n))
    if Axe_neutre==0:
        Coeff_grav=0
    elif N_sup<epsc2 and N_sup!=0:
        Coeff_grav=-((abs(N_sup)/epsc2)**2*n**2-2*(abs(N_sup)/epsc2)**2*(1-(abs(N_sup)/epsc2))**n+3*(abs(N_sup)/epsc2)**2*n+2*(abs(N_sup)/epsc2)**2+4*(abs(N_sup)/epsc2)*(1-(abs(N_sup)/epsc2))**n-2*(1-(abs(N_sup)/epsc2))**n-2*(abs(N_sup)/epsc2)*n-4*(abs(N_sup)/epsc2)+2)/(2*(abs(N_sup)/epsc2)*(n+2)*((abs(N_sup)/epsc2)*(1-(abs(N_sup)/epsc2))**n-(1-(abs(N_sup)/epsc2))**n-(abs(N_sup)/epsc2)*n+1-(abs(N_sup)/epsc2)))
    elif N_sup==0:
        Coeff_grav=0
    else:
        Coeff_grav=((n/(n+1))*((abs(N_sup)/epsc2)-1+(n+1)/(2*n+4))+0.5*((abs(N_sup)/epsc2)-1)**2)/((abs(N_sup)/epsc2)*((n/(n+1))+((abs(N_sup)/epsc2)-1)))
    Effort_beton=0
    if Axe_neutre!=0:
        Effort_beton=Coeff_remp*Axe_neutre*b*fck/1.5
    if abs(eps_sup)<2.17:
        sigma_sup=eps_sup*Es/1000 
        sigma_inf=eps_inf*Es/1000 
    else:
        sigma_sup=fyk/1.15*((1+((k-1)*(abs(eps_sup)/1000-fyk/1.15/Es))/(eps_uk/1000-fyk/1.15/Es)))*abs(eps_sup)/eps_sup
        sigma_inf=fyk/1.15*((1+((k-1)*(abs(eps_inf)/1000-fyk/1.15/Es))/(eps_uk/1000-fyk/1.15/Es)))*abs(eps_inf)/eps_inf
    Effort_sup=sigma_sup*As_sup*10**-4
    Effort_inf=sigma_inf*As_inf*10**-4
    N_tot=Effort_beton+Effort_sup+Effort_inf
    M_tot=Effort_beton*(h/2-Coeff_grav*Axe_neutre)+Effort_inf*(h/2-d)-Effort_sup*(d_-h/2)

    return N_tot, M_tot
    
def pivot_B(b,h,d,fck,fyk,epsc2, n, eps_uk, k, As_inf, As_sup):
    d_=h-d
    N_sup=[3.5]*21
    eps_sup=[0]*21
    eps_inf=[-50]*21
    N_inf=[0]*21
    Axe_neutre=[0]*21
    Coeff_remp=[0]*21
    Coeff_grav=[0]*21
    Effort_beton=[0]*21
    sigma_sup=[0]*21
    sigma_inf=[0]*21
    Effort_sup=[0]*21
    Effort_inf=[0]*21
    N_tot=[0]*21
    M_tot=[0]*21
    
    for i in range(4):
        eps_inf[i]=-50+50/15*(i+1)
    eps_inf[4]=-50+50/15*6
    eps_inf[5]=-50+50/15*8
    eps_inf[6]=-50+50/15*10
    for i in range(7, 10):
        eps_inf[i]=-50+50/15*(i+4)
    eps_inf[10]=-50+50/15*13.5
    eps_inf[11]=-50+50/15*14
    eps_inf[12]=-50+50/15*14.2
    eps_inf[13]=-50+50/15*14.4
    eps_inf[14]=-50+50/15*14.6
    eps_inf[15]=-50+50/15*14.8
    eps_inf[16]=0    
    for i in range(17):
        N_inf[i]=(-(N_sup[i]-eps_inf[i])/d)*h+N_sup[i]    
    
    for i in range(17,20):
        N_inf[i]=N_inf[16]-N_inf[16]/4*(i-16)
    N_inf[20]=0
    
    for i in range(17,21):
        eps_inf[i]=-(N_sup[i]-N_inf[i])/h*d+N_sup[i]
    for i in range(21):
        eps_sup[i]=(-(N_sup[i]-eps_inf[i])/d)*d_+N_sup[i]
    for i in range(21):
        y=N_sup[i]*h/(abs(N_sup[i])+abs(N_inf[i]))
        if y>=0:
            Axe_neutre[i]=y
    for i in range(21):
        if Axe_neutre[i]==0:
            Coeff_remp[i]=0
            Coeff_grav[i]=0
        elif N_sup[i]<epsc2 and N_sup[i]!=0:
            Coeff_remp[i]=1+(((1-(N_sup[i])/epsc2)**(1+n))-1)/((1+n)*abs(N_sup[i])/epsc2)
            Coeff_grav[i]=-((abs(N_sup[i])/epsc2)**2*n**2-2*(abs(N_sup[i])/epsc2)**2*(1-(abs(N_sup[i])/epsc2))**n+3*(abs(N_sup[i])/epsc2)**2*n+2*(abs(N_sup[i])/epsc2)**2+4*(abs(N_sup[i])/epsc2)*(1-(abs(N_sup[i])/epsc2))**n-2*(1-(abs(N_sup[i])/epsc2))**n-2*(abs(N_sup[i])/epsc2)*n-4*(abs(N_sup[i])/epsc2)+2)/(2*(abs(N_sup[i])/epsc2)*(n+2)*((abs(N_sup[i])/epsc2)*(1-(abs(N_sup[i])/epsc2))**n-(1-(abs(N_sup[i])/epsc2))**n-(abs(N_sup[i])/epsc2)*n+1-(abs(N_sup[i])/epsc2)))
        elif N_sup[i]==0:
            Coeff_remp[i]=0
            Coeff_grav[i]=0
        else:
            Coeff_remp[i]=1-1/(abs(N_sup[i])/epsc2*(1+n))
            Coeff_grav[i]=((n/(n+1))*((abs(N_sup[i])/epsc2)-1+(n+1)/(2*n+4))+0.5*((abs(N_sup[i])/epsc2)-1)**2)/((abs(N_sup[i])/epsc2)*((n/(n+1))+((abs(N_sup[i])/epsc2)-1)))
    for i in range(21):
        if Axe_neutre[i]!=0:
            Effort_beton[i]=Coeff_remp[i]*Axe_neutre[i]*b*fck/1.5
    for i in range(21):
        if abs(eps_sup[i])<2.17:
            sigma_sup[i]=eps_sup[i]*Es/1000 
        else:
            if eps_sup[i]!=0:
                sigma_sup[i]=fyk/1.15*((1+((k-1)*(abs(eps_sup[i])/1000-fyk/1.15/Es))/(eps_uk/1000-fyk/1.15/Es)))*abs(eps_sup[i])/eps_sup[i]
            else:
                sigma_sup[i]=0
        if abs(eps_inf[i])<2.17:  
            sigma_inf[i]=eps_inf[i]*Es/1000
        else:
            if eps_inf[i]!=0:
                sigma_inf[i]=fyk/1.15*((1+((k-1)*(abs(eps_inf[i])/1000-fyk/1.15/Es))/(eps_uk/1000-fyk/1.15/Es)))*abs(eps_inf[i])/eps_inf[i]
            else:
                sigma_inf[i]=0
                    
    for i in range(21):
        Effort_sup[i]=sigma_sup[i]*As_sup*10**-4
        Effort_inf[i]=sigma_inf[i]*As_inf*10**-4
        
    for i in range(21):
        N_tot[i]=Effort_beton[i]+Effort_sup[i]+Effort_inf[i]
        if Axe_neutre[i]==0:
            M_tot[i]=Effort_inf[i]*(h/2-d)-Effort_sup[i]*(d_-h/2)
        else:
            M_tot[i]=Effort_beton[i]*(h/2-Coeff_grav[i]*Axe_neutre[i])+Effort_inf[i]*(h/2-d)-Effort_sup[i]*(d_-h/2)
    return N_tot, M_tot
    
def pivot_B_C(b,h,d,fck,fyk,epsc2,n,eps_uk, k, As_inf, As_sup):
    d_=h-d
    N_sup=[3.5]*8
    eps_sup=[0]*8
    eps_inf=[0]*8
    N_inf=[0]*8
    Axe_neutre=[0]*8
    Coeff_remp=[0]*8
    Coeff_grav=[0]*8
    Effort_beton=[0]*8
    sigma_sup=[0]*8
    sigma_inf=[0]*8
    Effort_sup=[0]*8
    Effort_inf=[0]*8
    N_tot=[0]*8
    M_tot=[0]*8
    

    for i in range(8):
        eps_sup[i]=(-(N_sup[i]-N_inf[i])/h)*d_+N_sup[i]
        eps_inf[i]=(-(N_sup[i]-N_inf[i])/h)*d+N_sup[i]
    for i in range(8):
        y=N_sup[i]*h/(abs(N_sup[i])-abs(N_inf[i]))
        if y>=0:
            Axe_neutre[i]=y
    for i in range(8):
        if Axe_neutre[i]==0:
            Coeff_remp[i]=0
            Coeff_grav[i]=0
        elif N_sup[i]<epsc2 and N_sup[i]!=0:
            Coeff_remp[i]=1+(((1-(N_sup[i])/epsc2)**(1+n))-1)/((1+n)*abs(N_sup[i])/epsc2)
            Coeff_grav[i]=-((abs(N_sup[i])/epsc2)**2*n**2-2*(abs(N_sup[i])/epsc2)**2*(1-(abs(N_sup[i])/epsc2))**n+3*(abs(N_sup[i])/epsc2)**2*n+2*(abs(N_sup[i])/epsc2)**2+4*(abs(N_sup[i])/epsc2)*(1-(abs(N_sup[i])/epsc2))**n-2*(1-(abs(N_sup[i])/epsc2))**n-2*(abs(N_sup[i])/epsc2)*n-4*(abs(N_sup[i])/epsc2)+2)/(2*(abs(N_sup[i])/epsc2)*(n+2)*((abs(N_sup[i])/epsc2)*(1-(abs(N_sup[i])/epsc2))**n-(1-(abs(N_sup[i])/epsc2))**n-(abs(N_sup[i])/epsc2)*n+1-(abs(N_sup[i])/epsc2)))
        elif N_sup[i]==0:
            Coeff_remp[i]=0
            Coeff_grav[i]=0
        else:
            Coeff_remp[i]=1-1/(abs(N_sup[i])/epsc2*(1+n))
            Coeff_grav[i]=((n/(n+1))*((abs(N_sup[i])/epsc2)-1+(n+1)/(2*n+4))+0.5*((abs(N_sup[i])/epsc2)-1)**2)/((abs(N_sup[i])/epsc2)*((n/(n+1))+((abs(N_sup[i])/epsc2)-1)))
    for i in range(8):
        if Axe_neutre[i]!=0:
            Effort_beton[i]=Coeff_remp[i]*Axe_neutre[i]*b*fck/1.5
    for i in range(8):
        if abs(eps_sup[i])<2.17:
            sigma_sup[i]=eps_sup[i]*Es/1000  
        else:
            sigma_sup[i]=fyk/1.15*((1+((k-1)*(abs(eps_sup[i])/1000-fyk/1.15/Es))/(eps_uk/1000-fyk/1.15/Es)))*abs(eps_sup[i])/eps_sup[i]
        if abs(eps_inf[i])<2.17:
            sigma_inf[i]=eps_inf[i]*Es/1000 
        else:
            sigma_inf[i]=fyk/1.15*((1+((k-1)*(abs(eps_inf[i])/1000-fyk/1.15/Es))/(eps_uk/1000-fyk/1.15/Es)))*abs(eps_inf[i])/eps_inf[i]
    for i in range(8):
        Effort_sup[i]=sigma_sup[i]*As_sup*10**-4
        Effort_inf[i]=sigma_inf[i]*As_inf*10**-4
        
    for i in range(8):
        N_tot[i]=Effort_beton[i]+Effort_sup[i]+Effort_inf[i]
        if Axe_neutre[i]==0:
            M_tot[i]=Effort_inf[i]*(h/2-d)-Effort_sup[i]*(d_-h/2)
        else:
            M_tot[i]=Effort_beton[i]*(h/2-Coeff_grav[i]*Axe_neutre[i])+Effort_inf[i]*(h/2-d)-Effort_sup[i]*(d_-h/2)
    return N_tot, M_tot

def pivot_C(b,h,d,fck,fyk, epsc2,n, eps_uk, k, As_inf, As_sup):
    d_=h-d
    N_sup=[0]*10+[2]
    eps_sup=[0]*11
    eps_inf=[0]*11
    N_inf=[0]*11
    Axe_neutre=[0]*11
    Coeff_remp=[0]*11
    Coeff_grav=[0]*11
    Effort_beton=[0]*11
    sigma_sup=[0]*11
    sigma_inf=[0]*11
    Effort_sup=[0]*11
    Effort_inf=[0]*11
    N_tot=[0]*11
    M_tot=[0]*11
    
    for i in range(10):
        N_sup[i]=3.5-(3.5-N_sup[10])/11*(i+1)
    for i in range(11):
        eps_sup[i]=(-(N_sup[i]-2)/(3/7*h))*d_+N_sup[i]
        eps_inf[i]=(-(N_sup[i]-2)/(3/7*h))*d+N_sup[i]
        N_inf[i]=(-(N_sup[i]-2)/(3/7*h))*h+N_sup[i]
    for i in range(11):
        if N_sup[i]!=N_inf[i]:
            y=N_sup[i]*h/(abs(N_sup[i])-abs(N_inf[i]))
        else:
            y=100000000000000000000000000
        if y>=0:
            Axe_neutre[i]=y
    for i in range(11):
        if N_sup[i]!=N_inf[i]:
            Coeff_remp[i]=1-(1-N_inf[i]/epsc2)**(n+1)/((n+1)*(N_sup[i]/epsc2-N_inf[i]/epsc2))
            Coeff_grav[i]=(1/((N_sup[i]/epsc2)-(N_inf[i]/epsc2)))*((1+n*(1-(N_inf[i]/epsc2))+(1-(N_inf[i]/epsc2))**n*(-1+(N_inf[i]/epsc2))-(N_inf[i]/epsc2))/(1+n)*(((1+n)*(n-2*(-1+(1-(N_inf[i]/epsc2))**n))*(1-(N_inf[i]/epsc2)))/(2*(2+n)*(1+n-(1-(N_inf[i]/epsc2))**n))+(N_sup[i]/epsc2)-1)+0.5*((N_sup[i]/epsc2)-1)**2)/((1+n*(1-(N_inf[i]/epsc2))+(1-(N_inf[i]/epsc2))**n*(-1+(N_inf[i]/epsc2))-(N_inf[i]/epsc2))/(1+n)+(N_sup[i]/epsc2)-1)
        else:
            Coeff_remp[i]=1
            Coeff_grav[i]=0.5
    for i in range(11):
        if Axe_neutre[i]>=h:
            Effort_beton[i]=Coeff_remp[i]*h*b*fck/1.5
        else:
            Effort_beton[i]=Coeff_remp[i]*Axe_neutre[i]*b*fck/1.5
    for i in range(11):
        if abs(eps_sup[i])<2.17:
            sigma_sup[i]=eps_sup[i]*Es/1000  
        else:
            sigma_sup[i]=fyk/1.15*((1+((k-1)*(abs(eps_sup[i])/1000-fyk/1.15/Es))/(eps_uk/1000-fyk/1.15/Es)))*abs(eps_sup[i])/eps_sup[i]
        if abs(eps_inf[i])<2.17:
            sigma_inf[i]=eps_inf[i]*Es/1000 
        else:
            sigma_inf[i]=fyk/1.15*((1+((k-1)*(abs(eps_inf[i])/1000-fyk/1.15/Es))/(eps_uk/1000-fyk/1.15/Es)))*abs(eps_inf[i])/eps_inf[i]
    for i in range(11):
        Effort_sup[i]=sigma_sup[i]*As_sup*10**-4
        Effort_inf[i]=sigma_inf[i]*As_inf*10**-4
        
    for i in range(11):
        N_tot[i]=Effort_beton[i]+Effort_sup[i]+Effort_inf[i]
        M_tot[i]=Effort_beton[i]*(h/2-Coeff_grav[i]*h)+Effort_inf[i]*(h/2-d)-Effort_sup[i]*(d_-h/2)
    return N_tot, M_tot

def verif_section_diagramme_interaction(As_inf, As_sup, M_elu, N_elu, b, h, d, fck, fyk, classe_acier):
    N_, N_2, M_, M_2=diagramme_interaction(As_inf, As_sup, M_elu, N_elu, b, h, d, fck, fyk, classe_acier)
    res=False
    res_1=False
    res_2=False
    
    N_soll=[N_elu ]
    M_soll=[M_elu]
    for i in range(1,len(N_)):
        if  N_soll[0]>=N_[i-1] and N_soll[0]<=N_[i] and M_soll[0]<=M_[i]:
            res_1=True
    for i in range(len(N_2)):
        if N_soll[0]>=N_2[i-1] and N_soll[0]<=N_2[i] and M_soll[0]>=M_2[i]:
            res_2=True
            
    if res_1==True and res_2==True:
        res=True
    
    if res==True:
        return "La section d'acier choisie convient ! ", plt.plot(N_,M_), plt.plot(N_2,M_2), plt.scatter(N_soll, M_soll), plt.grid()
    else: 
        return "La section d'acier choisie ne convient pas !", plt.plot(N_,M_), plt.plot(N_2,M_2), plt.scatter(N_soll, M_soll), plt.grid(), plt.show()

def section_min_flexion(b, d, h, fck, fyk, coeff_secu_acier):   # MAJ
    fctm=f_ctm(fck)
    fyd=fyk/coeff_secu_acier
    As_min= max(0.26*fctm*b*d/fyk, 0.0013*b*d)
    return As_min*10**4

def section_min(b, d, h, fck, fyk, coeff_secu_acier, cuvelage, precaution, M_elu, N_elu):   # MAJ
    if cuvelage==False or cuvelage=="Etancheite":
        As_min=section_min_flexion(b, d, h, fck, fyk, coeff_secu_acier)
    elif cuvelage=="Imperméabilisation":
        if precaution==True:
            As_min_=1/1000*b*h*10**4
            if As_min_>4:
                As_min_=4.00
            As_min=max(As_min_, section_min_flexion(b, d, h, fck, fyk, coeff_secu_acier) )
        else:
            As_min=2.5/1000*b*h*10**4
    elif cuvelage=="Etanche":
        if N_elu<0 or (M_elu!=0 and N_elu<0 and M_elu/N_elu<=h/2):
            if precaution==True:
                As_min_=1/1000*b*h*10**4
                if As_min_>4:
                    As_min_=4.00
                As_min=max(As_min_, section_min_flexion(b, d, h, fck, fyk, coeff_secu_acier))
            else:
                As_min=2.5/1000*b*h*10**4
        else:
            As_min=section_min_flexion(b, d, h, fck, fyk, coeff_secu_acier)
    return round(As_min, 3)
        
    
def inertie_fissuree(n, As1, As2, b, h, d):
    d_=h-d
    As_1=As1*10**-4
    As_2=As2*10**-4
    poly=np.polynomial.polynomial.Polynomial([-n*As_1*d-n*As_2*d_, n*As_1+n*As_2, b/2])
    res=poly.roots()
    for i in range(len(res)):
        if res[i]>=0:
            axe_neutre=res[i]
    inertie=b/3*axe_neutre**3+n*As_1*(d-axe_neutre)**2+n*As_2*(d_-axe_neutre)**2
    return axe_neutre, inertie

def inertie_homogene(As1, As2, b,d,h,n):
    d_=h-d
    
    I_c=b*h**3/12
    y_gc=h/2
    Ac=b*h
    Sc=Ac*y_gc
    
    y_gc1=d
    y_gc2=d_
    Ss1=As1*y_gc1
    Ss2=As2*y_gc2
    
    A=Ac+n*(As1+As2)
    S=Sc+n*(Ss1+Ss2)
    y=S/A
    
    inertie=I_c+(y_gc-y)**2*S+n*(y_gc1-y)**2*S+n*(y_gc2-y)**2*y
    return A, inertie, y

def ep_mini_flexion(b, M_elu, fck, enrobage, coeff_secu_beton):  #MAJ
    d=1/(0.372*(fck/coeff_secu_beton)*b/M_elu)**0.5
    return d+enrobage

def verification_tranchant(T_elu, N_elu, b, h, d, As1, fck, coeff_secu_beton): # MAJ
    Crd_c=0.12
    k=min(2, 1+(200/(d*1000))**0.5)
    rho=min(As1/b/d, 0.02)
    k1=0.15
    sigma=min(0.2*fck/coeff_secu_beton, N_elu/b/h)
    nu_min=0.23*(fck)**0.5
    Vrd_c=max((nu_min+k1*sigma)*b*d, (Crd_c*k*(100*rho*fck)**(1/3)+k1*sigma)*b*d)
    if T_elu<=Vrd_c:
        return True
    else:
        return False
###############################################################################

############################### Cuvelage ######################################  

def impermeabilisation(M_elu, N_elu, As1, As2, fck, n, h, b, precaution, enrobage): # PAS NECESSAIRE
    #### Epaisseur minimale 
    h_=enrobage+0.01
    while recherche_ep_mini(b, h_, h_-enrobage, M_elu, N_elu, As1, As2, fck, n)==False:
        h_+=0.01
        
    if precaution==True:
        As_min=1/1000*b*h*10**4
        if As_min>4:
            As_min=4.00
    else:
        As_min=2.5/1000*b*h*10**4
    return h_, As_min

def recherche_ep_mini(b, h, d, M_elu, N_elu, As1, As2, fck, n):
    if N_elu<0 and M_elu==0:
        theta=1
    elif M_elu!=0 and N_elu<0 and M_elu/N_elu<=h/2:
        theta=1+(4*M_elu/N_elu/3*h)
    else:
        theta=5/3
    A, Ih, y=inertie_homogene(As1, As2, b, d, h, n)
    sigma_ct=abs(N_elu/A-M_elu*(h-y)/Ih)
    if sigma_ct>1.1*(0.6+0.06*fck)*theta:
        return True
    else:
        return False

def etancheite(b, d, h, fck, fyk, coeff_secu_acier): #MAJ
    As_min=section_min_flexion(b, d, h, fck, fyk, coeff_secu_acier)
    return As_min

def etanche(M_elu, N_elu, b, h, d, As1, As2, fck, fyk, precaution, coeff_secu_acier, enrobage): # PAS NECESSAIRE
    #Section mini sur la face opposée à celle en contact avec l'eau
    h_=enrobage
    if N_elu<0 or (M_elu!=0 and N_elu<0 and M_elu/N_elu<=h/2):
        while recherche_ep_mini(b, h_, h_-enrobage, M_elu, N_elu, As1, As2, fck, n)==False:
            h_+=0.01
        if precaution==True:
            As_min=1/1000*b*h*10**4
            if As_min>4:
                As_min=4.00
        else:
            As_min=2.5/1000*b*h*10**4
    else:
        h_=0
        As_min=section_min_flexion(b, d, h, fck, fyk, coeff_secu_acier)
    return h_, As_min
    
def ouverture_fissure(wmax, Mqp, As1, As2, b, h, d, n, fck, Duree_ouverture, phi, Es): #Necessite le choix du ferraillage
    #Mqp=Moment ELS Quasi Permanent
    #phi=diamètre du treillis (6-9 mm)
    x, If=inertie_fissuree(n, As1, As2, b, h, d)
    Sigma_s=n*Mqp*(d-x)*If
    if Duree_ouverture=="Longue":
        kt=0.4
    else:
        kt=0.6
    hc_ef=min(2.5*(h-d), (h-x)/3, h/2)
    Ac_eff=b*hc_ef
    rho_eff=As1/Ac_eff
    alpha_e=Es/(22*((fck+8)/10)**0.3)
    f=fct_eff(fck)
    eps=max(0.6*Sigma_s/Es, (Sigma_s-kt*f/rho_eff*(1+alpha_e*rho_eff))/Es)
    
    k1=0.8
    k2=0.5
    k3=3.4
    k4=0.425
    sr_max=k3*c+k1*k2*k4*phi/rho_eff
    wk=sr_max*eps
    
    if wk<=wmax:
        return "La vérification des fissures est OK"
    else:
        return "La vérification des fissures n'est PAS OK"
    
###############################################################################

############################### Liernes #######################################

def methode_forfaitaire_simplifiee(q, nb_butons, liste_espacement): # PAS NECESSAIRE DANS UN PREMIER TEMPS - AMELIORATION DE L'ALGO FEM
    M_travee, M_appuis, T_appuis, R=creation_liste_vide(nb_butons+1), creation_liste_vide(nb_butons+2), creation_liste_vide(nb_butons), creation_liste_vide(nb_butons)    
    if nb_butons==1:
        M_o1=q*liste_espacement[0]**2/8
        M_o2=q*liste_espacement[1]**2/8
        M_appuis[0]=0.15*M_o1
        M_appuis[2]=0.15*M_o2
        M_appuis[1]=-0.65*max(M_o1, M_o2)
        M_travee[0]=1.15*M_o1-abs(M_appuis[1]+M_appuis[0])/2
        M_travee[1]=1.15*M_o2-abs(M_appuis[2]+M_appuis[1])/2
        T_appuis[0]=(-1.15*q*liste_espacement[0]/2, 1.15*q*liste_espacement[1]/2)
        R[0]=T_appuis[0][1]-T_appuis[0][0]
    elif nb_butons>1:
        nb_travee=nb_butons+1
        M_o=[]
        for i in range(nb_travee):
            if i==0:
                M_o.append(q*liste_espacement[0]**2/8)
            elif i==nb_travee-1:
                M_o.append(q*liste_espacement[2]**2/8)
            else:
                M_o.append(q*liste_espacement[1]**2/8)
        for i in range(nb_travee-1):
            if i==0 or i==nb_travee-2:
                M_appuis[i+1]=-0.55*max(M_o[i], M_o[i+1])
            else:
                M_appuis[i+1]=-0.45*max(M_o[i], M_o[i+1])
        M_appuis[0]=0.15*M_o[0]
        M_appuis[-1]=0.15*M_o[-1]
        for i in range(nb_travee):
            if i==0 or i==nb_travee-1:
                M_travee[i]=1.15*M_o[i]-abs(M_appuis[i]+M_appuis[i+1])/2
            else:
                M_travee[i]=1.10*M_o[i]-abs(M_appuis[i]+M_appuis[i+1])/2
        for i in range(nb_butons):
            if i==0:
                T_appuis[i]=(-1.10*q*liste_espacement[0]/2, 1.10*q*liste_espacement[1]/2)
            elif i==nb_butons-1:
                T_appuis[i]=(-1.10*q*liste_espacement[1]/2, 1.10*q*liste_espacement[2]/2)
            else:
                T_appuis[i]=(-q*liste_espacement[1]/2, q*liste_espacement[1]/2)
        for i in range(len(T_appuis)):
            R[i]=T_appuis[i][1]-T_appuis[i][0]
    return M_appuis, M_travee, T_appuis, R

def methode_forfaitaire(G, Q, nb_butons, liste_espacement, Coeff_ELU_G, Coeff_ELU_Q): # PAS NECESSAIRE DANS UN PREMIER TEMPS - AMELIORATION DE L'ALGO FEM
    q=ELU(G,Q, Coeff_ELU_G, Coeff_ELU_Q)
    alpha=Q/(G+Q)
    M_travee, M_appuis, T_appuis, R=creation_liste_vide(nb_butons+1), creation_liste_vide(nb_butons+2), creation_liste_vide(nb_butons), creation_liste_vide(nb_butons)    
    if nb_butons==1:
        M_o1=q*liste_espacement[0]**2/8
        M_o2=q*liste_espacement[1]**2/8
        M_appuis[0]=0.15*M_o1
        M_appuis[2]=0.15*M_o2
        M_appuis[1]=-0.6*max(M_o1, M_o2)
        M_travee[0]=max(max((1+0.3*alpha)*M_o1, 1.05*M_o1)-abs(M_appuis[1]+M_appuis[0])/2, (1.2+0.3*alpha)/2*M_o1)
        M_travee[1]=max(max((1+0.3*alpha)*M_o2, 1.05*M_o2)-abs(M_appuis[2]+M_appuis[1])/2, (1.2+0.3*alpha)/2*M_o2)
        T_appuis[0]=(-1.15*q*liste_espacement[0]/2, 1.15*q*liste_espacement[1]/2)
        R[0]=T_appuis[0][1]-T_appuis[0][0]
    elif nb_butons>1:
        nb_travee=nb_butons+1
        M_o=[]
        for i in range(nb_travee):
            if i==0:
                M_o.append(q*liste_espacement[0]**2/8)
            elif i==nb_travee-1:
                M_o.append(q*liste_espacement[2]**2/8)
            else:
                M_o.append(q*liste_espacement[1]**2/8)
        for i in range(nb_travee-1):
            if i==0 or i==nb_travee-2:
                M_appuis[i+1]=-0.5*max(M_o[i], M_o[i+1])
            else:
                M_appuis[i+1]=-0.4*max(M_o[i], M_o[i+1])
        M_appuis[0]=0.15*M_o[0]
        M_appuis[-1]=0.15*M_o[-1]
        for i in range(nb_travee):
            if i==0 or i==nb_travee-1:
                M_travee[i]=max(max((1+0.3*alpha)*M_o[i], 1.05*M_o[i])-abs(M_appuis[i]+M_appuis[i+1])/2, (1.2+0.3*alpha)/2*M_o[i])
            else:
                M_travee[i]=max(max((1+0.3*alpha)*M_o[i], 1.05*M_o[i])-abs(M_appuis[i]+M_appuis[i+1])/2, (1+0.3*alpha)/2*M_o[i])
        for i in range(nb_butons):
            if i==0:
                T_appuis[i]=(-1.10*q*liste_espacement[0]/2, 1.10*q*liste_espacement[1]/2)
            elif i==nb_butons-1:
                T_appuis[i]=(-1.10*q*liste_espacement[1]/2, 1.10*q*liste_espacement[2]/2)
            else:
                T_appuis[i]=(-q*liste_espacement[1]/2, q*liste_espacement[1]/2)
        for i in range(len(T_appuis)):
            R[i]=T_appuis[i][1]-T_appuis[i][0]
    return M_appuis, M_travee, T_appuis, R
      
def caquot(q, nb_butons, liste_espacement): # PAS NECESSAIRE DANS UN PREMIER TEMPS - AMELIORATION DE L'ALGO FEM
    if nb_butons==1:
        L_portee=[liste_espacement[0], liste_espacement[-1]]
        L_portee_f=[liste_espacement[0], liste_espacement[-1]]
    else:
        L_portee=[liste_espacement[0]]+[liste_espacement[1]]*(nb_butons-1)+[liste_espacement[-1]]
        L_portee_f=[liste_espacement[0]]+[0.8*liste_espacement[1]]*(nb_butons-1)+[liste_espacement[-1]]
    M_appuis, M_travee=creation_liste_vide(nb_butons+2), creation_liste_vide(nb_butons+1)
    T_appuis, R=creation_liste_vide(nb_butons+2), creation_liste_vide(nb_butons+2)
    for i in range(nb_butons):
        M_appuis[i+1]=-1*(q*(L_portee_f[i+1]**3+L_portee_f[i]**3)/(8.5*(L_portee_f[i+1]+L_portee_f[i])))
    M_appuis[0]=0.15*q*L_portee_f[0]**2/8
    M_appuis[-1]=0.15*q*L_portee_f[-1]**2/8
    for i in range(len(M_travee)):
        x=L_portee[i]/2-(M_appuis[i]-M_appuis[i+1])/(q*L_portee[i])
        M_travee[i]=q*L_portee[i]**2/8+M_appuis[i]*(1-x/L_portee[i])+M_appuis[i+1]*x/L_portee[i]
    for i in range(len(T_appuis)):
        if i==0:
            T_appuis[i]=(0,q*L_portee[i]/2-(M_appuis[i+1]-M_appuis[i])/L_portee[i])
        elif i==len(T_appuis)-1:
            T_appuis[i]=(-q*L_portee[i-1]/2-(M_appuis[i]-M_appuis[i-1])/L_portee[i-1],0)
        else:
            T_appuis[i]=(-q*L_portee[i-1]/2-(M_appuis[i]-M_appuis[i-1])/L_portee[i-1],q*L_portee[i]/2-(M_appuis[i+1]-M_appuis[i])/L_portee[i])
    for i in range(len(T_appuis)):
        R[i]=T_appuis[i][1]-T_appuis[i][0]
    return M_appuis, M_travee, T_appuis, R

def choix_methode_forfaitaire(G, Q, liste_espacement, cuvelage): # PAS NECESSAIRE DANS UN PREMIER TEMPS - AMELIORATION DE L'ALGO FEM
    #G et Q en MN/m²
    #cond1=charges d'exploitation modérées
    #cond2=portée successives
    #cond3=fissuration préjudiciable
    #1=condition pas respectée
    #0= condition respectée
    cond1, cond2, cond3= 0,0,0
    if cuvelage!=False:
        cond3=1
    if Q<=2*G or Q<=5*10**-3:
        pass
    else: 
        cond1=1
    if 0.8<=liste_espacement[1]/liste_espacement[0]<=1.25 and 0.8<=liste_espacement[1]/liste_espacement[2]<=1.25:
        pass
    else:
        cond2=1
    if cond3==1:
        return "Méthode de Caquot"
    else: 
        if cond1==0:
            if cond2==0 and cond3==0:
                return "Méthode forfaitaire simplifiée"
            else: 
                return "Méthode forfaitaire approchée"
        else: 
            return "Méthode de Caquot"

def lierne_epaisseur(M_elu, M_els, h, d, espacement_butons, fck, fyk, classe_exposition, classe_acier, palier_acier, coeff_secu_beton, coeff_secu_acier, cuvelage, niveau_eau, Es):
    b=3*h 
    bf=espacement_butons/5+b
    mu_lim1,mu_lu1,alpha_u1,z1,sigma_s,Asa,As_m, Asr, Asb=flexion_simple_rect(M_elu, M_els, bf, d, h, fck, fyk, classe_exposition, classe_acier, palier_acier, coeff_secu_beton, coeff_secu_acier, cuvelage, niveau_eau, Es)
    hf=d*alpha_u1
    mu_lim, mu_lu, alpha_u, z, sigma_s1, As1, As_min, As_retenu, As2=flexion_simple_T(M_elu,M_els,b,d,h,hf, bf, fck,fyk,classe_exposition,classe_acier,palier_acier, coeff_secu_beton, coeff_secu_acier, cuvelage, niveau_eau, Es)
    return   mu_lim, mu_lu, alpha_u, z, sigma_s1, As1, As_min, As_retenu, As2

def lierne_surepaisseur_int(M_elu, M_els, b, h, d, hf, espacement_butons, fck, fyk, classe_exposition, classe_acier, palier_acier, coeff_secu_beton, coeff_secu_acier, cuvelage, niveau_eau, Es):
    #hf epaisseur voile
    #h epaisseur totale de la lierne
    #b largeur de la surépaisseur
    bf=2*espacement_butons/10+b
    mu_lim, mu_lu, alpha_u, z, sigma_s1, As1, As_min, As_retenu, As2=flexion_simple_T(M_elu,M_els,b,d,h,hf, bf, fck,fyk,classe_exposition,classe_acier,palier_acier, coeff_secu_beton, coeff_secu_acier, cuvelage, niveau_eau, Es)
    return mu_lim, mu_lu, alpha_u, z, sigma_s1, As1, As_min, As_retenu, As2

def lierne_surepaisseur_ext(M_elu, M_els, b, h, d, espacement_butons, fck, fyk, classe_exposition, classe_acier, palier_acier, coeff_secu_beton, coeff_secu_acier, cuvelage, niveau_eau, Es):
    #b=largeur de la surépaisseur de la lierne
    #h epaisseur totale de la lierne
    mu_lim, mu_lu, alpha_u, z, sigma_s1, As1, As_min, As_retenu, As2=flexion_simple_rect(M_elu,M_els,b,d,h,fck,fyk,classe_exposition,classe_acier,palier_acier, coeff_secu_beton, coeff_secu_acier, cuvelage, niveau_eau, Es)
    return mu_lim, mu_lu, alpha_u, z, sigma_s1, As1, As_min, As_retenu, As2

def tranchant_lierne(T_elu, N_elu, b, h, d, As1, fck, fyk, theta, coeff_secu_beton, coeff_secu_acier):
    verif=verification_tranchant(T_elu, N_elu, b, h, d, As1, fck, coeff_secu_beton)
    alpha=1 #car flexion simple
    Z=0.9*d
    nu_1=0.6*(1-fck/250)
    Vrd_max=alpha*b*Z*nu_1*fck/coeff_secu_beton*(1/m.tan(90*m.pi/180)+1/m.tan(theta*m.pi/180))/(1+(1/m.tan(theta*m.pi/180))**2)
    if Vrd_max>=abs(T_elu): 
        verif2=True
    else: 
        verif2=False
    Asw_s=abs(T_elu)/(Z*fyk/coeff_secu_acier*(1/m.tan(90*m.pi/180)+1/m.tan(theta*m.pi/180))*m.sin(m.pi/2))
    Asw_s_min=0.08*b*m.sin(m.pi/2)*fck/fyk
    Asw_s_max=0.5*alpha*b*nu_1*fck/coeff_secu_beton/(fyk/coeff_secu_acier*m.sin(m.pi/2))
    if verif==True:
        res=Asw_s_min
    elif verif==False and verif2==True:
        res=Asw_s
    elif verif==False and verif2==False:
        res="Erreur - redimensionner l'élément"
    return res

def verification_deversement_cas_general(nom_profile, lamine, M_elu, W, Iz, Iw, It, L, h, b, fy, G, Em):
    #Cas général
    #lamine= le profilé est il laminé
    Gamma_M1=1
    C1=1.13
    C2=0.45
    M_cr=C1*(m.pi)**2*Em*Iz/(L)**2*((Iw/Iz+L**2*G*It/((m.pi**2)*Em*Iz)+(C2*h/2)**2)**0.5-C2*(h/2))
    lambda_lt=(W*fy/M_cr)**0.5
    if lambda_lt<=0.2 and M_elu/M_cr<=0.2:
        verif=True
        return verif
    if lamine==True:
        if h/b<=2:
            courbe="a"
        else:
            courbe="b"
    else:
        if h/b<=2:
            courbe="c"
        else:
            courbe="d"
    if courbe=="a":
        alpha_lt=0.21
    elif courbe=="b":
        alpha_lt=0.34
    elif courbe=="c":
        alpha_lt=0.49
    else:
        alpha_lt=0.76
    phi_lt=0.5*(1+alpha_lt*(lambda_lt-0.2)+lambda_lt**2)
    ksi_lt=1/(phi_lt+(phi_lt**2-lambda_lt**2)**0.5)
    kc=0.9
    f=min(1-0.5*(1-kc)*(1-2.0*(lambda_lt-0.8)**2), 1)
    ksi_lt_mod=min(ksi_lt/f, 1, 1/lambda_lt**2)
    ksi=max(ksi_lt, ksi_lt_mod)
    Mb_Rd=ksi*W*fy/Gamma_M1
    if M_elu<=Mb_Rd:
        verif=True
    else:
        verif=False
    return verif
    
def verification_deversement_cas_I(nom_profile, lamine, M_elu, W, Iz, Iw, It, L, h, b, fy, G, Em):
    #Cas général
    #Le profilé est laminé ou soudés 
    
    Gamma_M1=1
    C1=1.13
    C2=0.45
    beta=1
    M_cr=C1*(m.pi)**2*Em*Iz/(L)**2*((Iw/Iz+L**2*G*It/((m.pi**2)*Em*Iz)+(C2*h/2)**2)**0.5-C2*(h/2))
    lambda_lt=(W*fy/M_cr)**0.5
    if lamine==True:
        lambda_lt0=0.2+0.1*b/h
        alpha_lt=max(0.4-0.2*b/h*lambda_lt**2,0)
    else:
        lambda_lt0=0.3*b/h
        alpha_lt=max(0.5-0.25*b/h*lambda_lt**2,0)
    if lambda_lt<=lambda_lt0 and M_elu/M_cr<=lambda_lt0:
        verif=True
        return verif
    if lamine==True:
        if h/b<=2:
            courbe="a"
        else:
            courbe="b"
    else:
        if h/b<=2:
            courbe="c"
        else:
            courbe="d"
    phi_lt=0.5*(1+alpha_lt*(lambda_lt-lambda_lt0)+beta*lambda_lt**2)
    ksi_lt=min(1/(phi_lt+(phi_lt**2-beta*lambda_lt**2)**0.5),1,1/lambda_lt**2)
    kc=0.9
    f=min(1-0.5*(1-kc)*(1-2.0*(lambda_lt-0.8)**2), 1)
    ksi_lt_mod=min(ksi_lt/f, 1, 1/lambda_lt**2)
    Mb_Rd=ksi_lt_mod*W*fy/Gamma_M1
    if M_elu<=Mb_Rd:
        verif=True
    else:
        verif=False
    return verif

def verification_deversement(nom_profile, lamine, M_elu, L, fy, G, Em):
    if nom_profile.classe==1 or nom_profile.classe==2:
        W=nom_profile.Wpl_y
    elif nom_profile.classe==3:
        W=nom_profile.Wel_y
    Iz=nom_profile.Iz
    Iw=nom_profile.Iw
    It=nom_profile.It
    h=nom_profile.h
    b=nom_profile.b
    verif_gen=verification_deversement_cas_general(nom_profile, lamine, M_elu, W, Iz, Iw, It, L, h, b, fy, G, Em)
    verif_part=verification_deversement_cas_I(nom_profile, lamine, M_elu, W, Iz, Iw, It, L, h, b, fy, G, Em)
    if verif_gen==True or verif_part==True:
        return True
    else:
        return False
    
def verification_profile(nom_profile, p_els, M_elu, T_elu, f_adm, L, fy, nb_travee, Em):
    #p_els est la réaction d'appuis s'exercant sur la lierne en MN/ml
    if nom_profile.classe==1 or nom_profile.classe==2:
        W=nom_profile.Wpl_y
    elif nom_profile.classe==3:
        W=nom_profile.Wel_y
    Avz=nom_profile.Avz
    Iy=nom_profile.Iy
    tf=nom_profile.tf
    tw=nom_profile.tw
    if tw>0.040:
        fy=fy-20
    M_r=W*fy #MPa
    V_r=0.58*Avz*fy
    if nb_travee==2:
        alpha=0.415
    elif nb_travee==3:
        alpha=0.519
    elif nb_travee==4:
        alpha=0.485
    elif nb_travee==5:
        alpha=0.495
    elif nb_travee==6:
        alpha=0.49
    elif nb_travee==7:
        alpha=0.49
    else:
        alpha=0.49
    f0=5*p_els*L**4/384/Em/(Iy)  #m p_els en MPa
    f=alpha*f0
    if M_r>=M_elu and V_r>=T_elu and f<=f_adm:
        verif=True
    else:
        verif=False
    return verif

def predim_lierne(fy, M_elu, T_elu, p_els, f_adm, L, nb_travee, Liste_profile, Em):
    Selection_elu=[]
    Selection_els=[]
    Selection=[]
    Gamma_M0=1
    if nb_travee==2:
        alpha=0.415
    elif nb_travee==3:
        alpha=0.519
    elif nb_travee==4:
        alpha=0.485
    elif nb_travee==5:
        alpha=0.495
    elif nb_travee==6:
        alpha=0.49
    elif nb_travee==7:
        alpha=0.49
    else:
        alpha=0.49
    for i in range(len(Liste_profile)):
        tw=Liste_profile[i].tw
        if tw>0.040:
            fy=fy-20
        W_y=M_elu*Gamma_M0/fy
        if Liste_profile[i].Wpl_y>=W_y:
            Selection_elu.append(Liste_profile[i])
        
        I=Liste_profile[i].Iy
        f0=5*p_els*L**4/384/Em/I
        f=alpha*f0
        if f<=f_adm:
            Selection_els.append(Liste_profile[i])
    for i in range(len(Selection_elu)):
        if Selection_elu[i] in Selection_els:
            Selection.append((Selection_elu[i], Selection_elu[i].poids))
    if len(Selection)==0:
        return False
    else:
        Selection.sort(key= lambda poids: poids[1])
        for i in range(len(Selection)):
            res=verification_profile(Selection[i][0], p_els, M_elu, T_elu, f_adm, L, fy, nb_travee, Em)
            if res==True:
                return Selection[i][0].name
        
        
       
###############################################################################

################################## Butons #####################################  

def verification_compression_metal(nom_profile, lamine, N_elu, L, fy, delta_T, Em, alpha_T):
    #delta_T: delta température à demander en entrée
    Gamma_M1=1
    type_, A, tf, Iy, h, b=nom_profile.type, nom_profile.A, nom_profile.tf, nom_profile.Iy, nom_profile.h, nom_profile.b
    i_=(A/Iy)**0.5
    Lf=L
    lambda_=Lf/i_
    lambda_reduit=lambda_/m.pi*(fy/Em)**0.5
    if type_=="Tube":
        courbe_y=courbe_z="a"
    else:
        if lamine==True:
            if h/b>1.2:
                if tf<=40*10**-3:
                    courbe_y="a"
                    courbe_z="b"
                else:
                    courbe_y="b"
                    courbe_z="c"
            else:
                if tf<=100*10**-3:
                    courbe_y="b"
                    courbe_z="c"
                else:
                    courbe_y="d"
                    courbe_z="d"
        else:
            if tf<=40*10**-3:
                courbe_y="b"
                courbe_z="c"
            else:
                courbe_y="c"
                courbe_z="d"
    if courbe_y=="a":
        alpha_y=0.21
    elif courbe_y=="b":
        alpha_y=0.34
    elif courbe_y=="c":
        alpha_y=0.49
    elif courbe_y=="d":
        alpha_y=0.76
    if courbe_z=="a":
        alpha_z=0.21
    elif courbe_z=="b":
        alpha_z=0.34
    elif courbe_z=="c":
        alpha_z=0.49
    elif courbe_z=="d":
        alpha_z=0.76
    
    phi_y=0.5*(1+alpha_y*(lambda_reduit-0.2)+lambda_reduit**2)
    phi_z=0.5*(1+alpha_z*(lambda_reduit-0.2)+lambda_reduit**2)
    ksi_y=min(1, 1/(phi_y+(phi_y**2-lambda_reduit**2)**0.5))
    ksi_z=min(1, 1/(phi_z+(phi_z**2-lambda_reduit**2)**0.5))
    Nr_y=ksi_y*A*fy/Gamma_M1
    Nr_z=ksi_z*A*fy/Gamma_M1
    
    N_u=N_elu+1.35*alpha_T*delta_T*Em*A
    if N_u<=Nr_y and N_u<=Nr_z:
        return True
    else:
        return False
            
def predim_buton_metal(N_elu, fy, Liste_profile): #N_elu peut être augmenter si le buton est un bracon attention de bien prendre la bonne valeur 
    res=[]
    for i in range(len(Liste_profile)):
        A=Liste_profile[i].A
        if A>N_elu/fy:
            res.append(Liste_profile[i])
    if len(res)==0:
        return False
    else:
        for i in range(len(res)):
            if res[i].poids==min([res[j].poids for j in range(len(res))]):
                return res[i].name

def kmod_(classe_service, Duree_action):
    if classe_service==1 or classe_service==2:
        if Duree_action=="Permanent":
            kmod=0.6
        elif Duree_action=="Long terme":
            kmod=0.7
        elif Duree_action=="Moyen terme":
            kmod=0.8
        elif Duree_action=="Court terme":
            kmod=0.9
        elif Duree_action=="Instantanée":
            kmod=1.1
    elif classe_service==3:
        if Duree_action=="Permanent":
            kmod=0.5
        elif Duree_action=="Long terme":
            kmod=0.55
        elif Duree_action=="Moyen terme":
            kmod=0.65
        elif Duree_action=="Court terme":
            kmod=0.7
        elif Duree_action=="Instantanée":
            kmod=0.9
    return kmod

def verification_compression_bois(Diametre, Classe, Classe_service, Duree_action, N_elu, L, beta, Gamma_M): #N_elu peut être augmenter si le buton est un bracon attention de bien prendre la bonne valeur
    fc_0_k, E_005=Classe.fc_0_k, Classe.E_005
    kmod=kmod_(Classe_service, Duree_action)
    A=m.pi/4*Diametre**2
    I=m.pi/64*Diametre**4
    sigma=N_elu/A
    lambda_=L*((I/A)**-1)**0.5
    lambda_rel=lambda_/m.pi*(fc_0_k/E_005)**0.5
    ky=0.5*(1+beta*(lambda_rel-0.3)+lambda_rel**2)
    kc_y=1/(ky+(ky**2-lambda_rel**2)**0.5)
    if sigma<=kc_y*kmod*fc_0_k/Gamma_M:
        return True, kc_y*kmod*fc_0_k/Gamma_M*A
    else: 
        return False, kc_y*kmod*fc_0_k/Gamma_M*A

def predim_bois(N_elu, Liste_diametre, Classe, Classe_service, Duree_action, L, beta, Gamma_M): #N_elu peut être augmenter si le buton est un bracon attention de bien prendre la bonne valeur
    res=[]
    for i in range(len(Liste_diametre)):
        verif=verification_compression_bois(Liste_diametre[i].diam*10**-2, Classe, Classe_service, Duree_action, N_elu, L, beta, Gamma_M)
        if verif[0]==True:
            res.append(Liste_diametre[i])
    if len(res)==0:
        return False
    else:
        return res[0].diam

def verification_soulevement_voile(Liste_reaction, Liste_inclinaison, ep_voile, h_voile, espacement_butons, rho_beton):
    V=0
    for i in range(len(Liste_reaction)):
        V+=Liste_reaction[i]/m.tan(Liste_inclinaison[i]*m.pi/180)
    P_voile=ep_voile*h_voile*rho_beton*espacement_butons
    if V<=P_voile:
        return True
    else:
        return False

def verification_portance_butons(V_elu, V_els, sigma_els, L, B, h, rho_beton, Gamma_r_v, Gamma_r_v_elu):
    A=L*B
    V_elu=V_elu+1.35*rho_beton*L*B*h
    V_els=V_els+rho_beton*L*B*h
    sigma_u=V_elu/A
    sigma_ser=V_els/A
    if sigma_ser<=sigma_els and sigma_u<=Gamma_r_v/Gamma_r_v_elu*sigma_els:
        return True
    else:
        return False
    
def verification_glissement_butons(V, L, B, h, H, phi_, cu, gamma):
    #En conditions drainées
    if Type_interface=="Frottante":
        Rd=V*m.tan(phi_*m.pi/180)/Gamma_R_d/Gamma_R_h
    #En conditions non drainées
    elif Type_interface=="Adhérente":
        Rd=min(L*B*cu/Gamma_R_d/Gamma_R_h, 0.4*V)
    if Type_fondation=="Coulée pleine fouille":
        K_p=1/((m.tan(m.pi/4-phi_/2*m.pi/180))**2)
        butee=K_p*gamma*h**2/2
        H=H-butee
    if H<=Rd:
        return True
    else:
        return False

def predim_semelle_butons(V_elu, V_els, sigma_els, a, b, c, rho_beton): #donne la section minimale si on ne renseigne aucune dimension
    #c est l'enrobage
    A_els=V_els/sigma_els
    sigma_elu=2.3/1.4*sigma_els
    A_elu=V_elu/sigma_elu
    A=max(A_els, A_elu)
    L=B=A**0.5
    h=max((B-b)/4, (L-a)/4)+c
    h=round(h,2)
    verif=verification_portance_butons(V_elu, V_els, sigma_els, L, B, h, rho_beton)
    while verif==False:
        L+=0.01
        B+=0.01
        h=max((B-b)/4, (L-a)/4)+c
        h=round(h,2)
        verif=verification_portance_butons(V_elu, V_els, sigma_els, L, B, h, rho_beton)
    return L, B, h

def predim_hauteur_semelle_butons(V, L, B, H, phi_, cu, gamma):
    h=0.01
    verif=verification_glissement_butons(V, L, B, h, H, phi_, cu, gamma)
    while verif==False:
        h+=0.01
        verif=verification_glissement_butons(V, L, B, h, H, phi_, cu, gamma)
    return round(h,2)

def verification_portance(G, Q, sigma_els, L, B, h, rho_beton):
    A=L*B
    V_elu=ELU_STR_portance(G+rho_beton*L*B*h, Q)
    sigma_u=V_elu/A
    V_els=ELS_QP(G+rho_beton+L*B*h, Q, psy_2)
    sigma_ser=V_els/A
    if sigma_ser<=sigma_els and sigma_u<=2.3/1.4*sigma_els:
        return True
    else:
        return False

def predim_semelle(G, Q, sigma_els, a, b, c): #donne la section minimale si on ne renseigne aucune dimension
    #c est l'enrobage
    V_elu=ELU_STR_portance(G, Q)
    V_els=ELS_QP(G, Q, psy_2)
    A_els=V_els/sigma_els
    sigma_elu=2.3/1.4*sigma_els
    A_elu=V_elu/sigma_elu
    A=max(A_els, A_elu)
    L=B=A**0.5
    h=max((B-b)/4, (L-a)/4)+c
    h=round(h,2)
    return L, B, h
    
def verification_glissement(G, Q, L, B, H, phi_, cu, Gamma_R_h, Gamma_R_d):
    V_elu=ELU_STR_glissement_V(G, Q)
    #En conditions drainées
    Rd=V_elu*m.tan(phi_*m.pi/180)/Gamma_R_d/Gamma_R_h
    #En conditions non drainées
    Rnd=min(L*B*cu/Gamma_R_d/Gamma_R_h, 0.4*V_elu)
    if H<=Rd and H<=Rnd:
        return True
    else:
        return False
    
def reaction_sur_semelle(Liste_reaction, Liste_inclinaison):
    H=sum(Liste_reaction[i] for i in range(len(Liste_reaction)))
    V=sum(Liste_reaction[i]/m.tan(Liste_inclinaison[i]*m.pi/180) for i in range(len(Liste_reaction)))
    F=(H**2+V**2)**0.5
    return H, V, F

def verification_poinconnement(N_elu, M_elu, L, B , h, d, a, b, fck, Asx, Asy, dx, dy): #N_elu ne doit pas tenir compte du poids de la semelle
    x_=2*d
    X=creation_liste_abscisse(pas, 0.001, x_)
    u_ref=2*a+2*b+4*m.pi*d
    W_ref=a**2/2+a*b+4*b*d+16*d**2+2*m.pi*d*a
    alpha=a/b
    if alpha<=0.45:
        k=0.45
    elif alpha==1:
        k=0.6
    elif alpha==2:
        k=0.7
    elif alpha>=3:
        k=0.8
    elif 0.45<alpha<1:
        k=(0.6-0.45)*(alpha-1)/(1-0.45)+0.6
    elif 1<alpha<2:
        k=(0.7-0.6)*(alpha-2)/(2-1)+0.7
    L_ved=[]
    L_Vrd_c=[]
    for i in range(len(X)):
        u=2*a+2*b+2*m.pi*X[i]
        A_c=(a+2*X[i])*b+(b+2*X[i])*a-a*b+m.pi*(X[i])**2
        Ved_red=N_elu*(1-A_c/L/B)
        e=M_elu/Ved_red
        beta=1+k*e*u_ref/W_ref
        ved=beta*Ved_red/u/d
        L_ved.append(ved)
        Vrd_c=tranchant_semelle(L, B, d, X[i], Asx, Asy, fck, dx, dy)
        L_Vrd_c.append(Vrd_c)
    for i in range(len(X)):
        if L_ved[i]>L_Vrd_c[i]:
            return False
    return True
    
def tranchant_semelle(L, B, d, x_, Asx, Asy, fck, dx, dy): #on pourra prendre dx=dy=d
    Crd_c=0.12
    k=min(2, 1+(200/(d*1000))**0.5)
    rho=min((Asx/B/dx*Asy/L/dy)**0.5, 0.02)
    nu_min=0.035*k**(3/2)*(fck)**0.5
    Vrd_c=max((nu_min)*2*d/x_, (Crd_c*k*(100*rho*fck)**(1/3))*2*d/x_)
    return Vrd_c

def necessite_armatures(h, d0, sigma_sol, fck, coeff_secu_beton):
    fctm=f_ctm(fck)
    fctk_005=0.7*fctm
    fctd=fctk_005/coeff_secu_beton
    fctd_pl=0.8*fctd
    if 0.85*h/d0<(3*sigma_sol/fctd_pl)**0.5:
        return False
    else:
        return True
    
def armatures_semelle(N_elu, L, B, a, b, fyk, dx, dy, coeff_secu_acier):
    Med_x=N_elu*(L/2-0.35*a)**2/(2*L)
    Med_y=N_elu*(B/2-0.35*b)**2/(2*B)
    Asx=Med_x/(0.9*dx*fyk/coeff_secu_acier)
    Asy=Med_y/(0.9*dy*fyk/coeff_secu_acier)
    return (round(Asx*10**4,3), round(Asy*10**4, 3))

def corbeaux(a, b, lambda_, theta, enrobage, fck, fyk, N_elu):
    #a,b sont les dimensions du butons 
    #lambda_ permet de définir les dimensions du corbeaux =10 ou 20cm
    #theta est l'angle d'inclinaison avec la verticale du buton
    #N_elu est l'effort (incliné ou non) dans le buton
    b_c=b+2*lambda_
    a_c=a/2+lambda_
    h_c=2*a_c/m.cos(theta*m.pi/180)
    sigma_rd_max=(1-fck/250)*fck/Coeff_beton
    d=h_c-c*m.cos(theta*m.pi/180)
    d_=h_c-a_c*m.cos(theta*m.pi/180)
    a_c_=a_c*m.cos(theta*m.pi/180)
    x_1=N_elu*m.cos(theta*m.pi/180)/b_c/sigma_rd_max
    poly=np.polynomial.polynomial.Polynomial([x_1*(x_1+2*a_c*m.cos(theta*m.pi/180)), 2*d_, 1])
    x_0=max(poly.roots())
    alpha=m.atan((d_-x_0/2)/(a_c_+x_1/2))
    alpha_=m.atan(x_1/x_0)
    z_0=a_c*m.cos(theta*m.pi/180)*m.tan(alpha)
    F_t=N_elu/m.tan(theta*m.pi/180)
    F_c=N_elu*m.cos(alpha)/m.sin(theta*m.pi/180)
    As_main=F_t/(fyk/Coeff_acier)*10**4
    As_ink=0.25*As_main
    verif=True
    print(m.tan(alpha), m.tan(alpha_))
    if m.tan(alpha)<=1 or m.tan(alpha)>2.5:
        verif=False
    elif F_t/(a_c_*b_c)>sigma_rd_max:
        verif=False
    elif N_elu>0.5*b_c*d*0.6*(1-fck/250)*fck/Coeff_beton:
        verif=False
    return As_main, As_ink, verif

def corbeaux2(a, b, lambda_, theta, enrobage, fck, fyk, N_elu, coeff_secu_beton, coeff_secu_acier): #on privilégiera l'utilisation de cette fonction conforme à la feuille de calcul Thonier
    #a,b sont les dimensions du butons 
    #lambda_ permet de définir les dimensions du corbeaux =10 ou 20cm
    #theta est l'angle d'inclinaison avec la verticale du buton
    #N_elu est l'effort (incliné ou non) dans le buton
    b_c=b
    #b_c=b+2*lambda_
    a_c=a/2+lambda_
    h_c=2*a_c/m.cos(theta*m.pi/180)
    h=h_c-a_c*m.sin(theta*m.pi/180)
    print(h)
    a_c_=a_c*m.cos(theta*m.pi/180)
    print(a_c_)
    Fx=N_elu*m.cos(theta*m.pi/180)
    Fy=N_elu*m.sin(theta*m.pi/180)
    fcd=fck/coeff_secu_beton
    fyd=fyk/coeff_secu_acier
    sigma_rd_max=(1-fck/250)*fcd
    d_=h-enrobage
    A=a_c_+Fx/2/b_c/sigma_rd_max
    B=-a_c_*d_
    C=(Fx*a_c_**2+Fy*a_c_*enrobage)/2/b_c/sigma_rd_max
    D=B**2-4*A*C
    z_0=(-B+D**0.5)/2/A
    F_t=Fx*a_c_/z_0+Fy*(enrobage+z_0)/z_0
    As_main=F_t/fyd*10**4
    As_ink=0.25*As_main
    
    ###### Calcul de Vrd_c
    sigma_cp=-Fy/b_c/d_
    k=min(2, 1+(0.2/d_)**0.5)
    v_min=0.035*k**(3/2)*fck**0.5
    rho=min(0.02, As_main*10**-4/d_/b_c)
    Vrd_c=max((0.12*k*(100*rho*fck)**(1/3)+0.15*sigma_cp)*b_c*d_, (v_min)*b_c*d_)
    
    a_b=(F_t-Fy)/b_c/sigma_rd_max
    a_e=Fx/b_c/sigma_rd_max
    alpha=m.atan((d_-a_b/2)/(a_c_+a_e/2))
    verif=True
    print((m.tan(alpha)<=1 or m.tan(alpha)>2.5), F_t/(a_c_*b_c)>sigma_rd_max, Fx>0.5*b_c*d_*0.6*(1-fck/250)*fck/coeff_secu_beton, Fx>Vrd_c )
    if m.tan(alpha)<=1 or m.tan(alpha)>2.5:
        verif=False
    elif F_t/(a_c_*b_c)>sigma_rd_max:
        verif=False
    elif Fx>0.5*b_c*d_*0.6*(1-fck/250)*fck/coeff_secu_beton:
        verif=False
    #elif Fx>Vrd_c:
     #   verif=False
    
    if Fx>Vrd_c:
        As_ink=0.5*Fx/fyd*10**4
    else:
        As_ink=0.25*As_main
    return As_main, As_ink, verif

def platine(nb_cheville, type_cheville, liste_cheville, N_elu, T_elu):
    if nb_cheville==False and type_cheville!=False:
        nb=1
        N_rd, V_rd=type_cheville.Nrd, type_cheville.Vrd
        N, V=N_elu/nb, T_elu/nb
        while N>N_rd or V>V_rd:
            nb+=1
            N=N_elu/nb
            V=T_elu/nb
        return (type_cheville.name, nb)
    elif type_cheville==False and nb_cheville!=False:
        liste=[]
        N, V=N_elu/nb_cheville, T_elu/nb_cheville
        for i in range(len(liste_cheville)):
            N_rd=liste_cheville[i].Nrd
            V_rd=liste_cheville[i].Vrd
            if N_rd>N and V_rd>V:
                liste.append(liste_cheville[i])
        if len(liste)==0:
            return False
        else:
             for i in range(len(liste)):
                 if liste[i].diametre==min(liste[j].diametre for j in range(len(liste))):
                     return (liste[i].name, nb_cheville)
    elif nb_cheville==False and type_cheville==False:
        res=[]
        for i in range(len(liste_cheville)):
            type_che=liste_cheville[i]
            Nrd=type_che.Nrd
            V_rd=type_che.Vrd
            nb=1
            N=N_elu/nb
            V=T_elu/nb
            while N>Nrd or V>V_rd:
                nb+=1
                N=N_elu/nb
                V=T_elu/nb
            res.append((type_che.name, nb))
        return res
    elif nb_cheville!=False and type_cheville!=False:
        Nrd=type_cheville.Nrd
        Vrd=type_cheville.Vrd
        N=N_elu/nb_cheville
        V=T_elu/nb_cheville
        if N<=Nrd and V<=Vrd:
            return True
        else:
            return False
        
###############################################################################

################################## Fondations #################################

def ep_dallage_voute(p, L, a, fck, fyk, enrobage, coeff_secu_beton, coeff_secu_acier):
    b=0.2
    sigma_b_lim=0.85*(1-fck/250)*(0.8*fck/coeff_secu_beton)
    h=0.15*L
    d=0.9*h
    L_2=0.5*p*L/b/sigma_b_lim
    if L_2<a:
        L_2=a
    elif L_2>L/2:
        L_2=L/2
    p_1=0.5*p*L/sigma_b_lim
    L_4=L_2-a
    Ved=p_1*L_4
    L_6=L_4+a/2
    M=p_1*L_6**2/8
    mu=M/b/d**2/(fck/coeff_secu_beton)
    alpha=1/0.8*(1-(1-2*mu)**0.5)
    z=d*(1-0.5*0.8*alpha)
    As=M/z/(fyk/coeff_secu_acier)
    k=min(2, 1+(0.2/d)**0.5)
    rho=max(0.02, As/b/d)
    nu_min=0.035*k**(3/2)*fck**0.5
    Vrd_c=max(0.12*k*(100*rho*fck)**(1/3)*b*d, nu_min*b*d)
    while Ved>Vrd_c:
        b+=0.01
        L_2=0.5*p*L/b/sigma_b_lim
        if L_2<a:
            L_2=a
        elif L_2>L/2:
            L_2=L/2
        p_1=0.5*p*L/sigma_b_lim
        L_4=L_2-a
        Ved=p_1*L_4
        L_6=L_4+a/2
        M=p_1*L_6**2/8
        mu=M/b/d**2/(fck/coeff_secu_beton)
        alpha=1/0.8*(1-(1-2*mu)**0.5)
        z=d*(1-0.5*0.8*alpha)
        As=M/z/(fyk/coeff_secu_acier)
        k=min(2, 1+(0.2/d)**0.5)
        rho=max(0.02, As/b/d)
        nu_min=0.035*k**(3/2)*fck**0.5
        Vrd_c=max(0.12*k*(100*rho*fck)**(1/3)*b*d, nu_min*b*d)
    return round(b,2)

def voute_decharge(p, L, a, b, fck, fyk, enrobage, coeff_secu_beton, coeff_secu_acier):
    ################ Données ##################################################
    h=0.15*L
    d=0.9*h
    mu, c=0.6, 0.2
    sigma_b_lim=0.85*(1-fck/250)*(0.8*fck/coeff_secu_beton)
    fctm=f_ctm(fck)
    fctk_=0.7*fctm
    fctd=fctk_/1.5
    ########################### L #############################################
    L_2=0.5*p*L/b/sigma_b_lim
    if L_2<a:
        L_2=a
    elif L_2>L/2:
        L_2=L/2
    L_3=L-2*L_2
    L_4=L_2-a
    L_5=L-2*a
    L_6=L_4+a/2
    ############# Contraintes et tirant #######################################
    sigma_n=0.5*p*L/b/L_2
    cot_alpha=mu+c*fctd/sigma_n
    alpha=m.atan(1/cot_alpha)
    sigma_b=sigma_n/(m.sin(alpha)**2)
    T=0.5*p*L*cot_alpha
    As1_1=T/(fyk/coeff_secu_acier)*10**4
    f=L*m.tan(alpha)/4
    p_1=b*sigma_n
    ######## Effort tranchant #################################################
    if L_4<0.5*d:
        V1_red=0.25*p_1*L_4
    elif 0.5*d<=L_4<2*d:
        V1_red=p_1*d/16+p_1*L_4**2/4/d
    else:
        V1_red=17*p_1*d/16+p_1*(L_4-2*d)
    V_ed=p_1*L_4
    As_w_s=0.08*fck**0.5*b/(fyk/coeff_secu_acier)
    ###### Vrd_c ##############################################################
    M=p_1*L_6**2/8
    mu=M/b/d**2/(fck/coeff_secu_beton)
    alpha_=1/0.8*(1-(1-2*mu)**0.5)
    z=d*(1-0.5*0.8*alpha_)
    As=M/z/(fyk/coeff_secu_acier)
    As_min=section_min_flexion(b, d, h, fck, fyk, coeff_secu_acier)
    As_=max(As*10**4, As_min)
    k=min(2, 1+(0.2/d)**0.5)
    rho=max(0.02, As/b/d)
    nu_min=0.035*k**(3/2)*fck**0.5
    Vrd_c=max(0.12*k*(100*rho*fck)**(1/3)*b*d, nu_min*b*d)
    if V_ed>Vrd_c:
        return False
    ############################ Glissement ###################################
    A_g=0.5*V_ed/(fyk/coeff_secu_acier)
    ######################### Flexion #########################################
    M_a=0.15*M
    mu_2=M_a/b/d**2/(fck/coeff_secu_beton)
    alpha_2=1/0.8*(1-(1-2*mu_2)**0.5)
    z_2=d*(1-0.5*0.8*alpha_2)
    As_a=M_a/z_2/(fyk/coeff_secu_acier) #Calculer sigma avec la fonction contraintes acier
    
    return (As1_1, A_g*10**4, As_a*10**4, As_, As_w_s)

def ple_(D, B, liste_pl):
    ple_res=1
    hr=1.5*B
    n=0
    for i in range(len(liste_pl)):
        if D<=liste_pl[i][0]<=D+hr:
            n+=1
            ple_res=ple_res*liste_pl[i][1]
    if n==0:
        return False
    else:
        ple_res=(ple_res)**(1/n)
        return ple_res
    
def D_e(D, ple_, liste_pl):
    X, Y=[], []
    for i in range(len(liste_pl)):
        if 0<=liste_pl[i][0]<=D:
            X.append(liste_pl[i][0])
            Y.append(liste_pl[i][1])
    res=0
    if len(X)==0:
        res=0
    elif len(X)==1:
        res=X[0]*Y[0]/ple_
    else:
        for i in range(len(X)-1):
            res+=((Y[i+1]+Y[i])*(X[i+1]-X[i]))/2
    return min(D, res)

def kp(Categorie_sol, D_e, B):
    if D_e/B>2:
        return False
    else:
        if Categorie_sol=="Argiles" or Categorie_sol== "Limons":
            a=0.2
            b=0.02
            c=1.3
            kp_0=0.8
        elif Categorie_sol=="Sables" or Categorie_sol=="Graves":
            a=0.3
            b=0.05
            c=2
            kp_0=1
        elif Categorie_sol=="Craies":
            a=0.28
            b=0.22
            c=2.8
            kp_0=0.8
        elif Categorie_sol=="Marnes" or Categorie_sol=="Marno-calcaires":
            a=0.2
            b=0.2
            c=3
            kp_0=0.8
        elif Categorie_sol=="Roches":
            a=0.2
            b=0.3
            c=3
            kp_0=0.8
        k_p=kp_0+(a+b*D_e/B)*(1-m.exp(-c*D_e/B))
        return k_p
    
def Idelta(V, H, phi, c, Gamma_sol, D_e, B):
    #phi=(phi_u, phi')
    #c=(c_u, c')
    delta=m.atan(H/V)
    i_delta=1
    if phi[0]==0 and c[0]>0:
        i_delta=(1-2*delta/m.pi)**2
    elif phi[1]>0 and c[1]==0:
        if delta<m.pi/4:
            i_delta=(1-2*delta/m.pi)**2-2*delta/m.pi*(2-3*2*delta/m.pi)*m.exp(-D_e/B)
        else:
            i_delta=(1-2*delta/m.pi)**2-(1-2*delta/m.pi)**2*m.exp(-D_e/B)
    elif phi[1]>0 and c[1]>0:
        alpha=0.6
        i_1=(1-2*delta/m.pi)**2
        if delta<m.pi/4:
            i_2=(1-2*delta/m.pi)**2-2*delta/m.pi*(2-3*2*delta/m.pi)*m.exp(-D_e/B)
        else:
            i_2=(1-2*delta/m.pi)**2-(1-2*delta/m.pi)**2*m.exp(-D_e/B)
        i_delta=i_2+(i_1-i_2)*(1-m.exp(-alpha*c[1]/(Gamma_sol*B*m.tan(phi[1]))))
    return min(i_delta, 1)

def q_net(V, H, D, B, liste_pl, Categorie_sol, phi, c, Gamma_sol):
    ple=ple_(D, B, liste_pl)
    De=D_e(D, ple, liste_pl)
    k_p=kp(Categorie_sol, De, B)
    i_delta=Idelta(V, H, phi, c, Gamma_sol, De, B)
    qnet=ple*k_p*i_delta
    return round(qnet,2)

def predim_semelle3(V, qnet, Gamma_r_v, Gamma_r_v_d):
    sigma_adm=qnet/Gamma_r_v/Gamma_r_v_d
    B=V/sigma_adm
    return round(B,2)

def verification_portance1(V, B, qnet, Gamma_r_v, Gamma_r_v_d):
    sigma_adm=qnet/Gamma_r_v/Gamma_r_v_d
    print(sigma_adm, V/B)
    if V/B>sigma_adm:
        return False
    else:
        return True
    
def predim_semelle4(torseur, liste_appuis, D, ep, d0, qnet_defaut, liste_pl, sol,Gamma_R_h,Gamma_R_d, Gamma_r_v, Gamma_r_v_d, presence_dallage,ep_dallage, fck_dallage, Type_interface, coeff_secu_beton, Coeff_ELU_G, Coeff_ELU_Q, psy_2, rho_beton): #h: epaisseur du voile, torseur en tête de semelle, qnet_defaut=(Valeur, combinaison)
    Categorie_sol, phi, c, Gamma_sol=sol[0], sol[1], sol[2], sol[3]
    hauteur=abs(liste_appuis[0]-liste_appuis[-1])
    torseur_sup=torseur_sup_semelle(torseur, Coeff_ELU_G, Coeff_ELU_Q, psy_2)
    if qnet_defaut[0]==False:
        B=ep+0.01
        h=0.3*B
        torseur_inf=torseur_inf_semelle(torseur, B, h, rho_beton, Coeff_ELU_G, Coeff_ELU_Q, psy_2)
        V_els_c, H_els_c, M_els_c=torseur_inf[0][0], torseur_inf[0][1], torseur_inf[0][2]
        V_els_qp, H_els_qp, M_els_qp=torseur_inf[1][0], torseur_inf[1][1], torseur_inf[1][2]
        if V_els_c==0:
            V_els_c=0.0000001
        elif V_els_qp==0:
            V_els_qp=0.0000001
        qnet_els_c=q_net(V_els_c, H_els_c, D, B, liste_pl, Categorie_sol, phi, c, Gamma_sol)
        qnet_els_qp=q_net(V_els_qp, H_els_qp, D, B, liste_pl, Categorie_sol, phi, c, Gamma_sol)
        verif_ELS_c=verification_portance1(V_els_c, B, qnet_els_c, Gamma_r_v, Gamma_r_v_d)
        verif_ELS_qp=verification_portance1(V_els_qp, B, qnet_els_qp, Gamma_r_v, Gamma_r_v_d)
        while verif_ELS_c==False or verif_ELS_qp==False:
            B+=0.01
            h=0.3*B
            torseur_inf=torseur_inf_semelle(torseur, B, h, rho_beton, Coeff_ELU_G, Coeff_ELU_Q, psy_2)
            V_els_c, H_els_c, M_els_c=torseur_inf[0][0], torseur_inf[0][1], torseur_inf[0][2]
            V_els_qp, H_els_qp, M_els_qp=torseur_inf[1][0], torseur_inf[1][1], torseur_inf[1][2]
            if V_els_c==0:
                V_els_c=0.0000001
            elif V_els_qp==0:
                V_els_qp=0.0000001
            qnet_els_c=q_net(V_els_c, H_els_c, D, B, liste_pl, Categorie_sol, phi, c, Gamma_sol)
            qnet_els_qp=q_net(V_els_qp, H_els_qp, D, B, liste_pl, Categorie_sol, phi, c, Gamma_sol)
            verif_ELS_c=verification_portance1(V_els_c, B, qnet_els_c,Gamma_r_v, Gamma_r_v_d)
            verif_ELS_qp=verification_portance1(V_els_qp, B, qnet_els_qp,Gamma_r_v, Gamma_r_v_d)
    else:
        qnet=qnet_defaut[0]
        if qnet_defaut[1]=="QP":
            j=1
        elif qnet_defaut[1]=="ELU":
            j=2
        else:
            j=0
        B=ep+0.01
        h=0.3*B
        torseur_inf=torseur_inf_semelle(torseur, B, h, rho_beton, Coeff_ELU_G, Coeff_ELU_Q, psy_2)
        V_els, H_els, M_els=torseur_inf[j][0], torseur_inf[j][1], torseur_inf[j][2]
        verif_=verification_portance1(V_els, B, qnet,Gamma_r_v, Gamma_r_v_d)
        while verif_==False:
            B+=0.01
            h=0.3*B
            torseur_inf=torseur_inf_semelle(torseur, B, h, rho_beton, Coeff_ELU_G, Coeff_ELU_Q, psy_2)
            V_els, H_els, M_els=torseur_inf[j][0], torseur_inf[j][1], torseur_inf[j][2]
            verif_=verification_portance1(V_els, B, qnet,Gamma_r_v, Gamma_r_v_d)
            
    ############ Limitation de l'excentrement #################################
    B=round(B,2)
    h=round(0.3*B,2)
    torseur_inf=torseur_inf_semelle(torseur, B, h, rho_beton, Coeff_ELU_G, Coeff_ELU_Q, psy_2)
    P_els_c, Mo_els_c=torseur_inf[0][0], torseur_inf[0][2]
    P_els_qp, Mo_els_qp=torseur_inf[1][0], torseur_inf[1][2]
    e_els_c=(torseur_sup[0][0]*((B-d0)/2-ep/2)+Mo_els_c)/(P_els_c)
    e_els_qp=(torseur_sup[1][0]*((B-d0)/2-ep/2)+Mo_els_qp)/(P_els_qp)
    verif_C=False
    verif_QP=False
    if B>=4*e_els_c:
        verif_C=True
    if B>=6*e_els_qp:
        verif_QP=True
        
    if presence_dallage==False and (verif_C==False or verif_QP==False):
        if Type_interface=="Adhérente":
            Rd_els_c=min(B*c[0]/Gamma_R_h/Gamma_R_d, 0.4*P_els_c)
            Rd_els_qp=min(B*c[0]/Gamma_R_h/Gamma_R_d, 0.4*P_els_qp)
        else:
            Rd_els_c=P_els_c*m.tan(phi[1]*m.pi/180)/Gamma_R_d/Gamma_R_h
            Rd_els_qp=P_els_qp*m.tan(phi[1]*m.pi/180)/Gamma_R_d/Gamma_R_h
        Med_els_c=max(0, P_els_c*e_els_c-Rd_els_c*hauteur)
        Med_els_qp=max(0, P_els_qp*e_els_qp-Rd_els_qp*hauteur)
        e_els_c=Med_els_c/P_els_c
        e_els_qp=Med_els_qp/P_els_qp
        while B<4*e_els_c or B<6*e_els_qp:
            B+=0.01
            if Type_interface=="Adhérente":
                Rd_els_c=min(B*c[0]/Gamma_R_h/Gamma_R_d, 0.4*P_els_c)
                Rd_els_qp=min(B*c[0]/Gamma_R_h/Gamma_R_d, 0.4*P_els_qp)
            else:
                Rd_els_c=P_els_c*m.tan(phi[1]*m.pi/180)/Gamma_R_d/Gamma_R_h
                Rd_els_qp=P_els_qp*m.tan(phi[1]*m.pi/180)/Gamma_R_d/Gamma_R_h
            hauteur=abs(liste_appuis[0]-liste_appuis[-1])
            Med_els_c=max(0, P_els_c*e_els_c-Rd_els_c*hauteur)
            Med_els_qp=max(0, P_els_qp*e_els_qp-Rd_els_qp*hauteur)
            e_els_c=Med_els_c/P_els_c
            e_els_qp=Med_els_qp/P_els_qp
        B=round(B,2)
        h=round(0.3*B,2)
        if B>=4*e_els_c:
            verif_C=True
        if B>=6*e_els_qp:
            verif_QP=True
            
    elif presence_dallage==True and (verif_C==False or verif_QP==False):
        ep_dal=ep_dallage
        if P_els_c*e_els_c/hauteur*ep_dal>fck_dallage/coeff_secu_beton:
            Med_els_c=P_els_c*e_els_c-fck_dallage/coeff_secu_beton*hauteur
        else:
            Med_els_c=0
        if P_els_qp*e_els_qp/hauteur*ep_dal>fck_dallage/coeff_secu_beton:
            Med_els_qp=P_els_qp*e_els_qp-fck_dallage/coeff_secu_beton*hauteur
        else:
            Med_els_qp=0
        e_els_c=abs(Med_els_c/P_els_c)
        e_els_qp=abs(Med_els_qp/P_els_qp)
        while B<4*e_els_c or B<6*e_els_qp:
            ep_dal+=0.01
            if P_els_c*e_els_c/hauteur*ep_dal>fck_dallage/coeff_secu_beton:
                Med_els_c=P_els_c*e_els_c-fck_dallage/coeff_secu_beton*hauteur
            else:
                Med_els_c=0
            if P_els_qp*e_els_qp/hauteur*ep_dal>fck_dallage/coeff_secu_beton:
                Med_els_qp=P_els_qp*e_els_qp-fck_dallage/coeff_secu_beton*hauteur
            else:
                Med_els_qp=0
            e_els_c=abs(Med_els_c/P_els_c)
            e_els_qp=abs(Med_els_qp/P_els_qp)
        if B>=4*e_els_c:
            verif_C=True
        if B>=6*e_els_qp:
            verif_QP=True
        if ep_dal>ep_dallage:
            verif_dal="Augmenter l'épaisseur du dallage à "+str(round(ep_dal,2))+" m"+ "  Remarque: si l'épaisseur du dallage est trop importante, il faut considérer une solution avec des longrines de redressement"
        else:
            verif_dal="L'épaisseur du dallage est correcte: "+str(ep_dal)+" m"
        return B,h,verif_dal, "La vérification de l'excentrement à l'ELS Caractéristique est "+str(verif_C)+" et à l'ELS QP "+str(verif_QP)
    return B,h, None, "La vérification de l'excentrement à l'ELS Caractéristique est "+str(verif_C)+" et à l'ELS QP "+str(verif_QP)

def torseur_sup_semelle(torseur, Coeff_ELU_G, Coeff_ELU_Q, psy_2 ):
    Vg, Vq, Hg, Hq, Mg, Mq=torseur[0][0], torseur[0][1], torseur[1][0], torseur[1][1], torseur[2][0], torseur[2][1]
    V_els_c, H_els_c, M_els_c=ELS_C(Vg, Vq), ELS_C(Hg, Hq), ELS_C(Mg, Mq)
    V_els_qp, H_els_qp, M_els_qp=ELS_QP(Vg, Vq, psy_2), ELS_QP(Hg, Hq, psy_2), ELS_QP(Mg, Mq,psy_2)
    V_elu_f, H_elu_f, M_elu_f=ELU(Vg, Vq, Coeff_ELU_G, Coeff_ELU_Q), ELU(Hg, Hq, Coeff_ELU_G, Coeff_ELU_Q), ELU(Mg, Mq,Coeff_ELU_G, Coeff_ELU_Q)
    torseur_sup=[[V_els_c, H_els_c, M_els_c], [V_els_qp, H_els_qp, M_els_qp], [V_elu_f, H_elu_f, M_elu_f]]
    return torseur_sup

def torseur_inf_semelle(torseur_sup_semelle, B, h_s, rho_beton,Coeff_ELU_G, Coeff_ELU_Q, psy_2):
    Vg, Vq, Hg, Hq, Mg, Mq=torseur_sup_semelle[0][0], torseur_sup_semelle[0][1], torseur_sup_semelle[1][0], torseur_sup_semelle[1][1], torseur_sup_semelle[2][0], torseur_sup_semelle[2][1]
    V_els_c, H_els_c, M_els_c=ELS_C(Vg+rho_beton*B*h_s, Vq), ELS_C(Hg, Hq), ELS_C(Mg, Mq)
    V_els_qp, H_els_qp, M_els_qp=ELS_QP(Vg+rho_beton*B*h_s, Vq, psy_2), ELS_QP(Hg, Hq, psy_2), ELS_QP(Mg, Mq, psy_2)
    V_elu_f, H_elu_f, M_elu_f, V_elu_portance, V_elu_glissement=ELU(Vg+rho_beton*B*h_s, Vq, Coeff_ELU_G, Coeff_ELU_Q), ELU(Hg, Hq, Coeff_ELU_G, Coeff_ELU_Q), ELU(Mg, Mq, Coeff_ELU_G, Coeff_ELU_Q), ELU_STR_portance(Vg+rho_beton*B*h_s, Vq), ELU_STR_glissement_V(Vg+rho_beton*B*h_s, Vq)
    torseur=[[V_els_c, H_els_c, M_els_c], [V_els_qp, H_els_qp, M_els_qp], [V_elu_f, H_elu_f, M_elu_f, V_elu_portance, V_elu_glissement]]
    return torseur

def verification_fondations(torseur, B, h, a, d0, D, fck, fyk, dx, dy, hauteur, liste_pl, sol, Gamma_R_h,Gamma_R_d, Gamma_r_v, Gamma_r_v_d, Gamma_r_v_elu, presence_dallage,ep_dallage,p_dallage, a_dallage, L_dallage, enrobage_dallage, fck_dallage, Type_interface, coeff_secu_beton, coeff_secu_acier, cuvelage, classe_exposition, palier_acier, classe_acier, niveau_eau, Es, mode_voute_decharge, rho_beton,Coeff_ELU_G, Coeff_ELU_Q, psy_2, Butee, H_ELU):
    Categorie_sol, phi, c, Gamma_sol=sol[0], sol[1], sol[2], sol[3]
    torseur_sup=torseur_sup_semelle(torseur, Coeff_ELU_G, Coeff_ELU_Q, psy_2)
    torseur_inf=torseur_inf_semelle(torseur, B, h, rho_beton,Coeff_ELU_G, Coeff_ELU_Q, psy_2)
    torseur_inf[2][1]+=H_ELU
    P_els_c, H_els_c, M_els_c=torseur_inf[0][0], torseur_inf[0][1], torseur_inf[0][2]
    P_els_qp, H_els_qp, M_els_qp=torseur_inf[1][0], torseur_inf[1][1], torseur_inf[1][2]
    P_elu_f, H_elu_f, M_elu_f, P_elu_po, P_elu_g=torseur_inf[2][0], torseur_inf[2][1], torseur_inf[2][2], torseur_inf[2][3],torseur_inf[2][4]
    Aire=B
    #Portance
    verif_sigma=False
    qnet_els_c=q_net(P_els_c, H_els_c, D, B, liste_pl, Categorie_sol, phi, c, Gamma_sol)
    qnet_els_qp=q_net(P_els_qp, H_els_qp, D, B, liste_pl, Categorie_sol, phi, c, Gamma_sol)
    qnet_elu_f=q_net(P_elu_po, H_elu_f, D, B, liste_pl, Categorie_sol, phi, c, Gamma_sol)
    sigma_els_c=qnet_els_c/Gamma_r_v/Gamma_r_v_d
    sigma_els_qp=qnet_els_qp/Gamma_r_v/Gamma_r_v_d
    sigma_elu_f=qnet_elu_f/Gamma_r_v_elu/Gamma_r_v_d
    if sigma_els_c>=P_els_c/Aire and sigma_els_qp>=P_els_qp/Aire and sigma_elu_f>=P_elu_po/Aire:
        verif_sigma=True
        
    #Limitation de l'excentrement
    verif_exce=False
    e=(B-d0)/2-a/2
    e_els_c=(torseur_sup[0][0]*e+M_els_c)/(P_els_c)
    e_els_qp=(torseur_sup[1][0]*e+M_els_qp)/(P_els_qp)
    e_elu_f=(torseur_sup[2][0]*e+M_elu_f)/(P_elu_f)
    if presence_dallage==False:
        if Type_interface=="Adhérente":
            Rd_els_c=min(B*c[0]/Gamma_R_h/Gamma_R_d, 0.4*P_els_c)
            Rd_els_qp=min(B*c[0]/Gamma_R_h/Gamma_R_d, 0.4*P_els_qp)
            Rd_elu_f=min(B*c[0]/Gamma_R_h/Gamma_R_d, 0.4*P_elu_f)
        else:
            Rd_els_c=P_els_c*m.tan(phi[1]*m.pi/180)/Gamma_R_d/Gamma_R_h
            Rd_els_qp=P_els_qp*m.tan(phi[1]*m.pi/180)/Gamma_R_d/Gamma_R_h
            Rd_elu_f=P_elu_f*m.tan(phi[1]*m.pi/180)/Gamma_R_d/Gamma_R_h
    else:
        if P_els_c*e_els_c/hauteur*ep_dallage>fck_dallage/coeff_secu_beton:
            Rd_els_c=fck_dallage/coeff_secu_beton
        else:
            Rd_els_c=P_els_c*e_els_c/hauteur
        if P_els_qp*e_els_qp/hauteur*ep_dallage>fck_dallage/coeff_secu_beton:
            Rd_els_qp=fck_dallage/coeff_secu_beton
        else:
            Rd_els_qp=P_els_qp*e_els_qp/hauteur
        if P_elu_f*e_elu_f/hauteur*ep_dallage>fck_dallage/coeff_secu_beton:
            Rd_elu_f=fck_dallage/coeff_secu_beton
        else:
            Rd_elu_f=P_elu_f*e_elu_f/hauteur
    Md_els_c=max(0,P_els_c*e_els_c-Rd_els_c*hauteur)
    Md_els_qp=max(0,P_els_qp*e_els_qp-Rd_els_qp*hauteur)
    Md_elu_f=max(0,P_elu_f*e_elu_f-Rd_elu_f*hauteur)
    e_els_c=(Md_els_c/P_els_c)
    e_els_qp=(Md_els_qp/P_els_qp)
    e_elu_f=(Md_elu_f/P_elu_f)
    if B>=4*e_els_c and B>=6*e_els_qp and B>=15*e_elu_f/7:
        verif_exce=True
        
    # Glissement
    verif_glissement=False
    if Type_interface=="Adhérente":
        Rd_elu=min(B*c[0]/Gamma_R_h/Gamma_R_d, 0.4*P_elu_g)
    else:
        Rd_elu=P_elu_g*m.tan(phi[1]*m.pi/180)/Gamma_R_d/Gamma_R_h
    if Butee=="Oui":
        H_r=H_elu_f-Gamma_sol*h*(1/(m.tan(m.pi/4-phi[1]/2*m.pi/180))**2)*h/2
    else:
        H_r=H_elu_f
    if H_r<=Rd_elu:
        verif_glissement=True
    
    #Estimation du tassement
    
    #Calcul des armatures
    Med_x=P_elu_f*(B/2-0.35*a)**2/(2*B)
    mu=abs(Med_x)/(B*dx**2*fck/coeff_secu_beton)
    alpha=1/0.8*(1-(1-2*mu)**0.5)
    z=dx*(1-0.5*0.8*alpha)
    sigma_s1=contrainte_acier(cuvelage, alpha, fyk, palier_acier, classe_acier, niveau_eau, coeff_secu_acier, Es)
    Asx=abs(Med_x)/z/sigma_s1*10**4
    
    Med_y=P_elu_f*(0.35*1)**2/2
    mu_2=abs(Med_y)/(dy**2*fck/coeff_secu_beton)
    alpha_2=1/0.8*(1-(1-2*mu_2)**0.5)
    z=dy*(1-0.5*0.8*alpha_2)
    sigma_s1_2=contrainte_acier(cuvelage, alpha, fyk, palier_acier, classe_acier, niveau_eau, coeff_secu_acier, Es)
    Asy=abs(Med_y)/(z*sigma_s1_2)*10**4
    
    #Vérification du poinçonnement
    #verification_poinconnement(N_elu, M_elu, L, B , h, d, a, b, fck, Asx, Asy, dx, dy): #N_elu ne doit pas tenir compte du poids de la semelle
    verif_poinconnement=verification_poinconnement(torseur_sup[2][0], torseur_sup[2][2], B, 1, h, dx, a, 1, fck, Asx, Asy, dx, dy)
    
    #Armature dallage
    #Verif dallage: Rd_elu_f + p_dallage < fck_dallage/coeff_secu_beton
    verif_ep_dallage=None
    if presence_dallage==True:
        verif_ep_dallage=False
        if Rd_elu_f+p_dallage<=fck_dallage*ep_dallage/coeff_secu_beton and ep_dallage>=0.2:
            verif_ep_dallage=True
        As_dallage=0.4/100*ep_dallage*10**4
        if mode_voute_decharge=="Fonctionnement en compression" or mode_voute_decharge==False:
            As_tirant=False
        elif mode_voute_decharge=="Fonctionnement en voûte de décharge":
            As_tirant=voute_decharge(p_dallage, L_dallage, a_dallage, ep_dallage, fck, fyk, enrobage_dallage, coeff_secu_beton, coeff_secu_acier)
    else: 
        As_dallage=False
        As_tirant=False
        
    #Armatures supplémentaire voile
    d_voile=0.9*a
    e_elu_v=(torseur_sup[2][0]*e+M_elu_f)/(P_elu_f)
    e_els_v=(torseur_sup[0][0]*e+M_els_c)/(P_els_c)
    print(P_elu_f*e_elu_v, P_els_c*e_els_v, 1, d_voile, a, fck, fyk, classe_exposition, classe_acier,palier_acier, coeff_secu_beton, coeff_secu_acier, cuvelage, niveau_eau, Es)
    As_voile=flexion_simple_rect(P_elu_f*e_elu_v, P_els_c*e_els_v, 1, d_voile, a, fck, fyk, classe_exposition, classe_acier,palier_acier, coeff_secu_beton, coeff_secu_acier, cuvelage, niveau_eau, Es)[7]
    
    #Contraintes exercée sur le sol à l'ELS QP
    q_els_qp=P_els_qp/Aire
    return verif_sigma, verif_exce, verif_glissement, Asx, Asy, (As_dallage, As_tirant), As_voile, q_els_qp, verif_ep_dallage, verif_poinconnement

def enrobage_mini(fck, classe_exposition):
    cdev=0.01
    if fck>=30 and (classe_exposition=="X0" or classe_exposition=="XC1" or classe_exposition=="XC2" or classe_exposition=="XC3"):
        R1=1
    elif fck>=35 and (classe_exposition=="XC4" or classe_exposition=="XF1"):
        R1=1
    elif fck>=40 and (classe_exposition=="XD1" or classe_exposition=="XS1" or classe_exposition=="XA1" or classe_exposition=="XF2" or classe_exposition=="XF3" or classe_exposition=="XD2" or classe_exposition=="XS2" or classe_exposition=="XA2" or classe_exposition=="XF4"):
        R1=1
    elif fck>=45 and (classe_exposition=="XD3" or classe_exposition=="XS3" or classe_exposition=="XA3"):
        R1=1
    else:
        R1=0
    if fck>=50 and (classe_exposition=="X0" or classe_exposition=="XC1"):
        R2=1
        R1=0
    elif fck>=55 and (classe_exposition=="XC2" or classe_exposition=="XC3"):
        R2=1
        R1=0
    elif fck>=60 and (classe_exposition=="XC4" or classe_exposition=="XF1" or classe_exposition=="XD1" or classe_exposition=="XS1" or classe_exposition=="XA1" or classe_exposition=="XF2" or classe_exposition=="XF3" or classe_exposition=="XD2" or classe_exposition=="XS2" or classe_exposition=="XA2" or classe_exposition=="XF4"):
        R2=1
        R1=0
    elif fck>=70 and (classe_exposition=="XD3" or classe_exposition=="XS3" or classe_exposition=="XA3"):
        R2=1
        R1=0
    else:
        R2=0
    Rqualite=0
    Rdalle=1
    RCEM1=0
    classe=max(1, 4-(R1+2*R2)-Rqualite-Rdalle-RCEM1)
    if classe==1:
        if (classe_exposition=="X0" or classe_exposition=="XC1" or classe_exposition=="XC2" or classe_exposition=="XC3"):
            cmin=0.01
        elif (classe_exposition=="XC4" or classe_exposition=="XF1"):
            cmin=0.015
        elif (classe_exposition=="XD1" or classe_exposition=="XS1" or classe_exposition=="XA1" or classe_exposition=="XF2" or classe_exposition=="XF3"):
            cmin=0.02
        elif (classe_exposition=="XD2" or classe_exposition=="XS2" or classe_exposition=="XA2" or classe_exposition=="XF4"):
            cmin=0.025
        else:
            cmin=0.03
    elif classe==2:
        if (classe_exposition=="X0" or classe_exposition=="XC1"):
            cmin=0.01
        elif (classe_exposition=="XC2" or classe_exposition=="XC3"):
            cmin=0.015
        elif (classe_exposition=="XC4" or classe_exposition=="XF1"):
            cmin=0.02
        elif (classe_exposition=="XD1" or classe_exposition=="XS1" or classe_exposition=="XA1" or classe_exposition=="XF2" or classe_exposition=="XF3"):
            cmin=0.025
        elif (classe_exposition=="XD2" or classe_exposition=="XS2" or classe_exposition=="XA2" or classe_exposition=="XF4"):
            cmin=0.03
        else:
            cmin=0.035
    elif classe==3:
        if (classe_exposition=="X0" or classe_exposition=="XC1"):
            cmin=0.01
        elif (classe_exposition=="XC2" or classe_exposition=="XC3"):
            cmin=0.02
        elif (classe_exposition=="XC4" or classe_exposition=="XF1"):
            cmin=0.025
        elif (classe_exposition=="XD1" or classe_exposition=="XS1" or classe_exposition=="XA1" or classe_exposition=="XF2" or classe_exposition=="XF3"):
            cmin=0.030
        elif (classe_exposition=="XD2" or classe_exposition=="XS2" or classe_exposition=="XA2" or classe_exposition=="XF4"):
            cmin=0.035
        else:
            cmin=0.04
    elif classe==4:
        if (classe_exposition=="X0"):
            cmin=0.01
        elif classe_exposition=="XC1":
            cmin=0.015
        elif (classe_exposition=="XC2" or classe_exposition=="XC3"):
            cmin=0.025
        elif (classe_exposition=="XC4" or classe_exposition=="XF1"):
            cmin=0.03
        elif (classe_exposition=="XD1" or classe_exposition=="XS1" or classe_exposition=="XA1" or classe_exposition=="XF2" or classe_exposition=="XF3"):
            cmin=0.035
        elif (classe_exposition=="XD2" or classe_exposition=="XS2" or classe_exposition=="XA2" or classe_exposition=="XF4"):
            cmin=0.04
        else:
            cmin=0.045
    elif classe==5:
        if (classe_exposition=="X0"):
            cmin=0.015
        elif classe_exposition=="XC1":
            cmin=0.02
        elif (classe_exposition=="XC2" or classe_exposition=="XC3"):
            cmin=0.03
        elif (classe_exposition=="XC4" or classe_exposition=="XF1"):
            cmin=0.035
        elif (classe_exposition=="XD1" or classe_exposition=="XS1" or classe_exposition=="XA1" or classe_exposition=="XF2" or classe_exposition=="XF3"):
            cmin=0.04
        elif (classe_exposition=="XD2" or classe_exposition=="XS2" or classe_exposition=="XA2" or classe_exposition=="XF4"):
            cmin=0.045
        else:
            cmin=0.05
    elif classe==6:
        if (classe_exposition=="X0"):
            cmin=0.02
        elif classe_exposition=="XC1":
            cmin=0.025
        elif (classe_exposition=="XC2" or classe_exposition=="XC3"):
            cmin=0.035
        elif (classe_exposition=="XC4" or classe_exposition=="XF1"):
            cmin=0.04
        elif (classe_exposition=="XD1" or classe_exposition=="XS1" or classe_exposition=="XA1" or classe_exposition=="XF2" or classe_exposition=="XF3"):
            cmin=0.045
        elif (classe_exposition=="XD2" or classe_exposition=="XS2" or classe_exposition=="XA2" or classe_exposition=="XF4"):
            cmin=0.05
        else:
            cmin=0.055
    cmin_b=0.01
    cnom=max(cmin_b, cmin, 0.01)+cdev
    return round(cnom, 3)

def tassement(liste_sol, B, arase_inf_semelle, Gamma_moy, q): #ELS QP
    #q est la contrainte verticale appliquée par la fondation
    #liste_sol de la forme [[Em, alpha, (cote_sup, cote_inf)]]
    sigma_v=abs(liste_sol[0][2][0]-arase_inf_semelle)*Gamma_moy
    Bo=0.6
    alpha_moy, n=0, 0
    for i in range(len(liste_sol)):
        if arase_inf_semelle>=liste_sol[i][2][0]>=arase_inf_semelle-8*B or (liste_sol[i][2][0]>arase_inf_semelle and arase_inf_semelle>=liste_sol[i][2][1]>=arase_inf_semelle-8*B):
            alpha_moy+=liste_sol[i][1]
            n+=1
    alpha_moy=alpha_moy/n
    #if 1/B<=1:
     #   lambda_c=1.1
      #  lamnda_d=1.12
    #elif 1<1/B<=2:
     #   lambda_c=1.1+0.1*(2-1/B)
      #  lambda_d=1.12+(1.53-1.12)*(2-1/B)
    #elif 2<1/B<=3:
     #   lambda_c=1.2+0.1*(3-1/B)
      #  lambda_d=1.53+(1.78-1.53)*(3-1/B)
    #elif 3<1/B<=5:
     #   lambda_c=1.3+0.1/2*(5-1/B)
      #  lambda_d=1.78+(2.14-1.78)/2*(5-1/B)
    #elif 5<1/B<=20:
     #   lambda_c=1.4+0.1/15*(20-1/B)
      #  lambda_d=2.14+(2.65-2.14)/15*(20-1/B)
    #else:
    lambda_c=1.5
    lambda_d=2.65
    
    if liste_sol[0][2][1]>=8*B:
        Ec=liste_sol[0][0]
        Ed=liste_sol[0][0]
    else:
        k, E=[], []
        for i in range(1, 17):
            k.append((arase_inf_semelle+(i-1)*B/2, arase_inf_semelle+i*B/2))
        for i in range(len(k)):
            if k[i][1]>liste_sol[-1][2][1]:
                E.append(False)
            for j in range(len(liste_sol)):
                if liste_sol[j][2][0]<=k[i][1]<=liste_sol[j][2][1] and liste_sol[j][2][0]<=k[i][0]<=liste_sol[j][2][1]:
                    E.append(liste_sol[j][0])
                elif k[i][0]<=liste_sol[j][2][1]<=k[i][1]:
                    if j==len(liste_sol)-1:
                        E.append(False)
                    else:
                        E.append(1/((k[i][1]-liste_sol[j][2][1])/(B/2)*(1/liste_sol[j+1][0])+(liste_sol[j][2][1]-k[i][0])/(B/2)*(1/liste_sol[j][0])))
        Ec=E[0]
        if E[8]==False or E[9]==False or E[10]==False or E[11]==False or E[12]==False or E[13]==False or E[14]==False or E[15]==False or E[16]==False:
            E3_5=(5-3+1)/sum(1/E[i] for i in range(2,5))
            E6_8=(8-6+1)/sum(1/E[i] for i in range(5,8))  
            Ed=1/(0.25/E[0]+0.3/E[1]+0.25/E3_5+0.2/E6_8)
        elif E[5]==False or E[6]==False or E[7]==False:
            Ed=1/(0.25/E[0]+0.3/E[1]+0.45/E3_5)
        elif E[3]==False or E[4]==False or E[5]==False:
            E3_5=(5-3+1)/sum(1/E[i] for i in range(2,5))
            Ed=1/(0.25/E[0]+0.3/E[1])
        elif (E[i]!=False for i in range(17)):
            E3_5=(5-3+1)/sum(1/E[i] for i in range(2,5))
            E6_8=(8-6+1)/sum(1/E[i] for i in range(5,8))   
            E9_16=(16-9+1)/sum(1/E[i] for i in range(8,16))
            Ed=1/(0.25/E[0]+0.3/E[1]+0.25/E3_5+0.1/E6_8+0.1/E9_16)
    sc=(q-sigma_v)*lambda_c*B*alpha_moy/9/Ec
    sd=2/9/Ed*(q-sigma_v)*Bo*(lambda_d*B/Bo)**alpha_moy
    return round(sc+sd, 3)

def moyenne_gamma(nb_couche, Liste_cote, Liste_gamma): #MAJ
    res=0
    somme=0
    for i in range(nb_couche):
        res+=Liste_gamma[i]*(Liste_cote[i][0]-Liste_cote[i][1])
        somme+=(Liste_cote[i][0]-Liste_cote[i][1])
    res=res/somme
    return res
