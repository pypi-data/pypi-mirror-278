#!/usr/bin/env python3
# coding=utf-8
#
# Top-level docs builder
#
# This is just a front-end to sphinx-build that can call it multiple times for different language/target combinations
#
# Will build out to _build/LANGUAGES/BUILDERS by default

import argparse
import os
import subprocess
import datetime
from datetime import timedelta
import multiprocessing

CHIPS = ['at1k', 'at820', 'at5050']
LANGUAGES = ["en", "zh_CN"]
chips = CHIPS
BUILDERS = ["html", "latex"]
languages = LANGUAGES
builders = BUILDERS
ts_docs_path = os.environ["TS_DOCS_PATH"]
docs_path = os.path.join(ts_docs_path,"docs")



def main():
    parser = argparse.ArgumentParser(description='build_docs.py: Build AT1K docs', prog='build_docs.py')
    parser.add_argument("--language", "-l", choices=LANGUAGES, required=False, help="optional, default generate en and zh_CN")
    parser.add_argument("--builder", "-b", choices=BUILDERS, required=False, help="optional, default generate html and latex")
    parser.add_argument("--source-dir", "-s", type=str, default="", help="required")
    parser.add_argument('--chip', '-t', choices=CHIPS, nargs='+', required=False)
    parser.add_argument("--build-dir", "-d", type=str, default="_build", help="optional, default build out to _build/LANGUAGES/BUILDERS")

    args = parser.parse_args()
    global languages
    if args.language is None:
        print("Build all languages")
        languages = LANGUAGES
    else:
        languages = [args.language]

    global builders
    if args.builder is None:
        print("Build html and pdf")
    else:
        builders = [args.builder]

    global chips
    if args.chip is None:
        print('Building without a chip')
        chips = 'at1k'
    else:
        chips = args.chip
    global pdf_name_en
    global pdf_name_zh
    pdf_name_en = '{}-SDK Linux Host Development Environment Setup Guide'.format(chips)
    pdf_name_zh = '{}-SDK Linux 平台开发环境设置指南'.format(chips)

    parameters = []
    for language in languages:
        for builder in builders:
            source_dir = os.path.join(docs_path , language)
            build_dir = os.path.join(docs_path, args.build_dir, chips, language, builder)
            parameters.append((language, builder, source_dir, build_dir))

    # prepare for api docs
    generate_xml()

    build_docs(parameters)


def build_docs(parameters):
    num_cpus = multiprocessing.cpu_count()
    clean_cmd = "rm -rf {}/docs/_build/*".format(ts_docs_path)
    print("Deleting {}/docs/_build/".format(ts_docs_path))
    sbp_call(clean_cmd)
    for parameter in parameters:
        saved_cwd = os.getcwd()
        os.makedirs(parameter[3])
        build_cmd = "sphinx-build -j {} -b {} -c {} {} {} ;".format(num_cpus,parameter[1], parameter[2],parameter[2], parameter[3])
        print("Building {} of {} in {}".format(parameter[1], parameter[2], parameter[3]))
        print("Build command: {}".format(build_cmd))
        sbp_call(build_cmd)

        if parameter[1] == "latex":
            saved_cwd = os.getcwd()
            os.chdir(parameter[3])

            tex_filename = ""
            for dirpath, dirname, filename in os.walk(parameter[3]):
                for f in filename:
                    if os.path.splitext(f)[1] == ".tex":
                        tex_filename = f

            if len(tex_filename) != 0:
                pdf_cmd = "xelatex {};".format(tex_filename)
                sbp_call(pdf_cmd)
                sbp_call(pdf_cmd)

                # modify pdf filename
                src_name = "{}.pdf".format(tex_filename.split('.')[0])
                if parameter[0] == "en":
                    dst_name = '{}.pdf'.format(pdf_name_en.replace(' ', '_'))
                    os.rename(src_name, dst_name)
                else:
                    dst_name = '{}.pdf'.format(pdf_name_zh.replace(' ', '_'))
                    os.rename(src_name, dst_name)
            else:
                print("Not find tex file!")

            os.chdir(saved_cwd)


def sbp_call(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)

    wait_until = datetime.datetime.now() + timedelta(seconds=300)
    while True:
        line = p.stdout.readline()
        print(line.strip())
        if str(line).find("Error") != -1:
            p.terminate()
            break  
        elif wait_until < datetime.datetime.now():
            p.terminate()
            break
        elif p.poll() is not None:
            break

def generate_xml():
    # delete xml and generate new xml files
    if os.path.exists("xml"):
        del_cmd = "rm -rf xml"
        sbp_call(del_cmd)
        print("Delete old xml")

    xml_cmd = "doxygen Doxyfile"
    sbp_call(xml_cmd)


if __name__ == "__main__":
    main()