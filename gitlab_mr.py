
"""
Usage:
    gitlab-manager mr [--help]
    gitlab-manager mr ls <project> [--wip <wip>]

Options:    
    -h, --help
    --wip <wip> Yes|No
"""
from docopt import docopt
import gitlab_manager


def list_mrs(project, wip):
    if wip is None:
        mrs = project.mergerequests.list(state='opened', order_by='updated_at')
    else:
        mrs = project.mergerequests.list(state='opened', order_by='updated_at', wip=wip)
    print("\nHere is the list of MRs for your chosen project:\n")
    
    all_mr = ""
    for mr in mrs:
        current = gitlab_manager.MergeRequest(mr)
        all_mr = all_mr + "{}\n\n".format(current.print_mr())
    print(all_mr)
    return all_mr

def main(gl, arguments):
    projects = gl.projects.list(search=arguments['<project>'])
    if len(projects) != 1:
        print("can't find the project {}\n {}".format(arguments['<project>'], projects))
        exit()
    project = projects[0]
    if arguments['ls']:
        list_mrs(project, arguments['--wip'])

if __name__ == '__main__':
    arguments = docopt(__doc__)
    


