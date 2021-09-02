import wikipedia, re, pathlib, time, pickle, sys, os, json
from os.path import *

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
    args = get_arg('--category',args)
    if 'category' not in args:
        args['category'] = 'Flags'
    args = get_arg('--level',args)
    args = get_arg('--data-pickle',args)
    if not isfile(args['data-pickle']):
        data = []
        cat_data = {
            "level": 0,
            "name": "Category:" + args['category'],
            "supercategory": None,
            "subcategories": [],
        }
        data.append(cat_data)
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

    # wikimedia-specific
    args['wikipedia'] = wikipedia
    args['wikipedia'].set_lang('en')
    args = get_arg('--keyword',args)

    return args, data

def search(args,data):
    print(args['wikipedia'].search(keyword))
    return data

def main():
    args, data = get_args()
    if args['command'] == 'search':
        # python text-tools.py --command search --keyword <keyword>
        data = search(args,data)
    #elif args['command'] == 'regex-cats':
        # python text-tools.py --command 
        # pass
if __name__ == "__main__":
    main()
