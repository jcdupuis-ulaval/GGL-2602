# -*- coding: utf-8 -*-
"""
Routines pour les travaux de GGL-2602 
Auteur : JCD
Version : 2023
"""
import numpy as np
def grav_prisme (l,e,z,delta_rho,x,offset):
    # l longueur du prisme
    # e épaisseur du prisme
    # z prodondeur de l'axe central du prisme
    # la position le long du levé
    # la position du prisme par rapport à la station de référence
        
    G = 6.672*10**(-11)
    gz = 2.0*e*(np.arctan((l-(x-offset))/z) + np.arctan((x-offset)/z))*delta_rho*G*1e5
    return gz #  mGal
    
def grav_sphere (R,z,delta_rho,x,offset):
    G = 6.672*10**(-11)
    gz = (4/3)*np.pi*R**3.0 * delta_rho *(G*z)/((x-offset)**2 +z**2)**(3.0/2.0)*1.0e5
    return gz # mGal

def grav_worden_cal(t):
    # Conforme à la courbe d'étalonnage du Worden (807)
    # La température est en Farenheit 
    m=(0.40514-0.40546)/(0-120)
    b = 0.40514
    tcomp = m*t+b
    print ('Le facteur de calibration est de %.6f pour une température de %4.6f F' %(tcomp,t))
    return tcomp
    
def GMSYS_export (f,position,Elev,Grav):
    data_out = np.vstack((position[position!=0],Elev[position!=0],Grav[position!=0]))
    np.savetxt(f,np.transpose(data_out),fmt='%4.4f',delimiter='    ')