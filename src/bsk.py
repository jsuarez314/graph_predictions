import  numpy as np
import  os

def neigh_features(Max,ID,nc,ncn,ad,den,con): #Compute all properties for first neighbors (Gradient)
    nc_n = np.zeros(Max)
    ad_n = np.zeros(Max)
    a_n = np.zeros(Max)
    b_n = np.zeros(Max)
    c_n = np.zeros(Max)
    den_n = np.zeros(Max)
    IDnn = ID[(nc!=0)]
    kk=0
    pbar = tqdm(total=len(IDnn), desc="Computing Delta Features")
    for i in IDnn:
        nc_temp = 0.0
        ad_temp = 0.0
        den_temp = 0.0
        for j in con[i]:
            nc_temp = nc_temp+ncn[j]
            ad_temp = ad_temp+ad[j]
            den_temp = den_temp+den[j]
        nc_n[i] = nc_temp/(1.0*nc[i])
        ad_n[i] = ad_temp/(1.0*nc[i])
        den_n[i] = den_temp/(1.0*nc[i])
        kk = kk+1
        pbar.update(1)     
    pbar.close()
    nc_n = nc_n-ncn
    ad_n = ad_n-ad
    den_n = den_n-den
    return nc_n,ad_n,den_n