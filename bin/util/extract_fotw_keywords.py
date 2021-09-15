import re, pathlib, time, pickle, sys, os, json, html, webcolors
from subprocess import getoutput as go
from os.path import *
from scipy.spatial import KDTree
from webcolors import (
    CSS3_NAMES_TO_HEX,
    hex_to_rgb,
)

def exec_cmd(cmd,torun,toprint,towrite,togo,args):
    ret = False
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    if toprint:
        print(args['start time'] + " / " + timestamp + " -- " + cmd)
    if towrite:
        fd = open(args['log-file'],'a')
        fd.write(args['start time'] + " / " + timestamp + " -- " + cmd + "\n")
        fd.close()
    if torun:
        if togo:
            ret = go(cmd)
        else:
            ret = os.system(cmd)
    return ret

def get_arg(arg,args):
    value = False
    if arg in sys.argv:
        index = sys.argv.index(arg)
        if len(sys.argv) > index+1:
            value = sys.argv[index+1]
            arg = re.sub("^\-+","",arg)
            args[arg] = value
        else:
            sys.exit("No value for argument '" + arg + "', no fun!")
    return args

def get_args():
    args = {}
    meta_data = {}

    # timestamps
    args['start time'] = time.strftime("%Y-%m-%d %H:%M:%S")
    args['date'] = time.strftime("%Y-%m-%d")
    default_timestamp = '2020-08-24 12:00'
    
    # directories and logs
    if 'root-dir' not in args:
        args['root-dir'] = ".."
    if not exists(args['root-dir']):
        print("Creating root directory: " + args['root-dir'])
        os.mkdir(args['root-dir'])
    args = get_arg('--log-dir',args)
    if 'log-dir' not in args:
        args['log-dir'] = args['root-dir'] + "/logs"
    if not exists(args['log-dir']):
        print("Creating log directory: " + args['log-dir'])
        os.mkdir(args['log-dir'])
    args = get_arg('--log-file',args)
    if 'log-file' not in args:
        args['log-file'] = args['log-dir'] + "/pregolem-" + args['date'] + ".log"
    args = get_arg('--error-file',args)
    if 'error-file' not in args:
        args['error-file'] = args['log-dir'] + '/errors.log'
    args = get_arg('--data-dir',args)
    if 'data-dir' not in args:
        args['data-dir'] = args['root-dir'] + "/data"
    if not exists(args['data-dir']):
        print("Creating data directory: " + args['data-dir'])
        os.mkdir(args['data-dir'])
    args = get_arg('--download-dir',args)
    if 'download-dir' not in args:
        args['download-dir'] = args['root-dir'] + "/download"
    if not exists(args['download-dir']):
        os.mkdir(args['download-dir'])

    
    # general
    args = get_arg('--command',args)
    args = get_arg('--data-pickle',args)
    if 'data-pickle' not in args:
        data = {}
    else:
        data = pickle.load(open(args['data-pickle'],'rb'))
    args = get_arg('--output-pickle',args)
    if 'output-pickle' not in args:
        args['output-pickle'] = args['data-dir'] + "/meta-data.pickle"
    args = get_arg('--output-pickle',args)
    if 'temporary' not in args:
        args['temporary'] = args['data-dir'] + "/temporary"
    args = get_arg('--output-json',args)
    if 'output-json' not in args:
        args['output-json'] = args['data-dir'] + "/flag_data.json"
    args = get_arg('--import-dir',args)
    args = get_arg('--input-image',args)

    return args, data

def extract(args,data):
    data['dictionary'] = {}
    data['links'] = {}
    
    fds = os.listdir(args['import-dir'])
    fds.sort()

    sep = '###///###'
    fmin = 0
    fmax = len(fds)
    #fmax = 1
    for f in range(fmin,fmax):
        fd = args['import-dir'] + "/" + fds[f]
        cont = open(fd).read()
        cont = re.sub("\n",sep,cont)
        cont = re.findall("<DL>(.+?)</DL></BODY></HTML>",cont)[0]
        items = re.split("<DT>",cont)
        imin = 1
        imax = len(items)
        print(len(items))
        for i in range(imin,imax):
            item = items[i]
            head = html.unescape(re.findall("<B><FONT SIZE\=\+1><A NAME=\".+?\">(.+?)</A></FONT></B>",item)[0])
            keypairs = re.findall("<A HREF\=\"(.+?)\">(.+?)</A>",item)
            data['dictionary'][head] = {
                'subs': [],
            }
            keys = []
            for kp in keypairs:
                lkey = "https://www.crwflags.com/fotw/flags/" + kp[0]
                key = html.unescape(kp[1])
                data['links'][key] = lkey
                data['dictionary'][head]['subs'].append(key)
                keys.append(key)
            print(data['dictionary'][head])
            for key in keys:
                data['dictionary'][key] = {
                    'doms': [],
                    'sibs': [],
                }
                data['dictionary'][key]['doms'].append(head)
                list(set(data['dictionary'][key]['doms']))
                keys.remove(key)
                data['dictionary'][key]['sibs'] += keys
                list(set(data['dictionary'][key]['sibs']))
                print(data['dictionary'][key])
    return data

def analyze(args,data):
    # data['dictionary']
    # data['links']
    print(len(list(data['dictionary'].keys())))
    print(len(list(data['links'].keys())))
    return data


def convert_rgb_to_names(rgb_tuple):
    # From: https://medium.com/codex/rgb-to-color-names-in-python-the-robust-way-ec4a9d97a01f
    # a dictionary of all the hex and their respective names in css3
    css3_db = CSS3_NAMES_TO_HEX
    names = []
    rgb_values = []
    #for color_hex, color_name in css3_db.items():
    for color_name, color_hex in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))
    
    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return names[index]

def get_colors(args,data):
    colors = {}
    cmd = "convert " + args['input-image'] + " -format %c histogram:info:-"
    image_data = exec_cmd(cmd,True,True,False,True,args).split("\n")
    imin = 0
    imax = len(image_data)
    
    for i in range(imin,imax):
        imda = image_data[i].strip()
        imcols = re.split("\s+",imda)
        pixels = int(imcols[0][:-1])
        red, green, blue = tuple(imcols[1][1:-1].split(","))
        rgb = (int(float(red)), int(float(green)), int(float(blue)))
        name = convert_rgb_to_names(rgb)
        if name not in colors:
            colors[name] = 0
        colors[name] += pixels
    print(colors)
    return data

def main():
    args, data = get_args()
    if args['command'] == 'extract':
        # python exctract_fotw_keywords.py --command extract --import-dir <import dir> --output-pickle <output pickle>
        data = extract(args,data)
        pickle.dump(data,open(args['output-pickle'],'wb'))
    elif args['command'] == 'analyze':
        # python extract_fotw_keywords.py --command analyze --data-pickle <data pickle>
        data = analyze(args,data)
    elif args['command'] == 'get-colors':
        # python extract_fotw_keywords.py --command get_colors --input-image <image>
        data = get_colors(args,data)
        
if __name__ == "__main__":
    main()
