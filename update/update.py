import subprocess
import requests

def get_local_git_tag(repo_dir="."):
    """获取本地 Git 仓库的当前 Tag"""
    try:
        result = subprocess.run(
            ["git", "-C", repo_dir, "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None  # 可能不是 Git 仓库，或者没有 Tag

def get_latest_release_tag(owner, repo):
    """获取 GitHub 最新 Release 的 Tag"""
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["tag_name"]
    else:
        raise Exception(f"Failed to fetch release info (HTTP {response.status_code})")

# 示例：比较本地和远程版本
owner = "BAAI-EI-DATA"
repo = "WanX-Studio-Server"

local_tag = get_local_git_tag()  # 本地 Tag
print(local_tag)
remote_tag = get_latest_release_tag(owner, repo)  # 远程 Release Tag

print(f"Local Git Tag: {local_tag}")
print(f"Latest Release Tag: {remote_tag}")

if local_tag == remote_tag:
    print("✅ 本地代码与最新 Release 版本一致")
else:
    print("❌ 本地代码与最新 Release 版本不一致")
    print(f"建议更新：git pull origin main 或 git checkout {remote_tag}")