# git_lastrelease
**description**: get the latest release name from github or gitlab  project
- options:
  -  **repo**:
     description: url to the git repo
     required: true
     choices: ['github.com', 'gitlab.com', 'gitlab.your_instance.suffix']
   - **namespace**:
     description: the group, namespace or owner where the git project is
     required: true
   - **project**:
     description: the name of the project, usually in the url it's the part before the .git
     required: true
   - **draft**:
     description: only used with github.com, set to true if you want to get the latest draft release
     required: false
     choices: [ 'true', 'false']
     default: 'false'
   - **prerelease**:
     description: put to yes if you want to get future release, false if only existing one
     required: false
     choices: [ 'true', 'false']
     default: 'false'
   - **token**:
     description: if your project is not publicly available give your personnal token
     required: false

# How to install
put the file in your project library dir (depending your configuration see details here https://docs.ansible.com/ansible/latest/dev_guide/developing_locally.html )

# How to use: 
```
- name: check if hadolint command exist
  shell: command -v hadolint
  ignore_errors: yes
  register: hadolint_exist

- name: get hadolint latest release metada from github
  git_lastrelease:
    repo: 'github.com'
    namespace: hadolint
    project: hadolint
  register: hadolint_release
  when: hadolint_exist.rc
  
- name: download the hadolint binary
  get_url:
    url: "https://github.com/hadolint/hadolint/releases/download/{{ hadolint_release.results.name }}/hadolint-Linux-x86_64"
    dest: /usr/local/bin/hadolint
    remote_src: yes
    mode: 777
  become: true
  when: hadolint_exist.rc
```
