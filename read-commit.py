import subprocess
import json
import re
import argparse

def get_task_id_length(commit_message, task_prefix, only_number=False):
    task_prefix_with_dash = task_prefix + "-"
    start_index = commit_message.find(task_prefix_with_dash)
    if start_index != -1:
        dynamic_part = commit_message[start_index + len(task_prefix_with_dash):]  # Trích xuất từ vị trí sau "STA-" đến hết chuỗi

        return len(dynamic_part) if only_number else len(dynamic_part) + len(task_prefix) + 1  # Tính độ dài của phần động
    else:
        return -1

def check_format(input_string, task_prefix):
    number_part_len = get_task_id_length(input_string, task_prefix, True)
    pattern = r".* " + task_prefix + "-\w{" + str(number_part_len) + "}$"
    return re.match(pattern, input_string) is not None

parser = argparse.ArgumentParser()
parser.add_argument("repo", type=str, help="Github Repository")
parser.add_argument("pull_request_id", type=int, help="ID of pull request")
parser.add_argument("task_prefix", type=str, help="Jira task prefix")
args = parser.parse_args()

# Kích thước trang và số trang bắt đầu từ 1
per_page = 100
page = 1
owner = 'saritasa-nest'
repo = args.repo
pull_request_id = args.pull_request_id
task_prefix = args.task_prefix

task_array = []

while True:
    # Command để gọi API từ GitHub
    command = [
        "gh", "api",
        "-H", "Accept: application/vnd.github+json",
        "-H", "X-GitHub-Api-Version: 2022-11-28",
        f"/repos/{owner}/{repo}/pulls/{pull_request_id}/commits?per_page={per_page}&page={page}"
    ]

    # Gọi command và lấy kết quả đầu ra
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout

    # Kiểm tra xem đầu ra có dạng JSON hay không
    try:
        data = json.loads(output)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        break

    for commit in data:
        commit_message = commit.get("commit", {}).get("message")
        if commit_message.startswith("Merge pull reques"):
            continue
        # Check các commit message chứa jira task và get Task ID từ đó
        if check_format(commit_message, task_prefix):
          length = get_task_id_length(commit_message, task_prefix)
          
          if length != -1:
            task_array.append(commit_message[-length:])
        else:
            print(commit_message)

    # Kiểm tra xem còn trang tiếp theo hay không
    if len(data) < per_page:
        break
    else:
        page += 1

# Unique task id nhận được
task_array = list(set(task_array))
# In ra link jira task list
for task in task_array:
  print(f"https://saritasa.atlassian.net/browse/{task}")