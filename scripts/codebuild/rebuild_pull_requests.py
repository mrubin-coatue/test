import boto3
import re
import dateutil.parser
import datetime
import requests

client = boto3.client("codebuild")


def build_pull_requests(repo_url, codebuild_project_name, pull_request_age_limit=15):
    repo_name = re.match("https?://github.com/([^/]+/[^/]+)", repo_url).group(1)
    pull_requests = get_all_pull_requests(repo_name)
    pull_requests_to_build = [pr for pr in pull_requests if requires_building(pr, pull_request_age_limit)]
    branch_names = map(lambda pr: pr["head"]["ref"], pull_requests_to_build)
    [rebuild_branch(b, codebuild_project_name) for b in branch_names]


def get_age_in_days(pull_request):
    date1 = dateutil.parser.parse(pull_request["updated_at"]).replace(tzinfo=None)
    date2 = datetime.datetime.today()
    age = date2 - date1
    return age.days


def requires_building(pull_request, pull_request_age_limit):
    # only rebuild a branch if it has a recent commit on it
    if get_age_in_days(pull_request) >= pull_request_age_limit:
        return False

    # only rebuild a branch if the target of its pull request is
    # the branch whose modification triggered this lambda in the
    # first place i.e. master
    if pull_request["base"]["ref"] != "master":
        return False

    # only rebuild a branch if the branch is in the same repo as the
    # target of the branch's pull request (i.e. no forking)
    if pull_request["head"]["repo"]["id"] != pull_request["base"]["repo"]["id"]:
        return False

    return True


def get_all_pull_requests(repo_name):
    url = f"http://api.github.com/repos/{repo_name}/pulls"
    r = requests.get(url)
    r.raise_for_status()
    pull_requests = r.json()
    return pull_requests


def rebuild_branch(branch_name, codebuild_project_name):
    build_data = {
        "projectName": codebuild_project_name,
        "sourceVersion": branch_name,
    }
    client.start_build(**build_data)

if __name__ == "__main__":
    build_pull_requests(*sys.argv[0:2])
