# git_lastrelease
is an ansible module to download lastest release from github or gitlab and return the version number

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
```
