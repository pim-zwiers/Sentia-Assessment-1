Usage

Make sure the hosts are reachable:
```ansible all -m ping -i ./myazure_rm.yml
```
Run playbook against hosts:
```ansible-playbook -i myazure_rm.yml playbook.yml
```