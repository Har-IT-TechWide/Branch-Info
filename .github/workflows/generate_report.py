import subprocess
import json
import openpyxl
from openpyxl import Workbook
import sys
import os

def get_branches(repo_path):
    result = subprocess.run(['git', '-C', repo_path, 'for-each-ref', '--format=%(refname:short) %(creatordate) %(authorname)', 'refs/heads/'], capture_output=True, text=True)
    branches = []
    for line in result.stdout.splitlines():
        parts = line.split()
        branch_name = parts[0]
        created_date = " ".join(parts[1:5])
        author_name = " ".join(parts[5:])
        branches.append({
            'branch': branch_name,
            'created_date': created_date,
            'author': author_name
        })
    return branches

def create_excel(branches, repo_name):
    wb = Workbook()
    ws = wb.active
    ws.title = "Branches"

    # Headers
    ws.append(['Branch', 'Created Date', 'Author'])

    # Branch data
    for branch in branches:
        ws.append([branch['branch'], branch['created_date'], branch['author']])

    # Save the file
    file_name = f"branch_report_{repo_name}.xlsx"
    wb.save(file_name)

if __name__ == "__main__":
    repo_url = sys.argv[1]
    repo_path = sys.argv[2]
    repo_name = repo_url.split('/')[-1].replace('.git', '')

    branches = get_branches(repo_path)
    create_excel(branches, repo_name)

