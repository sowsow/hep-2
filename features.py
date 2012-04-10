import numpy as np
import cv2 as cv


def get_single(I,M):
    F=[]
    minI = np.min(I)
    maxI = np.max(I)
    I[M==0] = 0
    
    # Threshold image at multiple levels
    Theta = np.linspace(minI,maxI,20)
    for theta in Theta :
        BW = (I > theta).astype(np.uint8)
        m = cv.moments(BW)
        for key in m:
            F.append(m[key])
            
        Itmp = I.copy()
        Itmp[I<theta] = 0
        m = cv.moments(Itmp)
        for key in m:
            F.append(m[key])
        
    
    # Compute gradients with different sigmas
    sigma =  np.linspace(0.6,10.5,10);
    for s in sigma:
        k = int(round(3*s))
        if k%2==0: k=k+1
        Blr = cv.GaussianBlur(I,(k,k),s)
        dx = np.diff(Blr,1,0)
        dy = np.diff(Blr,1,1)
        G = np.sqrt(dx[:,:-1]**2 + dy[:-1,:]**2)
        
        F.append( np.mean(G) )
        F.append( np.median(G) )
        F.append( np.std(G) )
      

    # Aspect ratio
    F.append( float(I.shape[0]) / float(I.shape[1]) )
    
    return F
    
def get(I,M):
    Iblur1 = cv.GaussianBlur(I,(5,5),1.0)
    Iblur2 = cv.GaussianBlur(I,(15,15), 2.5)
    F1=get_single(I,M)
    F2=get_single(Iblur1,M)
    F3=get_single(Iblur2,M)
    F = F1 + F2 + F3
    return np.array(F, dtype=float)