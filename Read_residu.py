import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 12

def Residus(file):
    res = pd.read_csv(file)
    Name = list(res.head(0))
    print(Name)
    it = list(res[Name[2]][:])
    rms_ro = list(res[Name[3]][:])
    rms_rou = list(res[Name[4]][:])
    rms_rov = list(res[Name[5]][:])
    rms_roe = list(res[Name[6]][:])

    '''
    plt.plot(it, rms_ro,label="ro")
    plt.plot(it,rms_rou,label="rou")
    plt.plot(it,rms_rov,label="rov")
    plt.plot(it,rms_roe,label="rhoe")
    plt.xlabel("Iteration")
    plt.ylabel("Residu rho")
    plt.title('convergence')
    plt.legend()
    plt.grid()
    plt.show()
    '''

    Res = [it,rms_ro,rms_rou,rms_rov,rms_roe]
    return Res

#file_name = "Test/history.csv"
#Residus(file_name)








