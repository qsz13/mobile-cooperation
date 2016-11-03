import numpy as np
import time

def cirrdnPJ(base ,rc):
    x1=base[0]
    y1=base[1]
    a=2*np.pi*np.random.uniform(0.0, 1.0, len(x1))
    r=np.sqrt(np.random.uniform(0.0, 1.0, len(x1)))
    x=(rc*r)*np.cos(a)+x1
    y=(rc*r)*np.sin(a)+y1
    return [x,y]

# def adapt_loc(x,y,rge):
#     location=[x,y];
#     dist=pdist([0,0;location]);
#     if(dist+rge>scale)
#         a_loc=location*((scale-rge)/dist);
#     else
#         a_loc=location;
#     end
#     return a_loc


def mobility_poisson_mixture(N, flag, mu,alpha,uni_r,r,time,run,period,amplify):
    n=np.random.poisson(lam=N)
    scale = np.sqrt(n/np.pi)
    if flag == "exp":
        ranges = np.sqrt(np.random.exponential(1/mu,(n,1))) # not sure
    if flag == "pareto":
        ranges = np.sqrt(np.random.pareto(1/alpha,mu/alpha,mu,n,1)-mu);
    if flag == "uni":
        ranges = [uni_r]*n
    mean_range = np.mean(ranges)

    loc=cirrdnPJ([[0]*n,[0]*n], scale);
#   loc=arrayfun(@adapt_loc,loc(:,1),loc(:,2),Ranges,'UniformOutput',false);
#   loc=cell2mat(loc);
#   init_loc=loc;
    
    PGG_c=1
    PGG_r=amplify
    PGG_strategy=np.round(np.random.uniform(0.0, 1.0, n))
    PGG_uti=[0]*n


from MobilityModel.MobilityModel import MobilityModel
from PGG.Map import Map
N = 5000
lm_min_dist = 10
lm_possibility = 0.5


if __name__ == "__main__":
    start_time = time.time()
    mobile_map = Map(N, lm_min_dist)
    mobile_model = MobilityModel(N, mobile_map, lm_possibility, 24)
    mobile_model.one_day()
    print time.time() - start_time





# import numpy as np
#
# def cirrdnPJ(base ,rc):
#     x1=base[0]
#     y1=base[1]
#     a=2*np.pi*np.random.uniform(0.0, 1.0, len(x1))
#     r=np.sqrt(np.random.uniform(0.0, 1.0, len(x1)))
#     x=(rc*r)*np.cos(a)+x1
#     y=(rc*r)*np.sin(a)+y1
#     return [x,y]
#
# # def adapt_loc(x,y,rge):
# #     location=[x,y];
# #     dist=pdist([0,0;location]);
# #     if(dist+rge>scale)
# #         a_loc=location*((scale-rge)/dist);
# #     else
# #         a_loc=location;
# #     end
# #     return a_loc
#
#
# def mobility_poisson_mixture(N, flag, mu,alpha,uni_r,r,time,run,period,amplify):
#     n=np.random.poisson(lam=N)
#     scale = np.sqrt(n/np.pi)
#     if flag == "exp":
#         ranges = np.sqrt(np.random.exponential(1/mu,(n,1))) # not sure
#     if flag == "pareto":
#         ranges = np.sqrt(np.random.pareto(1/alpha,mu/alpha,mu,n,1)-mu);
#     if flag == "uni":
#         ranges = [uni_r]*n
#     mean_range = np.mean(ranges)
#
#     loc=cirrdnPJ([[0]*n,[0]*n], scale)
# #   loc=arrayfun(@adapt_loc,loc(:,1),loc(:,2),Ranges,'UniformOutput',false);
# #   loc=cell2mat(loc);
# #   init_loc=loc;
#
#     PGG_c=1
#     PGG_r=amplify
#     PGG_strategy=np.round(np.random.uniform(0.0, 1.0, n))
#     PGG_uti=[0]*n
#
#
#
#
# mobility_poisson_mixture(1000,'exp',0.5,0,0,0.5,30,1000,100,2)
