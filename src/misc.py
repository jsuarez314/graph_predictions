import pylab as pl
import numpy as np
import os

def Beta_sk(points, beta, nnb):
    inputfile  = './data/pos.tmp'
    np.savetxt(f'{inputfile}', points, fmt='%f %f %f')
    outputfile = 'posbsk.tmp'
    os.system('cd /pscratch/sd/j/jfsuarez/ALIGN/graph_pred/')
    command = f'sh ./src/run_BSK.sh {inputfile} ../data/{outputfile} {beta} {nnb}'
    os.system(command)
    rm = f'rm  {inputfile}'
    return np.loadtxt(f'./data/{outputfile}.BSKIndex', dtype=int)


def plot_3D(ax,points, connections):
    ax.scatter3D(points[:,0], points[:,1], points[:,2], 'o', c='black', s=15)   
    for i, con in enumerate(connections):
        for j in con:
            ax.plot3D([points[:,0][i], points[:,0][j]],
                      [points[:,1][i], points[:,1][j]],
                      [points[:,2][i], points[:,2][j]],'--k', lw=0.5, alpha=0.5)
    return ax
    
def plot_3D_unique(ax, points, connections, N, plot_all=False):
    if plot_all:
        ax.scatter3D(points[:,0], points[:,1], points[:,2], 'o', c='black', s=15)   
    for j in connections[N]:
        ax.scatter3D(points[:,0][j], points[:,1][j], points[:,2][j], 'o', c='black', s=15)
        ax.plot3D([points[:,0][N], points[:,0][j]],
                  [points[:,1][N], points[:,1][j]],
                  [points[:,2][N], points[:,2][j]],'--k', lw=0.5, alpha=0.5)
    ax.scatter3D(points[:,0][N], points[:,1][N], points[:,2][N], 'o', c='red', s=15)        
    return ax
    
def plot_3D_unique_neighbors(ax,points, connections, neighbors, N, plot_all=False):
    if plot_all:
        ax.scatter3D(points[:,0], points[:,1], points[:,2], 'o', c='black', s=15)
    for j in connections[N]:
        ax.scatter3D(points[:,0][j], points[:,1][j], points[:,2][j], 'o', c='k', s=15)
        ax.plot3D([points[:,0][N], points[:,0][j]],
                  [points[:,1][N], points[:,1][j]],
                  [points[:,2][N], points[:,2][j]], '--k', lw=0.5, alpha=0.5)
        for k in neighbors[j]:
            ax.scatter3D(points[:,0][k], points[:,1][k], points[:,2][k], 'o', c='b', s=15)
            ax.plot3D([points[:,0][k], points[:,0][j]],
                      [points[:,1][k], points[:,1][j]],
                      [points[:,2][k], points[:,2][j]], '-.b', lw=0.5, alpha=0.5) 
    ax.scatter3D(points[:,0][N], points[:,1][N], points[:,2][N], 'o', c='red', s=15)                
    return ax     
    
def distance(point1, point2):
    return  np.sqrt( (point1[0]-point2[0])**2
                    +(point1[1]-point2[1])**2
                    +(point1[2]-point2[2])**2 )    

def find_connections(p,n):
    return np.concatenate([p[:,0][(p[:,1]==n)], p[:,1][(p[:,0]==n)]], axis=0)

def topological_features(points, pairs):
    ID                            = np.zeros(len(points))
    N_CONNECTIONS                 = np.zeros(len(points))
    ID_CONNECTIONS                = np.zeros(len(points), dtype=object)
    DIS_CONNECTIONS               = np.zeros(len(points), dtype=object)
    AV_DIS_CONNECTIONS            = np.zeros(len(points))
    ID_FIRSTNEIGH_CONNECTIONS     = np.zeros(len(points), dtype=object)
    N_FIRSTNEIGH_CONNECTIONS      = np.zeros(len(points))
    # DIS_FIRSTNEIGH_CONNECTIONS_TO_NODE      = np.zeros(len(points), dtype=object)
    # DIS_FIRSTNEIGH_CONNECTIONS_TO_ORIGIN    = np.zeros(len(points), dtype=object)
    
    for n in range(len(points)):
        zero_neigh                = find_connections(pairs, n)
        ID[n]                     = n
        N_CONNECTIONS[n]          = len(zero_neigh)
        ID_CONNECTIONS[n]         = zero_neigh
        temp_dis                  = []
        temp_dis_neigh_to_node    = []
        temp_dis_neigh_to_origin  = []
        temp_first_neigh          = []
        for idc in ID_CONNECTIONS[n]:
            temp_dis.append(distance(points[n], points[idc]))
            first_neigh = find_connections(pairs, idc)
            first_neigh = first_neigh[first_neigh!=n] #dismiss first neigh loops in the graphs
            # first_neigh = np.array(list(set(first_neigh) - set(zero_neigh)))
            temp_first_neigh.append(first_neigh)
            # for idn in first_neigh:
            #     temp_dis_neigh_to_node.append(misc.distance(points[idc], points[idn]))
            #     temp_dis_neigh_to_origin.append(misc.distance(points[n], points[idn]))
        DIS_CONNECTIONS[n]           = np.array(temp_dis)
        AV_DIS_CONNECTIONS[n]        = np.average(DIS_CONNECTIONS[n])
        ID_FIRSTNEIGH_CONNECTIONS[n]            = np.unique(np.concatenate(temp_first_neigh, axis=0).ravel())
        N_FIRSTNEIGH_CONNECTIONS[n]             = len(ID_FIRSTNEIGH_CONNECTIONS[n])
        # DIS_FIRSTNEIGH_CONNECTIONS_TO_NODE[n]   = temp_dis_neigh_to_node
        # DIS_FIRSTNEIGH_CONNECTIONS_TO_ORIGIN[n] = temp_dis_neigh_to_origin
        
    return ID, N_CONNECTIONS, ID_CONNECTIONS, DIS_CONNECTIONS, AV_DIS_CONNECTIONS, ID_FIRSTNEIGH_CONNECTIONS, N_FIRSTNEIGH_CONNECTIONS



