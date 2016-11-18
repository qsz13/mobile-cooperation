import time, os, errno
from MobilityModel.MobilityModel import MobilityModel
from PGG.Map import Map
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import ConfigParser

MonoFont = FontProperties('monospace')

scriptDirectory = os.path.dirname(os.path.realpath(__file__))
_confile = "mobi-coop.conf"

# initialize the config parser
conf = ConfigParser.ConfigParser()
confFile = os.path.join(scriptDirectory,_confile)
conf.read(confFile)

N = conf.getint("map", "node")
lm_min_dist = conf.getint("map", "landmark_min_dist")
lm_possibility = conf.getfloat("map", "landmark_possibility")
(lm_no, lm_max, lm_step) = map(int, conf.get("map","landmark_number").split(","))

period = conf.getint("mobility", "period")
(enhancement, enhancement_max, enhancement_step) = map(float, conf.get("mobility","enhancement").split(","))
nb_limit = conf.getint("mobility", "neighbor_limit")

iteration = 1000

def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

def create_path_not_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

if __name__ == "__main__":
    create_path_not_exists("output/") # check if output directory exists
    print "landmark configuration: %i, %i, %i"%(lm_no, lm_max, lm_step)
    print "enhancement configuration: %.1f, %.1f, %.1f\n"%(enhancement, enhancement_max, enhancement_step)

    for lm_cur_no in xrange(lm_no, lm_max+lm_step, lm_step):
        enhancement_result = []
        print "current landmark no: %i"%lm_cur_no
        #if lm_cur_no == 1:
        mobile_map = Map(N, lm_min_dist, lm_cur_no)
        for enhancement_cur in drange(enhancement,enhancement_max+enhancement_step,enhancement_step):
            print "enhancement: %.1f "%enhancement_cur
            start_time = time.time()
            if enhancement_cur == enhancement:
                mobile_model = MobilityModel(N, mobile_map, nb_limit, lm_possibility, period, enhancement_cur, drawed = False) #need to plot map the first time
            else:
                mobile_model = MobilityModel(N, mobile_map, nb_limit, lm_possibility, period, enhancement_cur, drawed = True)  # no need to plot map
            result = [0.5]
            for i in xrange(iteration):
                result.append(mobile_model.one_day())
                #print i
            print time.time() - start_time
            print result
            print '\n'
            enhancement_result.append(result)
        '''
        else:
            start_time = time.time()
            mobile_map = Map(N, lm_min_dist, lm_cur_no)
            mobile_model = MobilityModel(N, mobile_map, nb_limit, lm_possibility, period, enhancement, drawed = False)
            for i in xrange(1):
                result.append(mobile_model.one_day())
                print i
            print time.time() - start_time
            print result
        '''

        #plot enhancement vs cooperation ratio
        i = 0
        base_line = np.arange(iteration + 1)
        enhance_list = []
        for enhancement_cur in drange(enhancement, enhancement_max + enhancement_step, enhancement_step):
            i += 1
            enhance_list.append(enhancement_cur)

        fig, ax = plt.subplots()
        legend_list = []
        for idx in xrange(i):
            plt.plot(base_line,enhancement_result[idx])
            legend_list.append('r = %.1f'%enhance_list[idx])
        ax.set_ylabel(u'Pc', color='k', style = 'italic')
        ax.set_xlabel(u'Days', color='k', style = 'italic')
        ax.set_title(u'Cooperation Rate under Different r (%i Node, %i Landmark)\n' % (N, lm_cur_no), fontproperties=MonoFont,fontsize=16)
        fontP = FontProperties()
        fontP.set_family('sans-serif')
        fontP.set_size(11)
        plt.legend(legend_list, loc = 'best', prop = fontP)
        fig.savefig(u'output/Cooperation_Rate_%iNode_%iLmk_%iiter_enhance%.1f_%.1f.png' % (N,lm_cur_no,iteration,enhancement,enhancement_max), dpi=300)
        plt.clf()

