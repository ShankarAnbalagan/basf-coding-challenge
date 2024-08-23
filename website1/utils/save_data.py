import os
import json
import urllib.request
import zipfile

def save(output_dir, data, html, page_num, project_index):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    page_dir = os.path.join(output_dir, f'page_{page_num}')
    project_dir = os.path.join(page_dir, f'project_{project_index + 1}')

    if not os.path.exists(page_dir):
        os.makedirs(page_dir)

    if not os.path.exists(project_dir):
        os.makedirs(project_dir)

    with open(os.path.join(project_dir, 'metadata.json'), 'w') as file:
        json.dump(data, file, indent=4)

    with open(os.path.join(project_dir, 'html_content.html'), 'w') as file:
        file.write(html)

    if(data['download_link']):
        attachment_dir = os.path.join(project_dir, 'attachments')
        if not os.path.exists(attachment_dir):
            os.makedirs(attachment_dir)

        download_file_path = ''
        with urllib.request.urlopen(data['download_link']) as response:
            content_disposition = response.headers.get('Content-Disposition')
            if content_disposition:
                filename = content_disposition.split('filename=')[-1].strip('\"')
                download_file_path = os.path.join(attachment_dir, filename)

                with open(download_file_path, 'wb') as file:
                    file.write(response.read())
        
        if('.zip' in download_file_path):
            os.makedirs(download_file_path.strip('.zip'))
            with zipfile.ZipFile(download_file_path, 'r') as zip_file:
                zip_file.extractall(attachment_dir)