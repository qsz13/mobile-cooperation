import numpy as np
import time, os, errno
from MobilityModel.MobilityModel import MobilityModel
from PGG.Map import Map
import matplotlib.pyplot as plt
import ConfigParser

scriptDirectory = os.path.dirname(os.path.realpath(__file__))
_confile = "mobi-coop.conf"

# initialize the config parser
conf = ConfigParser.ConfigParser()
confFile = os.path.join(scriptDirectory,_confile)
conf.read(confFile)

N = conf.getint("map", "node")
lm_min_dist = conf.getint("map", "landmark_min_dist")
lm_possibility = conf.getfloat("map", "landmark_possibility")
(lm_no, lm_max, lm_step) = map(int, conf.get("map", "landmark_number").split(","))

period = conf.getint("mobility", "period")
enhancement = conf.getfloat("mobility", "enhancement")
nb_limit = conf.getint("mobility", "neighbor_limit")

def create_path_not_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

if __name__ == "__main__":
    create_path_not_exists("output/") # check if output directory exists
    print "landmark configuration: %i, %i, %i\n"%(lm_no, lm_max, lm_step)
    for lm_cur_no in xrange(lm_no, lm_max + 1, lm_step):
        start_time = time.time()
        mobile_map = Map(N, lm_min_dist, lm_cur_no)
        mobile_model = MobilityModel(N, mobile_map, nb_limit, lm_possibility, period, enhancement)
        # mobile_model.one_day()
        result = []
        for i in xrange(1):
            result.append(mobile_model.one_day())
            print i
        print time.time() - start_time
        print result


# def cirrdnPJ(base ,rc):
#     x1=base[0]
#     y1=base[1]
#     a=2*np.pi*np.random.uniform(0.0, 1.0, len(x1))
#     r=np.sqrt(np.random.uniform(0.0, 1.0, len(x1)))
#     x=(rc*r)*np.cos(a)+x1
#     y=(rc*r)*np.sin(a)+y1
#     return [x,y]

# def adapt_loc(x,y,rge):
#     location=[x,y];
#     dist=pdist([0,0;location]);
#     if(dist+rge>scale)
#         a_loc=location*((scale-rge)/dist);
#     else
#         a_loc=location;
#     end
#     return a_loc

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

    # loc=cirrdnPJ([[0]*n,[0]*n], scale);
#   loc=arrayfun(@adapt_loc,loc(:,1),loc(:,2),Ranges,'UniformOutput',false);
#   loc=cell2mat(loc);
#   init_loc=loc;
#
#     PGG_c=1
#     PGG_r=amplify
#     PGG_strategy=np.round(np.random.uniform(0.0, 1.0, n))
#     PGG_uti=[0]*n
#
#
#
#
#



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
