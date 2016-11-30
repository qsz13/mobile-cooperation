#!/usr/bin/python
import matplotlib as mpl
mpl.use('Agg')
import time, os, errno, sys
from MobilityModel.MobilityModel import MobilityModel
from PGG.Map import Map
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import ConfigParser
import csv

current_repeat = 0
if len(sys.argv) > 1:
    current_repeat = int(sys.argv[1])

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
clr_period = conf.getint("mobility","clr_period")

distribution_map = conf.getboolean("plot","distribution_map")
enhance_vs_r = conf.getboolean("plot","enhance_vs_r")
if current_repeat > 1:
    distribution_map = False

iteration = conf.getint("iteration","iteration")
repeat = conf.getint("iteration","repeat")

landmark_random = conf.get("landmark","randomness")

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

def plot_in(data, step):
    base_line = np.arange(step)
    fig, ax = plt.subplots()

    plt.plot(data)

    ax.set_ylabel(u'Pc', color='k', style='italic')
    ax.set_xlabel(u'Days', color='k', style='italic')
    ax.set_title(u'Cooperation Rate under Different r (%i Node, %i Landmark)\n' % (N, lm_cur_no),
                 fontproperties=MonoFont, fontsize=16)
    fontP = FontProperties()
    fontP.set_family('sans-serif')
    fontP.set_size(11)
    fig.savefig(u'output/Cooperation_Rate_%iNode_%iLmk_%iiter_enhance%.1f_%.1f_step_%s.png' % (
    N, lm_cur_no, iteration, enhancement, enhancement_max, str(step)), dpi=300)
    plt.clf()


if __name__ == "__main__":
    create_path_not_exists("output/") # check if output directory exists
    print "landmark configuration: %i, %i, %i"%(lm_no, lm_max, lm_step)
    print "enhancement configuration: %.1f, %.1f, %.1f\n"%(enhancement, enhancement_max, enhancement_step)
    node_num_around_landmark = []
    for lm_cur_no in xrange(lm_no, lm_max+lm_step, lm_step):
        enhancement_result = []
        print "current landmark no: %i"%lm_cur_no
        #if lm_cur_no == 1:
        mobile_map = Map(N, lm_min_dist, lm_cur_no)
        append_to_node_around_lm = True
        for enhancement_cur in drange(enhancement,enhancement_max+enhancement_step,enhancement_step):
            print "enhancement: %.1f "%enhancement_cur
            start_time = time.time()
            if enhancement_cur == enhancement:
                mobile_model = MobilityModel(N, mobile_map, nb_limit, lm_possibility, period, enhancement_cur, drawed = not distribution_map, clr_period=clr_period, lm_random = landmark_random) #need to plot map the first time
            else:
                mobile_model = MobilityModel(N, mobile_map, nb_limit, lm_possibility, period, enhancement_cur, drawed = True, clr_period=clr_period, lm_random = landmark_random)  # no need to plot map
            result = [0.5]
            for i in xrange(iteration):
                result.append(mobile_model.one_day(i))
                #print i
                # if i>0 and i %1000 == 0:
                #     plot_in(result, i)
            # plot_in(result, iteration)
            print time.time() - start_time
            print result
            print '\n'
            outfile = open(u'output/Cooperation_Rate_%iNode_%iLmk_%iiter_enhance%.1f_repeat_%i.txt' % (N,lm_cur_no,iteration,enhancement_cur,current_repeat), 'w')
            for item in result:
                outfile.write("%s\n" % item)
            outfile.close()
            enhancement_result.append(result)
            if append_to_node_around_lm:
                node_num_around_landmark.append(mobile_model.node_num_around_landmark)
                append_to_node_around_lm = False
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
        if enhance_vs_r:
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
            fig.savefig(u'output/Cooperation_Rate_%iNode_%iLmk_%iiter_enhance%.1f_%.1f_repeat_%i.png' % (N,lm_cur_no,iteration,enhancement,enhancement_max,current_repeat), dpi=300)
            plt.clf()

    if distribution_map:
        fig, ax = plt.subplots()
        legend_list = []
        landmark_num = range(lm_no, lm_max+lm_step, lm_step)
        base_line = np.arange(0,5.5,0.5)
        # print landmark_num
        for idx, data in enumerate(node_num_around_landmark):
            plt.plot(base_line, data)
            legend_list.append('landmark = %.1f' % landmark_num[idx])
        ax.set_ylabel(u'Nodes', color='k', style='italic')
        ax.set_xlabel(u'Distance', color='k', style='italic')
        ax.set_title(u'Node number around landmarks with node size: %i\n' % N,
                     fontproperties=MonoFont, fontsize=16)

        fontP = FontProperties()
        fontP.set_family('sans-serif')
        fontP.set_size(11)
        plt.legend(legend_list, loc='best', prop=fontP)
        fig.savefig(u'output/Landmark_Node_%iNode.png' % N, dpi=300)
        plt.clf()
