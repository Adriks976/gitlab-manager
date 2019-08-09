#!/usr/bin/env python3

"""
gitlab_manager

Usage: 
   gitlab_manager [--version] [ --help | -h ] 
   gitlab_manager [--gitlab-url=<gitlab_url>] [--gitlab-token=<gitlab_token>] <command> [<args>...]

Options:
    --version
    --help, -h
    --gitlab-url <gitlab_url>
    --gitlab-token <gitlab_token>

The commands are:
   mr
        Manage merge requests
See 'gitlab-manager help <command>' for more information on a specific command.
"""
from subprocess import call

from docopt import docopt
import gitlab


class MergeRequest:
    def __init__(self, mr):
        self.Id = mr.iid
        self.Author = mr.author['username']
        self.Title = mr.title
        self.Description = mr.description
        self.Label = "info"
        if len(mr.labels) == 1:
            self.Label = "[{}]".format(mr.labels[0])
            
    
    def print_mr(self):
        return "### {}: {}\n\n{}\n\n    * by: {}\n\n    * Merge Request ID:{}\n".format(self.Label, self.Title, self.Description, self.Author, self.Id)


if __name__ == '__main__':

    args = docopt(__doc__,
                  version='gitlab-manager version 0.1.0',
                  options_first=True)
    # print(args)
    if args['--gitlab-url'] is not None and args['--gitlab-token'] is not None:
        gl = gitlab.Gitlab(args['--gitlab-url'], private_token=args['--gitlab-token'])
    else:
        print("Arguments gitlab-url and gitlab-token not set\nTrying with config-file")
        try:
            gl = gitlab.Gitlab.from_config()
        except gitlab.config.GitlabConfigMissingError as e:
            print(e)
            exit()
    argv = [args['<command>']] + args['<args>']
    if args['<command>'] == 'mr':
        # In case subcommand is implemented as python module:
        import gitlab_mr
        # print(docopt(gitlab_mr.__doc__, argv=argv))
        gitlab_mr.main(gl, docopt(gitlab_mr.__doc__, argv=argv))
    # elif args['<command>'] == 'branch':
    #     # In case subcommand is a script in some other programming language:
    #     exit(call(['python', 'git_branch.py'] + argv))
    # elif args['<command>'] in 'checkout clone commit push remote'.split():
    #     # For the rest we'll just keep DRY:
    #     exit(call(['python', 'git_%s.py' % args['<command>']] + argv))
    elif args['<command>'] in ['help', None]:
        print(docopt(__doc__,
        version='gitlab-manager version 0.1.0',
        options_first=True))
        # exit(call(['python3', 'gitlab-manager.py', '--help']))
    else:
        exit("%r is not a gitlab-manager command. See 'gitlab-manager help'." % args['<command>'])