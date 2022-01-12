import validators
import requests, re, os
from urllib.parse import urlparse
import urllib.request

# FUNCTIONS

def elementRegex(tag_name):
    arr_tag = {
        'js': 'src\s*=\s*"(.+?)"',
        'css': 'href\s*=\s*"(.+?)"',
        'image': 'src\s*=\s*"(.+?)"|href\s*=\s*"(.+?)"',
    }
    
    return arr_tag[tag_name]

def elementArray(tag_name, string):
    return re.findall(elementRegex(tag_name), string)

def currentPath(path = ""):
    return os.path.abspath(os.getcwd()) + path

def seperateLine():
    print('-------------------------------')

def getFileName(path):

    try:
        path = path.split('.')[1]
    except:
        pass

    split = path.split('/')
    for item in split:
        if '.' in item:
            return item.replace('/', '')
            
    return path

def getPath(path):
    split = path.split('/')
    for item in split:
        if '.' in item:
            return path.replace('/' + item, '')
            
    return path

def removeFileFromURL(url):
    scheme = urlparse(url).scheme # HTTP OR HTTPS
    domain = urlparse(url).netloc
    path = getPath(urlparse(url).path)

    return scheme + '://' + domain + path

def convertRegex_1(regex):
    search = re.search("(\'.*\',[\s\S]\'.*\')", regex)
    split = ((search.group(0)).replace("'", "")).split(', ')

    return split

#----------------

# CONFIG DATA
project_name = "zzz"
url = "https://jgmuchiri.github.io/simple-html-landing-page/"
clone_cdn = False
#----------------

# CHECK EXISTS PROJECT
if os.path.exists(currentPath('/' + project_name)) is True:
    print('This project name is already exists! Try another one :)')
    exit()

create_folder = os.path.join(currentPath(), project_name)
os.mkdir(create_folder)
print('Project [' + project_name + '] created')
seperateLine()
print('Crawling data, please wait!')
response = requests.get(url).text
print('Crawl data successfully, start cloning...')
seperateLine()

# CLONE MACHINE :D
index_html = open(currentPath('/' + project_name) + '/index.html', 'w')
index_html.write(response)
index_html.close()

print('# Cloning CSS files')
for css in elementArray('css', response):

    if clone_cdn is True:
        css = urlparse(css).path
    else:
        if validators.url(css) is True:
            continue

    try:
        
        # try:
        #     css = css.split('.')[1]
        # except:
        #     pass

        if css[0] == '/':
            string = css.split('/')[1]
        else:
            string = css

        extension_name = string.split('.')[len(string.split('.')) - 1]

        if extension_name == 'css':
            full_path = currentPath('/' + project_name + '/' + string)
            
            file_name = getFileName(full_path)
            path_name = getPath(full_path)

            # CHECK EXISTS FOLDER, IF NOT CREATE ONE
            if os.path.exists(path_name) is False:
                os.makedirs(path_name)

            # CHECK EXISTS FILE, IF NOT CREATE AND WRITE CONTENT TO IT :D
            if os.path.exists(full_path) is False:
                content = requests.get(removeFileFromURL(url) + '/' + string).text
                f = open(full_path, "w")
                f.write(content)
                f.close()

                print('[' + string + '] File saved')
    except:
        pass

print('\n')

print('# Cloning JS files')
for js in elementArray('js', response):
    if clone_cdn is True:
        js = urlparse(js).path
    else:
        if validators.url(js) is True:
            continue
    
    try:

        # try:
        #     js = js.split('.')[1]
        # except:
        #     pass

        if js[0] == '/':
            string = js.split('/')[1]
        else:
            string = js

        extension_name = string.split('.')[len(string.split('.')) - 1]

        if extension_name == 'js':
            full_path = currentPath('/' + project_name + '/' + string)
            
            file_name = getFileName(full_path)
            path_name = getPath(full_path)

            # CHECK EXISTS FOLDER, IF NOT CREATE ONE
            if os.path.exists(path_name) is False:
                os.makedirs(path_name)

            # CHECK EXISTS FILE, IF NOT CREATE AND WRITE CONTENT TO IT :D
            if os.path.exists(full_path) is False:
                content = requests.get(removeFileFromURL(url) + '/' + string).text
                f = open(full_path, "w")
                f.write(content)
                f.close()

                print('[' + string + '] File saved')
    except:
        pass

print('\n')

print('# Cloning IMAGE (png, jpeg, jpg, ico, svg) files')
for image in elementArray('image', response):

    for i in range(1):
        line = image[i]
        
        if clone_cdn is True:
            line = urlparse(line).path
        else:
            if validators.url(line) is True:
                continue

        try:

            # try:
            #     line = line.split('.')[1]
            # except:
            #     pass

            if line[0] == '/':
                string = line.split('/')[1]
            else:
                string = line

            extension_allow = ['png', 'jpeg', 'jpg', 'ico', 'svg']
            extension_name = string.split('.')[len(string.split('.')) - 1]

            if extension_name in extension_allow:
                full_path = currentPath('/' + project_name + '/' + string)
                
                file_name = getFileName(full_path)
                path_name = getPath(full_path)

                # CHECK EXISTS FOLDER, IF NOT CREATE ONE
                if os.path.exists(path_name) is False:
                    os.makedirs(path_name)

                # CHECK EXISTS FILE, IF NOT CREATE AND WRITE CONTENT TO IT :D
                if os.path.exists(full_path) is False:
                    urllib.request.urlretrieve(removeFileFromURL(url) + '/' + string, full_path)
                    print('[' + string + '] File saved')
        except:
            pass
print('\n')

seperateLine()
print('Mission completed! Check `index.html`')
