Usage

Make sure the hosts are reachable:
```bash
ansible all -m ping -i ./myazure_rm.yml
```
Run playbook against hosts:
```bash
ansible-playbook -i myazure_rm.yml playbook.yml
```