# git_lastrelease
is an ansible module to get the version number of current lastest release from github or gitlab project

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
