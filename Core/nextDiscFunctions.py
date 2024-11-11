import urllib.parse
import json
import requests
import re
import logging
import requests
from urllib3.exceptions import InsecureRequestWarning

def get_page_content(url, user_agent, timeout):
    headers = {'User-Agent': user_agent}
    try:
        response = requests.get(url, headers=headers, timeout=timeout, verify=False)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Error while get the page content: {url}: {e}")
        return None

def get_manifest_path(manifest_name, body_content):
    pattern = rf'/_next/static/[\w-]+/{manifest_name}\.js'
    match = re.search(pattern, body_content)
    if match:
        return match.group(0)
    else:
        return None

def get_manifest_content(manifest_url, user_agent, timeout):
    headers = {'User-Agent': user_agent}
    try:
        response = requests.get(manifest_url, headers=headers, timeout=timeout, verify=False)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Error while geting the manifesto {manifest_url}: {e}")
        return None

def parse_manifest_content(manifest_content):
    paths = set()
    matches = re.findall(r'"(/[a-zA-Z0-9_/\[\]\.-]+)"', manifest_content)
    for path in matches:
        paths.add(path)
    return paths

def extract_next_data(page_content):
    match = re.search(r'__NEXT_DATA__\s*=\s*(\{.*?\});', page_content, re.DOTALL)
    if match:
        json_data = match.group(1)
        try:
            data = json.loads(json_data)
            return data
        except json.JSONDecodeError as e:
            logging.error(f"[!] erro while parsing __NEXT_DATA__: {e}")
    return None

def parse_next_data(data):
    paths = set()


    if 'page' in data:
        paths.add(data['page'])
    
    
    if 'query' in data and isinstance(data['query'], dict):
        for value in data['query'].values():
            if isinstance(value, str):
                paths.add(value)
    
    
    if 'props' in data and 'pageProps' in data['props']:
        page_props = data['props']['pageProps']
        if isinstance(page_props, dict):
            for value in page_props.values():
                
                if isinstance(value, str) and value.startswith('/'):
                    paths.add(value)
                
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, str) and item.startswith('/'):
                            paths.add(item)
    return paths

def get_routes_manifest(target, user_agent, timeout):
    manifest_url = urllib.parse.urljoin(target + '/', '_next/routes-manifest.json')
    headers = {'User-Agent': user_agent}
    try:
        response = requests.get(manifest_url, headers=headers, timeout=timeout, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Erro ao acessar {manifest_url}: {e}")
    except json.JSONDecodeError as e:
        logging.error(f"Erro ao parsear JSON de {manifest_url}: {e}")
    return None

def parse_routes_manifest(data):
    paths = set()
    if 'dynamicRoutes' in data:
        for route in data['dynamicRoutes']:
            paths.add(route['page'])
    if 'staticRoutes' in data:
        for route in data['staticRoutes']:
            paths.add(route['page'])
    return paths

def process_additional_manifest(target, manifest_name, page_content, user_agent, timeout):
    manifest_path = get_manifest_path(manifest_name, page_content)
    if manifest_path:
        manifest_url = urllib.parse.urljoin(target + '/', manifest_path)
        manifest_content = get_manifest_content(manifest_url, user_agent, timeout)
        if manifest_content:
            paths = parse_manifest_content(manifest_content)
            return paths
    else:
        logging.warning(f"[!] {manifest_name}.js not found {target}.")
    return set()
