import argparse as arg
import os

from dfsspy.util import download_file_from_sophon_sftp, upload_file_to_sophon_sftp, sftp_login


def dfss_parser():
    parser = arg.ArgumentParser(description="download_file_from_sophon_sftp",
                                formatter_class=arg.ArgumentDefaultsHelpFormatter,
                                prog="python -m dfss")
    required_group = parser.add_argument_group(
        "download parameters", "parameters for download files from Sophgo server")
    required_group.add_argument("--url",
                                type=str,
                                help="url to remote sftp file")
    required_group.add_argument("--user",
                                type=str,
                                help="username to remote sftp")
    required_group.add_argument("--dflag",
                                type=str,
                                help="using dflag to down file")
    upload_file = parser.add_argument_group(
        "upload parameters", "parameters for upload files to Sophgo server")
    upload_file.add_argument("--upflag",
                             type=str,
                             help="flag of need upload file")
    upload_file.add_argument("--upfile",
                             type=str,
                             help="need to upload file")
    return parser


if __name__ == "__main__":
    print("dfss tool by Sophgo, version: 1.6.17")
    parser = dfss_parser()
    a = parser.parse_args()
    if a.url is not None:
        print('download from', a.url)
        if a.url.startswith("open@sophgo.com:"):
            file_path = a.url[len("open@sophgo.com:"):]
            for i in range(3):
                if download_file_from_sophon_sftp(file_path, os.getcwd(), isflag=False) is True:
                    exit(0)
                print('download num {}'.format(i))
            exit(1)
        else:
            print('please from open@sophgo.com download')
    elif a.upflag is not None and a.upfile is not None:
        print('neet upfile', a.upfile, 'with flag', a.upflag)
        for i in range(3):
            if upload_file_to_sophon_sftp(a.upflag, a.upfile) is True:
                exit(0)
            print('upload num {}'.format(i))
        exit(1)
    elif a.user is not None:
        sftp_login(a.user)
    elif a.dflag is not None:
        if download_file_from_sophon_sftp(a.dflag, os.getcwd(), isflag=True) is True:
            exit(0)
    else:
        print("Not capturing complete parameters.")
        exit(1)
